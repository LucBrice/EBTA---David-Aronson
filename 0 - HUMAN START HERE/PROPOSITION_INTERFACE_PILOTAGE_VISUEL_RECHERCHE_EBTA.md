# Interface de Pilotage Visuel de la Recherche EBTA
## Note d'intake : rendre le moteur palpable, sans devenir une source de decision concurrente

---

> [!IMPORTANT]
> **Statut : INTAKE non audite.** Ce document vit dans
> `0 - HUMAN START HERE/` et n'est donc pas executable en l'etat
> (`AGENTS.md` / `CLAUDE.md`). Avant tout `/start`, il lui manque le triage
> obligatoire (`Track`, `Lifecycle`, `Scope`, `Non-goals`, `Source`,
> `Exit criteria`).
>
> **Ce document propose une dependance technique externe** dans un moteur
> concu `stdlib-only by design`. `CLAUDE.md` l'interdit explicitement sans
> decision humaine explicite : *« Adding technical dependencies (the engine
> is stdlib-only by design) »* fait partie des « Modifications forbidden
> without an explicit human decision ». La decision de principe a deja ete
> discutee et actee en conversation le 2026-07-21 (« Autoriser une
> dependance web+graphiques ») — voir section 4, D1 — mais reste a tracer
> formellement au meme titre que les decisions D1-D6 du pivot Nautilus
> avant tout `/start`.
>
> Ce document ne modifie ni `Protocole/`, ni aucun fichier existant sous
> `Implementation/ebta_engine/procedures`, `validators/`, `governance/`,
> `manifests/`. Il propose un plan et un catalogue de visualisations.

---

## 0. Role du document et contexte

Discussion humaine du 2026-07-21, faisant suite a l'analyse de l'etat du
projet (pivot Nautilus execute, EPIC de maturite clos, moteur capable de
produire une campagne pre-OOS reproductible/calibree/stressee/auditable,
mais aucune stratégie encore concue ni validee). Le constat pose par
l'utilisateur : le backend est solide mais reste abstrait sans visuel ;
l'ancien outillage BACKTRADER offrait un espace palpable pour configurer
les donnees et visualiser payloads, equity curve et distributions. Le
besoin exprime va au-dela d'un simple visualiseur : une interface complete
de **Research Package Builder**, ou une strategie declare ses parametres
(modifiables / encadres / verrouilles / generes automatiquement) et
l'utilisateur construit, valide et lance une recherche sans reecrire de
code a chaque experimentation.

Ce document n'est pas la decision de lancer ce chantier — c'est la carte de
faisabilite et de decoupage prealable, au meme role que
`PROPOSITION_PIVOT_MOTEUR_NAUTILUS_TRADER.md` pour le pivot Nautilus.

### Ce qui motive ce projet, et ce qu'il ne doit pas devenir

| Element | Role | Change avec ce plan ? |
|---|---|---|
| `Protocole/` | Autorite normative : ordre des gates, SOP, decisions. | Non |
| `Implementation/ebta_engine/procedures/`, `validators/`, `governance/`, `manifests/` | Calculs, gates, scellement, G-BIAS. | Non — l'interface les lit, ne les remplace jamais |
| `Implementation/ebta_engine/strategies/payload_factory.py` (`StructuralAxis`, `StrategyFamilySpec`, `generate_family()`) | Contrat declaratif de parametres deja existant, aujourd'hui appele uniquement par du code Python. | **Etendu** — expose a une interface, pas reecrit |
| `Implementation/ebta_engine/strategies/indicator_library.py` (nom provisoire, n'existe pas encore) | Catalogue declaratif d'indicateurs et de filtres reutilisables (id, mode de calcul, parametres types, spec de rendu) referencable par `entry_criterion`/`exit_criterion`/`bias_filter`/`time_filter`, aujourd'hui du texte libre dans `strategies/payloads.py`. | **Nouveau composant partage** entre `strategies/` et l'interface — voir section 2.1 |
| **Nouvelle interface** (`Implementation/interface/`, nom provisoire) | Lit les artefacts produits (`reports/`, `series/`), construit un `config.json` candidat non scelle, affiche l'avancement d'une execution. | **Nouveau composant, jamais source de verite methodologique** |
| Ce document | Carte de faisabilite, catalogue de visualisations, decoupage en lots. | — |

Non-objectifs de ce document :

- ne pas rouvrir `Protocole/` ni les gates G0-G14 ;
- ne jamais permettre a l'interface de modifier un champ apres scellement
  (invariant G0 — preenregistrement avant resultat) ;
- ne jamais transformer l'interface en un raccourci d'ouverture OOS ;
- ne pas construire ici le sas humain pre-OOS (`registry_review`,
  `pre_oos_approval`) — sujet explicitement differe (voir section 4, D5) ;
- ne pas decider ici, unilateralement, la version exacte des dependances —
  ce document pose le choix (Flask + Plotly), une decision humaine formelle
  reste a tracer au `/start` ;
- ne jamais laisser l'interface choisir, deduire ou deviner un indicateur/
  filtre a afficher — elle affiche exactement et seulement ce que la
  strategie declare via la bibliotheque (section 2.1).

---

## 1. Frontiere : ce que l'interface fait, ce qu'elle ne fait jamais

| L'interface (via son adapter) fait | L'interface ne fait jamais |
|---|---|
| Lire des artefacts deja produits (`reports/*.json`, `series/`, `manifests/`) et les afficher | Calculer un WRC, un Sharpe, un p-value — elle affiche des nombres deja calcules par `procedures/`, jamais elle ne les recalcule |
| Construire un `config.json` candidat, non scelle, a partir d'un formulaire | Ecrire dans `registry.jsonl` ou `oos_access_log.jsonl` (append-only, jamais touches par l'interface) |
| Exposer les axes/parametres declares par `StrategyFamilySpec` sous forme de formulaire | Inventer un parametre ou une regle absente du contrat declare par la strategie |
| Afficher l'avancement d'une execution deja lancee (barres de progression) | Decider elle-meme si une etape passe au suivant — cette decision reste dans `validators/`, `governance/` |
| Verrouiller visuellement un champ apres scellement (lecture seule, feedback visuel) | Autoriser une modification d'un champ scelle — meme un contournement UI reste un contournement de G0 |
| Declencher un run pre-OOS explicitement autorise par l'utilisateur | Ouvrir l'OOS sans que les gates et les preuves humaines requises soient reunies |
| Lire les references d'indicateurs/filtres declarees par la strategie et les rendre selon la spec de rendu de la bibliotheque | Deviner, deduire ou choisir arbitrairement quel indicateur afficher — si une strategie ne declare rien, l'interface n'affiche rien, jamais un indicateur par defaut invente |

---

## 2. Decisions deja actees en conversation (2026-07-21)

