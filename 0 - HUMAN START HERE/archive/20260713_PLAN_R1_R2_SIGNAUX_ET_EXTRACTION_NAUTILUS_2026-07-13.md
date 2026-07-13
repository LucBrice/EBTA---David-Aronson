# Plan d'implémentation — R1 (moteur de signaux) + R2 (extraction réelle Nautilus)

> Brouillon d'intake, pas un chantier actif. Déposé pour audit/routage humain
> via `/start`. Reste `INTAKE`, non exécutable, tant qu'un humain ne l'a pas
> routé vers `.ai/backlog/`. Fondé sur l'audit
> `0 - HUMAN START HERE/AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md`.
> API Nautilus citée ci-dessous : **vérifiée empiriquement** sur
> `nautilus_trader==1.230.0` (venv `Implementation/adapters/nautilus_env/venv`),
> tracée dans `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`.

## Mise à jour 2026-07-13 (post-rédaction initiale)

L'humain a signalé que la logique de signal **existe déjà, codée, testée et
validée**, hors de ce dépôt EBTA, dans le repo BACKTRADER de référence :

```text
D:\TRADING\ENTREPRISE\0 - Phase de lancement\Stratégie de trading\0 - Backtest\BACKTRADER\strategies
D:\TRADING\ENTREPRISE\0 - Phase de lancement\Stratégie de trading\0 - Backtest\BACKTRADER\features
```

Lecture effectuée (lecture seule — BACKTRADER reste `reference-only` par
gouvernance, cf. `.ai/checkpoint.json` risque `R2` déjà `CONTROLLED`, et
`payloads.py` cite déjà `strategies/sweep_lq.py` comme source des payloads
E–I) : `features/core.py`, `features/entry_signal.py`, `features/filters.py`,
`strategies/sweep_lq.py`, `strategies/logic.py`.

Ceci **remplace** l'approche R1.1 initiale (« inventer deux règles
calculables ») par un **port fidèle** de la logique déjà validée. Voir
section « R1 — révisé » ci-dessous, qui remplace intégralement l'ancienne
section R1. Trois découvertes structurantes en résultent :

1. **Le moteur source est vectorisé/batch (pandas), pas event-driven.** Il
   calcule une série de décisions `X` sur tout l'historique d'un coup, alors
   que `Strategy.on_bar()` de Nautilus est appelé barre par barre sans accès
   au futur. Le port ne peut pas être un copier-coller direct.
2. **La stratégie a besoin de multi-timeframe** (M1, M3, M15/LQ, H1, H4, D1),
   dérivé par resampling depuis la même base 1-minute. Le chargeur EBTA actuel
   (`data/local_ohlcv.py`) ne charge qu'un seul timeframe par actif — aucun
   composant de resampling n'existe.
3. **Dépendance bloquante avec R4 pour le chemin de production.** Le moteur de
   signal a besoin de vraies barres intraday (M1/M3/M15) pour détecter
   patterns, sweeps et biais. Or `package_builder/nautilus_research_package.py`
   réduit aujourd'hui les données à **un bar par jour** via `_daily_sample`
   avant même d'appeler Nautilus. Le port du vrai signal peut être construit et
   prouvé **de façon autonome** (tests unitaires + un test d'intégration sur de
   vraies données de marché, hors chemin de production), mais son branchement
   dans `nautilus_research_package.py` restera bloqué tant que R4 (vrai volume
   de données) n'est pas résolu.

