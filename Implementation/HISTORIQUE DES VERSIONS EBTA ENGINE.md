# Historique des versions EBTA Engine

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - HISTORIQUE_IMPLEMENTATION |
| Date de creation | 2026-06-24 |
| Objet | Journaliser les evolutions du dossier `Implementation/` et du futur EBTA Engine Core. |
| Autorite normative | Aucune : l'autorite normative reste dans `Protocole/`. |
| Source documentaire | `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Hook de reprise | `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` |

## Fonction

Ce fichier est le registre d'evolution du runtime EBTA.

Il journalise :

- les changements de structure de `Implementation/` ;
- les decisions techniques du moteur EBTA ;
- les ajouts de schemas, validateurs, fixtures et tests ;
- les modifications de gouvernance du runtime ;
- les points qui doivent etre remontes vers `Protocole/` si une ambiguite ou un
  changement normatif apparait.

Ce fichier ne remplace pas :

- `Protocole/HISTORIQUE DES VERSIONS EBTA.md` ;
- `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` ;
- `Protocole/MANIFESTE DE GEL EBTA.md`.

## Regle d'autorite

`Implementation/` est evolutif. `Protocole/` est normatif.

Si une evolution du runtime :

- encode une regle deja presente dans `Protocole/`, elle est journalisee ici ;
- clarifie une decision technique sans changer la norme, elle est journalisee ici ;
- revele une ambiguite documentaire, elle est journalisee ici puis marquee
  `DOCUMENTATION_CLARIFICATION_NEEDED` ;
- exige une nouvelle decision methodologique, elle est marquee
  `NORMATIVE_CHANGE_REQUIRED` et doit passer par le processus officiel de
  version documentaire EBTA.

## Format des entrees

Chaque entree doit utiliser ce format :

```text
## YYYY-MM-DD - <titre>

| Champ | Valeur |
| --- | --- |
| Version runtime | <ex: EBTA-ENGINE-0.1.0 ou N/A> |
| Type | IMPLEMENTATION_DETAIL / CONTRACT_ENCODING / TEST_FIXTURE / GOVERNANCE / ADAPTER_MAPPING / DOCUMENTATION_CLARIFICATION_NEEDED / NORMATIVE_CHANGE_REQUIRED |
| Statut | DRAFT / ACCEPTED / SUPERSEDED / BLOCKED_NORMATIVE |
| Source normative | <fichier, section, SOP ou DN-ID> |
| Fichiers impactes | <liste> |
| Impact protocole | NONE / CLARIFICATION_NEEDED / NORMATIVE_CHANGE_REQUIRED |
| Verification | <commande ou preuve> |

### Contexte

...

### Decision

...

### Impact

...

### Suite

