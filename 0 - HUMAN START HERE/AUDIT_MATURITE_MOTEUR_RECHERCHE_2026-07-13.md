# Audit de maturite — Le moteur EBTA est-il pret pour une vraie campagne de recherche quantitative ?

> Note d'intake, pas un plan. Deposee ici pour triage humain futur, suite a un
> audit technique complet du depot demande le 2026-07-13.
> Etat machine au moment de l'audit : branche `main`, HEAD `184b013`.
> Ce fichier reste `INTAKE`, non executable, tant qu'un humain ne l'a pas
> audite et route vers `.ai/backlog/`.

## Mode de lecture — 2026-07-21

Ce document est separe en deux parties.

- **Partie A — Etat actuel et suites** : ce qu'il faut lire pour savoir ou le
  moteur en est aujourd'hui. La section 0 est la synthese primaire au
  2026-07-21 ; les sections 1 a 4 sont la photo intermediaire du 2026-07-20.
- **Partie B — Historique initial** : diagnostic du 2026-07-13 conserve pour
  comprendre l'origine des corrections, sans le relire comme l'etat courant.

Pour eviter l'ambiguite :

| Marqueur | Sens |
| --- | --- |
| **ACTUEL 2026-07-21** | Etat courant apres la cloture de l'EPIC de maturite et sa preuve globale pre-OOS. |
| **INTERMEDIAIRE 2026-07-20** | Photo de reprise conservee : utile pour comprendre le chemin parcouru, mais depassee par la section 0 si elle diverge. |
| **HISTORIQUE 2026-07-13** | Diagnostic initial conserve pour expliquer pourquoi les plans etaient necessaires ; ne pas le lire comme l'etat courant s'il contredit une mise a jour datee. |
| **RESIDUEL** | Risque encore ouvert, a transformer en plan separe si priorise. |

Lecture rapide : lire la section **0**, en particulier son bloc
**RESIDUEL** si une suite doit etre priorisee. Les sections **1 a 4** et la
partie historique servent de trace. La partie historique commence
apres le separateur **"Partie B — Historique initial"**.

---

# Partie A — Etat actuel et suites

## 0. Etat courant faisant foi — ACTUEL 2026-07-21

### Verdict

L'EPIC `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE` est `DONE` et aucun
workstream n'est actif dans `.ai/checkpoint.json`. Le moteur a demontre sa
**capacite de conduire une campagne de recherche pre-OOS reproductible,
calibree, stressee et auditable**. Ce verdict porte sur la capacite du moteur,
pas sur la validation d'une strategie : le package reel reste honnetement
refuse tant que les preuves humaines pre-OOS independantes ne sont pas
fournies.

La source de suivi executable est l'archive
`.ai/archive/20260721_EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE.md`; le present
fichier reste une note d'intake et de lecture humaine. La cloture est tracee
par le commit `f34cad1`.

### Ce qui est cloture

| Axe | Etat au 2026-07-21 | Preuve utile |
| --- | --- | --- |
| R7 — reproductibilite | **DONE** | Data root explicite et parametrable; hash de configuration SHA-256 reel; environnement Nautilus documente et recreable. |
| R5 — couts, slippage, latence | **DONE** | Calibration `1.0.0` mixte : spreads NASDAQ locaux et proxies conservateurs de plusieurs brokers officiels lorsque la grandeur est comparable; aucune composante inconnue n'est remplacee par zero. |
| R6 — robustesse | **DONE** | Scenarios `CENTRAL`, `PLAUSIBLE_BASE` et `EXTREME` reellement distincts; le rejet economique de `PLAUSIBLE_BASE` prouve que le gate peut echouer. |
| Lot 3 — chronologie et attestations | **DONE** | Chronologie UTC et registre pre-OOS controles; attestations humaines explicites et optionnelles; leur absence donne `INCONCLUSIVE`/`DENIED`; fixtures reservees aux tests. |
| R4-long — volume et scalabilite | **DONE** | Benchmark canonique 1 mois / 3 mois / 1 an `COMPLETED`, avec temps, RSS, ordres et exposition OOS documentes; scope `PRE_OOS_TEST_ONLY`. |
| Preuve globale Phase 5 | **DONE** | Package reel pre-OOS materialise apres refus, validation executee sans erreur de schema ni erreur semantique; conformance parent complete. |

