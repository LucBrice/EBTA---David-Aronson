# Audit de maturite — Le moteur EBTA est-il pret pour une vraie campagne de recherche quantitative ?

> Note d'intake, pas un plan. Deposee ici pour triage humain futur, suite a un
> audit technique complet du depot demande le 2026-07-13.
> Etat machine au moment de l'audit : branche `main`, HEAD `184b013`.
> Ce fichier reste `INTAKE`, non executable, tant qu'un humain ne l'a pas
> audite et route vers `.ai/backlog/`.

## Mode de lecture — 2026-07-16

Ce document melange volontairement une photo d'audit initiale et des mises a
jour posterieures. Pour eviter l'ambiguite :

| Marqueur | Sens |
| --- | --- |
| **ACTUEL 2026-07-16** | Etat courant apres les plans deja routes, executes et clotures. |
| **HISTORIQUE 2026-07-13** | Diagnostic initial conserve pour expliquer pourquoi les plans etaient necessaires ; ne pas le lire comme l'etat courant s'il contredit une mise a jour datee. |
| **RESIDUEL** | Risque encore ouvert, a transformer en plan separe si priorise. |

Lecture rapide : la source la plus actuelle de ce fichier est la table
**"Etat courant consolide — 2026-07-16"** en section 5, puis la section
**"Suite proposee"**. Les sections 1 a 4 sont surtout historiques.

## Etat courant resume — ACTUEL 2026-07-16

Cette note reste une **photo d'audit du 2026-07-13**. Depuis cet audit, sept
blocs critiques ont ete traites et clotures dans le cockpit `.ai/` :

- `PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS` est `DONE` : moteur de signaux
  incremental reel, bridge Nautilus delegue au registry, extraction R2 depuis
  snapshots NAV/fills/positions. Le package etait `PASS` a la cloture de ce
  chantier ; ce statut ne doit pas etre confondu avec le package courant apres
  correction WRC/validators/G5.
- `PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION` est `DONE` :
  segments de production alimentes en M1 reel, `bias_filter="none"` respecte
  par G/H/I, et preuve de passage sur la fenetre courte au moment de la
  cloture R4. Mise a jour 2026-07-16 : le `PASS` R4 historique est documente
  comme artefact de NAV degenerescente ; le package persistant courant ne doit
  plus etre lu comme `PASS`.
- Le bug Nautilus observe sur une position ouverte (`avg_px_close=None`) a ete
  corrige dans l'adapter et couvert par test de non-regression.
- `PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE` est `DONE` : le verdict WRC
  reel alimente maintenant `reports/economic.json::statistical_status` /
  `global_status` et `reports/incubation_gate.json::status`. Un WRC `FAIL`
  reel n'est donc plus masque par un `PASS` code en dur a ce niveau.
- `PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE` est `DONE` : le statut
  global du package n'ignore plus les gates reels en echec. `validate_gates()`
  exige maintenant `PASS` pour les champs de verdict connus
  (`PASS`/`FAIL`/`INCONCLUSIVE`), `validate_package_dir()` requiert et lit
  `reports/incubation_gate.json`, et `economic.json::global_status` fait
  echouer le package s'il est different de `PASS`.
- `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` est `DONE` : le champ
  `gates.json::pre_oos_robustness_verdict` n'est plus un litteral `"PASS"`.
  Il propage le verdict reel `procedure_reports["robustness"]["status"]`, et
  le test de verite connue prouve qu'une robustesse `FAIL` rend G5
  `INCONCLUSIVE` au lieu de le laisser passer.
- `PLAN_DOCUMENTATION_ARTEFACT_R4_ET_FAIL_WRC_NAUTILUS_M1` est `DONE` : le
  `PASS` R4 du commit `3bcfe35` est trace comme artefact de NAV degenerescente,
  et le `FAIL` WRC primaire courant du package Nautilus M1 est trace comme un
  verdict EBTA legitime, non comme un bug a masquer.

