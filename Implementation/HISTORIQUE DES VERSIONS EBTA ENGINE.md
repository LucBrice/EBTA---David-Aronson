# Historique des versions EBTA Engine

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - HISTORIQUE_IMPLEMENTATION |
| Date de creation | 2026-06-24 |
| Objet | Journaliser les evolutions du dossier `Implementation/` et du futur EBTA Engine Core. |
| Autorite normative | Aucune : l'autorite normative reste dans `Protocole/`. |
| Source documentaire | `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Hook de reprise | `Implementation/Active/HOOK.md` |

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

## 2026-07-20 - Derivation des attestations mecaniques G13/G14

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | SOP 11, SOP 12; Paquet d'execution G13/G14 |
| Fichiers impactes | producer du pilote et tests end-to-end |
| Impact protocole | NONE |
| Verification | 183 tests PASS; Pyrefly 0 erreur; build pilote complet avec G14 INCONCLUSIVE attendu |

### Decision

- deriver la version live et le kill-switch depuis le rapport live fourni ;
- deriver les trois exigences G14 uniquement depuis un mapping de chemins
  explicite, declare dans la forme du package, contenu sous sa racine et present ;
- retourner `INCONCLUSIVE` si la preuve manque et `FAIL` pour un chemin unsafe
  ou un kill-switch explicitement faux ;
- conserver le package courant `VALIDATION_READY` en `FAIL` global cause G14
  `INCONCLUSIVE`, plutot que de maintenir cinq attestations favorables codees en dur.

Les reviewers et approbations humaines restent inchanges et sont delegues au
sous-chantier suivant.

## 2026-07-20 - Chronologie effective avant ouverture OOS

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL |
| Statut | ACCEPTED |
| Source normative | SOP 03, SOP 10, SOP 12, SOP 13; Paquet d'execution EBTA |
| Fichiers impactes | builders pilote/Nautilus, fixture pilote et tests de chronologie |
| Impact protocole | NONE |
| Verification | 182 tests; Pyrefly 0 erreur; pilote minimal PASS; smoke donnees reelles `DENIED` sur `wrc_pass` avec aucun OOS execute |

### Contexte

Le builder Nautilus executait les segments OOS avant que le pilote calcule WRC,
robustesse, scellement, G-BIAS et autorisation. Les timestamps du registre et de
l'acces provenaient en outre de la fixture du pilote.

### Decision

- persister configuration et registre append-only avant le premier run Test ;
- calculer et hasher une fois les preuves pre-OOS, puis les reutiliser dans
  l'assemblage final sans resceller apres OOS ;
- fonder l'autorisation sur une preuve d'execution Test-only non circulaire ;
- retourner `DENIED` sans appel runner OOS ni faux package complet lorsqu'un
  gate pre-OOS manque ;
- journaliser chaque fold immediatement avant son appel OOS avec UTC runtime ou
  horloge fixture aware injectee.

### Impact

L'ordre declare par SOP 10 est maintenant l'ordre reel du chemin de production.
Un refus statistique ou de robustesse conserve seulement les artefacts pre-OOS
honnetes (`config.json`, `registry.jsonl`) et ne consomme plus l'OOS.

## 2026-07-20 - Reproductibilite operationnelle du build Nautilus R7

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE / DOCUMENTATION_CLARIFICATION_NEEDED |
| Statut | ACCEPTED |
| Source normative | SOP 12 ; `Protocole/PAQUET D'EXECUTION EBTA.md` section 3.1 |
| Fichiers impactes | `data/local_ohlcv.py` ; `package_builder/nautilus_research_package.py` ; pilote minimal ; tests R7 ; `adapters/nautilus_env/README.md` |
| Impact protocole | NONE |
| Verification | Tests cibles resolver/package/pilote ; suite runtime complete ; smoke `setup_env.ps1 -VenvRelativePath "Implementation\adapters\nautilus_env\venv" -SkipInstall` ; Pyrefly et audits de cloture du plan R7. |

### Contexte

Le build Nautilus acceptait deja un `data_root` explicite, mais son defaut etait
lie a un chemin Windows local lors de l'import. Son `document_hash` etait un
placeholder litteral et la procedure de recreation du venv n'avait pas de guide
operationnel unique.

### Decision

Le bord du build resout maintenant la precedence argument explicite,
`EBTA_DATA_ROOT`, puis fallback historique. Le pilote expose l'unique projection
pure du document `config.json`; le builder Nautilus retire le champ
auto-referentiel et calcule son SHA-256 sur la serialisation canonique existante.
Le guide du venv conserve le defaut court deja acte et distingue l'override
historique sans modifier les scripts.

### Impact

Une autre machine peut fournir son data root sans modifier le code, le package
porte une empreinte reelle de son document de configuration effectif, et
l'environnement pinne peut etre recree sans ambiguite. Aucun schema, gate, seuil
ou document normatif n'est modifie.

### Suite

Le Lot 2 R5/R6 du chantier mere porte separement la calibration economique et
les stress de robustesse ; ils ne sont pas traites par R7.