Les validations de cloture sont : suite runtime **208 PASS**, Pyrefly global
**0 erreur**, audit de conformite parent sans critere manquant et validation du
checkpoint contre son schema **PASS**.

### Etat exact du package reel

L'absence de `pre_oos_human_evidence` laisse volontairement le package
`nautilus_mvp` en `DENIED` et `validate_package_dir()` en `FAIL`. Ce n'est pas
un defaut masque : les rapports strictement pre-OOS sont maintenant
materialises et auditables. Le validateur retourne 3 gates `PASS`, 12
`INCONCLUSIVE`, `schema_errors=[]` et `semantic_errors=[]`.

Le package n'ouvre pas l'OOS : il ne contient ni journal d'acces OOS, ni
rapport ou serie OOS, ni rapport economique final, ni manifeste de stade. Les
preuves d'execution et de NAV pre-OOS sont reelles (42 ordres; cout total
11,564) et les stress font apparaitre le rejet attendu de
`PLAUSIBLE_BASE`.

### RESIDUEL — apres cloture de l'EPIC

Ces sujets ne rouvrent pas l'EPIC de maturite. Ils ne deviennent des plans que
si un humain decide de franchir l'etape correspondante :

1. **Ouvrir l'OOS de maniere gouvernee** : fournir les preuves humaines
   independantes pre-OOS requises, puis autoriser une execution OOS selon le
   Protocole. Sans ces elements, `DENIED` reste le resultat correct.
2. **R10 — incubation, live, kill-switch et monitoring** : reste hors du
   perimetre recherche actuel et ne peut etre envisage qu'apres la survie
   d'une strategie a un OOS reellement autorise.

## 1. Etat courant resume — INTERMEDIAIRE 2026-07-20

Cette note reste une **photo d'audit du 2026-07-13**. Depuis cet audit, neuf
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
- `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES` est `DONE` : les sous-chantiers
  Lot C, Lot A2 et Lot B sont clos. Les champs mecaniques G1/G7/G11/G12/G13
  derivent maintenant de statuts de procedures, `G9::power_report` derive
  d'une puissance atteinte calculee sur les rendements pre-OOS, et G6
  (`execution_report`, `cost_model`, `capacity_grid`, `nav_reconciliation`)
  derive des preuves execution/NAV et des rapports reels sur le chemin de
  generation. Le commit de cloture de l'EPIC est `063246b`, apres Lot B
  `6f0b212`.
- `EPIC_ATTESTATIONS_RESIDUELLES_R3` est `DONE` : Lots D/E/F clotures et
  package `nautilus_mvp` regenere. Le scellement produit automatiquement son
  horodatage UTC apres un `PASS`; les fixtures seulement utilisent une horloge
  injectee et etiquetee. `invariant_evidence.json` derive maintenant ses
  preuves de scellement, WRC local par fold, transformations et evenements de
  disponibilite. Le commit de cloture est `0bfd32e`.

La Partie B conserve sa valeur historique : elle explique pourquoi R1/R2/R4, le
defaut WRC masque et le defaut de statut global package etaient necessaires.
Elle ne doit plus etre lue comme l'etat courant exact de ces points. Les risques
restants a transformer en plans separes sont surtout : les attestations
humaines/post-OOS legitimes, l'horodatage automatique des autres jalons de
recherche, qualite des donnees longues, warm-up inter-fold, realisme
couts/slippage/latence, stress de robustesse reel, scalabilite du runner et
edge cases Nautilus.

Limite importante apres les corrections WRC + validators + G5 + EPIC C/A2/B + R3 :
le verdict global de package reflete maintenant les sorties
WRC/economic/incubation en echec, le verdict de robustesse pre-OOS reel atteint
G5, et les champs G1/G6/G7/G9/G11/G12/G13 corriges par l'EPIC ne sont plus des
attestations gratuites dans le chemin de generation. Cela ne transforme pas
encore toutes les attestations humaines/post-OOS du package en preuves
derivees. Les sujets residuels sont des plans separes : deriver ou expliciter
ces attestations legitimes, generaliser l'horodatage automatique aux autres
jalons, puis durcir les scenarios de robustesse eux-memes.