Les sections ci-dessous conservent leur valeur historique : elles expliquent
pourquoi R1/R2/R4, le defaut WRC masque et le defaut de statut global package
etaient necessaires. Elles ne doivent plus etre lues comme l'etat courant exact
de ces points. Les risques restants a transformer en plans separes sont surtout
: auto-attestations restantes dans `gates.json` / `invariant_evidence.json`
hors G5, qualite des donnees longues, warm-up inter-fold, realisme
couts/slippage/latence, stress de robustesse reel, scalabilite du runner et
edge cases Nautilus.

Limite importante apres les corrections WRC + validators + G5 : le verdict
global de package reflete maintenant les sorties WRC/economic/incubation en
echec, et le verdict de robustesse pre-OOS reel atteint G5. Cela ne transforme
pas encore toutes les attestations du package en preuves derivees. Les sujets
residuels sont des plans separes : remplacer progressivement les booleens
auto-attestes restants de `gates.json` et `invariant_evidence.json` par des
sorties derivees de preuves, puis durcir les scenarios de robustesse eux-memes.

## Audit complet de reprise — ACTUEL 2026-07-16

Cet audit de reprise compare l'audit initial du 2026-07-13 a l'etat reel apres
les workstreams clos jusqu'au commit courant `4df7ad6`. Il ne s'appuie pas
uniquement sur le dernier commit : il recoupe `.ai/checkpoint.json`, les plans
archives, les tests cites, le code d'assemblage et les artefacts persistants du
package Nautilus M1.

### Verdict de reprise

Le verdict initial **"echafaudage de gouvernance qui produit un package
structurellement valide mais scientifiquement creux"** n'est plus exact tel quel
:

- le moteur a maintenant une logique de signaux incrementale reelle ;
- l'extraction Nautilus ne se limite plus a une reconstruction naive ;
- le package courant ne masque plus un WRC primaire `FAIL` derriere des statuts
  verts ;
- le gate G5 lit le verdict de robustesse calcule au lieu d'un litteral
  `"PASS"`.

Mais le moteur n'est pas encore pret pour une vraie campagne quantitative
complete. Son niveau actuel est plutot :

```text
Pipeline EBTA/Nautilus coherent, capable de produire un FAIL honnete,
mais pas encore un moteur de campagne robuste, calibre et reproductible.
```

### Etat mecanique du package Nautilus M1 courant

Verification du package persistant `Implementation/research_packages/nautilus_mvp`
au 2026-07-16 :

| Artefact | Valeur observee | Lecture |
| --- | --- | --- |
| `reports/wrc.json::verdict` | `FAIL` | Verdict statistique primaire legitime, non masque. |
| `reports/wrc.json::wrc_pvalue` | `0.39492101579684064` | Aucune preuve d'edge sur cette famille/ce segment. |
| `reports/economic.json::economic_status` | `PASS` | Les criteres economiques propres passent. |
| `reports/economic.json::statistical_status` | `FAIL` | Le WRC est bien propage vers l'economique. |
| `reports/economic.json::global_status` | `FAIL` | Le statut global economique ne masque plus le WRC. |
| `reports/incubation_gate.json::status` | `FAIL` | L'incubation ne masque plus le WRC. |
| `reports/robustness.json::status` | `PASS` | G5 propage un verdict reel, ici favorable. |
| `reports/gates.json::wrc_status` | `FAIL` | G4 est rouge/inconclusive par valeur, plus seulement par presence. |
| `reports/gates.json::pre_oos_robustness_verdict` | `PASS` | G5 reflete le calcul de robustesse, pas un litteral. |
| `reports/execution.json::total_orders` | `28` | Activite non nulle sur l'ensemble du package. |
| `reports/execution.json::oos_total_orders` | `0` | Point faible restant : pas d'exposition OOS dans l'artefact courant. |
| `validate_package_dir()` | `FAIL` | Echec attendu et coherent : G4/WRC, `economic.global_status`, `incubation_gate`. |

Conclusion : le systeme est plus mature parce qu'il accepte de rester rouge
quand la preuve statistique manque. Ce `FAIL` est un progres de gouvernance,
pas une regression a masquer.

### Matrice complete fait / partiel / ouvert