## 2026-07-20 - Horodatage automatique du scellement et preuves d'invariants derivees

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` section 6 ; SOP 09A ; SOP 10 ; SOP 12 |
| Fichiers impactes | `Implementation/ebta_engine/procedures/sealing.py`, `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`, `Implementation/ebta_engine/tests/test_procedure_governance.py`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, package pilote regenere |
| Impact protocole | NONE |
| Verification | `test_procedure_governance.py` PASS (11 tests), `test_minimal_pilot_pipeline.py` PASS (9 tests), `test_nautilus_research_package.py` PASS (6 tests), suite runtime PASS (174 tests), build pilote PASS, Pyrefly PASS (`0 errors`) |

### Contexte

Le Lot F de `EPIC_ATTESTATIONS_RESIDUELLES_R3` a identifie quatre preuves
fabriquees dans `invariant_evidence.json` : date de scellement, statuts WRC
locaux, transformations ML et evenements de disponibilite. La decision humaine
du 2026-07-20 impose que les dates de jalons soient capturees automatiquement,
sans saisie humaine ni date choisie par une IA ; une horloge fixe reste admise
uniquement pour une fixture reproductible explicitement identifiee.

### Decision

- `validate_pre_oos_seal()` capture l'heure UTC runtime seulement apres un
  scellement `PASS`; un echec ne produit aucune date ;
- les tests et le pilote injectent une horloge fixe identifiee par
  `sealed_at_source: INJECTED_FIXTURE_CLOCK` ;
- `pre_oos_sealed_at` propage exactement `sealing.json::sealed_at` ;
- les transformations et evenements PIT derivent de `ml_manifest` et
  `data_availability_checks` ;
- le builder recalcule le WRC primaire sur la fenetre Test de chaque fold,
  persiste les rapports sous `wrc.json::local_reports` et mappe les ouvertures
  OOS par `fold_id`; une preuve locale absente reste `INCONCLUSIVE`.

### Impact

Les quatre literals historiques disparaissent du chemin d'assemblage. Le
package pilote et le package Nautilus multi-fold restent valides, mais un fold
sans observations Test locales ne peut plus obtenir un faux WRC local `PASS`.
Aucun validateur, gate, seuil, statut normatif ou document de `Protocole/` ne
change.

### Suite

La generalisation de cette capture automatique a tous les jalons EBTA reste un
chantier transversal distinct. Lot F fournit le patron executable pour le
scellement sans etendre son perimetre aux autres transitions de phase.

## 2026-07-18 - Derivation du gate G8 depuis l'autorisation OOS reelle

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` gate G8 ; SOP 10 |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/ebta_engine/tests/test_nautilus_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/research_package/` |
| Impact protocole | NONE |
| Verification | `test_minimal_pilot_pipeline.py` PASS (7 tests), `test_nautilus_research_package.py` PASS (6 tests), suite runtime PASS (169 tests), build pilote PASS, Pyrefly PASS |

### Contexte

Le chantier `PLAN_CORRECTION_ACCES_OOS_LOT_E`, sous-chantier 2/4 de
`EPIC_ATTESTATIONS_RESIDUELLES_R3`, a corrige le bug ou
`_oos_access_request()` forcait `wrc_pass` a `True`. Le package Nautilus
persistant exposait deja le symptome : WRC `FAIL` mais
`oos_access_decision.status = "AUTHORIZED"`.

### Decision

Le builder pilote transmet maintenant le rapport WRC a
`_oos_access_request()`, qui calcule `wrc_pass` depuis
`wrc["verdict"] == "PASS"`. Les trois champs G8 de `gates.json`
(`oos_access_log`, `opening_authorization`, `single_oos_execution_log`)
derivent du statut reel `oos_access_decision`.

### Impact

- Un WRC `FAIL` produit maintenant un acces OOS `DENIED` et des champs G8
  non passants.
- Le chemin Nautilus production possede un test de contraste WRC FAIL ->
  OOS DENIED.
- Le package exemple minimal est regenere pour remplacer les booleens G8 par
  des verdicts string derives.
- `Implementation/research_packages/nautilus_mvp/` n'est pas regenere dans ce
  lot ; cette regeneration reste reservee a la phase finale du chantier mere.
- Aucun changement de protocole, SOP, `gate_validator.py` ou
  `package_validator.py`.

### Suite

Continuer l'EPIC par le Lot F ou documenter explicitement son report si une
decision humaine est necessaire sur les sources exactes de
`invariant_evidence.json`.

## 2026-07-18 - Derivation des gates residuels Lot D depuis preuves reelles

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` gates G2/G3/G4/G5/G7/G10 ; SOP 02, SOP 03, SOP 05, SOP 06, SOP 08, SOP 09B, SOP 12 |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/examples/minimal_pilot_pipeline/research_package/` |
| Impact protocole | NONE |
| Verification | `test_minimal_pilot_pipeline.py` PASS (6 tests), `test_nautilus_research_package.py` PASS (6 tests), suite runtime PASS (168 tests), build pilote PASS |

### Contexte

Le chantier `PLAN_CORRECTION_REGISTRE_ECONOMIQUE_LOT_D`, sous-chantier 1/4
de `EPIC_ATTESTATIONS_RESIDUELLES_R3`, a traite les champs residuels de
`gates.json` encore codes en `True` pour G2/G3/G4/G5/G7/G10. Le bug G2
principal etait l'appel tautologique
`review_registry_lineage(candidate_ids, candidate_ids)`, qui rendait le
rapport `registry_review` incapable de signaler une candidate de matrice Test
absente du registre.

### Decision

Le builder pilote lit maintenant les candidates enregistrees depuis
`registry.jsonl` deja ecrit sur disque avant `_write_reports()`, puis compare
ces candidates a `candidate_matrix["candidate_ids"]` via
`review_registry_lineage()`. Les champs Lot D de `gates.json` sont derives
des rapports existants (`search_space`, `optimization_log`, `ml_manifest`,
`complexity_selection`, `candidate_matrix`, `wrc`, `robustness`, `economic`)
en verdicts `PASS`/`FAIL`/`INCONCLUSIVE`.

`test_reports` reste une derivation technique minimale de presence/coherence
des rapports Test existants ; aucune nouvelle procedure normative
`test_reports` n'est creee.

### Impact

- `registry_review` peut maintenant echouer si le registre omet une candidate
  de la matrice Test.
- Les champs G2/G3/G4/G5/G7/G10 vises ne sont plus des booleens `True` non
  derives dans le builder pilote.
- Le package exemple minimal est regenere pour refleter les verdicts string.
- `Implementation/research_packages/nautilus_mvp/` n'est pas regenere dans ce
  lot ; cette regeneration reste reservee a la phase finale du chantier mere.
- Aucun changement de protocole, SOP, `gate_validator.py` ou
  `package_validator.py`.

### Suite

Continuer l'EPIC par le Lot E (`PLAN_CORRECTION_ACCES_OOS_LOT_E`) apres
cloture conforme de ce Lot D.

## 2026-07-16 - Propagation du verdict OOS reel vers le gate G9

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 01 sections 3, 4, 7, 8, 10, 13, 15, 20; DN-019 a DN-022 |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_gates.py`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/examples/minimal_pilot_pipeline/research_package/reports/gates.json`, `Implementation/examples/minimal_pilot_pipeline/research_package/manifests/reproducibility_manifest.json`, `Implementation/examples/minimal_pilot_pipeline/research_package/reports/g_bias.json`, `Implementation/examples/minimal_pilot_pipeline/research_package/reports/invariant_evidence.json`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_gates.py` (PASS, 5 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py` (PASS, 5 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` (PASS, 155 tests); `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` (PASS); `.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package` depuis `Implementation/` (termine en ~115 s avec `status: FAIL`, attendu car verdicts reels non PASS) |

### Contexte

Le plan `PLAN_CORRECTION_GATE_STATISTIQUE_OOS_MASQUE` a identifie que
`_write_reports()` calculait deja le rapport `oos.json` via
`oos_confidence_interval()`, mais alimentait les quatre champs du gate G9
(`oos_report`, `concatenated_oos_series`, `oos_bootstrap_report`,
`power_report`) avec des litteraux `True`.

Ce comportement masquait un verdict OOS reel `FAIL`, `INCONCLUSIVE` ou
`NOT_VALIDATED` et permettait au gate G9 de rester vert par attestation. Le
validateur global n'est pas modifie : il exige deja `PASS` exact pour
`PASS`/`FAIL`/`INCONCLUSIVE`, mais traiterait une chaine brute
`NOT_VALIDATED` comme truthy si elle lui etait transmise telle quelle.

### Decision

Ajouter `_g9_gate_value()` au point d'assemblage du package, puis alimenter les
quatre champs G9 avec `oos["statistical_gate"]` normalise :

- `PASS` reste `PASS` ;
- toute autre valeur, y compris `FAIL`, `INCONCLUSIVE`, `NOT_VALIDATED` ou une
  valeur future inconnue, devient `INCONCLUSIVE`.

Le calcul OOS (`procedures/oos_confidence_interval.py`) et l'agregateur de
gates (`validators/gate_validator.py`) restent inchanges. Les artefacts suivis
du package pilote ont ete regeneres par le pipeline pilote apres correction :
`gates.json` porte maintenant `"PASS"` pour les quatre champs G9 parce que la
fixture pilote produit un verdict OOS reel `PASS`, et les hashes derives du
manifeste ont ete actualises.

### Impact

Le package Nautilus M1 courant expose maintenant le verdict OOS reel au gate
G9 : `oos.json::statistical_gate` vaut `FAIL` (`estimate=0.0`,
`lower_95_one_sided=0.0`, `replications=5000`) et les quatre champs G9 de
`gates.json` valent `INCONCLUSIVE`. Ce n'est pas une regression : c'est le
gate qui cesse de masquer un verdict deja calcule.

Le package M1 reste aussi en echec WRC (`gates.json::wrc_status == "FAIL"`),
deja documente dans l'entree de gouvernance precedente. Les deux constats sont
des verdicts EBTA legitimes ; ils ne doivent pas etre forces en `PASS` par une
calibration silencieuse.

### Suite

Ne pas ouvrir l'OOS ni presenter le package Nautilus M1 courant comme un edge
valide tant que les gates statistiques reels ne sont pas verts. Traiter dans un
chantier separe les lots explicitement exclus de ce plan : `power_check.status`
(A2), `execution_report`/`nav_reconciliation` (B), et
`independent_registry_review` (G2).

## 2026-07-16 - Acquittement gouvernance du PASS R4 artefactuel et du FAIL WRC M1

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | SOP 02 (WRC primaire), SOP 08 (NAV et rendements de reference), registre des decisions normatives EBTA |
| Fichiers impactes | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `git show 3bcfe35:Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py` (confirme `_call_float()` sans gestion du mapping `{Currency: Money}`); lecture de `Implementation/research_packages/nautilus_mvp/reports/wrc.json` (verdict `FAIL`, `wrc_pvalue` 0.39492101579684064, `exceedance_count` 1974, `replications` 5000, 11/16 candidats a moyenne negative); entree precedente "2026-07-16 - Stabilisation du build Nautilus M1 et extraction NAV" (suite runtime 152 tests PASS, build Nautilus reel termine avec `status: FAIL` sur WRC primaire reel) |

### Contexte

Le plan R4 cloture le 2026-07-15 au commit `3bcfe35` annoncait un package
Nautilus M1 `PASS` avec `total_orders > 0`. L'archeologie du commit montre
toutefois que `GenericPayloadStrategy.record_nav_snapshot()` utilisait
`_call_float(self.portfolio, "equity", self._venue)`, et que `_call_float()`
convertissait uniquement `float(str(result).split()[0])`. Cette version ne
gerait pas le retour Nautilus sous forme de mapping `{Currency: Money}`.

Le correctif ulterieur `ebff49d` a ajoute cette gestion, stabilise le build M1
reel et revele une NAV exploitable. Le package courant ne reste donc pas en
`FAIL` a cause d'un timeout ni d'une absence d'ordres : il echoue parce que le
WRC primaire reel ne rejette pas l'hypothese nulle sur la famille M1 courante.

### Decision

Acter que le `PASS` R4 du commit `3bcfe35` etait un artefact de NAV
degenerescente, et non une preuve d'edge. L'archive R4 et son `closure_reason`
ne sont pas reecrits : la correction de narration est append-only dans cet
historique runtime.

Acter aussi que le `FAIL` WRC primaire courant du package Nautilus M1 est un
verdict EBTA legitime : `wrc.json::verdict` vaut `FAIL`, la p-value WRC vaut
environ 0.395, 1974 tirages sur 5000 excedent la statistique observee, et 11
des 16 candidats ont une moyenne observee negative. Conformement a SOP 02, ce
resultat signifie que la famille M1 testee ne demontre pas d'edge sur ce
segment ; il ne doit pas etre force en `PASS`, masque, ni contourne par une
calibration silencieuse.

### Impact

Le chantier de documentation ne modifie aucun calcul, aucun seuil, aucun statut
EBTA, et aucun fichier `Protocole/`. Il ferme seulement le trou d'audit entre
l'archive R4, qui reste une trace historique, et l'etat runtime courant, qui
produit un `FAIL` WRC primaire honnete sur des rendements non degenerescents.

La lecon operationnelle est que `total_orders > 0` etait necessaire mais
insuffisant pour prouver la validite R4 : une preuve "NAV varie" et "rendements
non nuls" etait requise. Cette preuve existe maintenant dans la suite de tests
issue de `ebff49d`, notamment le test dedie au segment M1 qui verifie une NAV
reelle plutot qu'un faux `NO_M1`.

### Suite

Clore `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` sur ses exit criteria formels
de propagation du verdict G5, en documentant que le package Nautilus M1 reste
`FAIL` pour une raison exogene a G5 : le WRC primaire reel. Ne pas ouvrir de
chantier de recherche sur la famille M1 dans ce plan.

## 2026-07-16 - Stabilisation du build Nautilus M1 et extraction NAV

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | ADAPTER_MAPPING / IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 02 (WRC primaire), SOP 08 (NAV et rendements de reference), SOP 09B (execution/fills) |
| Fichiers impactes | `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`, `Implementation/ebta_engine/package_builder/nautilus_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase5_run_segment.py` (PASS, 4 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py` (PASS, 4 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_procedure_wrc.py` (PASS, 6 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` (PASS, 152 tests); `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` (PASS); `pyrefly check` sur les fichiers touches (0 errors); build Nautilus reel via venv termine en ~97 s mais retourne `status: FAIL` car le WRC primaire reel du package M1 est `FAIL` (`wrc_pvalue` ~= 0.395), non a cause d'un timeout |

### Contexte

La cloture du plan G5 a revele un blocage hors perimetre initial : le build
Nautilus reel depassait le timeout subprocess sur des segments M1 de 1440
barres, puis la construction des rapports devenait trop couteuse avec les
diagnostics secondaires WRC sur des series M1 longues.

### Decision

Precalculer une seule fois les decisions causales du payload pour chaque
segment et laisser `GenericPayloadStrategy` soumettre les ordres Nautilus aux
timestamps M1 correspondants. Conserver l'isolation subprocess par segment mais
executer ces subprocess sequentiellement sous Windows. Corriger l'extraction de
`portfolio.equity(venue)` lorsque Nautilus retourne un mapping `{Currency:
Money}` afin que la NAV ne soit plus convertie en `0.0`. Rendre l'execution des
diagnostics secondaires WRC pilotable par `statistical_plan` et la declarer
`NOT_RUN` pour le package Nautilus M1 long ; le WRC primaire conserve ses 5000
replications.

### Impact

Le build Nautilus ne reste plus bloque et les fills produisent des rendements
non nuls dans `SimulationResult`. Le package courant reste toutefois un echec
EBTA legitime : le WRC primaire reel est `FAIL`, donc G4 est
`INCONCLUSIVE`/non-PASS et `validate_package_dir()` retourne `FAIL`.

### Suite

Ne pas forcer `wrc_status` a `PASS`. Une decision humaine ou un chantier
dedie est requis pour traiter le fait que le package Nautilus M1 courant ne
passe pas le WRC primaire.

## 2026-07-16 - Propagation du verdict de robustesse pre-OOS reel vers G5

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 05 (robustesse pre-OOS, DN-030) |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/ebta_engine/tests/test_nautilus_research_package.py` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py` (PASS, 4 tests); `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` (PASS, 152 tests apres stabilisation Nautilus M1); `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` (PASS); `python -m json.tool .ai\checkpoint.json` (PASS); `python -m json.tool Implementation\Active\tracking.json` (PASS); schemas `.ai/checkpoint.json` + `Implementation/Active/tracking.json` (PASS); `pyrefly check` sur les fichiers Python touches (0 errors); `git diff --check -- .ai Implementation Protocole` (PASS, warnings CRLF uniquement); build Nautilus reel via venv termine mais retourne `status: FAIL` sur WRC primaire reel du package M1, hors champ G5 |

### Contexte

Le rapport de robustesse pre-OOS etait deja calcule par
`robustness_verdict()`, puis reutilise honnetement par `robustness.json` et
`incubation_gate.json`. En revanche, `gates.json` continuait a fixer
`pre_oos_robustness_verdict` a `PASS`, ce qui pouvait masquer un echec reel du
gate G5.

### Decision

Faire circuler `procedure_reports["robustness"]["status"]` vers
`gates.json::pre_oos_robustness_verdict`, sans modifier SOP 05, les seuils de
robustesse, les validateurs, ni les calculateurs `procedures/` et `risk/`.
Ajouter une preuve de non-regression sur le chemin
`build_nautilus_research_package()` avec un runner synthetique qui force un
scenario bloquant sous `minimum_mean_return`.

### Impact

G5 reflete maintenant le verdict de robustesse pre-OOS deja calcule. Aucun
nouveau statut, seuil, gate ou ordre de processus EBTA n'est introduit.

### Suite

Les sujets de couverture du catalogue preregistre DN-030 et de realisme des
scenarios de robustesse restent hors perimetre de ce correctif.

## 2026-07-15 - Statut global de package sensible aux gates reels en echec

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | Protocole/PAQUET D'EXECUTION EBTA.md sections 2, 3, 5, 6; SOP 02; SOP 05; SOP 08; SOP 11 |
| Fichiers impactes | `Implementation/ebta_engine/validators/gate_validator.py`, `Implementation/ebta_engine/validators/package_validator.py`, `Implementation/ebta_engine/fixtures/valid_minimal/reports/incubation_gate.json`, `Implementation/ebta_engine/tests/test_gates.py`, `Implementation/ebta_engine/tests/test_package_validator.py`, `Implementation/ebta_engine/tests/test_nautilus_research_package.py` |
| Impact protocole | NONE |
| Verification | `Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check ... --output-format min-text`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_gates.py`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_package_validator.py`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` |

### Contexte

Le plan `PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE` corrigeait le
risque R3 "preuve vs attestation" : les rapports individuels pouvaient deja
porter un WRC, un gate economique ou une incubation en echec, tandis que le
statut global du package restait `PASS` parce que les validateurs aval lisaient
la presence ou la verite Python des champs plutot que leur valeur.

### Decision

Durcir la lecture des validateurs sans modifier `Protocole/` :

- `validate_gates()` traite les valeurs de verdict connues
  `PASS`/`FAIL`/`INCONCLUSIVE` comme satisfaites uniquement si elles valent
  exactement `PASS` ;
- `validate_package_dir()` requiert `reports/incubation_gate.json` et fait
  echouer le package si `incubation_gate.status` ou `economic.global_status`
  est present et different de `PASS` ;
- la fixture minimale et les tests prouvent les cas `FAIL` et
  `REJECTED_ECONOMIC`, ainsi que les deux bascules de statut global sur le
  chemin `build_nautilus_research_package()`.

### Impact

Le statut global du package redevient subordonne aux gates EBTA deja calcules.
Aucun seuil, ordre de gate, statut EBTA ou SOP n'est modifie. Les procedures,
le protocole, la gouvernance, les manifests et les adaptateurs restent hors
perimetre.

### Suite

Traiter dans un plan separe le defaut de contenu du gate robustesse deja
documente : `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
fige encore `pre_oos_robustness_verdict` a `PASS` au lieu d'appeler le calcul
runtime existant.

## 2026-07-15 - Propagation du verdict WRC reel vers gates economique et incubation

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | SOP 02 (WRC), SOP 08 (gate economique), SOP 11 (incubation) |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`, `Implementation/ebta_engine/package_builder/nautilus_research_package.py`, `Implementation/ebta_engine/tests/test_nautilus_research_package.py` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` (PASS, 144 tests); `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` (PASS); `Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check ... --output-format min-text` (0 errors) |

### Contexte

Le rapport WRC etait calcule dans `_procedure_reports()`, mais son verdict
etait masque ensuite par un `statistical_status` fixe a `PASS` dans le gate
economique et le gate d'incubation.

### Decision

Faire circuler `wrc["verdict"]` vers `economic_gate_report()` et
`incubation_gate()`, retirer le `PASS` mort de la fixture pilote, et marquer
dans le builder Nautilus que le statut statistique initial n'est qu'un
placeholder ecrase par l'assemblage pilote.

### Impact

Les rapports `economic.json` et `incubation_gate.json` peuvent maintenant
refleter un WRC `FAIL` reel. Le `status` global de `validate_package_dir()`
reste volontairement hors perimetre de ce correctif, conformement au plan actif
qui reporte la correction des validateurs a un chantier separe.

### Suite

Traiter separement `validators/gate_validator.py` et
`validators/package_validator.py` si l'humain autorise le chantier plus large
sur le verdict global du package.

## 2026-07-15 - R4 donnees M1 reelles et package Nautilus production

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; SOP 04 ; SOP 08 ; plan `.ai/backlog/mainline/PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION.md` |
| Fichiers impactes | `Implementation/ebta_engine/package_builder/nautilus_research_package.py`, `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `Implementation/ebta_engine/strategies/incremental/payload_f.py`, `Implementation/ebta_engine/strategies/incremental/payload_ghi.py`, tests R2/R4 |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 143 tests ; Pyrefly bug-hunter -> 0 erreurs ; `.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package` -> PASS ; `validate_package_dir(Path('research_packages/nautilus_mvp'))` -> PASS ; `reports/execution.json` -> `total_orders=29`, `oos_total_orders=1` |

### Contexte

Le package Nautilus de production consommait encore un index quotidien au lieu
des barres M1 reelles. Les strategies G/H/I appliquaient aussi le filtre de
biais directionnel meme lorsque le candidate space demandait
`bias_filter="none"`.

### Decision

Conserver un index journalier uniquement pour les bornes de walk-forward, puis
trancher les segments train/test/OOS dans les barres M1 brutes. Mutualiser le
filtre MTF de F et ne l'appliquer dans G/H/I que lorsque le payload le demande.
Corriger l'extraction des positions Nautilus ouvertes en traitant
`avg_px_close=None` comme valeur manquante couverte par le `default` existant.

### Impact

Le runtime execute maintenant les segments de production a resolution M1 et le
package regenere prouve que le `PASS` n'est plus un package inerte sans ordre.
Le parallelisme `subprocess` du builder ne change pas la semantique des
segments ; il rend la validation R4 praticable apres timeout du mode sequentiel.
Aucun seuil, statut, ordre de gate ou contrat normatif n'est modifie.

### Suite

Traiter dans des chantiers separes une fenetre de donnees plus longue,
`warmup_bars` inter-fold, et une eventuelle migration du candidate space vers
les codes E/F/G/H/I purs.

## 2026-07-13 - R1 moteur de signaux reel et R2 extraction Nautilus reelle

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md` |
| Fichiers impactes | `Implementation/ebta_engine/data/resample.py`, `Implementation/ebta_engine/strategies/signals/`, `Implementation/ebta_engine/strategies/registry.py`, `Implementation/ebta_engine/strategies/incremental/`, `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`, `Implementation/ebta_engine/adapters/nautilus_mapping.py`, tests R1/R2, fixture golden-case, `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 139 tests ; `.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package` -> PASS ; `validate_package_dir(Path('research_packages/nautilus_mvp'))` -> PASS ; hardcoded checks `OrderSide.BUY`/`total_costs=0.0` -> False |

### Contexte

Le plan R1/R2 corrige deux limites bloquantes du pivot Nautilus : le bridge
achetait encore de facon deterministe sans moteur de signaux reel, et
`extract_simulation_result()` reconstruisait les series de performance a la
main avec `total_costs` nul.

### Decision

Ajouter un resampling causal multi-timeframe, un oracle vectorise de parite
issu du port lecture seule de BACKTRADER, un registry de strategies
incrementales, et des state machines E/F/G/H/I bar-by-bar. Refactoriser
`GenericPayloadStrategy` pour deleguer au registry, souscrire plusieurs
`BarType`, emettre des ordres BUY/SELL depuis la state machine, et capturer les
snapshots NAV uniquement sur M1.

Recrire l'extraction R2 pour lire les snapshots NAV, les commissions des fills
et les positions depuis les rapports Nautilus. Le golden-case daily est
recalibre en cas `no_m1_signal`, sans faux trade.

### Impact

Nautilus reste une couche d'execution/simulation sous frontiere d'adapter. Les
procedures, validateurs, manifests, governance et contrats EBTA restent
inchanges. Le package Nautilus reconstruit reste `PASS`.

### Suite

Le branchement production intraday reste hors scope de ce chantier : R4 doit
retirer le `_daily_sample` et fournir de vraies barres M1 avant qu'une recherche
reelle puisse consommer le moteur de signaux sans `no_m1_signal`.

## 2026-07-09 - Nautilus Phase 6 cutover et retrait natif

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / ADAPTER_MAPPING |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 6 ; decision E5 |
| Fichiers impactes | `Implementation/ebta_engine/package_builder/nautilus_research_package.py`, retrait `backtest/native_engine.py`, `risk/sizing.py`, `features/causal_signals.py`, `trading_signals/decision_frame.py`, `metrics/performance.py`, `package_builder/native_research_package.py`, tests et docs de traceabilite |
| Impact protocole | NONE |
| Verification | `pre-nautilus-cutover` tag cree sur le commit pre-retrait ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 106 tests apres retrait ; `.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package` -> PASS ; grep imports natifs -> aucune reference active |

### Contexte

Phase 6 devait prouver un paquet Nautilus complet avant tout retrait du moteur
natif, poser un point de retour, puis supprimer le cluster natif dans un commit
dedie et reversible.

### Decision

Ajouter `nautilus_research_package.py`, produire
`Implementation/research_packages/nautilus_mvp` avec statut `PASS`, creer le
tag annote `pre-nautilus-cutover`, puis retirer le cluster natif :

- `backtest/native_engine.py` ;
- `risk/sizing.py` ;
- `features/causal_signals.py` ;
- `trading_signals/decision_frame.py` ;
- `metrics/performance.py` ;
- `package_builder/native_research_package.py` ;
- le test MVP natif associe.

Les notebooks, README, carte et matrice de traceabilite pointent maintenant vers
le builder Nautilus actif.

### Impact

NautilusTrader devient le moteur de simulation actif sous frontiere d'adapter.
Le loader local OHLCV et les contrats EBTA restent conserves. BACKTRADER reste
reference historique en lecture seule.

### Suite

Le chantier `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` est complet du
point de vue runtime. Toute evolution ulterieure doit partir du package
Nautilus PASS et non restaurer le cluster natif.

## 2026-07-09 - Nautilus Phase 5 run_segment et extraction

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 5 |
| Fichiers impactes | `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py`, `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`, cockpit actif |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase5_run_segment.py` -> PASS 3 tests ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 111 tests |

### Contexte

Phase 5 devait produire des `SimulationResult` fiables depuis Nautilus et les
alimenter dans les procedures EBTA sans changer leurs signatures.

### Decision

Ajouter `run_segment()`, `extract_simulation_result()` et
`run_multifold_segments()`. Le golden case Nautilus reproduit le resultat
attendu, le cas `NO_MODEL` retourne une NAV plate, et l'orchestration multi-fold
ne transmet pas de metadonnee Train/Test/OOS au runner.

### Impact

Les procedures EBTA continuent de consommer `SimulationResult` via
`detrending_inputs()` et `economic_gate_evidence()`. Nautilus reste le moteur de
simulation, pas une autorite de verdict.

### Suite

Executer `NAUTILUS_PHASE_6_CUTOVER` : produire un `research_package` Nautilus
PASS, puis retirer le cluster moteur natif uniquement apres point de retour
reversible.

## 2026-07-09 - Nautilus Phase 4 strategie generique et couts

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 4 |
| Fichiers impactes | `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`, `Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py`, `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`, cockpit actif |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase4_strategy_costs.py` -> PASS 2 tests ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 108 tests |

### Contexte

Phase 4 devait mapper les couts scelles EBTA vers les modeles Nautilus et
introduire une seule classe de strategie pour toute la famille de candidates.

### Decision

Ajouter `map_cost_model_to_venue()` qui transmet explicitement a
`BacktestEngine.add_venue()` les modeles declares : `FillModel`,
`MakerTakerFeeModel` ou frais fixes supportes, `LatencyModel`,
`LeveragedMarginModel`, `OmsType.HEDGING` et `AccountType.MARGIN`.

Ajouter `GenericPayloadStrategyConfig` et `GenericPayloadStrategy`. La classe
parse `StrategyPayload.from_dict()` et reste unique pour toutes les candidates ;
les variations passent par `StrategyConfig`.

### Impact

Le runtime ne depend pas d'un `FillModel`, `FeeModel` ou `LatencyModel`
implicite de Nautilus. La portabilite recherche-vers-live est preservee par une
classe de strategie generique, sans classe Python par candidate.

### Suite

Executer `NAUTILUS_PHASE_5_N4_N5_MULTIFOLD` : `run_segment()`,
`extract_simulation_result()` et orchestration multi-fold compatible avec les
procedures EBTA existantes.

## 2026-07-09 - Nautilus Phase 3 ingestion et instruments

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 3 |
| Fichiers impactes | `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `Implementation/ebta_engine/tests/test_nautilus_instrument_nasdaq.py`, `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`, cockpit actif |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_instrument_nasdaq.py` -> PASS 2 tests ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 106 tests |

### Contexte

Phase 3 devait verifier la construction effective des instruments NASDAQ et
XAUUSD dans NautilusTrader et convertir les barres EBTA en barres Nautilus sans
perte de precision ni fuite temporelle.

### Decision

Ajouter `nautilus_mapping.py` avec imports Nautilus paresseux, construire les
instruments tradables via `Cfd` lorsque l'actif EBTA est un indice/commodity
CFD, et convertir les `OhlcvBar` en `Bar` Nautilus via `BarDataWrangler`.

`NASDAQ.SIM` est verifie comme `Cfd` sous-jacent `AssetClass.INDEX`.
`XAUUSD.SIM` est verifie comme `Cfd` sous-jacent `AssetClass.COMMODITY`.
Le mapping de timestamp utilise `ts_init_delta` afin que `ts_init` represente
la cloture de la barre lorsque le timestamp source represente l'ouverture.

### Impact

La suite EBTA reste importable sans Nautilus dans le Python systeme. Les objets
Nautilus reels sont construits uniquement dans l'adapter et verifies par la venv
dediee.

### Suite

Executer `NAUTILUS_PHASE_4_N2_N3_STRATEGY_COSTS` : mapper les couts scelles
vers le venue et introduire une strategie generique unique pour toutes les
candidates.

## 2026-07-09 - Nautilus Phase 2 spike deterministe

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | ADAPTER_MAPPING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 2 ; decisions E4, E6, E11 |
| Fichiers impactes | `Implementation/adapters/nautilus_env/setup_env.ps1`, `requirements.txt`, `run_golden_case.py`, `PHASE2_SPIKE_MEASUREMENT.md`, `NAUTILUS_API_NOTES.md`, fixture et tests `nautilus_golden_case`, cockpit actif |
| Impact protocole | NONE |
| Verification | `.\Implementation\adapters\nautilus_env\setup_env.ps1 -VenvRelativePath "Implementation\adapters\nautilus_env\venv" -SkipInstall` -> PASS ; `.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe .\Implementation\adapters\nautilus_env\run_golden_case.py` -> PASS ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase2_golden_case.py` -> PASS 3 tests |

### Contexte

Phase 2 devait prouver que NautilusTrader tourne reellement dans l'environnement
EBTA et peut produire un `SimulationResult` coherent avant d'investir dans les
briques completes N1 a N5.

### Decision

Versionner le script de setup `nautilus_trader==1.230.0`, creer un cas jouet
deterministe `GOLDEN.SIM`, construire explicitement un `CurrencyPair` a frais
nuls, executer une strategie minimale dans `BacktestEngine`, puis comparer la
sortie a un `expected_result()` stdlib calcule a la main.

Le spike documente aussi la mesure `K x (M+1)` : le pilote courant declare
`K=1`, la decision E11 fixe `M=16`, donc 17 runs. Le run isole mesure
2.22464 s, soit environ 37.82 s en extrapolation sequentielle sans reutilisation
d'etat ni parallelisation.

### Impact

Nautilus reste confine a `Implementation/adapters/nautilus_env/` pour le spike.
Les verdicts EBTA restent produits par les contrats, procedures et validateurs
EBTA ; les rapports et metriques Nautilus ne deviennent pas une autorite.

### Suite

Executer `NAUTILUS_PHASE_3_N1_DATA` : verifier les classes d'instruments
NASDAQ/XAUUSD, puis implementer `map_ohlcv_to_bars()` et `build_instrument()`
sans perte de precision ni lookahead.

## 2026-07-09 - Nautilus Phase 1 contrats et schemas

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | CONTRACT_ENCODING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` Phase 1 ; decisions E1, E2, E3, E10, E11, E12 |
| Fichiers impactes | `Implementation/ebta_engine/strategies/contracts.py`, `Implementation/ebta_engine/strategies/payloads.py`, `Implementation/ebta_engine/strategies/payload_factory.py`, `Implementation/ebta_engine/migrations/schema_migrations.py`, `Implementation/ebta_engine/schema_validation.py`, schemas et fixtures 1.1.0, tests Phase 1, pilote minimal |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase1_contracts.py` -> PASS 8 tests ; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 101 tests ; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` -> PASS |

### Contexte

La migration Nautilus exige un contrat EBTA stable avant tout import de
`nautilus_trader`. Phase 1 devait donc creer les types stdlib, rendre les
payloads reconstructibles, migrer les schemas et generer les familles de
candidates sans toucher aux procedures, validateurs, manifestes ou gates.

### Decision

Ajouter les contrats `Candidate`, `CostModel`, `InstrumentConfig`,
`SimulationResult` et `SegmentSimulator`, migrer `config` et `strategy_payload`
vers `1.1.0`, structurer les criteres d'entree/sortie, et introduire
`payload_factory.py` pour la grille `bias_filter x session x asset`. Un fake
`SegmentSimulator` prouve que les sorties peuvent alimenter `detrending.py` et
`economic_gate.py` sans changement de signature.

### Impact

Le runtime possede maintenant une frontiere de simulation claire pour Phase 2.
Aucun verdict EBTA n'est delegue a Nautilus et aucun import Nautilus n'est
introduit dans cette phase.

### Suite

Executer `NAUTILUS_PHASE_2_SPIKE` : environnement reproductible
`nautilus_trader==1.230.0`, cas jouet deterministe, puis premier
`SimulationResult` reel via adapter.

## 2026-07-02 - Moteur natif EBTA MVP jusqu'a Phase 8

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.x |
| Type | IMPLEMENTATION_DETAIL / ADAPTER_MAPPING |
| Statut | ACCEPTED |
| Source normative | `Protocole/` gele en EBTA-DOC-1.1 ; plan `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF.md` |
| Fichiers impactes | `Implementation/ebta_engine/data/`, `strategies/`, `features/`, `trading_signals/`, `backtest/`, `risk/`, `metrics/`, `package_builder/`, `schemas/strategy_payload.schema.json`, `Implementation/NATIVE_ENGINE_PROCEDURE_MAPPING.md`, `Implementation/PAYLOAD_DECOMPOSITION_E_TO_I.md`, `Implementation/BACKTRADER_DATA_SOURCE_AUDIT.md`, `Implementation/notebooks/` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` -> PASS 93 tests ; `python -m ebta_engine.package_builder.native_research_package` -> package PASS |

### Contexte

Le mainline BACKTRADER externe est remplace par un moteur EBTA natif. BACKTRADER
reste une reference lue en lecture seule apres gouvernance locale ; il n'est pas
une dependance runtime.

### Decision

Implementation fournit une verticale MVP native : chargement CSV local
XAUUSD/NASDAQ, decomposition E-I en `StrategyPayload`, signaux causaux simples,
backtest deterministe, generation d'un `research_package` valide, et notebooks
Jupyter d'orchestration.

### Impact

Le package reel est genere dans `Implementation/research_packages/native_mvp`
et reste ignore par git. Les validateurs EBTA existants restent l'autorite de
verdict ; aucun fichier `Protocole/` n'est modifie.

### Suite

Ne pas etendre le MVP vers une recherche reelle avant de trancher le gap
licence/vendor des donnees locales et de conserver les validations `PASS`.

## 2026-07-01 - Gate runtime G-BIAS complet

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING / GATE_CHECK / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md`; `Protocole/PAQUET D'EXECUTION EBTA.md` artefact `G-BIAS`; DN-042 a DN-047 |
| Fichiers impactes | `Implementation/ebta_engine/governance/`, `Implementation/ebta_engine/validators/package_validator.py`, `Implementation/ebta_engine/procedures/oos_access.py`, `Implementation/ebta_engine/procedures/robustness.py`, `Implementation/examples/minimal_pilot_pipeline/`, `Implementation/ebta_engine/tests/`, `Implementation/TRACEABILITY_MATRIX.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 87 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS |

### Contexte

Le socle initial avait expose le registre `BIAS-*` et le logger d'incidents,
mais le gate transversal `G-BIAS` restait a brancher. EBTA-DOC-1.1 exige que la
gouvernance des biais puisse bloquer l'ouverture OOS et la validation finale si
les preuves sont manquantes, modifiees ou contaminees.

### Decision

Ajouter le lot runtime complet :

- schéma de dérogation méthodologique ;
- checkers `registry_completeness`, `candidate_family`, `metric_lock` et
  `robustness_gate` ;
- `oos_access_guard` avec statut `BURNED` en cas d'accès OOS non autorisé ;
- `bias_gate` agregant les preuves en `PASS`, `FAIL`, `INCONCLUSIVE` ou
  `BURNED` ;
- intégration compatible dans `package_validator` : un rapport
  `reports/g_bias.json` présent ou explicitement enforcé doit etre `PASS` ;
- pilote minimal produisant `reports/g_bias.json` et exigeant `bias_gate_pass`
  avant l'autorisation OOS.

### Impact

Le runtime encode des regles deja presentes dans SOP 13 et ne cree pas de source
normative concurrente. Les anciens paquets restent validables tant que
`G-BIAS` n'est pas explicitement enforcé et qu'aucun rapport `g_bias.json`
non-PASS n'est fourni.

### Suite

Le chantier annexe `PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA` est complet.
La prochaine etape reste le mainline `STEP_3_BACKTRADER_INTEGRATION`, apres
lecture de la gouvernance locale BACKTRADER.

## 2026-07-01 - Socle runtime G-BIAS incidents et registre de biais

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md`; `Protocole/BIAS_RISK_REGISTER.md`; `Protocole/PAQUET D'EXECUTION EBTA.md` section 3.4; DN-042 a DN-046 |
| Fichiers impactes | `Implementation/ebta_engine/governance/`, `Implementation/ebta_engine/tests/test_governance_bias.py`, `Implementation/ebta_engine/__init__.py`, `Implementation/TRACEABILITY_MATRIX.md` |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_governance_bias.py` |

### Contexte

Le lot documentaire `EBTA-DOC-1.1` a cree SOP 13, le registre des risques de
biais, les templates d'incident et de derogation, ainsi que le gate transversal
`G-BIAS`. Le runtime devait commencer l'encodage sans creer de norme
concurrente.

### Decision

Ajouter un premier socle executable :

- `governance/bias_risk_schema.json` encode le format machine d'un risque de
  biais ;
- `governance/incident_schema.json` encode le format minimal d'un incident de
  biais ;
- `governance/bias_registry.py` expose les 20 categories `BIAS-001` a
  `BIAS-020` derivees de `BIAS_RISK_REGISTER.md` ;
- `governance/incident_logger.py` journalise les incidents en JSONL append-only
  et permet le chargement/filtrage des incidents ouverts ;
- `SUPPORTED_PROTOCOL_VERSIONS` accepte maintenant `EBTA-DOC-1.1`.

### Impact

Le lot encode seulement les artefacts documentaires deja valides. Il ne branche
pas encore le gate `G-BIAS` dans `package_validator`, ne remplace pas les gates
G0 a G14 et ne modifie pas BACKTRADER.

### Suite

Implementer les checkers pre-OOS (`registry_completeness_checker`,
`candidate_family_checker`, `metric_lock_checker`, `robustness_gate_checker`),
puis `oos_access_guard.py` et `bias_gate.py`, avec tests de non-divergence apres
chaque lot.

## 2026-06-29 - Encodage runtime de strategie x actif

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | CONTRACT_ENCODING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | Clarification documentaire `strategie x actif` dans `Protocole/PROTOCOLE EBTA.md`, SOP 03, SOP 08, SOP 09A |
| Fichiers impactes | `procedures/search_space.py`, `procedures/candidate_matrix.py`, `validators/invariant_validator.py`, `schema_validation.py`, schemas config/G1, pipeline pilote, tests |
| Impact protocole | NONE |
| Verification | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `git diff --check -- Implementation Protocole .ai AGENTS.md .agents` |

### Contexte

Le protocole explicite maintenant que, lorsque l'actif est selectionnable, la
famille de recherche porte sur des couples `strategie x actif`. Le runtime
devait donc rendre visible cet axe et refuser une WRC qui ne couvre pas la
famille complete des couples evalues.

### Decision

Encoder l'actif comme axe de candidates lorsque le processus evalue des couples
`strategie x actif` :

- `search_space` expose `asset_universe`, `asset_selection_axis`,
  `asset_candidate_count` et `candidate_asset_map` ;
- `candidate_matrix` rejette une matrice qui omet un actif declare ou un mapping
  candidat-actif ;
- `INV-017` verifie que la famille WRC couvre tous les couples applicables ;
- la fixture pilote devient multi-actifs (`EURUSD`, `XAUUSD`) avec 8 candidates ;
- les schemas config et G1 acceptent les metadonnees d'univers d'actifs.

### Impact

Cette evolution ne cree pas de nouveau gate ou seuil. Elle rend executable la
regle deja clarifiee dans le protocole : si l'actif est selectionnable, la WRC
doit couvrir la famille complete des couples `strategie x actif`.

### Suite

La reprise BACKTRADER reste en attente. Avant toute integration externe, mapper
ses sorties vers ce contrat runtime sans transformer une convention BACKTRADER
en norme EBTA.

## 2026-06-27 - Cockpit actif Implementation/Active pour hook et tracking

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | Gouvernance runtime; `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` |
| Fichiers impactes | `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`, `.ai/current_plan.md`, `.ai/checkpoint.json`, `AGENTS.md`, `Implementation/0-CARTE_DU_CODE_EBTA.md`, `Implementation/ARCHIVE_INVENTORY_2026-06-26.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`, `.agents/skills/EBTA_Protocol_Guardian/SKILL.md`, `Protocole/PROTOCOLE EBTA.md`, `Protocole/HISTORIQUE DES VERSIONS EBTA.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool .ai\checkpoint.json` PASS; `python -m json.tool Implementation\Active\tracking.json` PASS; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 52 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS - package status PASS; `git diff --check -- Implementation Protocole .ai AGENTS.md .agents` PASS; recherche anciens chemins PASS - aucun match |

### Contexte

Le hook actif et son JSON de suivi etaient places a la racine de
`Implementation/`, au milieu des cartes, guides, historiques et fichiers de
contrat. Cela rendait la reprise inconfortable et risquait de faire traiter un
ancien hook comme actif.

### Decision

Créer un cockpit stable :

```text
Implementation/Active/HOOK.md
Implementation/Active/tracking.json
```

`.ai/checkpoint.json` reste le pointeur de relais multi-IA et declare ces deux
chemins dans `active_paths`. `AGENTS.md` ne fige pas le nom du hook : il impose
de lire les chemins actifs declares par `.ai/checkpoint.json`.

### Impact

Le changement est organisationnel. Il ne modifie aucun gate, statut, seuil,
verdict ou ordre methodologique EBTA. `Protocole/` reste l'autorite normative et
`Implementation/Active/` devient seulement le cockpit de travail courant.

### Suite

Pour chaque nouveau lot, ecraser `Implementation/Active/HOOK.md` et
`Implementation/Active/tracking.json` ou mettre a jour `active_paths` si le
lot exige d'autres chemins. Archiver les anciens contenus dans
`Implementation/Archives/` lorsque leur lot est termine.

---

## 2026-06-27 - STEP_2 : Pipeline pilote local termine

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / TEST_FIXTURE / GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 1, 2, 3, 5, 6; SOP 01, SOP 02, SOP 03, SOP 04, SOP 05, SOP 06, SOP 07, SOP 08, SOP 09A, SOP 09B, SOP 10, SOP 11, SOP 12 |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`, `Implementation/examples/minimal_pilot_pipeline/inputs/package_shape.json`, `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/research_package/`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/Active/tracking.json`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\Active\tracking.json` PASS; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 52 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS; `git diff --check -- Implementation Protocole` PASS avec avertissements CRLF/LF uniquement |

### Contexte

`STEP_2_T1` avait rendu explicites les inputs pilotes et la shape du
`research_package/`. Les sous-taches restantes demandaient de connecter les
modules de procedure aux artefacts, de valider le paquet genere avec
`validate_package_dir()` et d'ajouter des tests limites au comportement pilote.

### Decision

Clore `STEP_2` comme pipeline pilote local input-driven :

- le builder lit `pilot_inputs.json` et `package_shape.json` ;
- les rapports de selection, WRC, OOS, robustesse, economie, folds, lineage,
  detrending, sealing, acces OOS, monitoring, incubation, lifecycle et
  reproduction validation sont produits via les modules existants quand ils
  existent ;
- `validate_package_dir()` reste le gate d'acceptation du paquet genere ;
- les tests ciblent le paquet `PASS`, les rapports procedures manifestes, le
  rejet d'une shape invalide et l'echec d'un drift de replications OOS.

### Impact

`Implementation/` avance comme traduction executable du protocole gele. Aucune
modification de `Protocole/` n'est faite, aucun seuil/statut/gate EBTA nouveau
n'est cree, et BACKTRADER reste non modifie.

### Suite

La prochaine etape du plan actif est `STEP_3_BACKTRADER_INTEGRATION`, a ne
demarrer qu'apres lecture de la gouvernance locale BACKTRADER et en gardant
EBTA comme autorite de contrat.

---

## 2026-06-27 - STEP_2_T1 : Contrat d'inputs et shape du pipeline pilote

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | IMPLEMENTATION_DETAIL / CONTRACT_ENCODING / TEST_FIXTURE |
| Statut | ACCEPTED |
| Source normative | `Protocole/PAQUET D'EXECUTION EBTA.md` sections 1, 2, 3, 5, 6; SOP 12; Template configuration |
| Fichiers impactes | `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`, `Implementation/examples/minimal_pilot_pipeline/inputs/package_shape.json`, `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`, `Implementation/examples/minimal_pilot_pipeline/README.md`, `Implementation/ebta_engine/schemas/config.schema.json`, `Implementation/ebta_engine/fixtures/valid_minimal/config.json`, `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`, `Implementation/Active/tracking.json`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\examples\minimal_pilot_pipeline\inputs\pilot_inputs.json`; `python -m json.tool Implementation\examples\minimal_pilot_pipeline\inputs\package_shape.json`; `python -m json.tool Implementation\ebta_engine\schemas\config.schema.json`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py` PASS; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_schemas.py` PASS; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 50 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS; `git diff --check -- Implementation Protocole` PASS avec avertissements CRLF/LF uniquement |

### Contexte

`STEP_2_T0` avait clos les angles morts d'exhaustivite et reporte le
durcissement complet de `config.schema.json` a `STEP_2_T1`. Le pipeline pilote
minimal produisait deja un paquet valide, mais son contrat d'entree et sa forme
de sortie restaient implicites dans le script.

### Decision

Ajouter deux contrats locaux et explicites pour le pilote :

- `inputs/pilot_inputs.json` decrit les identifiants, snapshot PIT, calendrier
  Walk-Forward, espace de candidates, plan statistique, robustesse, OOS,
  execution et series compactes du pilote ;
- `inputs/package_shape.json` decrit les artefacts attendus dans
  `research_package/` et la stage `VALIDATION_READY`.

Le script `build_research_package.py` lit ces contrats avant de produire le
paquet et continue a utiliser `validate_package_dir()` comme gate d'acceptation.
Le schema `config.schema.json` est durci sur les champs operationnels requis par
la configuration preenregistree du runtime.

### Impact

Le pilote devient input-driven pour la reprise de `STEP_2_T2` sans creer de
nouvelle regle EBTA. Les valeurs restent des donnees de fixture locales et ne
constituent ni donnees live, ni integration BACKTRADER, ni nouvelle source
normative.

### Suite

`STEP_2_T2` : connecter davantage les modules de procedure aux artefacts
generes, en reduisant les derniers rapports statiques et en conservant les
erreurs de contrat explicites lorsque la preuve pipeline manque.

---

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

**Gouvernance** : TRACEABILITY_MATRIX.md, PROCEDURE_CALCULATION_MAP.md, `Implementation/Active/tracking.json` mis a jour.

### Suite

STEP_2_T1 : definir les inputs pilotes concrets et construire le pipeline end-to-end. La condition supplementaire : aucun contrat normatif du PAQUET D'EXECUTION ne doit rester sans artefact Implementation/ correspondant - satisfaite.

---

## 2026-06-26 - Archivage des hooks plans et contextes termines

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Implementation/Active/HOOK.md` |
| Fichiers impactes | `Implementation/Archives/completed_2026-06-26/`, `Implementation/0-CARTE_DU_CODE_EBTA.md`, `Implementation/PROCEDURE_CALCULATION_MAP.md`, `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/tests/test_procedure_map.py`, `.agents/skills/EBTA_Protocol_Guardian/SKILL.md`, `Protocole/PROTOCOLE EBTA.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\Active\tracking.json`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS - 50 tests; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` PASS; `git diff --check -- Implementation Protocole Archives .gitignore .agents` PASS avec avertissements CRLF/LF uniquement |

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

Utiliser le hook actif et `tracking.json` pour les prochains lots. Lire les
artefacts archives uniquement pour l'historique des lots termines.

## 2026-06-26 - Creation du hook de plan actif et du suivi JSON

| Champ | Valeur |
| --- | --- |
| Version runtime | EBTA-ENGINE-0.1.0 |
| Type | GOVERNANCE |
| Statut | ACCEPTED |
| Source normative | `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`, `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Fichiers impactes | `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Impact protocole | NONE |
| Verification | `python -m json.tool Implementation\Active\tracking.json`; `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`; `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`; `git diff --check -- Implementation Protocole` |

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
`Implementation/Active/tracking.json`, inventorier les candidats a l'archive,
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