## 2. Audit complet de reprise — INTERMEDIAIRE 2026-07-20

Cet audit de reprise compare l'audit initial du 2026-07-13 a l'etat reel apres
les workstreams clos jusqu'au commit courant `0bfd32e`. Il ne s'appuie pas
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
  `"PASS"` ;
- les corrections C/A2/B ont fortement reduit les faux verts residuels de
  `gates.json` sur G1/G6/G7/G9/G11/G12/G13.

Mais le moteur n'est pas encore pret pour une vraie campagne quantitative
complete. Son niveau actuel est plutot :

```text
Pipeline EBTA/Nautilus coherent, capable de produire un FAIL honnete,
mais pas encore un moteur de campagne robuste, calibre et reproductible.
```

### Etat mecanique du package Nautilus M1 courant

Verification du package persistant `Implementation/research_packages/nautilus_mvp`
au 2026-07-20, **apres regeneration finale de l'EPIC R3** :

> `nautilus_research_package.py::main()` et `validate_package_dir()` ont ete
> executes. Le build se termine correctement mais retourne `FAIL`, ce qui est
> le verdict scientifique attendu : 10 gates `PASS`, 5 `INCONCLUSIVE`, aucun
> chemin/schema/manifest manquant et `INV-003 FAIL` non masque.

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
| `reports/gates.json::power_report` | `PASS` | A2 derive maintenant la puissance atteinte de ses preuves pre-OOS. |
| `reports/execution.json::total_orders` | `28` | Activite non nulle sur l'ensemble du package. |
| `reports/execution.json::oos_total_orders` | `0` | G6 est desormais `INCONCLUSIVE` (`execution_report` et `nav_reconciliation`), jamais un faux `PASS`. |
| `reports/gates.json::oos_access_log` / `opening_authorization` / `single_oos_execution_log` | `INCONCLUSIVE` | G8 reflete le refus/non-execution de l'acces OOS apres WRC `FAIL`. |
| `validate_package_dir()` | `FAIL` | Echec attendu et coherent : G4/G6/G8/G9/G10 non passants, `economic.global_status`, `incubation_gate` et `INV-003 FAIL`. |

Conclusion : le systeme est plus mature parce qu'il accepte de rester rouge
quand la preuve statistique manque. Ce `FAIL` est un progres de gouvernance,
pas une regression a masquer.

### Matrice complete fait / partiel / ouvert

| Point de l'audit initial | Etat 2026-07-17 | Verdict |
| --- | --- | --- |
| R1 — vrai moteur de signaux | Registry + strategies incrementales E/F/G/H/I branchees dans `GenericPayloadStrategy`. | FAIT |
| R2 — extraction Nautilus reelle | NAV snapshots, fills, positions, commissions et cas position ouverte couverts. | FAIT |
| R3 — preuve vs attestation | WRC, statut global, incubation, G5, Lots C/A2/B et R3 D/E/F sont derives de preuves/statuts calcules sur le chemin de generation ; `invariant_evidence.json` derive ses quatre preuves ciblees. Restent les attestations humaines/post-OOS et la generalisation de l'horodatage aux autres jalons. | TECHNIQUE RESOLU / GOUVERNANCE TRANSVERSALE RESIDUELLE |
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
5. **Les attestations residuelles principales de `gates.json` ont ete
   traitees.** Lot C a branche les statuts mecaniques, A2 calcule la puissance
   atteinte, et B interdit maintenant un G6 `PASS` si l'execution/NAV OOS est
   insuffisamment prouvee.
6. **`invariant_evidence.json` ne fabrique plus ses quatre preuves ciblees.**
   Le scellement UTC, les WRC locaux, les transformations et les evenements
   PIT sont derives de leurs sources; une preuve locale absente reste
   `INCONCLUSIVE` plutot que de devenir un faux `PASS`.

### Ce qui reste bloquant avant une campagne complete

1. **Package courant rouge par WRC.** Tant que `wrc.verdict=FAIL`, on ne peut
   pas parler d'une strategie candidate validee ; on peut seulement dire que le
   pipeline rejette honnetement cette famille.