| Point de l'audit initial | Etat 2026-07-16 | Verdict |
| --- | --- | --- |
| R1 — vrai moteur de signaux | Registry + strategies incrementales E/F/G/H/I branchees dans `GenericPayloadStrategy`. | FAIT |
| R2 — extraction Nautilus reelle | NAV snapshots, fills, positions, commissions et cas position ouverte couverts. | FAIT |
| R3 — preuve vs attestation | WRC, statut global, incubation et G5 sont derives de valeurs calculees ; beaucoup de booleens de `gates.json` / `invariant_evidence.json` restent declaratifs. | PARTIEL |
| R4 — vrai volume M1 | M1 reel branche sur fenetre courte ; le `PASS` R4 historique est requalifie comme artefact et ne vaut pas preuve d'edge. | FAIT TECHNIQUEMENT / PREUVE SCIENTIFIQUE NON |
| R5 — couts/slippage/latence | Code path existe (`MakerTakerFeeModel`, latency/slippage contracts), mais les parametres restent indicatifs ou nuls. | OUVERT |
| R6 — robustesse stressee | Scenarios et gate existent ; les scenarios reutilisent les memes resultats et `minimum_mean_return=-1.0` reste trop permissif. | OUVERT |
| R7 — reproductibilite operationnelle | Le venv Nautilus existe localement et n'est pas suivi par git, mais le data root reste absolu Windows et le hash config Nautilus reste placeholder. | PARTIEL / OUVERT |
| R8 — scalabilite | Runner subprocess conserve pour isolation Windows/Nautilus ; pas encore de benchmark long. | OUVERT |
| R9 — consolidation documentaire | Quelques clarifications ont ete faites dans `AGENTS.md` et les plans, mais les doublons terminologiques et docs historiques restent a nettoyer. | PARTIEL |
| R10 — post-OOS/live reel | Les rapports incubation/live/monitoring restent surtout des validations de rapports fournis en entree. | OUVERT |

### Ce qui a vraiment change depuis l'audit initial

1. **Le moteur n'est plus un buy-and-hold deguise.** Les strategies
   incrementales evaluent des signaux, le bridge Nautilus delegue au registry,
   et les payloads E/F/G/H/I ne sont plus seulement descriptifs.
2. **Le package sait maintenant echouer honnetement.** `wrc_status=FAIL`,
   `economic.global_status=FAIL`, `incubation_gate.status=FAIL` et
   `validate_package_dir().status=FAIL` sont coherents.
3. **G5 n'est plus un faux vert de contenu.** Quand la robustesse calculee est
   `FAIL`, le test de non-regression prouve que G5 devient `INCONCLUSIVE`.
4. **La relecture historique R4 est assainie.** Le `PASS` R4 est conserve comme
   trace historique, mais documente comme artefact de NAV degenerescente.

### Ce qui reste bloquant avant une campagne complete

1. **Package courant rouge par WRC.** Tant que `wrc.verdict=FAIL`, on ne peut
   pas parler d'une strategie candidate validee ; on peut seulement dire que le
   pipeline rejette honnetement cette famille.
2. **Aucune exposition OOS dans l'artefact courant.** `oos_total_orders=0` doit
   devenir un invariant futur si l'objectif est une preuve OOS tradable.
3. **Couts et execution non calibres.** Les frais maker/taker sont indicatifs,
   la latence et le slippage restent essentiellement nuls.
4. **Robustesse non stressee.** Les scenarios doivent appliquer de vrais chocs
   de cout, slippage, latence, fills ou donnees, pas seulement relire les memes
   resultats sous trois labels.
5. **Reproductibilite incomplete.** `DEFAULT_DATA_ROOT` reste absolu Windows et
   `NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER` reste litteral.
6. **Attestations residuelles.** Des champs de gouvernance/post-OOS restent
   declares par le builder au lieu d'etre produits par une decision ou une
   preuve externe.

### Priorite recommandee apres cette reprise

La suite la plus rationnelle n'est pas de chercher a rendre le package courant
`PASS` par ajustement. La prochaine tranche devrait etre un ou deux plans
dedies :

1. `R5/R6` — calibrer les couts/slippage/latence puis construire de vrais
   stress de robustesse.