...
```

## Entrees

## 2026-06-26 - STEP_2_T0 : Audit exhaustivite Implementation/ vs Protocole/ - 13 angles morts corriges

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING + IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | PAQUET D'EXECUTION EBTA.md sections 1-6; SOP 01-12; DN-001 a DN-041; INV-016 |
| Fichiers impactes | Voir liste ci-dessous |
| Impact protocole | NONE |
| Verification | `python -m pytest ebta_engine/tests/ -v --tb=short` : 50 passed, 16 subtests passed |

### Contexte

Audit d'exhaustivite systematique : chaque contrat normatif de `Protocole/` a ete compare aux artefacts de `Implementation/ebta_engine`. Objectif : garantir qu'un moteur de backtest construira sur des contrats complets, sans angle mort permettant de passer les gates EBTA en violant le protocole.

### Decision

Implementer l'exhaustivite en 3 phases (A critiques, B moderes, C mineurs) comme sous-etape STEP_2_T0 integree dans STEP_2. Les procedures restent des validateurs de contrat (non des calculateurs). La re-execution de reproduction est exclue du moteur (circulaire par nature).

### Impact

**Phase A - Angles morts critiques**

| Item | Fichier(s) | Source normative |
| --- | --- | --- |
| A1 - Registre append-only | `validators/registry_append_only_validator.py` (NEW) | SOP 03, DN-005 a DN-008 |
| A2 - Robustesse structuree | `procedures/robustness.py` (MODIFIED) | SOP 05, DN-030, DN-031 |
| A3 - Journal execution | `schemas/execution_journal_event.schema.json` (NEW) | SOP 09B, DN-028, DN-029 |
| A4 - Formulaires G1/G3/G5/G12-G13 | 4 schemas (NEW) | SOP 09A, SOP 04, SOP 05, SOP 11 |
| A5 - Hash catalogue WRC | `procedures/wrc.py` (MODIFIED) | SOP 02, DN-008 |

**Phase B - Angles morts moderes**

| Item | Fichier(s) | Source normative |
| --- | --- | --- |
| B2 - Monitoring sequentiel | `procedures/monitoring.py` (NEW) | SOP 11, DN-037 |
| B3 - Rapport incubation | `procedures/incubation_report.py` (NEW) | SOP 11, DN-035, DN-036 |
| B4 - Rapport reproduction | `procedures/reproduction_report.py` (NEW) + schema | SOP 12, DN-039, INV-016 |
| B5 - Puissance OOS | `procedures/oos_confidence_interval.py` (MODIFIED) | SOP 01, DN-004, DN-021 |

**Phase C - Angles morts mineurs**

| Item | Fichier(s) | Source normative |
| --- | --- | --- |
| C2 - Archive lifecycle | `schemas/lifecycle_archive.schema.json` (NEW) | SOP 12, DN-041 |
| C3 - Non-chevauchement preventif | `procedures/walk_forward.py` (MODIFIED) | SOP 04, DN-001, DN-004 |
| C1 - config.schema.json complet | REPORTE a STEP_2_T1 | Template configuration |

**Gouvernance** : TRACEABILITY_MATRIX.md, PROCEDURE_CALCULATION_MAP.md, task_tracking.json mis a jour.

### Suite

STEP_2_T1 : definir les inputs pilotes concrets et construire le pipeline end-to-end. La condition supplementaire : aucun contrat normatif du PAQUET D'EXECUTION ne doit rester sans artefact Implementation/ correspondant - satisfaite.

---

## 2026-06-26 - Archivage des hooks plans et contextes termines

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` |
| Fichiers impactes | `Implementation/Archives/completed_2026-06-26/`, `Implementation/0-CARTE_DU_CODE_EBTA.md`, `Implementation/PROCEDURE_CALCULATION_MAP.md`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/tests/test_procedure_map.py`, `.agents/skills/EBTA_Protocol_Guardian/SKILL.md`, `Protocole/PROTOCOLE EBTA.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\task_tracking.json`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 50 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS; `git diff --check -- Implementation Protocole Archives .gitignore .agents` PASS avec avertissements CRLF/LF uniquement |

### Contexte

Le niveau racine de `Implementation/` contenait encore des hooks, plans et
contextes de lots termines. Bien qu'ils restent utiles historiquement, ils
polluaient la surface active de reprise.

### Decision

Deplacer les artefacts termines vers :

```text
Implementation/Archives/completed_2026-06-26/
```

Artefacts archives :

- `HOOK - Reprise EBTA Engine Core autonome.md` ;
- `PLAN - Procedures de calcul EBTA et optimisation ML.md` ;
- `implementation_context.json`.

Les pointeurs actifs sont corriges vers le hook actif, le suivi actif ou les
chemins archives selon le role.

### Impact

Cette operation est un rangement de gouvernance runtime. Elle ne change aucun
gate, statut, seuil, invariant ou contrat EBTA. `Protocole/` reste l'autorite
normative.

### Suite

Utiliser le hook actif et `task_tracking.json` pour les prochains lots. Lire les
artefacts archives uniquement pour l'historique des lots termines.

## 2026-06-26 - Creation du hook de plan actif et du suivi JSON

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`, `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Fichiers impactes | `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md`, `Implementation/task_tracking.json`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\task_tracking.json`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `git diff --check -- Implementation Protocole` |

### Contexte

Le lot `EBTA-ENGINE-0.1.0` est construit et teste. Avant le checkpoint du lot
actuel, une pre-etape d'archivage controle des elements obsoletes est ajoutee
pour reduire la surface de reprise sans supprimer l'historique utile.

### Decision

Creer un hook de plan actif et un fichier JSON de suivi de tache. Le plan suit
l'ordre :

```text
Etape 0 - Archivage controle des obsoletes
Etape 1 - Checkpoint du lot actuel
Etape 2 - Pipeline pilote EBTA reel local
Etape 3 - Integration BACKTRADER apres lecture de sa gouvernance locale
```

### Impact

Cette evolution est une decision de gouvernance runtime. Elle ne cree aucun
gate EBTA, statut normatif, seuil methodologique ou changement d'ordre des
gates. `Protocole/` reste l'autorite normative.

### Suite

Commencer par `STEP_0_ARCHIVE_OBSOLETE` dans
`Implementation/task_tracking.json`, inventorier les candidats a l'archive,
puis verifier les references avant tout deplacement.

## 2026-06-24 - Creation du plan de reprise EBTA Engine Core autonome

| Champ | Valeur |
| --- | --- |
| Version runtime | N/A |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/MANIFESTE DE GEL EBTA.md`, `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Fichiers impactes | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | Creation documentaire hors `Protocole/`; `Protocole/` non modifie. |