Dépendances vérifiées dans le venv Nautilus (aucune nouvelle dépendance
requise) : `pandas`/`numpy` déjà présents **sur l'interpréteur de base ET dans
le venv Nautilus** (donc pas d'import paresseux nécessaire pour les nouveaux
modules de signal, à la différence de `nautilus_trader` lui-même) ;
`tzdata`/`pytz` déjà présents (filtres de session DST-aware sans nouvelle
dépendance) ; `cachetools` **absent** — le port abandonne la couche de cache
LRU de la source (optimisation de performance, pas de correction ;
n'affecte pas le résultat).

Nouveaux faits API Nautilus vérifiés le 2026-07-13 et tracés dans
`NAUTILUS_API_NOTES.md` : `Bar.ts_event`/`ts_init` (entiers nanosecondes),
`nautilus_trader.core.datetime.unix_nanos_to_dt(ts_event) -> pandas.Timestamp`
(UTC-aware) — nécessaire pour faire correspondre une barre `on_bar()` à une
décision précalculée indexée par timestamp.

## Mise à jour 2 — 2026-07-13 (discussion d'architecture, corrige la mise à jour ci-dessus)

Discussion ultérieure avec l'humain sur l'objectif long terme (fondations d'un
desk de trading algorithmique : recherche EBTA → déploiement live →
monitoring → réévaluation → portefeuille multi-stratégies). Cette discussion
**invalide et remplace le pattern « signal replay »** décrit dans la mise à
jour précédente (R1.1 initial) et la section R1 qui en découlait. Quatre
conclusions actionnables :

### 1. Le pattern « signal replay » est incompatible avec l'objectif live
Un précalcul vectorisé de la série de décisions n'a pas de sens en live : il
n'y a pas de futur à précalculer, les barres arrivent une par une
indéfiniment. Une stratégie qui consulte une table de décisions précalculées
ne peut, par construction, jamais devenir une stratégie live — elle serait à
réécrire entièrement au moment du passage en production. **La couche
stratégie/exécution doit être écrite une seule fois, sous forme incrémentale
native** (calcul bar-par-bar avec état interne, à l'intérieur de
`Strategy.on_bar()`), pour que le même code serve au backtest de recherche et
au live sans réécriture — c'est la promesse même de Nautilus (`Strategy`
identique entre `BacktestEngine` et un nœud live, seul l'adaptateur
data/exécution change).

### 2. Architecture en 5 couches (où investir maintenant, où ne pas investir encore)
| # | Couche | État | Décision |
|---|---|---|---|
| 1 | **Exploration/screening** (tri rapide d'idées, jetable) | La pipeline BACKTRADER vectorisée existante | **Gardée telle quelle, explicitement hors du chemin EBTA/Nautilus.** Sert uniquement à réduire une grille de candidats à un short-list ; n'a jamais besoin d'être "la même code que le live". |
| 2 | **Stratégie/exécution** (logique de trading) | Stub actuel, à construire | **Investissement prioritaire maintenant, en incrémental natif** avec un registry de stratégies (voir point 3). C'est le code qui ira un jour en live sans réécriture. |
| 3 | **Validation statistique/gouvernance** (WRC, OOS CI, detrending, G-BIAS) | `procedures/`, `governance/` | Déjà stable et agnostique à la stratégie (opère sur `SimulationResult`) — ne change pas. |
| 4 | **Artefacts/reproductibilité** (manifests, persistence, package_builder) | Déjà stable | Idem, agnostique — ne change pas. |
| 5 | **Portefeuille/monitoring/déploiement live** | N'existe pas | **Correctement différé** — tant que les contrats (`SimulationResult`, `CostModel`, `Candidate`) restent agnostiques à la stratégie (ils le sont déjà), rien à construire maintenant. |

### 3. Registry de stratégies (le mécanisme qui délivre "infra stable, stratégies changent")
Le stub actuel (`GenericPayloadStrategy` interprétant un dict `payload`) donne
une fausse impression de flexibilité : une logique de règle vraiment nouvelle
obligerait à retoucher le pont d'adaptateur. Il faut un **registry** : chaque
stratégie = un petit module autonome implémentant une interface stable ;
ajouter une stratégie = ajouter un fichier, jamais toucher
`nautilus_mapping.py`, `nautilus_research_package.py`, `procedures/` ou
`governance/`.

### 4. Nautilus est un moteur d'exécution, pas un outil de recherche (vérifié empiriquement)
Vérifications faites le 2026-07-13 (documentées **et** empiriques, tracées
dans `NAUTILUS_API_NOTES.md` section « BacktestNode / BacktestRunConfig —
absence de recherche paramétrique native ») :
- `BacktestNode.run()` est une boucle Python **séquentielle** sur les
  `BacktestRunConfig` (lu directement dans le code source :
  `for config in self._configs.values(): ...`) — aucun multiprocessing, aucune
  dépendance `ray`/`dask`/`joblib` importée ni installée.
- Recherche exhaustive de tous les sous-modules de `nautilus_trader` pour
  `optim`/`sweep`/`grid`/`search`/`param` : aucun module de génération
  automatique de grille de paramètres n'existe.
- La carte marketing du site (« Iterate faster — large parameter spaces »)
  renvoie vers `concepts/configuration/`, qui ne décrit que l'architecture des
  structs de config typées — la vraie promesse est que les paramètres sont
  **découplés du code de stratégie** (jamais besoin de modifier `Strategy`
  pour changer un paramètre), pas une génération ou une parallélisation
  automatique de la grille.
- **Conséquence** : la génération de familles de candidats, le balayage de
  grilles, et une éventuelle parallélisation restent **entièrement à la
  charge d'EBTA** (`strategies/payload_factory.py`, `procedures/search_space.py`,
  l'orchestrateur `package_builder/`) — ce n'est pas une limitation contournée,
  c'est la conception même de Nautilus. Ceci renforce la couche 1
  (exploration) du tableau ci-dessus : elle doit rester un outil EBTA/Python
  propre, pas quelque chose délégué à Nautilus.

### Fait API supplémentaire vérifié (nécessaire à la conception incrémentale)
`Strategy.subscribe_bars(bar_type)` peut être appelé plusieurs fois avec des
`BarType` différents (M1, M3, M15, H1, H4, D1) ; une **seule** méthode
`on_bar(self, bar: Bar)` reçoit les barres de tous les timeframes souscrits —
il faut discriminer via `bar.bar_type` à l'intérieur (confirmé par lecture du
code source de l'exemple officiel
`nautilus_trader.examples.strategies.subscribe.SubscribeStrategy`). C'est ce
qui permet à une seule `Strategy` de maintenir un état par timeframe (biais
H1/H4/D1, pools M15, fenêtre M1 récente) — voir `NAUTILUS_API_NOTES.md`
section « Souscription multi-timeframe dans une seule Strategy ».