2. `R7` — rendre le data root configurable, remplacer le hash placeholder et
   documenter l'environnement Nautilus sans committer le venv.
3. `R3-residuel` — deriver les attestations restantes de preuves ou de
   decisions humaines explicites.
4. `R4-long` — benchmark 1 mois / 3 mois / 1 an avec budget temps, memoire,
   ordres, exposition OOS et validation package.

## Avertissement initial — HISTORIQUE 2026-07-13

L'etat machine (`.ai/checkpoint.json`, `Implementation/Active/tracking.json`)
affiche `DONE` / `PASS` / `110 tests PASS` partout. **Ces statuts sont vrais
structurellement mais trompeurs scientifiquement.** L'audit a lu le chemin
critique complet : chargement de donnees -> strategie -> simulation Nautilus ->
extraction -> statistiques -> gates -> validation.

Mise a jour 2026-07-16 : cet avertissement reste utile comme principe de
lecture, mais certains exemples qui l'ont motive ont ete corriges depuis
(R1/R2/R4, WRC masque, validators/statut global package et G5). Le risque
residuel porte surtout sur les attestations restantes hors G5 et la validation
scientifique longue.

---

## 1. Diagnostic initial du moteur — HISTORIQUE 2026-07-13

**Verdict : ce n'est pas encore un moteur de recherche. C'est un echafaudage
de gouvernance qui produit un `research_package` structurellement valide dont
le contenu scientifique est creux.**

Ce verdict est conserve comme diagnostic initial. Il ne doit plus etre lu comme
une description exacte de l'etat courant apres les plans R1/R2/R4 et WRC
masque. A la date du 2026-07-13, quatre constats detruisaient l'idee d'un vrai
backtest :

### a) La strategie n'a aucune logique de signal
`Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::on_bar` :
- au **premier bar**, si `rule_id` est non-vide (toujours) -> **ACHETE**
  (toujours `OrderSide.BUY`) ;
- apres `horizon_bars` -> ferme la position.

Aucun calcul de liquidity sweep, engulfing, biais MTF, filtre de session, ni
direction. Les payloads E-I decrivent une strategie riche dans
`strategies/payloads.py`, mais **rien n'est evalue**. Tous les candidats
executent le meme comportement : acheter au bar 1, tenir N bars, vendre, long
uniquement. Le "backtest" est un buy-and-hold deguise.

### b) L'extraction de resultat est une reconstruction naive
`adapters/nautilus_mapping.py::extract_simulation_result` prend le premier fill
comme entree, le dernier comme sortie, puis reconstruit la NAV bar par bar
comme `starting_nav + (close - entry_price) * quantity` **pour tout le segment,
y compris apres la sortie** (bug de correction). De plus `total_costs = 0.0`
est code en dur : les frais Nautilus ne sont jamais extraits. On n'utilise ni
le portfolio, ni l'`analyzer`, ni le PnL reel de Nautilus.

### c) Le volume de donnees est un jouet
L'orchestrateur charge NASDAQ + XAUUSD, puis `_daily_sample` reduit le
1-minute a **un bar par jour** sur une fenetre de **10 jours** (~7 points par
actif), walk-forward `train=2, test=1, oos=1, K=2`. Or il existe **8 actifs en
1-minute sur toute l'annee 2020** sur `D:\TRADING\...\Data`. On dispose de
millions de barres et on en utilise sept.

### d) La robustesse ne stresse rien
Les trois scenarios `CENTRAL/PLAUSIBLE/EXTREME` recoivent **exactement les
memes donnees**, avec un seuil `minimum_mean_return = -1.0` (-100%). Aucun choc
de cout/slippage/latence. Le gate de robustesse ne peut structurellement pas
echouer.

**Peut-on executer un vrai backtest de recherche ? Non.** On peut executer un
prototype de bout-en-bout qui produit un artefact valide. La mecanique de
gouvernance est reelle ; le contenu simule ne l'est pas.

---

## 2. Audit par zones — HISTORIQUE avec notes 2026-07-15