### Contexte

Le protocole EBTA est gele en `EBTA-DOC-1.0` avec une phase
`DEFERRED_IMPLEMENTATION` pour les schemas machine-readable, registres JSONL,
validateurs, manifestes et tests.

### Decision

Creer un dossier `Implementation/` comme espace evolutif du futur EBTA Engine
Core autonome.

Le runtime doit etre construit avant l'adaptateur BACKTRADER afin d'eviter de
melanger norme EBTA, dette BACKTRADER et refonte de pipeline.

### Impact

Le dossier `Implementation/` devient maintenu par le Gardien EBTA, mais reste
subordonne a `Protocole/`.

### Suite

Avant le premier code runtime :

1. creer le README technique du runtime ;
2. reprendre la hierarchie des sources de verite ;
3. creer le premier schema de configuration ;
4. ajouter une fixture valide et une fixture invalide ;
5. ajouter le premier test de validation.

## 2026-06-24 - Ajout de la Phase 0bis maintenabilite du runtime

| Champ | Valeur |
| --- | --- |
| Version runtime | N/A |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, audit de maintenabilite pre-implementation |
| Fichiers impactes | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | Changement de gouvernance runtime hors `Protocole/`; aucune regle normative EBTA ajoutee. |

### Contexte

Avant de demarrer les schemas et validateurs, l'audit de maintenabilite a
identifie six angles morts : version/compatibilite, migrations de schemas,
quality gate, tracabilite, persistance et frontiere de confiance des
adaptateurs.

### Decision

Ajouter une `Phase 0bis - Maintenabilite du runtime` dans le hook de reprise.

Cette phase doit etre executee apres le cadrage initial et avant le premier
schema stable.

### Impact

La sequence de demarrage devient :

```text
Phase 0 -> Phase 0bis -> Phase 1
```

Les schemas machine-readable ne doivent pas commencer avant d'avoir defini les
regles minimales de version, migration, quality gate, tracabilite, persistance
et frontiere d'adaptateurs.

### Suite

Creer le README technique du runtime en y integrant les decisions de Phase 0 et
Phase 0bis, puis seulement demarrer `config.schema.json`.

## 2026-06-24 - Socle autonome EBTA Engine Core 0.1.0

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / CONTRACT_ENCODING / TEST_FIXTURE / IMPLEMENTATION_DETAIL / ADAPTER_MAPPING |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 2, 3, 5, 6; `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`; SOP 03, SOP 10, SOP 12 |
| Fichiers impactes | `Implementation/ebta_engine/README.md`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/schemas/`, `Implementation/ebta_engine/validators/`, `Implementation/ebta_engine/manifests/`, `Implementation/ebta_engine/fixtures/`, `Implementation/ebta_engine/tests/`, `Implementation/ebta_engine/adapters/backtrader_mapping.py` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` |

### Contexte

La Phase 0 et la Phase 0bis demandaient de stabiliser la frontiere entre
protocole, runtime et adaptateurs avant d'ecrire des validateurs normatifs.
Le paquet d'execution demandait ensuite des schemas, fixtures, manifestes,
invariants, rapports de gates et tests automatises.

### Decision

Creer un noyau Python standard-library first, versionne
`EBTA-ENGINE-0.1.0`, couvrant un premier socle autonome :

- README technique et quality gate;
- matrice de tracabilite runtime vers sources normatives;
- schemas minimaux de configuration, registre, journal OOS et manifeste;
- fixtures valides et invalides;
- generateur/verificateur de manifeste SHA-256;
- validateurs d'invariants executables avec deferral explicite pour les
  controles exigeant des donnees de pipeline;
- controle minimal des gates G0 a G14;
- stub contractuel d'adaptateur BACKTRADER;
- tests transversaux, dont verification des hashes du protocole gele.

### Impact

Le runtime encode des champs et controles deja presents dans les documents
geles. Aucun document de `Protocole/` n'est modifie et aucune nouvelle regle
methodologique n'est creee.

Les invariants qui exigent des artefacts de pipeline reels sont marques
`DEFERRED_REQUIRES_PIPELINE_DATA` plutot que normalises artificiellement.

### Suite

Etendre progressivement les validateurs a partir de vrais artefacts de
recherche EBTA, puis brancher BACKTRADER uniquement comme producteur/consommateur
d'artefacts conformes.