2. **Aucune exposition OOS autorisee dans l'artefact persistant.**
   `oos_total_orders=0` est coherent avec le WRC `FAIL`; G6/G8 restent
   `INCONCLUSIVE` et `INV-003` echoue au lieu de laisser croire a une preuve
   OOS exploitable.
3. **Couts et execution non calibres.** Les frais maker/taker sont indicatifs,
   la latence et le slippage restent essentiellement nuls.
4. **Robustesse non stressee.** Les scenarios doivent appliquer de vrais chocs
   de cout, slippage, latence, fills ou donnees, pas seulement relire les memes
   resultats sous trois labels.
5. **Reproductibilite incomplete.** `DEFAULT_DATA_ROOT` reste absolu Windows et
   `NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER` reste litteral.
6. **Attestations residuelles reduites mais pas nulles.** R3 traite les preuves
   techniques d'invariants; les attestations humaines/post-OOS et l'horodatage
   automatique des autres jalons doivent rester explicites ou devenir des plans
   dedies.

## 3. Suites actualisees — INTERMEDIAIRE 2026-07-20

Les plans R1/R2, R4, la correction ciblee du WRC masque, la correction du statut
global de package, la correction G5, la documentation du `PASS` R4 artefactuel
/ `FAIL` WRC M1 legitime, les EPIC C/A2/B et R3 des attestations residuelles ont ete
routes, executes et clotures apres l'audit initial. La suite utile n'est donc
plus de relancer ces chantiers, mais de creer un ou plusieurs plans separes pour
les risques encore ouverts.

Priorite recommandee :

1. `R5/R6` — calibrer les couts/slippage/latence puis construire de vrais
   stress de robustesse.
2. `R7` — rendre le data root configurable, remplacer le hash placeholder et
   documenter l'environnement Nautilus sans committer le venv.
3. Horodatage transversal et attestations humaines/post-OOS — generaliser
   l'evenement automatique de date aux autres jalons cles et expliciter les
   decisions qui ne peuvent pas etre derivees du runtime.
4. `R4-long` — benchmark 1 mois / 3 mois / 1 an avec budget temps, memoire,
   ordres, exposition OOS et validation package.

Backlog d'idees a transformer en plans si priorisees :

1. **Warm-up inter-fold / lookback** : verifier que les segments test/OOS
   recoivent assez de contexte historique pour les payloads avec lookback.
2. **Benchmark donnees longues / scalabilite** : tester 1 mois, 3 mois, puis
   1 an sur NASDAQ/XAUUSD, avec budget temps, memoire, timeouts, nombre
   d'ordres, exposition OOS et validation package.
3. **Validateur qualite CSV M1** : controler timestamps monotones UTC,
   doublons, trous, coherence OHLC, volumes invalides, journees partielles et
   changements de format.
4. **Edge cases Nautilus** : position ouverte, rapport vide, zero fill, fill
   partiel, ordre rejete/annule, precision prix/quantite, commissions absentes
   ou non numeriques.
5. **Invariant `PASS` non inerte** : renforcer l'exposition non nulle, les
   couts presents quand le modele l'exige, et la coherence fills/positions/NAV.
6. **Frontiere bug-hunter vs validation scientifique** : garder bug-hunter
   comme filet mecanique et ouvrir des plans dedies pour robustesse, puissance,
   realisme economique et qualite de recherche.

## 4. Question d'architecture residuelle — INTERMEDIAIRE 2026-07-20

La decision la plus risquee a long terme n'est pas Nautilus, c'est la porosite
entre la couche qui calcule les preuves et celle qui les declare. Le risque
residuel se concentre maintenant sur certaines attestations humaines/post-OOS
et sur les autres jalons non encore horodates automatiquement, plutot que sur
les quatre preuves ciblees de `invariant_evidence.json`.

Mise a jour 2026-07-20 : le premier vrai signal existe maintenant, le statut
global package consomme les echecs WRC/economic/incubation, G5 consomme le
verdict de robustesse pre-OOS reel, et l'EPIC C/A2/B a corrige les attestations
prioritaires de `gates.json`; R3 a ensuite derive les preuves techniques
restantes de `invariant_evidence.json` et regenere le package persistant. Le
sujet restant est donc cible : attestations humaines legitimes, post-OOS et
horodatage transversal des autres jalons.