### Solide et reellement operationnel
- `procedures/wrc.py` : White's Reality Check + SPA + Romano-Wolf + MCPM.
  Excellent, du vrai travail statistique.
- `procedures/oos_confidence_interval.py`, `bootstrap.py`, `zero_centering.py`.
- `procedures/detrending.py` (formule SOP 07 correcte, mais alimentee par des
  donnees canned — voir 3).
- `validators/*`, `schema_validation.py`, `schemas/` : rigoureux sur la
  structure et de nombreuses coherences croisees. Mise a jour 2026-07-15 :
  `validate_gates()` et `validate_package_dir()` font maintenant refleter les
  echecs WRC/economic/incubation dans le statut global du package ; les
  attestations residuelles de `gates.json` / `invariant_evidence.json` restent
  a traiter separement.
- `manifests/` : notarisation SHA-256 reelle et testee.
- `governance/` (G-BIAS, SOP 13) : checkers reels.
- `data/local_ohlcv.py`, `data/walk_forward.py` : reels et corrects.
- `adapters/nautilus_mapping.py` (mapping instrument/couts/barres) : reel,
  verifie contre l'API 1.230.0. C'est l'extraction (2b) qui est faible.

### Present mais trompeur / incomplet
- `adapters/nautilus_strategy_bridge.py` : stub de signal (1a). Trou noir du
  projet.
- `adapters/nautilus_mapping.py::extract_simulation_result` : NAV naive, couts
  a 0, ignore la compta Nautilus (1b).
- `risk/robustness.py` + grille orchestrateur : calcul reel mais aucun stress
  applique (1d).
- `package_builder/nautilus_research_package.py` : selection sur la moyenne des
  returns du stub ; downsampling ~7 barres ; detrending non recable.
- `examples/minimal_pilot_pipeline/build_research_package.py::_write_reports` :
  **le point le plus grave.** Le dict `gates` code en dur ~50 booleens a
  `True` et `invariant_evidence` fixe `gate_reports: {statistical: PASS,
  economic: PASS, final: PASS}`, tous les `package_stages` (jusqu'a
  `LIVE_LIMITED_STARTED`), `manifest_hash_failures: []`. Le validateur valide
  une auto-attestation, pas une preuve derivee. Mise a jour 2026-07-15 : le
  cas precis du verdict WRC masque dans les gates economique/incubation est
  corrige, et le statut global du package consomme maintenant ces echecs via
  les validators ; le reste du sujet d'auto-attestation demeure ouvert
  (`gates.json` / `invariant_evidence.json`, hors G5 depuis la correction du
  2026-07-16).
- `procedures/incubation_report.py`, `monitoring.py`, `lifecycle.py`,
  `reproduction_report.py` : valident des rapports fournis en entree statique.
  Tout le cycle post-OOS (incubation -> paper trading -> deploiement -> live ->
  kill switch -> monitoring) est fictif.

### Dette structurelle / incoherences
- Mise a jour 2026-07-16 : le venv Nautilus existe localement sous
  `Implementation/adapters/nautilus_env/venv/`, mais il n'est pas suivi par
  git dans l'etat courant verifie. La dette residuelle est donc la
  documentation/recreation de l'environnement, pas le retrait de fichiers tiers
  deja commites.
- `DEFAULT_DATA_ROOT` = chemin absolu Windows en dur (`local_ohlcv.py`). Non
  reproductible ailleurs.
- `document_hash: "NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER"` : le hash d'integrite
  de config est un placeholder litteral.
- Doublons de vocabulaire : `procedures/robustness.py` vs `risk/robustness.py`,
  `procedures/walk_forward.py` (validation) vs `data/walk_forward.py`
  (splitter).
- `CLAUDE.md` affirme "stdlib-only, no pyproject.toml" — desormais faux :
  pyproject.toml + numpy/pandas/nautilus_trader. La doc d'autorite a diverge.

---

## 3. Reel vs. impression de fonctionner — HISTORIQUE 2026-07-13

**Reellement execute :** WRC et secondaires, IC OOS, bootstrap, detrending (sur
ses entrees), selection de complexite, matrice de candidats, validation
schemas/manifests/invariants, checkers G-BIAS, mapping Nautilus, walk-forward
splitter, execution effective de `BacktestEngine`.