## 2026-06-24 - Completion locale des phases du hook EBTA Engine

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING / INVARIANT_CHECK / GATE_CHECK / MANIFEST_CHECK / TEST_FIXTURE / ADAPTER_MAPPING / GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 2, 3, 5, 6; `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` DN-001 a DN-041; SOP 03, SOP 04, SOP 05, SOP 08, SOP 09A, SOP 10, SOP 11, SOP 12 |
| Fichiers impactes | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/validators/`, `Implementation/ebta_engine/fixtures/`, `Implementation/ebta_engine/tests/`, `Implementation/ebta_engine/persistence.py`, `Implementation/ebta_engine/adapters/backtrader_mapping.py` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check` |

### Contexte

Le premier socle avait couvert le demarrage du runtime, mais pas encore les
phases du hook en profondeur. Les invariants etaient partiels, les gates
minimales, la fixture de paquet incomplete et l'adaptateur BACKTRADER limite a
un stub.

### Decision

Completer localement les phases du hook sans modifier le repo BACKTRADER :

- ajouter un suivi d'avancement dans le hook;
- rendre `INV-001` a `INV-016` executables sur preuves de paquet;
- ajouter une fixture invalide par invariant;
- enrichir le rapport de gates G0 a G14 avec preuves presentes/manquantes;
- valider un paquet EBTA minimal de bout en bout;
- ajouter la persistance atomique et append-only locale;
- mapper un payload externe vers les artefacts EBTA dans l'adaptateur local,
  sans lecture ni ecriture dans BACKTRADER.

### Impact

Le runtime reste subordonne au protocole gele. Les champs de fixture servent a
porter les preuves demandees par le paquet d'execution et le registre normatif;
ils ne creent pas de statut, seuil, gate ou definition methodologique nouvelle.

La Phase 6 est marquee
`LOCAL_CONTRACT_DONE_BACKTRADER_REPO_UNTOUCHED` dans le hook, car l'utilisateur a
explicitement demande de ne pas modifier le repo BACKTRADER pour l'instant.

### Suite

Avant toute integration reelle BACKTRADER, lire sa gouvernance locale, puis
brancher le mapping comme producteur/consommateur d'artefacts EBTA conformes.

## 2026-06-24 - Guide de construction d'un pipeline de recherche EBTA

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Protocole/PAQUET D'EXECUTION EBTA.md`, `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` |
| Fichiers impactes | `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | Guide documentaire hors `Protocole/`; aucune regle normative ajoutee. |

### Contexte

Le runtime EBTA etait valide comme banc de controle, mais il manquait un pont
explicite entre le protocole, les contrats `Implementation/ebta_engine/` et la
construction concrete d'un pipeline de recherche.

### Decision

Ajouter un guide dedie qui explique :

- le role respectif de `Protocole/`, `Implementation/` et d'un pipeline reel ;
- les artefacts qu'un pipeline EBTA doit produire ;
- le workflow de construction ou de refonte d'un pipeline existant ;
- comment utiliser `package_validator` comme controle d'acceptation ;
- le prompt de depart a donner a une IA pour construire un pipeline conforme.

### Impact

Le guide clarifie l'usage du runtime sans changer les contrats, les schemas, les
gates, les invariants ou les SOP.

### Suite

Choisir entre un pipeline pilote minimal dans ce repo ou l'ouverture du repo
BACKTRADER pour construire un adaptateur reel apres lecture de sa gouvernance.

## 2026-06-24 - Ajout des routes build refactor audit pour pipeline EBTA

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md`, `Protocole/PROTOCOLE EBTA.md`, `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Fichiers impactes | `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check` |

### Contexte

Le guide expliquait deja les blocs de recherche et les artefacts EBTA, mais il
ne donnait pas encore a une IA une cle de decision claire face a un repo reel.

### Decision

Ajouter trois routes d'intervention :

- construire de zero ;
- refondre ou migrer un pipeline existant ;
- auditer et corriger un pipeline qui se declare EBTA.

Chaque route precise l'ordre de travail, les questions d'audit, les classes
d'ecart et la definition de fini.

### Impact

Cette clarification ne change aucun contrat runtime et aucune regle normative.
Elle rend l'utilisation de `Protocole/` et `Implementation/` plus actionnable
pour une IA arrivee face a un repo.

### Suite

Utiliser cette cle de decision avant tout travail sur un pipeline pilote ou sur
BACKTRADER.

## 2026-06-24 - Audit d'obsolescence des documents Implementation

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Implementation/ebta_engine/README.md`, `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md` |
| Fichiers impactes | `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`, `Implementation/ebta_engine/README.md`, `Implementation/ebta_engine/migrations/README.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check` |

### Contexte

Le hook contenait encore deux sections de demarrage (`Premier lot recommande` et
`Etat de reprise`) qui demandaient de lancer Phase 0 / Phase 0bis et de creer le
squelette `Implementation/ebta_engine/`, alors que le tableau d'avancement, le
README runtime, la matrice de tracabilite et les tests prouvaient que le socle
`EBTA-ENGINE-0.1.0` existait deja.