## Track
mainline — débloque la capacité de recherche réelle.

## Lifecycle
INTAKE (à router en PLANNED puis ACTIVE via `/start`).

## Source
- Audit `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` (constats 1a, 1b).
- Observation archivée `archive/20260710_OBSERVATION_GATE_ECONOMIQUE_BOOLEENS_CODES_EN_DUR.md`.
- SOP 03 (règles de signal / familles de candidats), SOP 07/08 (detrending,
  gate économique), SOP 05 (robustesse).
- API vérifiée : `NAUTILUS_API_NOTES.md` sections « Strategy / StrategyConfig »,
  « OrderFactory.bracket() », « Modules d'indicateurs », « Extraction de
  performance réelle : Portfolio / PortfolioAnalyzer / Trader reports »,
  « Bar.ts_event et conversion en timestamp ».
- **Logique de stratégie validée, lue en lecture seule le 2026-07-13** (source
  de référence externe, hors dépôt EBTA, `reference-only` par gouvernance) :
  - `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Stratégie de trading\0 - Backtest\BACKTRADER\features\core.py`
    (détection d'engulfing, biais de marché MTF, pools de liquidité empilés
    avec expiration).
  - `...\BACKTRADER\features\entry_signal.py` (SSOT du signal M1 sweep → M3
    confirmation de clôture, garanties anti-lookahead documentées en commentaire).
  - `...\BACKTRADER\features\filters.py` (filtre de session DST-aware
    asia/london/us ; signal M1/M3 bidirectionnel).
  - `...\BACKTRADER\strategies\sweep_lq.py` (orchestration des payloads A–I,
    déjà la source citée par `strategies/payloads.py::payload_by_code` dans ce
    dépôt).

## Problème résolu

Aujourd'hui deux mensonges silencieux invalident tout backtest :

1. **R1 — Pas de signal.** `adapters/nautilus_strategy_bridge.py::on_bar`
   achète au 1er bar (`OrderSide.BUY` en dur) et sort après N bars, quel que
   soit le payload. Aucune règle E–I n'est évaluée. Tous les candidats sont
   identiques = buy-and-hold long.
2. **R2 — Extraction faussée.** `adapters/nautilus_mapping.py::extract_simulation_result`
   reconstruit la NAV à la main (`starting_nav + (close - entry_price)*qty` sur
   tout le segment, y compris après la sortie = bug), fixe `total_costs=0.0`,
   et ignore la comptabilité réelle de Nautilus (`portfolio`, `analyzer`,
   `positions_report`).