| # | Decision | Portee |
|---|---|---|
| 1 | Perimetre : interface complete (visualiseur + builder de parametres + lancement), pas seulement un visualiseur passif. | Cadre l'ambition du projet, phase en lots (section 5) |
| 2 | Dependance technique autorisee : un framework web leger et une librairie de graphiques, confines dans une nouvelle frontiere dediee (meme principe que `adapters/` pour Nautilus). | Debloque le choix technique — a tracer formellement au `/start` (D1, section 4) |
| 3 | Choix technique recommande : **Flask** (leger, mature, pas de besoin d'async pour un outil de formulaires/tableaux) + **Plotly** (genere du HTML/JS autonome, pas de JavaScript a ecrire a la main). | Point de depart, modifiable par decision humaine au `/start` |
| 4 | Navigation : vue d'ensemble d'abord, puis zoom sur une candidate/un fold. | Structure l'ecran principal (section 3.1) |
| 5 | Detail des gates : feu tricolore simple par defaut, detail chiffre au clic. | Structure le tableau de bord des gates (section 3.1) |
| 6 | Le suivi d'execution en direct (barres de progression) est une capacite distincte d'un visualiseur de packages termines — mecanisme different (observer un run en cours vs. lire un artefact fini). | Justifie que ce soit un lot separe (Lot 2, section 5), pas le meme livrable que le Lot 1 |
| 7 | Ce que l'interface affiche (indicateurs, filtres, features) ne doit jamais etre arbitraire ou devine par l'interface — cela doit deriver entierement de ce que la strategie declare vouloir afficher. | Introduit la bibliotheque d'indicateurs/filtres (section 2.1) comme prealable a l'Ecran F (builder) et l'Ecran G (serie OHLC + overlays) |

---

## 2.1 Bibliotheque d'indicateurs et de filtres — principe

Constat : `strategies/payloads.py::StrategyPayload` porte aujourd'hui
`entry_criterion`, `exit_criterion`, `bias_filter`, `time_filter` comme
texte libre ou dict non structure — deja signale comme un trou dans
`PROPOSITION_PIVOT_MOTEUR_NAUTILUS_TRADER.md` (section 4, Brique N3 :
*« entry_criterion/exit_criterion restant des champs texte libres dans
strategy_payload.schema.json, aucun enum de type d'ordre »*). Sans
structure, l'interface n'a aucun moyen fiable de savoir quoi tracer sur
l'Ecran G — elle serait forcee de deviner, ce que ce document interdit.

Principe propose : chaque strategie reference des indicateurs/filtres par
identifiant et parametres, au lieu de texte libre. Une bibliotheque
declarative centralise, pour chaque entree :

| Champ | Role |
|---|---|
| `id` | Identifiant stable (ex. `sma`, `rsi`, `session_window`, `liquidity_sweep`) |
| `computation` | Reference au calcul reel — un indicateur `nautilus_trader.indicators` deja utilise par `GenericPayloadStrategy` (voir Brique N3 du pivot Nautilus), ou une procedure EBTA custom |
| `parameters` | Parametres types avec limites (ex. `period: int, 2-200`) |
| `rendering_spec` | Comment l'afficher : `overlay_line`, `oscillator_panel`, `band`, `marker`, `feature_row` — jamais decide par l'interface elle-meme |
| `version` | Verrouillee une fois referencee par un `config.json` scelle (voir D8, section 4) |

Une strategie qui declare `entry_criterion: {indicator: "rsi", period: 14,
threshold: 30}` permet a la fois (a) a `GenericPayloadStrategy` de savoir
quoi executer, et (b) a l'interface de savoir quoi tracer sur l'Ecran G —
la meme declaration alimente les deux, sans duplication ni divergence.

Ce catalogue vit dans `strategies/`, pas dans l'interface : ce n'est donc
pas un composant confine a `Implementation/interface/` comme le reste de
ce document le proposait — il touche le contrat de strategie lui-meme,
avec les memes regles de modification qu'un changement de
`strategies/payloads.py` (voir `.ai/governance/AI_MODIFICATION_CHECKLIST.md`).
Ce document ne le construit pas ; il pose le principe et ses consequences
(D7 revise, D8 nouveau — section 4).

---

## 2.2 Taxonomie des verdicts et echecs "metier" — ce que l'interface ne doit pas aplatir

Verifie dans le Protocole (`SOP 10`, `SOP 06`) et confirme identique dans
`Implementation/ebta_engine/constants.py`. Ce ne sont pas des variantes
d'un meme "FAIL" — ce sont des verdicts normatifs distincts, avec des
regles d'affichage propres :

| Statut | Niveau | Sens | Regle d'affichage imposee |
|---|---|---|---|
| `PASS` | Paquet | Seul statut autorisant l'incubation (G12) | — |
| `NOT_VALIDATED` | Paquet | Preuve statistique insuffisante | Jamais presente comme reparable |
| `REJECTED_ECONOMIC` | Paquet | Gate statistique PASS, mais rendement/risque/couts/capacite echouent | **Ne doit jamais etre presente comme un echec statistique** (SOP 10 §15, exigence normative explicite) |
| `FAIL` | Paquet | μ_OOS ≤ 0 ou violation methodologique irreparable | OOS "brule" pour toute version descendante |
| `INCONCLUSIVE` | Paquet/gate | Cause prespecifiee (donnees invalides, non-determinisme, incident externe) | N'autorise ni reparation ni changement de metrique |
| `INVALID_TECHNICAL` | Paquet/gate | Erreur technique objective (voir D10) — une mauvaise performance n'est **jamais** un bug | Reexecution encadree possible, sinon nouvelle version |
| `NO_MODEL` / `STOP_PROCESS` | Fold local | Aucune candidate deployee sur ce fold / processus arrete | Convention cash, jamais un echec cache |
| `BURNED` | Segment OOS / G-BIAS | Contamination collective, periode non vierge | Bloque toute reutilisation, meme pour une version descendante |

Consequence directe : l'Ecran A (feu tricolore par gate, section 3.1) tel
que decrit initialement aplatit tout ceci en 3 etats (`PASS`/`FAIL`/
`INCONCLUSIVE`). C'est insuffisant — le badge de statut package et le
detail au clic doivent refleter la valeur exacte parmi les 6 verdicts
ci-dessus, avec l'habillage impose pour `REJECTED_ECONOMIC` en
particulier (voir D11, section 4).

## 2.3 Cycle de vie d'un research_package — ouverture et fermeture

Il n'existe pas de fonction normative unique « ouvrir une recherche ». Le
cycle reel est une suite de scellements gates, verifie dans
`constants.py::PACKAGE_STAGES` et `PAQUET D'EXECUTION EBTA.md` :

```
config construit (Lot 4)
  -> G0 preenregistrement scelle
  -> G7  PRE_OOS_SEALED        (checklist G-BIAS initiale jointe)
  -> G8  acces OOS autorise    (reviewer + G-BIAS PASS obligatoires)
  -> G9/G10  estimation OOS + gate economique
  -> G11 VALIDATION_READY      (rapports complets + reproduction independante PASS + approbation d'incubation)
  -> G12 incubation (paper trading)
  -> G13 DEPLOYMENT_CERTIFIED  (paper trading PASS + kill switch + approbation de deploiement signee)
  -> G14 LIFECYCLE_ARCHIVED    (fermeture)
```

« Ouvrir une nouvelle recherche » via l'interface correspond donc
precisement au Lot 4 (construire et valider `config.json`) suivi du
scellement G0/G7 — pas a un bouton generique "nouveau projet". « Fermer »
correspond a G14 : un artefact dedie
(`Implementation/ebta_engine/schemas/lifecycle_archive.schema.json`)
exige `archive_id`, `package_stage=LIFECYCLE_ARCHIVED`, `archived_at`,
`retention_expires_at` (>= 10 ans, decision normative DN-041),
`withdrawal_reason`, `final_verdict` (les 6 valeurs de la section 2.2 +
`LIFECYCLE_END`). **Ni l'ouverture precise (G7/G8) ni la fermeture (G14)
n'etaient couvertes par le decoupage en lots initial (section 5) — corrige
ci-dessous.**

Point de vigilance verifie dans le code : `LIVE_LIMITED_STARTED`, cite
dans l'audit de maturite du 2026-07-13, n'est **pas** un stade normatif —
c'est la trace d'un bug deja corrige (auto-attestation factice de stades
non atteints, commit `3bcfe35`). Ne jamais le faire apparaitre dans
l'interface comme un stade reel.

## 2.4 Autorisations humaines — trois familles distinctes

Le sas pre-OOS deja identifie (D5) n'est qu'une des trois familles
d'autorisation humaine que le Protocole exige :

| Famille | Ou | Champs exiges d'un humain | Code existant |
|---|---|---|---|
| 1. Preuves pre-OOS | `governance/human_evidence.py` | `registry_review`, `pre_oos_approval` (evidence_id, reviewer_id, status, scope, approved_at UTC, source_reference, subject_id, independence_attested) | Oui — deja code, aucune interface (D5, differe) |
| 2. Reviewer G-BIAS transversal | SOP 13 — incident de biais (gravite `LEVEL_0`-`LEVEL_5`) ou derogation methodologique | Incident : `reviewer`, `review_decision`, `gbias_status`, `approved_by`. Derogation : 6 booleens d'admissibilite (`documented_before_affected_decision`, `independent_of_observed_result`, `no_oos_repair_effect`, `no_metric_or_hurdle_repair`, `no_candidate_family_reduction`, `reviewer_independent`) + decision `APPROVED/REJECTED/INCONCLUSIVE` signee | Partiel — `bias_gate.py` verifie deja `reviewer_report.independent_reviewer`/`status`, mais aucune interface |
| 3. Approbations de gate de paquet | G8 (acces OOS, champ `reviewer` du schema `oos_access_event`), G11 (approbation d'incubation), G13 (approbation de deploiement), G14 (raison de retrait) | Signature/justification humaine par gate | **Inegal** — G8 a un champ `reviewer` verifie mecaniquement ; G11/G13 sont normatifs dans le Protocole mais n'ont **pas encore** de module Python dedie qui les verifie — meme risque que D10 (ne pas fabriquer un formulaire pour une approbation que le moteur ne consomme pas encore reellement, voir D12) |

---

## 2.5 Statuts et domaines des parametres de recherche

Retour utilisateur du 2026-07-21 : un input "libere" (rendu modifiable) ne
doit jamais devenir une simple case editable — il doit obligatoirement
declarer **comment** il est explore, sinon le Research Package ne doit pas
pouvoir se construire. Verifie dans le code reel : ce systeme n'existe pas
aujourd'hui.

**Ce qui existe** (`strategies/payload_factory.py::StructuralAxis`) :
uniquement des valeurs discretes explicites (`values: tuple[str, ...]`),
combinees par produit cartesien pur (`search_space.py::expand_parameter_grid()`,
`itertools.product`, aucun random/sampling). Le champ `requires` gere une
dependance conditionnelle entre axes, mais en repli **silencieux** sur la
valeur par defaut si la condition n'est pas remplie — jamais une erreur ou
un etat explicite. C'est le meme risque de "silence" que ce projet
interdit ailleurs (jamais un defaut invente sans le dire).

**Ce qui n'existe pas** : min/max + pas, nombre de valeurs a generer,
echelle lineaire/log, distribution d'echantillonnage, un statut "derive"
type par champ (aujourd'hui une simple convention de nommage, ex.
`complexity` calcule et injecte sans etre marque comme tel), un statut
"verrouille apres validation" par champ (seul un hash global du payload
existe, pas un verrou par parametre), et aucune regle qui bloque la
construction si un parametre libre n'a pas de domaine defini (seul un
`ValueError` generique si une liste de valeurs est vide par accident).

**Modele propose** — sept statuts explicites par parametre, chacun avec sa
regle de generation obligatoire si le statut l'exige :

| Statut | Regle de generation exigee |
|---|---|
| Fixe | Une seule valeur, jamais dans la grille de recherche |
| Libre discret | Liste explicite de valeurs |
| Libre par intervalle | min, max, pas (ou nombre de valeurs), echelle lineaire/log |
| Libre echantillonne | Methode/distribution d'echantillonnage declaree |
| Derive | Formule/reference vers le(s) parametre(s) source, jamais saisi directement |
| Conditionnel | Regle explicite dependant d'un autre parametre — **jamais un repli silencieux** (corrige le comportement actuel de `requires`) |
| Verrouille apres validation | Editable avant scellement, immuable des que le Research Package est valide (G0) |

Ce n'est pas seulement un habillage du Builder (Ecran F) — c'est une
extension du contrat de strategie lui-meme (`StructuralAxis`/
`StrategyFamilySpec`, ou un nouveau `ParameterSpec`), au meme titre que la
bibliotheque d'indicateurs (section 2.1). Voir D15.

---

## 3. Catalogue des visualisations

Chaque ligne est reliee a un artefact ou module reel du moteur — pas une
invention. Quand la donnee necessaire n'est pas encore persistee, c'est
signale explicitement (ne jamais fabriquer une preuve pour l'affichage).

| Famille | Contenu | Source dans le moteur | Statut de la donnee |
|---|---|---|---|
| Vue d'ensemble | Statut package, feu tricolore par gate (G0-G14), indicateurs cles (candidates testees, complexite retenue, p-value corrigee, cout total) | `reports/gates.json`, `reports/economic.json` | Deja persiste |
| Selection de complexite | Complexite testee vs score de validation, configuration retenue mise en evidence, calibree sur Train (jamais sur Test) | `procedures/complexity_selection.py`, `candidate_matrix.json` | A verifier si le detail par complexite est persiste au-dela du resultat final retenu |
| Diagnostics statistiques | Distribution bootstrap/nulle WRC, position de la statistique observee, p-value brute et corrigee (WRC/SPA/Romano-Wolf/MCPM), IC OOS (`estimate`, `lower_95_one_sided`, `ci_90_descriptive`, rendements annualises, `power`, `statistical_gate`), seuils et decision | `procedures/wrc.py`, `procedures/oos_confidence_interval.py` (les deux calculent une distribution bootstrap complete) | Champs resumes deja persistes et affichables (Lot 2) ; **les deux distributions brutes (WRC et OOS) sont jetees avant persistance, seul un hash de la distribution OOS est garde** — a trancher (D2, section 4) ; aucun histogramme fabrique a partir d'un hash |
| Structure temporelle | Frise Train / Test / Validation / OOS par fold, zones de purge/embargo, alignement multi-actifs, statut verrouille/ouvert de l'OOS | `data/walk_forward.py`, `fold_schedule` | Le calendrier (structure) existe et peut etre affiche ; **aucune equity curve/serie de rendements distincte par phase par fold n'est persistee** (seule une serie OOS globale plate existe) — a trancher (D14, section 4) |
| Metriques secondaires de performance | Sharpe, Sortino, Calmar, Profit Factor, max drawdown, duree de drawdown, Ulcer Index | Aucune procedure ne les calcule aujourd'hui | **N'existe pas** malgre l'obligation normative `SOP 08 §17` ("diagnostiques obligatoires sauf gate preenregistre") — ecart Protocole/Implementation, a trancher (D13, section 4) ; ne jamais afficher un chiffre invente |
| Execution et couts | Ordres, fills, NAV, couts, exposition | `reports/execution.json` | Deja persiste |
| Serie OHLC et overlays | Chandeliers du segment affiche, positions (entree/sortie, duree de detention), indicateur(s) utilises par le `entry_criterion`/`exit_criterion` de la strategie, bandes de features (session, filtre de biais, signal detecte) alignees sur le meme axe temporel | `data/local_ohlcv.py` (barres), `strategies/payloads.py` (criteres), `reports/execution.json` (ordres/fills pour placer les marqueurs) | Barres et ordres deja persistes ; l'indicateur affiche doit etre recalcule cote interface a partir du critere declare (lecture, jamais un nouveau calcul de verdict) ou expose par la strategie si deja trace pendant le run — a trancher (D7, section 4) |
| Suivi live d'une execution | Etapes du protocole (preparation, generation, backtests, bootstrap, multiple testing, stabilite pre-OOS, acces OOS, rapport final), pourcentage, duree, couleur selon statut (vert/orange/rouge/gris/bleu), detail au clic | — | N'existe pas encore : necessite d'observer un run **en cours**, pas seulement lire un package termine (D3, section 4) |
| Builder de parametres | Formulaire expose depuis `StructuralAxis` / `StrategyFamilySpec` avec les 7 statuts de la section 2.5 (Fixe/Libre discret/Libre par intervalle/Libre echantillonne/Derive/Conditionnel/Verrouille apres validation) ; blocage de validation si un parametre libre n'a pas de domaine defini | `strategies/payload_factory.py` (valeurs discretes + produit cartesien seulement, deja code) | Contrat partiel existant ; les 7 statuts et la regle de blocage restent a construire (D15) |
| Presentation des inputs (config.json) | Vue lecture seule de la « carte d'identite » d'un package : univers/donnees, segmentation walk-forward, modele de couts, scenarios de robustesse, famille de strategies, attestations humaines pre-OOS (absentes ou fournies), champs generes automatiquement — chaque champ etiquete modifiable / encadre (SOP proprietaire) / verrouille / auto-genere | `config.json` (deja le format preenregistre normatif) | Deja persiste comme artefact ; jamais rendu lisible par un humain autrement qu'en ouvrant le JSON brut |
| Cycle de vie / ouverture-fermeture | Scellement G0/G7, autorisation d'acces OOS G8, approbation d'incubation G11, approbation de deploiement G13, archivage G14 (`final_verdict`, `withdrawal_reason`, `retention_expires_at`) | `constants.py::PACKAGE_STAGES`, `schemas/lifecycle_archive.schema.json`, `schemas/oos_access_event.schema.json` | G0/G7/G8 codes et verifiables ; G11/G13/G14 normatifs, pas encore verifies mecaniquement (D12) |
| Autorisations humaines | Les 3 familles de la section 2.4 : preuves pre-OOS, reviewer G-BIAS (incidents/derogations), approbations de gate | `governance/human_evidence.py`, `governance/bias_gate.py`, `governance/incident_logger.py` | Familles 1 et 2 codees ; famille 3 non codee (D12) |

### 3.1 A quoi ca pourrait ressembler — maquettes d'ecran

Maquettes illustratives (donnees fictives), pour discussion de disposition
uniquement — pas une specification pixel-perfect. Une premiere version
interactive de cet aspect a ete montree en conversation le 2026-07-21
(tableau de bord Plotly/HTML) ; les blocs ci-dessous en sont la version
texte, portable dans ce document.

#### Ecran A — Vue d'ensemble (Lot 1)

```
+--------------------------------------------------------------------+
| nautilus_mvp  ·  famille E-I  ·  NASDAQ, XAUUSD  ·  K=2 folds       |
|                                          [ FAIL · refus gouverne ]  |
+--------------------------------------------------------------------+
| Gates  (G0)(G1)(G2)(G3)(G4)(G5)(G6)(G7)(G8)(G9)(G10)(G11)(G12)(G13)(G14) |
|         o   o   .   .   x   o   .   .   .   .   .    .    .    .    .   |
|         o=PASS   .=INCONCLUSIVE   x=FAIL                            |
+--------------------------------------------------------------------+
| Candidates testees | Complexite retenue | WRC p corrigee | Cout    |
|        45           |        3 / 7        |      0.39      | $11.56 |
+--------------------------------------------------------------------+
```

#### Ecran B — Selection de complexite (Lot 1)

```
 score
  0.6 |                    *4        *5
  0.5 |            [3]------------------  <- retenue (Train-only)
  0.4 |        *2                *6
  0.3 |    *1                         *7
       ----------------------------------> complexite
        1    2    3    4    5    6    7

  [3] = configuration retenue, encadree, avec justification au clic
  * = candidates testees, cliquables pour voir leur detail
```

#### Ecran C — Diagnostics statistiques (Lot 2, apres D2)

```
+--------------------------------------------------------------------+
| Distribution bootstrap (WRC) — statistique observee vs H0           |
|        (histogramme -> disponible seulement si D2 tranche en (a))  |
|              ▂▄▆█████▇▅▃▁      <- statistique observee ici (▮)      |
| p brute: 0.31    p corrigee (WRC): 0.39                              |
| Decision: PAS de rejet de H0 — aucune preuve d'edge sur ce segment  |
+----------------------------------------------------------------------+
| Intervalle de confiance OOS (SOP 01) — champs reels, deja persistes   |
| estimate: 0.0021   IC 90 descriptif: [-0.3%, 1.0%]   lower_95: -0.4% |
| rendement annualise (log/simple)   power: 0.61   statut: INCONCLUSIVE|
+----------------------------------------------------------------------+
| Metriques secondaires (Sharpe, Sortino, max DD, duree DD)             |
|                                    [ NON DISPONIBLE — ecart SOP 08 §17 |
|                                      voir D13, pas encore calcule ]   |
+----------------------------------------------------------------------+
```

#### Ecran D — Structure temporelle (Lot 1 pour le calendrier ; D14 pour l'equity par phase)

```
Fold 1  [=== Train ===][P][== Test ==][E][///// OOS non ouvert /////]
Fold 2  [===== Train =====][P][== Test ==][E][/// OOS non ouvert ///]

        Train = calibration   Test = selection/verdict pre-OOS
        P = purge   E = embargo   /// = verrouille tant que G0-G14
        et les preuves humaines requises ne sont pas reunies

  Equity par phase (Train/Test/OOS), fold par fold :
  [ ASPIRATIONNEL — necessite D14, aucune serie par phase persistee    ]
  [ aujourd'hui. Illustre la disposition envisagee, pas une donnee reelle ]
```

#### Ecran E — Suivi live d'une execution (Lot 2)

```
Preparation des donnees     [############################] 100%  (vert)
Generation des candidates   [############################] 100%  (vert)
Execution des backtests     [############################] 100%  (vert)
Bootstrap + WRC             [############################] 100%  (rouge — FAIL scientifique)
Stabilite pre-OOS           [######......................]  40%  (violet — ERREUR TECHNIQUE)
Acces OOS                   [                            ]   0%  (gris — verrouille)
Rapport final                [                            ]   0%  (gris — bloque par l'erreur ci-dessus)

Legende : vert=valide  orange=fragile/proche du seuil
          rouge=echec scientifique (verdict de gate, legitime, jamais un bug)
          violet=erreur technique (crash/exception, PAS un verdict — voir D10)
          gris=pas encore execute  bleu=en cours
Clic sur une ligne -> detail ; pour une erreur technique : trace/exception,
jamais confondue avec la raison d'un FAIL scientifique
```

Distinction volontaire : la ligne "Bootstrap + WRC" rouge est un refus
**gouverne** (un WRC qui ne rejette pas H0, deja rencontre sur le package
`nautilus_mvp` reel — rien a corriger). La ligne "Stabilite pre-OOS"
violette illustre un **crash** (ex. exception non geree dans le runner
subprocess) — aujourd'hui le code ne produit aucun statut structure pour
ce cas (voir D10), donc cette couleur violette n'a rien a lire pour
l'instant : c'est un etat que l'interface ne peut pas encore afficher
honnetement tant que D10 n'est pas traite.

#### Ecran F — Builder de parametres (Lot 3, statuts D15)

```
Strategie : Famille E — Liquidity Sweep MTF

  Timeframe        [ M15 ]                                    [ Fixe ]
  Direction        (x) Both                                   [ Fixe ]
  Session          [ NY overlap v ]                            [ Libre discret ]
                   domaine : { NY overlap, London, Asia }       -> requis, rempli
  Stop loss ATR    [ 1.0 ---o------ 3.0 ]  pas 0.1              [ Libre par intervalle ]
                   domaine : min 1.0, max 3.0, pas 0.1          -> requis, rempli
  Taille position  ( ratio du stop x facteur de risque )        [ Derive ]
                   formule : risk_fraction / (stop_atr * atr)   -> non saisi directement
  Session filter   ( actif seulement si Session = "NY overlap" )[ Conditionnel ]
                   regle : session == "NY overlap" -> actif      -> jamais un repli silencieux
  Bias filter      [ ??? ]                                      [ Libre discret ]
                   domaine : NON DEFINI                     ⚠ BLOQUE LA VALIDATION
  ----------------------------------------------------------------
  research_family_id   AUTO-GENERE : RF-2026-07-21-E-014     [ Verrouille apres validation ]
  config hash           (calcule au scellement)               [ Verrouille apres validation ]
  ----------------------------------------------------------------
  [ Valider la configuration ]  <- desactive : "Bias filter" est
                                    libre sans domaine defini (D15)
  [ Construire le research_package ]  <- desactive tant que non valide
```

#### Ecran G — Serie OHLC, positions, indicateur, features (Lot 1)

```
  prix
       |            __                    indicateur = moyenne mobile
       |         __/  \__      /\__       (ou tout autre critere declare
       |     ▟▙_/       \_▟▙__/    \▟▙    par entry_criterion/exit_criterion)
       |   ▟▙          ▟▙    ▙▟        ▙▟
       |  ▟▙  [######### position ##########]
       |            ^entree              ^sortie
        ------------------------------------------------> temps (bar)
  Session NY        [############################        ]
  Sweep detecte      [.....X...........X..................]
  Bias filter actif  [    ###########################      ]

  ▟▙ = bougie haussiere/baissiere   [####] = position ouverte (translucide)
  ^ = marqueur d'entree/sortie      lignes du bas = features alignees sur le meme axe
```

#### Ecran H — Presentation des inputs du research package (Lot 1, lecture seule)

```
+----------------------------------------------------------------------+
| Univers et donnees          [modifiable]  NASDAQ, XAUUSD, 2023-2025,  |
|                                            M15                        |
+----------------------------------------------------------------------+
| Segmentation walk-forward   [encadre · SOP 04]  K=2, purge/embargo    |
|                                            non nuls obligatoires      |
+----------------------------------------------------------------------+
| Modele de couts/execution   [encadre · SOP 09B]  fees/slippage/       |
|                                            latence, calibration 1.0.0 |
+----------------------------------------------------------------------+
| Robustesse pre-OOS          [encadre · SOP 05]  CENTRAL/PLAUSIBLE_    |
|                                            BASE/EXTREME, seuil=0.0    |
+----------------------------------------------------------------------+
| Famille de strategies       [modifiable -> Ecran F]  Famille E, 7     |
|                                            niveaux de complexite      |
+----------------------------------------------------------------------+
| Attestations humaines       [non fourni]  registry_review,            |
| pre-OOS                                   pre_oos_approval absents    |
+----------------------------------------------------------------------+
| Champs generes auto.        [verrouille]  research_family_id,         |
|                                            document_hash, seed        |
+----------------------------------------------------------------------+
|                          [ Construire le research_package (apercu) ] |
+----------------------------------------------------------------------+
```

#### Ecran I — Autorisations humaines (Lot 6, perimetre D12)

```
+----------------------------------------------------------------------+
| 1. Preuves pre-OOS              [ NON FOURNI -> INCONCLUSIVE/DENIED ] |
|    registry_review, pre_oos_approval          (code existant, D5)    |
+----------------------------------------------------------------------+
| 2. Reviewer G-BIAS transversal  [ AUCUN INCIDENT OUVERT ]             |
|    incidents (LEVEL_0-5), derogations          (code existant)       |
|    [ Declarer un incident ]  [ Demander une derogation ]             |
+----------------------------------------------------------------------+
| 3. Approbations de gate (G11/G13/G14)     [ NON DISPONIBLE ]          |
|    incubation, deploiement, retrait/archive    (D12 - pas encore     |
|    verifie mecaniquement par le moteur, ecran non construit tant     |
|    que le code de verification n'existe pas)                         |
+----------------------------------------------------------------------+
```

Cycle d'ouverture/fermeture correspondant (section 2.3) :

```
[ Construire config.json ]  ->  [ Sceller (G0/G7) ]  ->  [ Autoriser acces OOS (G8) ]
                                                                    |
        [ Archiver / fermer (G14) ]  <-  [ Approuver deploiement (G13) ]  <-  [ Approuver incubation (G11) ]
```

---

## 4. Conflits de gouvernance a trancher explicitement (avant tout code)

| # | Conflit | Ce qui doit etre decide |
|---|---|---|
| D1 | Dependance technique externe (framework web + librairie de graphiques) dans un moteur `stdlib-only by design`. | Discute et acte en conversation le 2026-07-21 : dependance autorisee, confinee a une nouvelle frontiere (`Implementation/interface/`), jamais importee par `procedures/`, `validators/`, `governance/`, `manifests/`, `adapters/nautilus_*`. **A tracer formellement au `/start`**, au meme format que D1-D6 du pivot Nautilus, avec le choix precis de bibliotheques et leurs versions. |
| D2 | Verifie dans le code reel : deux distributions bootstrap completes sont calculees puis jetees avant persistance, jamais gardees en clair. (a) `procedures/wrc.py::wrc_test()` calcule `bootstrap_distribution`, absent de `reports/wrc.json`. (b) `procedures/oos_confidence_interval.py::oos_confidence_interval()` calcule `bootstrap_means` (methode bloc stationnaire), remplace dans `reports/oos.json` par `bootstrap_mean_count` + `bootstrap_means_hash` (empreinte seulement). Les champs resumes (`estimate`, `lower_95_one_sided`, `ci_90_descriptive`, rendements annualises, `power`, `statistical_gate`) sont eux bien persistes et affichables des le Lot 2. | Decision humaine : accepter l'ajout des deux distributions brutes en clair dans `reports/wrc.json` et `reports/oos.json` (ou artefacts dedies), impact sur la taille des packages — additif, pas un changement de methodologie. Tant que non tranche, l'Ecran C n'affiche que les intervalles/estimateurs resumes, jamais un histogramme fabrique a partir d'un hash. |
| D3 | Le suivi live (Ecran E) exige d'observer un run **en cours**, pas seulement un package termine. Deux mecanismes possibles : (a) un fichier d'etat local mis a jour en direct par le runner, relu par polling cote interface ; (b) un flux d'evenements (ex. Server-Sent Events) emis par le runner. | Decision humaine sur le mecanisme — impacte le perimetre du Lot 2. Recommandation par defaut : (a), plus simple, coherent avec l'absence de base de donnees et le style stdlib du runtime cote calcul. |
| D4 | Comment l'interface materialise l'invariant G0 (aucune modification apres scellement) — verrouillage visuel seul (facile a contourner par un appel direct) vs. verrouillage impose cote serveur (le serveur refuse toute ecriture sur un champ scelle, quelle que soit la requete). | Decision humaine : le verrouillage cote serveur doit etre la regle par defaut — le visuel seul ne suffit jamais comme garde-fou reel. A confirmer explicitement au `/start` du Lot 3/4. |
| D5 | Relation avec le sas humain pre-OOS deja identifie comme manquant (`registry_review`, `pre_oos_approval` — contrat technique existant dans `governance/human_evidence.py`, aucune interface). | **Explicitement differe.** Ce document ne propose pas de le construire maintenant. Question ouverte a trancher plus tard, sans engagement ici : cette interface devient-elle le futur lieu naturel de saisie de ces preuves (Lot au-dela de ceux decrits ici), ou reste-t-il un sujet separe ? |
| D6 | Perimetre de donnees affichables : l'interface doit-elle pouvoir lire des packages `DENIED`/`FAIL` (cas normal et frequent dans ce projet) aussi bien que `PASS`, sans jamais laisser croire qu'un refus gouverne est une erreur a corriger dans l'UI ? | Position par defaut proposee : oui, afficher les refus normalement, avec le meme habillage que documente dans l'audit de maturite (« refus gouverne, pas un bug ») — a confirmer, pas a inventer silencieusement. |
| D7 | Revise a la lumiere de la bibliotheque (section 2.1) : l'indicateur trace sur l'Ecran G doit-il etre (a) recalcule cote interface a partir de la reference et des parametres declares (`computation` de la bibliotheque, formule versionnee et connue), ou (b) explicitement trace et persiste pendant le run lui-meme pour eviter toute divergence entre ce qui a ete execute et ce qui est affiche ? | Decision humaine sur le mecanisme. La bibliotheque rend l'option (a) plus sure qu'avant (formule versionnee, pas devinee) SI et seulement si le `computation` de la bibliotheque est garanti identique a ce que `GenericPayloadStrategy`/Nautilus execute reellement au runtime — sinon (b) reste necessaire pour eviter toute divergence silencieuse. Recommandation par defaut inchangee : (b), le temps que cette garantie d'identite soit demontree. |
| D8 | Une fois qu'un `config.json` scelle reference une entree de la bibliotheque (ex. `rsi` version `1.0.0`), modifier plus tard cette entree changerait silencieusement le sens d'une preuve deja scellee — meme risque que modifier une SOP sans nouvelle version documentaire (`Protocole/0-README`, regles de maintenance). | Decision humaine : chaque entree de bibliotheque doit etre versionnee et immuable des qu'elle est referencee par un `config.json` scelle ; toute correction de formule cree une nouvelle version, jamais une modification en place. A tracer comme regle de gouvernance de la bibliotheque avant le premier `/start` qui la construit. |
| D9 | Qui peut ajouter une nouvelle entree a la bibliotheque, et avec quelle revue — un nouvel indicateur reste du code (quelqu'un doit implementer son calcul), la bibliotheque ne supprime pas ce besoin, elle evite seulement de le repeter a chaque strategie/run. | Decision humaine sur le processus d'ajout (probablement le cycle standard `/start`→`/evaluate`→`/continue` du repo, comme pour tout ajout a `strategies/`) — a documenter pour eviter l'illusion que la bibliotheque rend tout indicateur disponible sans aucune intervention de code. |
| D10 | Verifie dans le code reel (pas suppose) : aucun echec **technique** (crash, exception, extraction Nautilus ratee) n'est aujourd'hui structure. `NautilusExtractionError` (prevue dans le pivot Nautilus) n'existe pas ; `nautilus_strategy_bridge.py` avale silencieusement des erreurs d'extraction (`except Exception: return 0.0`, lignes 167 et 173, sans log) ; le point d'entree subprocess (`nautilus_segment_cli.py`) n'a aucun `try/except` ; la boucle multi-fold n'a ni retry ni checkpoint (un crash au segment N arrete tout, folds N+1..K jamais executes) ; `constants.py::TECHNICAL_STATUSES = {"INVALID_TECHNICAL"}` existe mais n'est reference nulle part (schemas, validators, gates) — statut mort. Consequence directe sur ce document : l'Ecran E (suivi live) ne peut pas honnetement distinguer un `FAIL` scientifique gouverne d'un crash technique tant que ce statut n'est pas cable ; et le mecanisme de polling de D3 ne peut pas detecter un run crashe (fichier d'etat qui ne bouge plus) sans un heartbeat/timeout, qui n'existe pas non plus. | Decision humaine : ce gap technique doit-il etre traite (a) comme prealable au Lot 2 (cabler `INVALID_TECHNICAL`, ajouter un heartbeat/timeout, avant de construire le suivi live), ou (b) comme un chantier separe, independant de l'interface, a router de son cote ? Ne pas construire l'Ecran E en pretendant afficher un etat que le runtime ne produit pas reellement. |
| D11 | L'Ecran A (feu tricolore, section 3.1) aplatit la taxonomie reelle des verdicts (section 2.2, 6 statuts paquet + 2 statuts fold + `BURNED`) en 3 etats. La regle normative SOP 10 §15 (`REJECTED_ECONOMIC` ne doit jamais etre presente comme un echec statistique) est une exigence explicite, pas un detail cosmetique. | Decision humaine : valider le jeu de couleurs/etiquettes complet propose en section 2.2 avant `/start` du Lot 1 — ne pas laisser l'implementation choisir un mapping simplifie par defaut. |
| D12 | Sur les 3 familles d'autorisation humaine (section 2.4), seules (1) preuves pre-OOS et (2) reviewer G-BIAS ont un code de verification reel. La famille (3) — approbations de gate G11/G13/G14 — est normative dans le Protocole mais n'a aucun module Python dedie aujourd'hui. Construire un ecran d'autorisation pour G11/G13/G14 reviendrait a fabriquer un formulaire pour une verification qui n'existe pas encore. | Decision humaine : (a) construire d'abord le code de verification manquant pour G11/G13/G14 (hors perimetre de ce document, touche `governance/`), puis l'ecran ; ou (b) limiter l'Ecran I (section 3.1) aux deux familles deja codees (pre-OOS, G-BIAS) pour une premiere version, en marquant G11/G13/G14 comme non disponible ; ou (c) differer entierement, comme D5. Recommandation par defaut : (b), coherent avec la regle "ne jamais afficher un etat que le moteur ne produit pas reellement" (meme principe que D10). |
| D13 | Verifie dans le code et le Protocole : `Protocole/SOP 08 - Mesures de performance et serie de rendement de reference.md` §17 rend Sharpe, Sortino, Calmar, Profit Factor, max drawdown, duree de drawdown, Ulcer Index **obligatoires comme diagnostics secondaires** ("diagnostiques sauf gate explicitement preenregistre"). Aucune procedure du moteur ne les calcule (`procedures/economic_gate.py` suppose un `drawdown_pass` deja fourni, ne le calcule jamais ; `returns.py` ne produit que des rendements quotidiens bruts, aucun ratio). C'est un ecart Protocole/Implementation, decouvert en concevant l'interface, pas une question d'affichage. | Decision humaine : ce gap est plus large que ce document (touche `procedures/`, potentiellement un nouveau module) — a router comme chantier separe si priorise. En attendant, l'interface affiche ces metriques comme "non disponible" a cote des metriques reelles (jamais un chiffre invente), et ne bloque pas le reste de l'interface sur ce manque. |
| D14 | Verifie dans le code : seule une serie de rendements OOS globale et plate est persistee (`series/oos_primary_returns.json`) ; il n'existe aucune equity curve ou serie de rendements distincte par phase (Train/Test/OOS) et par fold. `procedures/walk_forward.py` valide uniquement la structure du calendrier (ordre chronologique, purge/embargo/warmup), il ne persiste aucune serie. L'Ecran D (structure temporelle) peut donc afficher honnetement le calendrier des folds, mais pas une equity curve par phase par fold tant que cette persistance n'existe pas. | Decision humaine : construire cette persistance (touche `package_builder`/procedures, hors perimetre de ce document) est un prealable a toute equity curve par phase par fold reelle. En attendant, l'Ecran D peut inclure un rendu illustratif explicitement etiquete "aspirationnel, necessite D14" pour discuter de la disposition — jamais presente comme une donnee reelle. |
| D15 | Verifie dans le code (section 2.5) : `StructuralAxis` ne supporte que des valeurs discretes explicites, combinees par produit cartesien pur — aucun intervalle+pas, aucune echelle lineaire/log, aucune distribution d'echantillonnage, aucun statut "derive" ou "verrouille apres validation" type par champ. `requires` (dependance conditionnelle) se replie silencieusement sur le defaut plutot que de lever une erreur explicite. Le modele a 7 statuts (Fixe/Libre discret/Libre par intervalle/Libre echantillonne/Derive/Conditionnel/Verrouille apres validation) demande par l'utilisateur n'est donc pas un habillage d'ecran — c'est une extension du contrat de strategie lui-meme. | Decision humaine : etendre `StructuralAxis`/`StrategyFamilySpec` (ou creer un nouveau `ParameterSpec`) pour porter ces 7 statuts et leurs regles de generation, plus une regle de validation qui bloque la construction du research_package si un parametre "libre" n'a pas de domaine defini. Meme perimetre que Lot 1a (touche `strategies/`) — a fusionner ou sequencer avec la bibliotheque d'indicateurs, pas a construire cote interface seule. |

**Aucun lot au-dela du Lot 0 ne doit demarrer avant que D1 a D15 soient
explicitement tranches**, au meme format que les decisions D1-D6/1B/2A/3A
deja tracees dans les chantiers precedents.

---

## 5. Decoupage en lots propose

| Lot | Objectif | Depend de |
|---|---|---|
| Lot 0 — Gouvernance | Trancher D1-D15, triage `/start` (`Track`/`Lifecycle`/`Scope`/`Non-goals`/`Source`/`Exit criteria`) | — |
| Lot 1a — Bibliotheque d'indicateurs/filtres + statuts de parametres | Construire `strategies/indicator_library.py` (indicateurs/filtres, D7-D9) ET etendre `StructuralAxis`/`StrategyFamilySpec` (ou nouveau `ParameterSpec`) pour les 7 statuts de parametres et la regle de validation associee (D15, section 2.5). Meme perimetre `strategies/`, sequences ou fusionnes selon decision humaine. | Lot 0, D7, D8, D9, D15 |
| Lot 1 — Visualiseur statique | Lire un `research_package` termine et afficher Ecrans A (avec la taxonomie complete D11), B, D, H (vue d'ensemble, complexite, structure temporelle, presentation des inputs) ; Ecran G (serie OHLC + positions + features), rendu exclusivement a partir des references de la bibliotheque (Lot 1a) | Lot 0, Lot 1a, D11 |
| Lot 2 — Diagnostics et suivi live | Prealable (D10) : cabler `INVALID_TECHNICAL` et un heartbeat/timeout pour distinguer un crash technique d'un run lent, si D10 = option (a). Puis : persister les distributions brutes (D2), Ecran C ; mecanisme d'observation d'un run en cours (D3), Ecran E ; si D7 = option (b), tracage et persistance de l'indicateur pendant le run | Lot 1, D2, D3, D7, D10 |
| Lot 3 — Builder de parametres | Exposer `StructuralAxis` / `StrategyFamilySpec` sous forme de formulaire (Ecran F), avec les 7 statuts de la section 2.5 (Fixe/Libre discret/Libre par intervalle/Libre echantillonne/Derive/Conditionnel/Verrouille apres validation) et blocage de validation si un parametre libre n'a pas de domaine ; selection d'indicateurs/filtres depuis la bibliotheque (Lot 1a) plutot qu'un champ texte libre | Lot 1, Lot 1a |
| Lot 4 — Ouverture d'une recherche | Construire le package candidat depuis l'interface, valider sa conformite au schema, sceller (G0/G7 — "ouverture" au sens normatif, section 2.3) | Lot 3, D4 |
| Lot 5 — Lancement encadre | Declencher une execution pre-OOS depuis l'interface, avec verrouillage serveur apres scellement (D4) | Lot 2, Lot 4 |
| Lot 6 — Autorisations et fermeture | Ecran I : familles 1 et 2 d'autorisation humaine (pre-OOS, G-BIAS) ; fermeture G14 (`lifecycle_archive`). Famille 3 (G11/G13) hors perimetre tant que D12 n'est pas tranche. | Lot 5, D12 |

**Ordre de construction (lots) vs ordre de navigation (interface)** : l'ordre
des lots ci-dessus reflete des dependances techniques reelles (le Builder,
Lot 3, depend de la bibliotheque d'indicateurs, Lot 1a) — ce n'est pas
forcement l'ordre dans lequel un humain doit rencontrer les ecrans une
fois l'interface construite. Retour utilisateur du 2026-07-21 : le
Builder et la presentation des Inputs (construire/definir une recherche)
doivent apparaitre pres de la Vue d'ensemble dans la navigation, avant les
ecrans de resultats (diagnostics, prix, suivi live) — la construction
precede logiquement l'observation. Ordre de navigation propose :
Vue d'ensemble -> Builder -> Inputs -> Structure temporelle -> Diagnostics
statistiques -> Prix et indicateurs -> Suivi live -> Cycle de vie et
autorisations. A confirmer au `/start` du Lot 1 (premiere maquette
navigable reelle).

Chaque lot suit le cycle habituel du repo : brouillon dans
`0 - HUMAN START HERE/`, `/start`, boucle `/evaluate` (minimum 2 passes),
baseline committee, `/continue`, tests, bug-hunter, conformance,
`/close`.

---

## 6. Non-objectifs (rappel)

- Ne jamais faire de l'interface une source de verite concurrente de
  `config.json`, `registry.jsonl` ou des rapports de `procedures/`.
- Ne jamais permettre un raccourci d'ouverture OOS depuis l'interface.
- Ne jamais recalculer un verdict statistique ou economique cote interface
  — elle affiche, elle ne calcule jamais un gate.
- Ne pas construire le sas humain pre-OOS dans ce chantier (D5, differe) —
  une des trois familles d'autorisation de la section 2.4, pas la seule.
- Ne pas construire d'ecran d'autorisation pour une famille non encore
  verifiee mecaniquement par le moteur (D12 — G11/G13/G14).
- Ne pas modifier `Protocole/`, `procedures/`, `validators/`,
  `governance/`, `manifests/`.
- Ne jamais laisser l'interface afficher un indicateur ou un filtre absent
  de la bibliotheque (section 2.1) et de la reference declaree par la
  strategie.
- Ne jamais presenter `REJECTED_ECONOMIC` comme un echec statistique, ni
  aplatir la taxonomie de verdicts de la section 2.2 (D11).
- Ne jamais permettre a un parametre "libre" d'entrer dans la grille de
  recherche sans domaine defini (D15) ; ne jamais laisser un statut
  "Conditionnel" se replier silencieusement sur un defaut sans le dire.

---

## 7. Prochaine etape

Ce document reste `INTAKE`. La suite naturelle, si retenu : triage humain
(`Track`, `Lifecycle`, `Scope`, `Non-goals`, `Source`, `Exit criteria`),
tracage formel des decisions D1-D15, puis `/start` sur le Lot 0, suivi du
Lot 1a (bibliotheque d'indicateurs/filtres + statuts de parametres) avant
tout ecran qui en depend.

Voir aussi la section 8 ci-dessous (audit complementaire du 2026-07-21) —
a integrer dans le triage avant `/start`, pas a traiter separement.

---

## 8. Audit complementaire (consultant produit, 2026-07-21) — a trancher, pas encore arbitre

Cette section consigne les questions et critiques issues d'une relecture
independante du present document et du code reel, en vue d'une reprise
ulterieure. Rien ci-dessous n'a ete tranche par l'humain — ce sont des
points a arbitrer au meme titre que D1-D15, pas des decisions actees.

### 8.1 Questions structurantes complementaires (Q1-Q10)

| # | Question | Compris / constat | Recommandation par defaut |
|---|---|---|---|
| Q1 | Portee utilisateur : mono-utilisateur ou multi-role des le MVP ? | Aucun mecanisme d'authentification/role code ; seuls des champs `reviewer_id`/`approved_by` existent dans les schemas. | MVP mono-utilisateur, sans couche d'authentification ; la tracabilite (qui/quand) suffit, le controle d'acces peut attendre. |
| Q2 | Sequencement : livrer l'Ecran G (serie OHLC) avec le reste du Lot 1, ou le decoupler ? | Le Lot 1 actuel bloque A/B/D/H derriere Lot 1a (bibliotheque d'indicateurs) alors que seul G en a besoin. | Decoupler : livrer A/B/D/H des que Lot 0 est tranche, sans attendre la bibliotheque d'indicateurs. |
| Q3 (= D1) | Flask + Plotly, choix definitif ? | Deja discute et acte en conversation le 2026-07-21 selon ce document. | Conserver ce choix, le tracer formellement au `/start` du Lot 0 plutot que de rouvrir le debat technique — voir toutefois 8.2 qui nuance le perimetre exact ou ce choix s'applique. |
| Q4 (= D2) | Persister les distributions bootstrap brutes (WRC + OOS) en clair ? | Aujourd'hui jetees apres calcul, seul un hash de la distribution OOS est garde. | Oui, additif et sans risque methodologique ; a faire tot (Lot 2) apres mesure de l'impact sur la taille des packages. |
| Q5 (= D10) | Cabler `INVALID_TECHNICAL` avant ou apres le suivi live (Ecran E) ? | `TECHNICAL_STATUSES` existe dans `constants.py` mais n'est reference nulle part ailleurs. | Avant — un Ecran E qui ne distingue pas un crash d'un refus gouverne est trompeur par construction. |
| Q6 (= D13) | Qui traite l'ecart Sharpe/Sortino/Calmar/Ulcer manquant malgre SOP 08 §17 ? | Ce n'est pas un manque d'affichage : aucune procedure ne les calcule. | Chantier separe, priorise independamment de l'interface ; afficher "non disponible" en attendant, jamais un chiffre invente. |
| Q7 (= D15) | Etendre `StructuralAxis` a 7 statuts avant de construire le Builder (Ecran F) ? | Le modele actuel ne supporte que des valeurs discretes explicites. | Oui — construire le Builder sur le modele actuel produirait un faux confort ("libre" sans domaine defini). |
| Q8 | Controle concret anti-"relance jusqu'a p-value favorable" ? | Non traite explicitement dans ce document, seulement cite comme risque generique. | Un compteur immuable de tentatives par `research_family_id`, visible sur l'Ecran A, jamais remis a zero — a trancher avant le Lot 4. |
| Q9 (= D5) | Le sas humain pre-OOS reste-t-il hors perimetre de cette interface ? | Ce document le differe explicitement sans engagement. | Confirmer le report — le construire maintenant anticiperait un besoin non encore priorise. |
| Q10 | Ce chantier devient-il le prochain workstream mainline, orchestre via `epic-orchestrator` ? | `checkpoint.json::active_workstream_id` est `null` ; le depot est au repos depuis la cloture de `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`. | Oui — moment propre pour ouvrir ce chantier ; `epic-orchestrator` vu le multi-lot deja identifie (section 5). |

### 8.2 Critique d'architecture : memes ecrans, decoupage different

Question posee en conversation : *"si tu devais recommencer sur une page
blanche, adopterais-tu la meme UX, la meme experience de recherche ?"*
Reponse resumee — le contenu (catalogue d'ecrans A-I, taxonomie des
verdicts, gates) reste juste ; l'architecture, elle, serait different sur
trois points :

1. **Separer le visualiseur du builder.** Ce document batit une seule
   application Flask pour tout. Or lire un package termine (Ecrans A/B/D/H)
   n'a besoin d'aucun etat ni serveur — c'est un probleme de generation de
   rapport statique (script qui lit `reports/*.json` et sort un HTML/Plotly
   autonome, dans l'esprit stdlib du moteur). Seuls le Builder (verrouillage
   G0 cote serveur) et le suivi live (Lot 2) ont reellement besoin d'un vrai
   backend. Bundler les deux force a assumer tout le risque de dependance
   externe (D1) avant de livrer le moindre ecran.
2. **L'ecran d'accueil ne devrait pas etre l'Ecran A d'un package unique.**
   Aucun ecran "liste/registre de tous les research_package" n'existe dans
   le decoupage actuel, alors qu'en usage reel le premier reflexe est de
   comparer plusieurs packages, pas d'en ouvrir un au hasard.
3. **Par package, un document d'audit scrollable a ancres plutot que des
   onglets d'application.** Colle mieux a la mentalite "preuve a relire" du
   Protocole, et se double gratuitement du rapport exportable demande par
   ailleurs (catalogue "Rapports").

Consequence potentielle sur le decoupage en lots (section 5) si ces points
sont retenus : Lot 1 se scinderait en un generateur de rapport statique
(sans dependance a un serveur, potentiellement livrable avant meme D1) et
un Lot "app interactive" resserre au seul Builder + suivi live. Non tranche
— a rearbitrer avec l'humain avant tout `/start`.

### 8.3 Nuance factuelle sur la section 2.1 (bibliotheque d'indicateurs)

Verifie dans le code : contrairement a la formulation de la section 2.1
("texte libre ou dict non structure"), `entry_criterion`/`exit_criterion`
sont deja des `dict` structures avec un `rule_id` stable (voir
`Implementation/ebta_engine/strategies/payloads.py` et
`Implementation/ebta_engine/strategies/payload_factory.py::liquidity_sweep_family_spec()`,
qui peuple `rule_id: "m1_liquidity_sweep_engulfing_m3_close_confirmation"`).
Le trou reel n'est donc pas l'absence de structure, mais l'absence d'un
catalogue separe qui documente ce que chaque `rule_id` signifie et comment
le tracer (`computation`/`rendering_spec` de D7-D9 restent justes, seule la
severite du constat initial est a revoir legerement a la baisse).