### Decision

Remplacer les consignes de demarrage par un etat courant :

- Phase 0 a Phase 5 terminees localement ;
- Phase 6 limitee au contrat local BACKTRADER sans modification du repo externe ;
- prochaine decision orientee vers un pipeline pilote ou l'integration
  BACKTRADER apres lecture de sa gouvernance ;
- statut du README runtime aligne sur `ACTIF - RUNTIME_CONTRACT_0.1.0` ;
- note de migrations alignee sur la version de schema active `1.0.0`.

### Impact

La mise a jour supprime une contradiction documentaire interne sans changer les
schemas, validateurs, gates, invariants, statuts EBTA ou documents geles du
protocole.

### Suite

Choisir une cible de pipeline et utiliser `Implementation/ebta_engine/` comme
banc de controle. Toute integration BACKTRADER reelle doit commencer par la
lecture de sa gouvernance locale.

## 2026-06-25 - Pipeline pilote minimal local

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 2, 3, 5, 6; `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md` |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `validate_package_dir()` sur `Implementation/examples/minimal_pilot_pipeline/research_package`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation .gitignore` |

### Contexte

Le socle `EBTA-ENGINE-0.1.0` validait deja une fixture minimale, mais le lot
suivant recommande demandait de prouver qu'un pipeline local pouvait produire un
vrai `research_package/` valide par le banc de controle.

### Decision

Ajouter un pipeline pilote local dans
`Implementation/examples/minimal_pilot_pipeline/`.

Le script `build_research_package.py` recree un paquet deterministe, ecrit les
artefacts requis, genere le manifeste de reproductibilite via le runtime et
valide le paquet avec `validate_package_dir()`.

Un test dedie verifie que ce pilote continue de produire un paquet `PASS`.

### Impact

Le changement ne modifie aucun schema, gate, invariant, statut EBTA ou document
gele du protocole. Il ajoute une preuve executable qu'un workflow minimal peut
produire les artefacts attendus par `Implementation/ebta_engine/`.

Le repo BACKTRADER reste non lu et non modifie.

### Suite

Utiliser ce pilote comme point de comparaison avant de brancher un pipeline reel
ou d'ouvrir BACKTRADER apres lecture de sa gouvernance locale.

## 2026-06-25 - Plan procedures de calcul EBTA et optimisation ML

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | SOP 01, SOP 02, SOP 03, SOP 04, SOP 06, SOP 07, SOP 08, SOP 09B, SOP 12; `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md` |
| Fichiers impactes | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | Plan documentaire hors `Protocole/`; `git diff --check -- Implementation` |

### Contexte

Le pipeline pilote minimal prouve qu'un paquet EBTA peut etre produit et valide,
mais il reste declaratif sur les calculs internes qui doivent produire les
preuves : optimisation parametrique, manifeste ML, matrice de candidates,
selection de complexite, detrending, zero-centering, WRC et IC OOS.

### Decision

Ajouter et figer un plan avant implementation des procedures de calcul.

Le plan classe les angles morts actuels et propose une sequence de construction
des modules `Implementation/ebta_engine/procedures/`, en commencant par le bloc
SOP 06 optimisation / ML / complexite.

Le perimetre du premier lot est verrouille :

- `Phase 1 + Phase 2` seulement ;
- SOP 06 uniquement ;
- ML factice et deterministe ;
- standard-library first ;
- artefacts pilotes non encore schemas obligatoires ;
- second pilote dedie `procedure_sop06_pilot` si necessaire ;
- pas de WRC numerique dans ce lot ;
- pas de donnees de marche reelles ;
- pas de BACKTRADER ;
- pas de changement `Protocole/`.

Un audit complementaire contre les gates G0 a G14 et les invariants INV-001 a
INV-016 ajoute au plan les angles morts processus a traiter dans des phases
ulterieures : donnees point-in-time, construction des folds, registre lineage,
robustesse pre-OOS, scellement et acces OOS, gate economique separe, incubation
et lifecycle.

### Impact

Le changement ne cree aucun nouveau contrat machine-readable et ne modifie
aucune regle EBTA. Il prepare un lot d'implementation subordonne aux SOP
existantes. Le premier lot fige reste inchange et cible SOP 06 seulement.

### Suite

Implementer ensuite le premier lot fige : cartographie executable et bloc SOP
06 optimisation / ML / complexite.

## 2026-06-25 - Ajout du contexte JSON de suivi IA au plan procedures

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md`, `Implementation/HOOK - Reprise EBTA Engine Core autonome.md` |
| Fichiers impactes | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `git diff --check -- Implementation` |