Tant que R1 et R2 ne sont pas levés, les procédures aval (WRC, detrending,
gate économique) — pourtant correctes — travaillent sur du bruit.

## Scope

- **Nouveau** `Implementation/ebta_engine/strategies/signals/` (sous-package) :
  port fidèle, stdlib + pandas/numpy, de la logique de détection validée —
  `engulfing.py`, `market_bias.py`, `liquidity.py`, `sessions.py`,
  `entry_signal.py`. Rôle : **oracle de parité** pour la version incrémentale
  (R1.6) et réutilisable tel quel par la couche 1 (exploration/screening, hors
  EBTA/Nautilus) — plus un précalcul rejoué en production.
- **Nouveau** `Implementation/ebta_engine/strategies/registry.py` (ou
  équivalent) : interface stable de stratégie + registry `{payload_code:
  StrategyClass}` (R1.1).
- **Nouveau** `Implementation/ebta_engine/strategies/incremental/` (ou
  équivalent) : implémentation incrémentale/à état des payloads E, F, G/H/I
  (R1.5), une classe par niveau de complexité, chacune enregistrée dans le
  registry.
- **Nouveau** `Implementation/ebta_engine/data/resample.py` : resampling causal
  (right-closed, aucune barre en formation) de barres 1-minute EBTA
  (`OhlcvBar`) vers M3/M15/H1/H4/D1.
- `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py` (R1) :
  souscrit aux timeframes nécessaires (R1.3) et délègue au registry — ne
  contient plus de logique de pattern elle-même.
- `Implementation/ebta_engine/adapters/nautilus_mapping.py`
  (`extract_simulation_result`, `run_segment`) (R2).
- Tests : `tests/test_nautilus_phase4_strategy_costs.py`,
  `test_nautilus_phase5_run_segment.py`, nouveaux tests unitaires par module de
  signal vectorisé (oracle), un test de parité par niveau de payload (E, F,
  G/H/I) contre l'oracle, un test d'intégration réel à travers Nautilus, et un
  test d'extraction R2.
- Fixtures golden-case : recalibrer `expected_result.py` sur la vraie compta.

## Non-goals

- **Aucune** modification de `Protocole/`.
- **Aucune** modification de la signature du contrat `SimulationResult`
  (`strategies/contracts.py`) : R2 doit remplir les mêmes champs, mieux.
- **Aucune** fuite d'identité de segment (Train/Test/OOS) dans Nautilus :
  la Strategy et `run_segment` restent aveugles au rôle du segment (invariant
  RISK_003 du tracking).
- **Aucune** dépendance runtime BACKTRADER : le port est un portage de logique
  (lecture seule, une fois), pas un import ou une dépendance vers le dépôt
  BACKTRADER à l'exécution.
- **Aucune** nouvelle dépendance externe : `cachetools` (cache LRU de la
  source) est délibérément abandonné plutôt qu'ajouté ; `pandas`/`numpy`/
  `tzdata`/`pytz` sont déjà présents des deux côtés (interpréteur de base et
  venv Nautilus).
- **Aucun** branchement dans le chemin de production
  `package_builder/nautilus_research_package.py` tant que `_daily_sample`
  n'est pas résolu (R4) : le moteur de signal doit être construit et prouvé de
  façon autonome (tests + intégration sur données réelles hors orchestrateur
  de production) dans ce chantier ; le branchement en production est un
  chantier séparé et explicite, pas une conséquence silencieuse de celui-ci.
- Ne pas traiter R3 (découpler preuve/attestation dans `_write_reports`) ici —
  chantier suivant, mais R1+R2 le rendent possible.
- Ne pas recalibrer les seuils économiques de production (décision humaine
  SOP 08, déjà tracée).
- **Aucune** construction de couche portefeuille/monitoring/déploiement live
  (couche 5) — délibérément différée ; les contrats existants
  (`SimulationResult`, `CostModel`, `Candidate`) restent déjà agnostiques à la
  stratégie et n'ont pas besoin de changer de forme pour une future couche
  portefeuille.
- **Aucune** sur-ingénierie du registry de stratégies (R1.1) : une interface
  minimale + un dict d'enregistrement pour la seule famille liquidity sweep
  (E, F, G/H/I) — pas un framework anticipant des besoins non encore exprimés.