Second point : avoir choisi Nautilus puis contourner sa comptabilite reviendrait
a payer le cout sans le benefice. La suite devrait donc verifier que la NAV, les
fills, les couts et les positions restent alignes avec les sorties exploitables
de Nautilus, ou assumer explicitement les limites du mapping.

---

# Partie B — Historique initial conserve

## H0. Avertissement initial — HISTORIQUE 2026-07-13

L'etat machine (`.ai/checkpoint.json`, `Implementation/Active/tracking.json`)
affiche `DONE` / `PASS` / `110 tests PASS` partout. **Ces statuts sont vrais
structurellement mais trompeurs scientifiquement.** L'audit a lu le chemin
critique complet : chargement de donnees -> strategie -> simulation Nautilus ->
extraction -> statistiques -> gates -> validation.

Mise a jour 2026-07-20 : cet avertissement reste utile comme principe de
lecture, mais certains exemples qui l'ont motive ont ete corriges depuis
(R1/R2/R4, WRC masque, validators/statut global package, G5 et attestations
prioritaires `gates.json` via l'EPIC C/A2/B, puis les quatre preuves cibles de
`invariant_evidence.json` via R3). Le risque residuel porte surtout sur les
attestations humaines/post-OOS, l'horodatage transversal et la validation
scientifique longue.

---

## H1. Diagnostic initial du moteur — HISTORIQUE 2026-07-13

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

## H2. Audit par zones — HISTORIQUE avec notes 2026-07-15

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
  attestations residuelles de `gates.json` ont ensuite ete traitees par
  l'EPIC C/A2/B du 2026-07-17 ; `invariant_evidence.json` et les attestations
  humaines/post-OOS restent a traiter separement si priorisees.
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
  les validators. Mise a jour 2026-07-17 : les attestations prioritaires de
  `gates.json` visees par C/A2/B sont corrigees sur le chemin de generation.
  Mise a jour 2026-07-20 : R3 derive ensuite les quatre preuves cibles de
  `invariant_evidence.json` et regenere le package persistant. Restent les
  attestations humaines/post-OOS legitimes et l'horodatage transversal.
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

## H3. Reel vs. impression de fonctionner — HISTORIQUE 2026-07-13

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

## H4. Ecart initial avec un vrai moteur de recherche quantitative — HISTORIQUE 2026-07-13

Liste initiale des composants manquants, par gravite decroissante. Voir la
partie A pour l'etat courant et les suites actualisees.

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

## H5. Roadmap initiale — HISTORIQUE 2026-07-13

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

### Renvoi vers l'etat courant

La table actuelle, les priorites et les idees de futurs plans ont ete deplacees
en Partie A pour eviter deux sources de lecture concurrentes. Voir :

- section 2 pour la matrice fait / partiel / ouvert ;
- section 3 pour les suites actualisees ;
- section 4 pour la question d'architecture residuelle.

---

## H6. Vision globale initiale — HISTORIQUE 2026-07-13

Les pourcentages ci-dessous sont des estimations **HISTORIQUES 2026-07-13**,
non recalculees apres R1/R2/R4/WRC. Ils doivent etre relus comme une mesure de
maturite initiale, pas comme un score courant exact.

- Echafaudage gouvernance/stats/validation : **~70-75%** (reellement construit,
  teste, serieux — la vraie valeur du depot).
- Capacite de moteur de recherche quantitative : **~15-20%** (coeur absent).
- Global vers "campagne robuste et reproductible" : **~20-25%**.

### Risques techniques principaux initiaux — HISTORIQUE / deja requalifies en Partie A
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

La liste actuelle des bloquants a ete deplacee en section 2, puis convertie en
suites actionnables en section 3. Cette sous-section historique ne maintient
plus de seconde liste de priorites.

---

## H7. Remise en question de l'architecture — DEPLACEE

La synthese actuelle de ce point est maintenant en section 4. Cette section
historique est conservee comme renvoi pour ne pas maintenir deux formulations.

---

## H8. Suite proposee — DEPLACEE

La suite actuelle est maintenant en section 3. Cette section historique est
conservee comme renvoi pour ne pas maintenir deux listes concurrentes.

Ce document reste volontairement en `INTAKE` : il sert de reservoir de constats
et de futurs plans, pas de source executable.