### Contexte

Le plan de procedures doit etre executable par une session IA longue sans perte
de contexte entre les phases, les modules et les tests de non-divergence.

### Decision

Ajouter au plan la creation de
`Implementation/implementation_context.json` comme fichier de suivi
machine-readable.

Ce fichier doit indiquer le lot actif, les phases terminees, la phase courante,
le prochain pas, les fichiers touches, les verifications lancees, les blocages
et les non-objectifs actifs.

### Impact

Le fichier de contexte est un outil de reprise operationnelle. Il ne devient pas
une source normative, ne remplace pas le plan, ne remplace pas l'historique
runtime et ne modifie aucun schema EBTA existant.

### Suite

Lors de l'implementation du premier lot Phase 1 + Phase 2, creer ou mettre a
jour `Implementation/implementation_context.json` avant de commencer les
modules de procedures, puis le maintenir apres chaque etape significative.

## 2026-06-25 - Phase 1 cartographie executable des procedures

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md`; `Protocole/PROTOCOLE EBTA.md`; `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`; `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Fichiers impactes | `Implementation/implementation_context.json`, `Implementation/PROCEDURE_CALCULATION_MAP.md`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/tests/test_procedure_map.py` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

Le plan de procedures demande une carte `procedure -> SOP -> inputs -> outputs
-> artefacts` avant d'ajouter les modules de calcul.

### Decision

Ajouter une carte markdown couvrant les procedures statistiques et de
gouvernance prevues par les phases 2 a 8, et initialiser le contexte JSON de
suivi IA.

### Impact

La carte reste un artefact de reprise et de tracabilite. Elle ne cree pas de
seuil, statut, gate ou definition EBTA.

### Suite

Executer la validation de Phase 1, puis implementer les modules SOP 06 de la
Phase 2.

## 2026-06-25 - Phase 2 procedures SOP 06 optimisation ML complexite

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 06 sections 5, 8, 9, 11, 12, 16, 17, 19, 23; SOP 03 sections 6, 8, 14; SOP 02 sections 4, 5 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/search_space.py`, `Implementation/ebta_engine/procedures/optimization.py`, `Implementation/ebta_engine/procedures/ml_manifest.py`, `Implementation/ebta_engine/procedures/complexity_selection.py`, `Implementation/ebta_engine/procedures/candidate_matrix.py`, `Implementation/ebta_engine/tests/test_procedure_sop06.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 2 doit combler l'angle mort prioritaire du plan : produire les
artefacts pilotes de snapshot d'espace, optimisation Train, manifeste ML,
selection de complexite Test et matrice complete des candidates.

### Decision

Ajouter des fonctions de reference deterministes, standard-library first, qui
encodent uniquement les procedures deja presentes dans SOP 06 et les sources
associees.

### Impact

Les modules produisent des dictionnaires JSON-ready et refusent explicitement
l'OOS dans les procedures de selection. Les artefacts pilotes ne deviennent pas
des schemas obligatoires.

### Suite

Executer la validation de Phase 2, puis passer aux calculs de rendements et
transformations SOP 07 / SOP 08 / SOP 09B.

## 2026-06-25 - Phase 3 rendements et detrending

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 07 sections 3, 6, 8, 14, 20, 26; SOP 08 sections 3, 5, 6, 8, 10, 24, 25; SOP 09B sections 3, 33 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/returns.py`, `Implementation/ebta_engine/procedures/detrending.py`, `Implementation/ebta_engine/tests/test_procedure_returns.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 3 demande de rendre reproductibles les series de performance et les
transformations avant WRC et OOS.

### Decision

Ajouter des fonctions de reference pour construire les log-rendements quotidiens
economiques, verifier la reconciliation P&L net, calculer la moyenne primaire et
appliquer le detrending d'evaluation SOP 07.

### Impact

Les sorties gardent separes rendement economique, serie detrendee et flux de
signal. Les jours `NO_MODEL` restent dans la chronologie.

### Suite

Executer la validation de Phase 3, puis implementer zero-centering, bootstrap et
WRC numerique minimal.

## 2026-06-25 - Phase 4 zero-centering bootstrap WRC

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 02 sections 6, 7, 8, 9, 14, 15, 18; SOP 07 sections 15, 16, 17; DN-008 a DN-011, DN-018, DN-020 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/zero_centering.py`, `Implementation/ebta_engine/procedures/bootstrap.py`, `Implementation/ebta_engine/procedures/wrc.py`, `Implementation/ebta_engine/tests/test_procedure_wrc.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 4 transforme le rapport WRC declaratif en calcul numerique minimal.

### Decision

Ajouter zero-centering par colonne, bootstrap stationnaire conjoint et WRC local
sur matrice complete avec seed fixe. SPA, Romano-Wolf et MCPM restent signales
comme analyses secondaires non implementees dans ce lot.

### Impact

Le WRC refuse une matrice contenant seulement la gagnante et conserve la famille
complete comme objet statistique. L'OOS reste exclu du zero-centering.

### Suite

Executer la validation de Phase 4, puis implementer l'intervalle de confiance
OOS separe.

## 2026-06-25 - Phase 5 intervalle de confiance OOS

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 01 sections 3, 4, 7, 8, 10, 13, 15, 20; DN-019 a DN-022 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/oos_confidence_interval.py`, `Implementation/ebta_engine/tests/test_procedure_oos_ci.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 5 demande un intervalle OOS qui ne reutilise jamais la distribution WRC
Test.

### Decision

Ajouter une procedure d'IC OOS fondee sur la serie OOS concatenee et un
bootstrap stationnaire separe. Le verdict statistique suit la mecanique SOP 01 :
`PASS`, `NOT_VALIDATED`, `FAIL` ou `INCONCLUSIVE`.

### Impact

Le module bloque explicitement toute source `WRC` ou `TEST` pour l'IC OOS. Les
sorties incluent estimation, bornes, seed, replications et puissance.

### Suite

Executer la validation de Phase 5, puis implementer les procedures de
gouvernance non statistiques.

## 2026-06-25 - Phase 6 procedures de gouvernance non statistiques

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 03, SOP 04, SOP 05, SOP 08, SOP 09A, SOP 09B, SOP 10, SOP 11, SOP 12; DN-001 a DN-041 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/data_availability.py`, `Implementation/ebta_engine/procedures/walk_forward.py`, `Implementation/ebta_engine/procedures/registry_lineage.py`, `Implementation/ebta_engine/procedures/robustness.py`, `Implementation/ebta_engine/procedures/sealing.py`, `Implementation/ebta_engine/procedures/oos_access.py`, `Implementation/ebta_engine/procedures/economic_gate.py`, `Implementation/ebta_engine/procedures/lifecycle.py`, `Implementation/ebta_engine/tests/test_procedure_governance.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 6 demande de modeliser les procedures qui entourent les calculs
statistiques : disponibilite des donnees, calendrier Walk-Forward, registre,
robustesse pre-OOS, scellement, acces OOS, gate economique et lifecycle.

### Decision

Ajouter des validateurs de procedure simples et deterministes qui retournent des
rapports JSON-ready et separents les dimensions methodologiques, statistiques,
economiques et operationnelles.

### Impact

Ces modules n'ajoutent aucun nouveau seuil. Ils encodent des conditions deja
presentes dans les SOP et signalent `FAIL`, `DENIED`, `REJECTED_ECONOMIC` ou
`INCONCLUSIVE` selon les taxonomies existantes.

### Suite

Executer la validation de Phase 6, puis brancher le pipeline pilote sur les
procedures.

## 2026-06-25 - Phase 7 integration des procedures dans le pipeline pilote

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md` Phase 7; SOP 01, SOP 02, SOP 03, SOP 04, SOP 05, SOP 06, SOP 07, SOP 08, SOP 09A, SOP 09B |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