- **Aucun traitement de R6 (robustesse non stressée)** dans ce chantier :
  les scénarios `CENTRAL/PLAUSIBLE/EXTREME` du package Nautilus continuent de
  recevoir les mêmes données et un seuil `-100%` non bloquant
  (`nautilus_research_package.py::_nautilus_robustness_grid`). Ce chantier ne
  corrige pas ce point — **différé explicitement**, à traiter dans un chantier
  séparé dédié au stress réel (chocs de coûts/slippage/latence).
- **Aucun traitement de R7 (hygiène de reproductibilité)** dans ce chantier :
  le venv Nautilus reste commité dans le dépôt, `DEFAULT_DATA_ROOT` reste un
  chemin Windows absolu en dur (`data/local_ohlcv.py`), et `document_hash`
  reste le placeholder littéral `NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER`
  (`nautilus_research_package.py`). **Différé explicitement**, à traiter dans
  un chantier séparé d'hygiène/reproductibilité.

---

## R1 — Moteur de signaux réel (révisé 2026-07-13, deuxième passe : incrémental natif)

> Cette section **remplace intégralement** la version précédente (pattern
> « signal replay », R1.1 à R1.7 d'origine) — invalidée par « Mise à jour 2 »
> ci-dessus. La logique de détection (engulfing, biais MTF, pools de
> liquidité, confirmation M1/M3, session) reste **portée fidèlement** depuis
> la source BACKTRADER (voir Source) ; ce qui change est la **forme** du
> portage : incrémentale/à état, pas un précalcul vectorisé rejoué.

### R1.0 Principe
La couche stratégie/exécution doit être écrite **une seule fois**, sous forme
incrémentale native (état interne, mis à jour barre par barre dans
`on_bar()`), pour que le même code serve au backtest de recherche et, plus
tard, au live sans réécriture. Les modules vectorisés portés depuis la
source restent utiles à deux titres : (a) **oracle de parité** — vérité de
référence pour valider mécaniquement la version incrémentale ; (b) réutilisés
tels quels par la couche 1 (exploration/screening, hors EBTA/Nautilus) pour
le tri rapide de grilles de candidats.

### R1.1 Registry de stratégies (infrastructure, construite une fois)
Une interface stable (ex. protocole `SignalStrategy` : état interne +
méthode de mise à jour par barre) et un registry `{payload_code:
StrategyClass}` consulté par `nautilus_strategy_bridge.py`. Ajouter une
nouvelle stratégie = ajouter un module qui implémente l'interface et
s'enregistre — jamais toucher `nautilus_mapping.py`,
`nautilus_research_package.py`, `procedures/` ou `governance/`. C'est ce
mécanisme, pas seulement "Nautilus event-driven", qui délivre l'exigence
« infra stable, seules les stratégies changent ».

### R1.2 Resampling multi-timeframe (inchangé)
La logique a besoin de M1, M3, M15 (`lq_tf_minutes`, configurable), H1, H4,
D1 — tous dérivés de la même base 1-minute. Nouveau module
`data/resample.py` : resampling causal (barres closes uniquement) des
`OhlcvBar` 1-minute EBTA vers ces résolutions.

### R1.3 Souscription multi-timeframe dans une seule Strategy (vérifié)
`Strategy.subscribe_bars(bar_type)` appelé une fois par timeframe (M1, M3,
M15, H1, H4, D1) dans `on_start()`. Une seule méthode `on_bar(bar)` reçoit
toutes les barres ; discrimination par `bar.bar_type` pour router vers l'état
interne concerné (biais H1/H4/D1, pools M15, fenêtre M1 récente pour
l'engulfing).

### R1.4 Modules vectorisés portés — gardés comme oracle de parité et pour l'exploration
Le portage fidèle des modules suivants (stdlib + pandas/numpy) reste réalisé
comme prévu, mais leur rôle change : ils ne sont plus rejoués en production,
ils servent de **référence testable** pour la version incrémentale, et sont
réutilisables tels quels par la couche 1 (exploration) :
- `strategies/signals/engulfing.py` (patterns bull/bear 2/3 bougies + pivots).
- `strategies/signals/market_bias.py` (biais MTF H1/H4/D1, anti-lookahead déjà
  documenté en commentaire dans la source : `shift(1)`/`shift(2)`).
- `strategies/signals/liquidity.py` (pools avec expiration `expiry_days`).
- `strategies/signals/sessions.py` (DST-aware via `pandas`/`zoneinfo`/`pytz`).
- `strategies/signals/entry_signal.py` (sweep M1 → engulfing M1 → clôture M3 ;
  garde anti-signal-simultané BUY+SELL conservée), sans `cachetools` (absent,
  non nécessaire).

### R1.5 Portage incrémental — séquence de construction (du plus simple au plus complet)
Construire dans cet ordre, chaque étape ajoutant un seul incrément d'état,
jamais tout d'un coup :

1. **Payload E (confirmation seule, le plus simple)** : état M1 (2-3 dernières
   bougies pour l'engulfing, mis à jour à chaque barre M1) + pool de liquidité
   M15 (petite liste avec expiration, mise à jour à chaque barre M15 qui
   clôture) + machine à états sweep → engulfing → confirmation M3 (state
   machine directement inspirée de la boucle déjà présente dans
   `get_m1m3_entry_signal`, mais tenue en continu au lieu d'être calculée en
   batch). **Livrable isolé et testé avant de passer à F.**
2. **Payload F (+ biais MTF)** : ajoute un état de biais mis à jour uniquement
   quand `bar.bar_type` correspond à H1/H4/D1 (R1.3).
3. **Payloads G/H/I (+ session)** : filtre trivial calculé depuis le timestamp
   de la barre courante — aucun état supplémentaire nécessaire.

### R1.6 Test de parité (garde-fou obligatoire, pas une option)
Avant de faire confiance à une étape incrémentale, la faire tourner sur un
segment réel identique à la version vectorisée de référence (R1.4), et
vérifier **mécaniquement**, barre par barre, que les décisions coïncident
(mêmes timestamps de sweep/engulfing/confirmation/biais/signal final). Ce
test devient permanent dans la suite — une divergence future doit le faire
échouer, pas passer inaperçue. C'est la façon EBTA-native de réconcilier
« incrémental natif » avec « ne pas réinventer silencieusement une logique
déjà validée ».

### R1.7 Continuité des pools de liquidité et du biais entre segments (méthodologique)
Les pools de liquidité et le biais MTF ont une « mémoire » qui dépasse la
fenêtre d'un seul fold (`expiry_days=3` par défaut). En incrémental natif,
ceci se résout naturellement si la Strategy reçoit un historique de barres
continu jusqu'au point de coupure d'information du fold (purge/embargo SOP
04) avant l'entrée dans la fenêtre Train/Test/OOS elle-même (warm-up), plutôt
que de démarrer l'état à zéro pile au début du fold. À vérifier explicitement
par un test (un pool né avant le début du warm-up ne doit pas apparaître
par magie, ni un pool légitimement actif être ignoré par démarrage à froid).

### R1.8 Direction et sortie
- **Direction** : le signe de la décision pilote `OrderSide.BUY`/`SELL`
  (aujourd'hui `BUY` codé en dur). Vérifier que le compte `MARGIN`/`HEDGING`
  déjà configuré autorise bien le short.
- **Sortie** : horizon fixe (`fixed_horizon`, `horizon_bars`) piloté par
  `exit_criterion`, fermeture via `close_all_positions`/`close_position` —
  la source ne gère pas de stop/target en exécution réelle (`sl_long`/
  `sl_short` sont des distances diagnostiques du feature lab, jamais des
  ordres stop soumis) ; ne pas sur-construire au-delà de ce que la source
  valide réellement.

### R1.9 Ordres (API déjà vérifiée)
Entrée simple : `order_factory.market(...)`. `OrderFactory.bracket()`
**[vérifié]** reste disponible pour une extension future stop/target, hors
scope ici.

### R1.10 Invariant anti-fuite
La Strategy ne reçoit jamais le `fold_id`/rôle de segment — seulement des
barres (y compris le warm-up de R1.7). Test : deux exécutions du même
candidat sur des barres identiques mais étiquetées Train vs OOS produisent le
même `SimulationResult`.

### R1 — Critères de sortie
- Le registry de stratégies existe ; ajouter le payload E ne touche aucun
  fichier hors `strategies/signals/` et le registry lui-même.
- Payload E incrémental : test de parité vert contre la version vectorisée de
  référence sur un segment réel (extrait de `D:\TRADING\...\Data`, pas une
  fixture jouet).
- Payloads F, G/H/I : chacun ajoute son incrément d'état, chacun avec son
  propre test de parité vert.
- Les payloads E, F, G/H/I produisent des séries de décisions **différentes**
  entre elles sur le même segment.
- La direction short est réellement empruntée quand la décision l'exige.
- Un test d'intégration exécute au moins un segment réel (2+ jours de M1) à
  travers `run_segment()`/Nautilus et produit des ordres reflétant les
  décisions de la state machine (pas un achat systématique au premier bar).
- Continuité des pools/biais vérifiée par test (R1.7) ; aucune branche sur
  l'identité de segment ; test anti-fuite vert (R1.10).
- **Non atteint par ce chantier, explicitement** : le branchement dans
  `nautilus_research_package.py` (chemin de production) — bloqué par R4
  (`_daily_sample`), voir Non-goals.

---

## R2 — Extraction réelle depuis Nautilus

### R2.0 Principe
Remplacer la reconstruction manuelle par la comptabilité de Nautilus. Le
contrat `SimulationResult` ne change pas ; ses champs sont désormais **dérivés
du portfolio/analyzer**, pas recalculés naïvement.

### R2.1 Sources vérifiées (nautilus_trader 1.230.0)
- `engine.portfolio` **[vérifié]** : `equity`, `net_exposure`, `realized_pnl`,
  `unrealized_pnl`, `total_pnl`, `is_flat`, `account`, `analyzer`.
- `engine.portfolio.analyzer` (`PortfolioAnalyzer`) **[vérifié]** : `returns()`,
  `realized_pnls()`, `total_pnl()`, `total_pnl_percentage()`,
  `get_performance_stats_pnls()`, `get_performance_stats_returns()`,
  `add_return`.
- `engine.trader.generate_positions_report()` /
  `generate_order_fills_report()` / `generate_account_report(venue)`
  **[vérifié]**.
- `engine.get_result()` → `BacktestResult` **[vérifié]** : `total_orders`,
  `total_positions`, `stats_pnls`, `stats_returns`.

### R2.2 Série NAV / returns / exposition (par barre)
La NAV instantanée par barre n'est pas exposée telle quelle. Deux options,
à trancher en phase de conception :
- **Option A (recommandée, fidèle)** : la Strategy enregistre un snapshot
  `portfolio.equity` (ou solde de compte) et `portfolio.net_exposure` **à
  chaque `on_bar`**, horodaté par `bar.ts_event`. `extract_simulation_result`
  lit cette série → `nav`, `daily_exposure`. `daily_returns` = variations
  relatives de la NAV. Élimine le bug post-sortie (la NAV reflète l'état réel,
  plat après clôture).
- **Option B** : dériver la NAV cumulée depuis `analyzer.returns()` +
  `starting_nav`. Plus simple mais returns au niveau position, pas par barre.

Décider A vs B au début de R2 (A préféré pour un vrai equity curve).

### R2.3 Coûts réels
- `total_costs` = somme des commissions réelles (colonne commission de
  `generate_positions_report()` / `generate_order_fills_report()`), plus
  financement si activé. Fin de `total_costs = 0.0` en dur.
- **Note de calibration** (déjà tracée) : `MakerTakerFeeModel` est **sans
  effet tant que `maker_fee`/`taker_fee == "0"`** sur l'instrument
  (`NAUTILUS_API_NOTES.md`). Les `_instrument_config()` du package Nautilus
  portent désormais `0.0002/0.0005` : vérifier que des commissions non nulles
  apparaissent réellement dans le rapport après R1 (trades réels).

### R2.4 PnL réalisé / positions
Remplir `positions` depuis `generate_positions_report()` (entry/exit/realized
PnL réels, multi-positions), au lieu de la position unique reconstruite.

### R2.5 Golden-case
Recalibrer `tests/fixtures/nautilus_golden_case/expected_result.py` sur la
sortie réelle du portfolio (le `result_hash` changera — c'est attendu et sain).
Documenter la bascule dans `NAUTILUS_API_NOTES.md`.

### R2.6 NO_MODEL
Conserver le cas « aucun trade » (`_flat_simulation_result`) : NAV plate,
exposition nulle, `total_costs=0.0` — mais désormais dérivé de
`portfolio.is_flat` + rapport vide, pas d'un chemin séparé codé en dur.

### R2 — Critères de sortie
- `nav`, `daily_returns`, `daily_exposure`, `positions`, `total_costs`
  proviennent du portfolio/analyzer/rapports Nautilus, pas d'une reconstruction
  manuelle.
- Le bug post-sortie est éliminé : après clôture, la NAV est plate (test).
- `total_costs > 0` sur un candidat qui trade avec `maker_fee/taker_fee` non
  nuls (test).
- Golden-case recalibré, suite runtime verte, `validate_package_dir()` PASS.

---

## Dépendances et ordre

1. **R1.1** (registry/interface de stratégie) — infrastructure, construite
   une fois, avant toute stratégie concrète.
2. **R1.2/R1.3** (resampling multi-timeframe + souscription multi-bar-type) —
   autonome, prérequis technique du portage incrémental.
3. **R1.4** (modules vectorisés portés comme oracle) — autonome, testable
   sans Nautilus.
4. **R1.5 étape 1** (payload E incrémental) + **R1.6** (parité E) — le
   premier incrément complet, prérequis de tout ce qui suit.
5. **R1.5 étape 2** (F, +biais) + parité F — dépend de (4).
6. **R1.5 étape 3** (G/H/I, +session) + parité G/H/I — dépend de (5).
7. **R2** (Option A) — dépend d'avoir, via (4)-(6), de vrais trades
   différenciés à comptabiliser.
8. **Branchement production** (`nautilus_research_package.py`) — **bloqué**
   tant que R4 (retrait de `_daily_sample`, vrai volume intraday) n'est pas
   résolu ; chantier séparé, explicite, hors scope ici.
9. Ouvre R3 (dériver les gates de `_write_reports` depuis ces vrais artefacts)
   une fois (7) et le branchement production faits.

## Impact sur le pipeline
- WRC teste enfin une famille de candidats réellement distincts, issus d'une
  logique de signal validée plutôt que d'un stub.
- `economic_gate` / `detrending` consomment une NAV et des coûts réels.
- Le `status: PASS` cesse d'être une attestation (une fois R3 fait).
- La couche stratégie/exécution (registry + implémentations incrémentales)
  devient le même code utilisable en recherche et, plus tard, en live — pas
  une réécriture à prévoir.
- Le chemin de production reste sur `_daily_sample` tant que R4 n'est pas
  traité — ce chantier ne doit pas être présenté comme « recherche prête »
  avant que ce branchement existe réellement.

## Risques
- **Divergence silencieuse du portage incrémental** : recoder bar-par-bar une
  logique validée en batch (engulfing, pools, MTF, confirmation M1/M3) peut
  introduire des écarts subtils (off-by-one sur l'expiration, sémantique de
  `reindex`/`ffill` différente en incrémental). **Mitigation obligatoire** :
  le test de parité (R1.6) par niveau de payload, jamais optionnel.
- **Continuité des pools de liquidité et du biais entre folds** (R1.7) :
  démarrer l'état à froid pile au début du fold au lieu d'un warm-up sur
  historique continu casserait la fidélité au comportement validé de la
  source — risque silencieux si non testé.
- **Perf** : le branchement production (vrai volume, R4) exposera le coût du
  `subprocess`-par-segment (R8), indépendamment de cette section. Anticiper
  mais ne pas bloquer R1/R2.
- **Changement de hash golden-case** : attendu ; ne pas le traiter comme une
  régression.
- **Fuite de segment** : la tentation d'optimiser via le rôle du segment doit
  être barrée par le test anti-fuite (R1.10).
- **Confusion chantier fini vs branché** : sans le garde-fou explicite de
  Non-goals, ce chantier pourrait être perçu comme rendant la recherche
  possible en production alors qu'il reste bloqué par R4.
- **Sur-ingénierie du registry** : construire une abstraction plus large que
  nécessaire pour une seule famille de stratégies (liquidity sweep) — le
  registry doit rester minimal (une interface, un dict d'enregistrement), pas
  un framework anticipant des besoins non encore exprimés.

## Validation (à lancer en fin de chantier)
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
python -c "from pathlib import Path; from ebta_engine.validators.package_validator import validate_package_dir; print(validate_package_dir(Path('Implementation/research_packages/nautilus_mvp'))['status'])"
```