**Facade :**
- Le `status: PASS` du research_package (attestation, pas decouverte).
- La strategie (buy-and-hold quel que soit le payload).
- L'economie (NAV/couts) : reconstruction naive, couts nuls.
- La robustesse : 3 scenarios identiques, jamais bloquants.
- Le detrending du paquet Nautilus : alimente par les entrees canned du pilote,
  deconnecte de la simulation.
- L'experience "gagnant vs perdant" : prouve que le gate rejette une serie a
  return negatif (arithmetique correcte), via des fixtures concues pour que
  NASDAQ monte et XAUUSD baisse sous le stub. Ne demontre aucune discrimination
  de strategie.

**Prevu par l'architecture mais inexistant :** moteur de features/signaux,
extraction de la compta reelle Nautilus, realisme des couts, stress reel,
boucle d'incubation/monitoring/deploiement live.

---

## 4. Ecart initial avec un vrai moteur de recherche quantitative — HISTORIQUE 2026-07-13

Liste initiale des composants manquants, par gravite decroissante. Voir la
table d'etat courant en section 5 pour savoir lesquels ont ete traites depuis.

1. Moteur de signaux / features (coeur absent) — bloquant absolu.
2. Extraction fidele de la performance depuis Nautilus — bloquant.
3. Realisme des couts (frais/slippage calibres).
4. Volume de donnees (vrai 1-minute multi-mois/multi-actifs).
5. Stress de robustesse effectif.
6. Boucle de recherche reelle (candidats distincts par leur logique,
   calibration Train-only, selection OOS-safe).
7. Separation preuve/attestation (les gates doivent deriver leurs booleens).
8. Reproductibilite operationnelle (data root parametrable, hash reel, venv
   hors depot).
9. Performance/scalabilite (aujourd'hui un `subprocess` Python relance par
   segment).

---

## 5. Roadmap initiale et etat courant

### Roadmap initiale — HISTORIQUE 2026-07-13

Cette sous-section conserve les priorites telles qu'elles existaient au moment
de l'audit. Elle explique l'ordre des chantiers deja executes ; elle n'est pas
la liste courante des prochains travaux.

#### CRITIQUE
- **R1 — Vrai moteur de signaux dans la strategie.** Sans lui tout teste du
  vide. Aucune dependance ; debloque tout.
- **R2 — Extraire la performance reelle depuis Nautilus.** Depend de R1.
  Rend `economic_gate` et `detrending` valides.
- **R3 — Decoupler preuve et attestation dans `_write_reports`.** Depend de
  R1/R2. Le `PASS` redevient une decouverte auditable.

#### IMPORTANT
- **R4 — Vrai volume de donnees** (retirer `_daily_sample`). Depend de R2 pour
  la perf.
- **R5 — Realisme des couts** (frais/slippage/latence calibres, sources).
- **R6 — Robustesse reellement stressee** (chocs appliques). Depend de R5.
- **R7 — Sortir le venv du depot + requirements.txt + data root parametrable +
  hash de config reel.** Independant, rapide, gros gain.