Le pipeline pilote produisait un paquet valide mais plusieurs rapports etaient
encore des fixtures declaratives.

### Decision

Brancher le pilote local sur les modules `procedures/` pour produire les
rapports `search_space`, `optimization_log`, `ml_manifest`,
`complexity_selection`, `candidate_matrix`, `wrc`, `oos`, `economic`,
`robustness`, `data_availability`, `fold_schedule`, `registry_review` et
`detrending`.

### Impact

Le pilote reste deterministe, local a `Implementation/` et sans donnees de
marche reelles. Le repo BACKTRADER reste non lu et non modifie.

### Suite

Executer la validation de Phase 7, puis produire le mapping de pre-adaptation
BACKTRADER sans ouvrir le repo externe.

## 2026-06-25 - Phase 8 pre-adaptation moteur externe

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | ADAPTER_MAPPING / IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md` Phase 8; `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`; SOP 10, SOP 11, SOP 12 |
| Fichiers impactes | `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md`, `Implementation/ebta_engine/adapters/backtrader_mapping.py`, `Implementation/ebta_engine/tests/test_backtrader_adapter.py`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | A executer: `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `git diff --check -- Implementation` |

### Contexte

La Phase 8 doit preparer un futur branchement vers un moteur externe sans lire
ni modifier BACKTRADER dans ce lot.

### Decision

Ajouter une cartographie locale des sorties attendues d'un moteur externe vers
les entrees des procedures EBTA, ainsi que les erreurs contractuelles attendues.

### Impact

Le noyau EBTA reste proprietaire du contrat. Aucune convention BACKTRADER n'est
importee et le repo BACKTRADER reste non lu et non modifie.

### Suite

Avant toute integration reelle, ouvrir une execution separee, lire la
gouvernance BACKTRADER, puis mapper ses sorties effectives vers ce contrat.

## 2026-06-25 - Durcissement des angles morts de validation package

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING / TEST_FIXTURE / GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 2, 4, 5, 6; SOP 01; SOP 02; SOP 04; SOP 06; SOP 08; SOP 09B; SOP 12; DN-008, DN-020, DN-022, DN-023, DN-027, DN-038, DN-039 |
| Fichiers impactes | `Implementation/ebta_engine/validators/package_validator.py`, `Implementation/ebta_engine/manifests/manifest_builder.py`, `Implementation/ebta_engine/schemas/reproducibility_manifest.schema.json`, `Implementation/ebta_engine/procedures/search_space.py`, `Implementation/ebta_engine/procedures/walk_forward.py`, `Implementation/ebta_engine/procedures/economic_gate.py`, `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/fixtures/valid_minimal/`, `Implementation/ebta_engine/tests/`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `git diff --check -- Implementation` |

### Contexte

Un audit d'angle mort a identifie que le package pouvait encore retourner
`PASS` malgre des gates ou invariants non verts, que les rapports de procedures
ajoutes en phases 2 a 8 n'etaient pas obligatoires, et que le pilote declarait
un paquet `VALIDATION_READY` tout en executant des parametres miniatures.

### Decision

Durcir le runtime sans modifier `Protocole/` :

- faire echouer `validate_package_dir()` si un gate est non `PASS`, si un
  invariant est non `PASS`, si un artefact obligatoire manque ou si le
  manifeste ne reference pas tous les artefacts requis ;
- valider le manifeste SOP 12 par schema et ajouter les sections runtime
  obligatoires : configuration, snapshots, environnement, seeds, calendrier,
  registre, matrices, rapports et logs ;
- ajouter des controles de coherence entre configuration preenregistree,
  search-space, matrice candidates, WRC, OOS, fold schedule et gate economique ;
- aligner le pilote sur une famille complete de candidates et sur 5 000
  replications WRC/OOS preenregistrees ;
- enrichir la fixture minimale et les tests pour couvrir ces echecs.

### Impact

Le runtime devient plus strict et plus fidele au paquet d'execution EBTA. Les
changements encodent des obligations deja presentes dans les SOP et le registre
normatif; ils ne creent aucun nouveau seuil, statut ou ordre de gate.

Le repo BACKTRADER reste non lu et non modifie.

### Suite

Avant tout branchement de pipeline reel, utiliser le validateur durci comme gate
d'acceptation. Toute adaptation BACKTRADER doit rester une execution separee
apres lecture de sa gouvernance locale.

## 2026-06-25 - Durcissement WRC et analyses secondaires SOP 02

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 02 sections 6, 7, 8, 9, 10, 11, 12, 14, 15, 18; DN-008 a DN-011; DN-018 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/wrc.py`, `Implementation/ebta_engine/tests/test_procedure_wrc.py`, `Implementation/examples/minimal_pilot_pipeline/research_package/reports/wrc.json`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/implementation_context.json` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` |

### Contexte

Le module WRC encodait deja le test primaire local sur famille complete avec
zero-centering et bootstrap stationnaire conjoint, mais les analyses secondaires
SOP 02 restaient marquees `DEFERRED_SECONDARY_ANALYSIS`.

### Decision

Remplacer ces marqueurs par des rapports secondaires structures :

- SPA de sensibilite avec studentisation et troncature explicite;
- Romano-Wolf stepdown execute uniquement apres rejet global WRC;
- MCPM bloquee sans schema causal preregistre et recalcul complet fourni par le
  pipeline;
- diagnostic de limite de puissance du WRC lorsque l'univers contient de
  nombreuses candidates mediocres.

### Impact

Le WRC reste l'unique gate confirmatoire primaire. SPA, Romano-Wolf et MCPM ne
peuvent pas ouvrir l'OOS apres un WRC `FAIL` ou `INCONCLUSIVE` et ne creent
aucun nouveau seuil, statut ou ordre de gate.

### Suite

Pour un pipeline reel, fournir un schema MCPM preregistre et un recalcul
signal-position-PnL complet si la MCPM est activee. Ne pas remplacer ce blocage
par une permutation generique du PnL final.