#### AMELIORATION
- **R8 — Remplacer le subprocess-par-segment** par un runner in-process.
- **R9 — Consolider les doublons + realigner `CLAUDE.md`.**
- **R10 — Rendre la boucle post-OOS reelle** (seulement quand une strategie
  survit reellement a l'OOS).

### Etat courant consolide — ACTUEL 2026-07-16

| Item de la roadmap initiale | Etat courant | Commentaire |
| --- | --- | --- |
| R1 — Vrai moteur de signaux | TRAITE / DONE | Le bridge Nautilus execute maintenant des strategies incrementales E/F/G/H/I via registry. |
| R2 — Extraction performance Nautilus | TRAITE / DONE | Extraction via snapshots NAV, fills, positions ; cas position ouverte couvert. |
| R3 — Preuve vs attestation | PARTIELLEMENT TRAITE / RESIDUEL A PLANIFIER | Le bug WRC masque est corrige dans `economic.json` et `incubation_gate.json`, `PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE` a corrige `validate_gates()` + `validate_package_dir()` pour que le statut global du package bascule quand WRC/economic/incubation echouent, et `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` a branche le verdict reel de robustesse pre-OOS dans G5. Reste le sujet d'architecture : `gates.json` / `invariant_evidence.json` contiennent encore des attestations a deriver de preuves hors G5. |
| R4 — Vrai volume M1 | TRAITE / DONE pour fenetre actuelle | M1 reel branche dans le package de production ; reste a tester sur horizon long. |
| R5 — Realisme couts/slippage/latence | A PLANIFIER | Necessite sources et calibration, pas seulement un code path. |
| R6 — Robustesse stressee | A PLANIFIER | Les scenarios doivent appliquer de vrais chocs. |
| R7 — Reproductibilite operationnelle | PARTIEL / A PLANIFIER | Le venv Nautilus est local et non suivi par git, mais le data root reste un chemin Windows absolu, le hash config Nautilus reste placeholder, et la doc d'autorite reste a realigner. |
| R8 — Performance/scalabilite | A PLANIFIER | R4 a ajoute un parallelisme subprocess controle ; un benchmark long reste necessaire. |
| Correction WRC masque | TRAITE / DONE | Le verdict WRC reel atteint les gates economique et incubation. |
| Correction statut global package | TRAITE / DONE | `validate_gates()` et `validate_package_dir()` ne laissent plus un package global `PASS` quand les gates WRC/economic/incubation reels echouent. |
| Correction G5 robustesse fige | TRAITE / DONE | `gates.json::pre_oos_robustness_verdict` propage le statut reel de robustesse ; le `FAIL` WRC M1 courant reste exogene a G5 et documente comme verdict legitime. |

### Note a garder dans un coin — futurs plans de durcissement

Ces points ne sont pas a executer directement depuis ce fichier. Ils doivent
etre transformes plus tard en plans `0 - HUMAN START HERE/` puis routes via
`/start` si l'humain decide de les prioriser.

1. **Warm-up inter-fold / lookback**
   Verifier que les segments test/OOS recoivent assez de contexte historique
   pour les payloads qui utilisent une fenetre de lookback. C'est un risque
   technique concret, pas une regle normative nouvelle.

2. **Benchmark donnees longues / scalabilite**
   Tester 1 mois, 3 mois, puis 1 an sur NASDAQ/XAUUSD, avec budget temps,
   memoire, timeouts, nombre d'ordres, `validate_package_dir()` et package
   `PASS` si la famille testee le merite statistiquement. Le chantier R4 a
   prouve le branchement M1 sur fenetre courte, pas l'echelle ni l'edge.

3. **Validateur qualite CSV M1**
   Ajouter des controles sur timestamps monotones UTC, doublons, trous,
   coherence OHLC, volumes invalides, journees partielles et changements de
   format. Ces controles doivent etre en amont de toute recherche longue.

4. **Edge cases Nautilus**
   Ajouter des tests cibles : position ouverte, rapport vide, zero fill, fill
   partiel, ordre rejete/annule, precision prix/quantite, commissions absentes
   ou non numeriques.

5. **Invariant `PASS` non inerte**
   R4 impose deja `total_orders > 0`. A renforcer plus tard avec
   `oos_total_orders > 0`, exposition non nulle, NAV non plate, couts presents
   si le modele de frais le requiert, et coherence entre fills/positions/NAV.

6. **Frontiere bug-hunter vs validation scientifique**
   `bug-hunter` doit rester le filet mecanique (typage, contrats Python,
   Optional non gardes, regressions testables). Les risques de robustesse,
   puissance statistique, realisme economique et qualite de recherche doivent
   devenir des plans de validation dedies, pas des heuristiques de bug-hunter.

---

## 6. Vision globale

Les pourcentages ci-dessous sont des estimations **HISTORIQUES 2026-07-13**,
non recalculees apres R1/R2/R4/WRC. Ils doivent etre relus comme une mesure de
maturite initiale, pas comme un score courant exact.

- Echafaudage gouvernance/stats/validation : **~70-75%** (reellement construit,
  teste, serieux — la vraie valeur du depot).
- Capacite de moteur de recherche quantitative : **~15-20%** (coeur absent).
- Global vers "campagne robuste et reproductible" : **~20-25%**.

### Risques techniques principaux — RESIDUEL / a requalifier par plan
1. **Illusion de completude** (risque n1) : tout est `DONE`/`PASS`, d'ou le
   danger d'ouvrir une vraie campagne sur un moteur creux et de "valider" du
   bruit. Le checkpoint a deja connu ce faux-positif (RISK_007).
2. **Attestation != calcul** : l'architecture laisse le pipeline ecrire ses
   propres verdicts.
3. **Reproductibilite** : chemin data en dur, hash placeholder, environnement
   Nautilus local a rendre recreable proprement.
4. **Scalabilite** : subprocess-par-segment.
5. **Fidelite de simulation** : rejeter la compta Nautilus annule le benefice
   du choix de Nautilus.

### Points bloquants avant une campagne complete
Etat 2026-07-16 : R1, R2, R4 et G5 ne doivent plus etre lus comme des bloquants
ouverts pour la fenetre de production courte. Le `FAIL` WRC M1 courant est un
verdict EBTA legitime : il bloque une lecture "package gagnant", pas la cloture
du chantier G5. Les bloquants restants sont :

1. Gates/invariants encore partiellement auto-attestes (R3 residuel hors statut global package et hors G5).
2. Realisme couts/slippage/latence non calibre (R5).
3. Robustesse non stressee par de vrais chocs (R6).
4. Reproductibilite operationnelle incomplete (R7).
5. Preuve d'echelle longue encore absente : donnees multi-mois/multi-actifs,
   warm-up inter-fold, edge cases Nautilus et budget temps/memoire.

Tant que ces points ne sont pas leves, lancer une campagne complete pourrait
encore produire un research_package `PASS` scientifiquement trop faible — le
pire resultat pour un cadre dont toute la valeur est l'honnetete statistique.

---

## Remise en question de l'architecture

La decision la plus risquee a long terme n'est pas Nautilus, c'est la
**porosite entre la couche qui calcule les preuves et celle qui les declare**.
Le pilote ecrit encore une partie de `gates.json` / `invariant_evidence.json`
comme des documents "tout est vrai", puis les validateurs relisent ces
artefacts. C'est inverse : les gates
devraient etre des **sorties** produites par les procedures a partir des
artefacts de simulation, jamais des **entrees** redigees par le constructeur du
paquet. Mise a jour 2026-07-16 : le premier vrai signal existe maintenant, le
statut global package consomme desormais les echecs WRC/economic/incubation, et
G5 consomme le verdict de robustesse pre-OOS reel. Le sujet restant est donc a
traiter cote contenu des attestations residuelles (`gates.json`,
`invariant_evidence.json` hors G5), pas comme un prealable au signal.

Second point : avoir choisi Nautilus (moteur event-driven lourd) puis
contourner sa comptabilite revient a payer le cout sans le benefice. Soit on
utilise reellement le portfolio/analyzer de Nautilus (recommande), soit un
moteur vectoriel leger suffirait a ce stade.

---

## Suite proposee

Les plans R1/R2, R4, la correction ciblee du WRC masque, la correction du statut
global de package, la correction G5 et la documentation du `PASS` R4 artefactuel
/ `FAIL` WRC M1 legitime ont ete routes, executes et clotures apres cet audit.
La suite utile n'est donc plus de relancer ces chantiers, mais de creer un ou
plusieurs plans separes pour les risques encore ouverts :

- preuve vs attestation residuelle (`R3`) : deriver progressivement les champs
  restants de `gates.json` et `invariant_evidence.json` de preuves plutot que
  d'attestations ;
- realisme couts/slippage/latence (`R5`) ;
- robustesse vraiment stressee (`R6`) ;
- reproductibilite operationnelle (`R7`) ;
- durcissement donnees longues / warm-up / edge cases Nautilus (note ci-dessus).

Ce document reste volontairement en `INTAKE` : il sert de reservoir de constats
et de futurs plans, pas de source executable.
