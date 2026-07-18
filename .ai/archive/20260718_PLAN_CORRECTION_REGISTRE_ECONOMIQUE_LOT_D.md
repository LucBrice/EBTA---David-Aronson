# Plan - Lot D : gates registre/pre-OOS/economique derives de preuves reelles

> Sous-chantier **1/4** de `EPIC_ATTESTATIONS_RESIDUELLES_R3`. Ce plan est un
> `SINGLE` : ses phases sont sequentielles et servent un seul critere de
> sortie, meme s'il couvre plusieurs champs de gates. Il corrige les
> attestations residuelles G2/G3/G4/G5/G7/G10 et le bug G2
> `review_registry_lineage(candidate_ids, candidate_ids)` sans modifier le
> protocole ni les validateurs globaux.

---

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Non. `.ai/checkpoint.json::active_workstream_id` est `null`; le chantier mere `EPIC_ATTESTATIONS_RESIDUELLES_R3` est `TRIAGED/PENDING` et attend ce Lot D. Aucun workstream `PLAN_CORRECTION_REGISTRE_ECONOMIQUE_LOT_D` n'existe encore. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Non. Le chantier mere autorise les Lots D/E sans retour humain entre eux, hors invariants et decisions non tranchees. |
| Ce plan a-t-il besoin d'une decision humaine explicite pour lever ce verrou avant d'etre routable via `/start` ? | Non. Les decisions de perimetre post-OOS/live hors scope et l'inclusion du bug G2 dans Lot D sont deja journalisees dans le chantier mere le 2026-07-17. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il transforme le brouillon `0 - HUMAN START HERE/PLAN_CORRECTION_REGISTRE_ECONOMIQUE_LOT_D.md` en sous-chantier executable. |

### Test de detection multi-lot (`.agents/skills/epic-orchestrator/SKILL.md`)

Verdict : **SINGLE**. Les corrections G2/G3/G4/G5/G7/G10 doivent etre
implementees ensemble dans le meme assemblage `gates.json` :

1. les helpers de gate dependent tous de `_procedure_reports()` et du meme
   point d'ecriture `_write_reports()`;
2. le contraste registre incomplet doit etre disponible avant de brancher
   G2, puis les mappings G3/G4/G5/G10 reutilisent les rapports deja produits;
3. un seul critere de sortie couvre le lot : aucun champ vise ne reste un
   litteral `True` non derive, sauf decision explicitement documentee.

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif (`AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`).
- [x] `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` et `.ai/governance/AI_MODIFICATION_CHECKLIST.md` lus car le chantier touche `Implementation/`.
- [x] `EBTA_Protocol_Guardian` applique : `Implementation/` reste une traduction executable, sans modification normative.
- [x] `epic-orchestrator` applique : ce lot est `SINGLE` et trace comme sous-chantier 1/4 du parent.
- [x] Brouillon source relu et audite en 2 passes `/evaluate` avant promotion.
- [x] Ce plan est ecrit comme nouveau fichier dans `.ai/backlog/fixes/`; le brouillon original reste dans `0 - HUMAN START HERE/` jusqu'a l'archivage par `plan.ps1 start`.
- [x] Autorite normative identifiee : `Protocole/PAQUET D'EXECUTION EBTA.md` gates G2/G3/G4/G5/G7/G10 ; SOP 02, 03, 05, 06, 08, 09B, 10, 12 selon les rapports reutilises.
- [x] Perimetre de fichiers autorises/interdits explicite section 5.
- [x] Etat des lieux verifie dans le code reel : `build_package()` ecrit `registry.jsonl` avant `_write_reports()`, `gate_validator.py` accepte deja les verdicts `PASS/FAIL/INCONCLUSIVE`, `nautilus_research_package.py` reutilise `pilot.build_package()`.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Remplacer les litteraux `True` residuels G2/G3/G4/G5/G7/G10 dans `gates.json` par des verdicts derives des rapports/registres reels, et rendre `registry_review` non tautologique. |
| Non-goals | Ne pas modifier `Protocole/`, les SOP, `validators/gate_validator.py::GATE_REQUIREMENTS`/`VERDICT_VALUES`, `validators/package_validator.py`, `Implementation/research_packages/nautilus_mvp/`, les lots C/A2/B archives, ni le Lot E/F. Ne pas rouvrir `independent_registry_review`, `independent_pre_oos_approval`, G13/G14 ou un vrai cycle live. Ne pas inventer une nouvelle procedure normative `test_reports`. |
| Source | Sous-chantier 1/4 de `EPIC_ATTESTATIONS_RESIDUELLES_R3`, issu de la demande humaine du 2026-07-17 et du brouillon audite archive par `plan.ps1` sous `0 - HUMAN START HERE/archive/20260718_PLAN_CORRECTION_REGISTRE_ECONOMIQUE_LOT_D.md`. |
| Exit criteria | (1) `registry_review` lit les candidates enregistrees depuis `registry.jsonl` ou une source equivalente non tautologique. (2) Les champs G2/G3/G4/G5/G7-residuel/G10 ne sont plus des litteraux `True` non derives dans `build_research_package.py`. (3) Un test de registre incomplet prouve que G2 peut devenir non `PASS`. (4) Les tests cibles minimal pilot et Nautilus passent. (5) Suite runtime complete PASS, bug-hunter PASS, plan-conformance PASS avant `/close`. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `DONE - implementation Lot D terminee, audits pre-cloture PASS` |
| Date de creation | 2026-07-18 |
| Date d'activation | 2026-07-18 |
| Autorite normative | `Protocole/PAQUET D'EXECUTION EBTA.md` gates G2/G3/G4/G5/G7/G10 ; SOP 03 pour registre, SOP 06 pour selection, SOP 02 pour WRC, SOP 05 pour robustesse, SOP 08/09B pour economique, SOP 12 pour package. |
| Autorite executable | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` et procedures EBTA deja existantes. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune nouvelle. Nautilus est seulement teste via le builder existant qui appelle `pilot.build_package()`. |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `Protocole/PAQUET D'EXECUTION EBTA.md` | Autorite des gates et artefacts attendus. |
| `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` | Assemblage fautif a corriger pour les champs D. |
| `Implementation/ebta_engine/procedures/*` | Rapports deja calcules et reutilises comme sources de verdict. |
| `Implementation/ebta_engine/validators/gate_validator.py` | Validateur deja suffisant pour `PASS/FAIL/INCONCLUSIVE`; intouchable dans ce lot. |
| Ce plan | Carte d'implementation du Lot D uniquement. |

Non-objectifs :

- ne pas reecrire l'autorite normative ;
- ne pas ajouter de statut de gate ;
- ne pas corriger G8 (`_oos_access_request()`), reserve au Lot E ;
- ne pas corriger `invariant_evidence.json`, reserve au Lot F ;
- ne pas regenerer le package persistant `nautilus_mvp`, reserve a la phase finale du parent.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`.
2. `.agents/skills/epic-orchestrator/SKILL.md` pour la relation parent/lot.
3. `.ai/backlog/fixes/EPIC_ATTESTATIONS_RESIDUELLES_R3.md` sections 0, 3, 5 et 10.
4. `0 - HUMAN START HERE/archive/20260717_EPIC_ATTESTATIONS_RESIDUELLES_R3_INVARIANT_EVIDENCE.md` sections 1.1, 1.5 et 1.6.
5. `Protocole/PAQUET D'EXECUTION EBTA.md` gates G2/G3/G4/G5/G7/G10.
6. `Implementation/PROCEDURE_CALCULATION_MAP.md`.
7. Fichiers de code cibles : `build_research_package.py`, `registry_lineage.py`, `gate_validator.py`, tests minimal pilot/Nautilus.

**Hierarchie d'autorite applicable a ce chantier** :

```text
1. Protocole/MANIFESTE DE GEL EBTA.md
2. Protocole/PROTOCOLE EBTA.md
3. Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md
4. SOP proprietaires et Protocole/PAQUET D'EXECUTION EBTA.md
5. Implementation/ executable
6. Adaptateurs externes dont Nautilus
```

## 3. Table des gates (points de decision sequentiels)

| Ordre | Gate | Question posee au systeme | Sortie si echec |
| --- | --- | --- | --- |
| G2 | Registre et candidates | Le registre reel contient-il les candidates de la matrice Test complete et la matrice locale existe-t-elle ? | G2 `INCONCLUSIVE` ou `FAIL` selon le verdict derive. |
| G3 | Selection locale | La selection et la calibration Train/Test sont-elles prouvees par les rapports `complexity_selection`, `optimization_log` et `ml_manifest` ? | G3 `INCONCLUSIVE`. |
| G4 | WRC Test | Le rapport WRC et la matrice familiale associee existent-ils et sont-ils coherents avec les candidates evaluees ? | G4 `INCONCLUSIVE` ou `FAIL`. |
| G5 | Robustesse pre-OOS | Le rapport et la matrice de robustesse existent-ils et exposent-ils un statut reel ? | G5 `INCONCLUSIVE` ou `FAIL`. |
| G7 | Package PRE_OOS_SEALED | Les rapports Test requis sont-ils presents/coherents sans inventer une procedure `test_reports` ? | G7 `INCONCLUSIVE` pour `test_reports`. |
| G10 | Gate economique | Les verdicts statistique, economique et global sont-ils derives de `economic.json` ? | G10 `INCONCLUSIVE` ou `FAIL`. |

## 4. Etat des lieux (avant/apres) - reutiliser avant de recreer

### Ce qui existe deja

| Module actuel | Chemin | Role reel verifie | Suffisant pour l'objectif ? |
| --- | --- | --- | --- |
| `build_package()` | `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` | Ecrit `_write_registry()` avant `_write_reports()`, puis valide le package. | Oui, ordre reutilisable. |
| `_write_reports()` | meme fichier | Assemble `gates.json` avec plusieurs litteraux `True` residuels. | A modifier. |
| `_procedure_reports()` | meme fichier | Calcule les rapports sources : `search_space`, `optimization_log`, `ml_manifest`, `complexity_selection`, `candidate_matrix`, `wrc`, `robustness`, `economic`, `registry_review`. | A modifier pour rendre `registry_review` non tautologique. |
| `review_registry_lineage()` | `Implementation/ebta_engine/procedures/registry_lineage.py` | Detecte une candidate influente absente si les listes fournies sont distinctes. | Reutiliser, ne pas remplacer. |
| `gate_validator.py` | `Implementation/ebta_engine/validators/gate_validator.py` | Traite `PASS/FAIL/INCONCLUSIVE` correctement. | Inchange. |
| `nautilus_research_package.py` | `Implementation/ebta_engine/package_builder/nautilus_research_package.py` | Appelle `pilot.build_package()`, donc herite du mapping. | Tester, ne pas modifier dans ce lot. |

### Ce qui manque reellement

| Brique manquante | Module a creer/modifier | Source de la regle | Reutilisation requise |
| --- | --- | --- | --- |
| Lecture non tautologique du registre | `build_research_package.py` | SOP 03 / G2 | Lire `registry.jsonl` deja ecrit ; appeler `review_registry_lineage()`. |
| Helpers de verdict D | `build_research_package.py` | Gates G2/G3/G4/G5/G7/G10 | Reutiliser les rapports en memoire, pas le validateur. |
| Tests de contraste | `test_minimal_pilot_pipeline.py` | Incident R3 residuel | Tester un registre incomplet et le mapping des gates. |
| Trace runtime | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | EBTA_Protocol_Guardian | Journaliser le changement. |

## 5. Decision d'architecture

Principe directeur : le builder du package doit transformer les rapports EBTA
deja calcules en verdicts de gates auditablement derives. Le validateur global
reste un consommateur, pas une source de correction.

Raisons :

- Le bug G2 vient d'un appelant tautologique, pas d'une absence de procedure.
- Les champs vises ont deja des rapports sources produits avant `gates.json`.
- `PASS/FAIL/INCONCLUSIVE` permet de representer l'etat reel sans etendre
  `GATE_REQUIREMENTS`.

### Frontieres explicites

| Couche | Elle fait | Elle NE fait PAS |
| --- | --- | --- |
| `build_research_package.py` | Lit les rapports et registres, derive les champs D de `gates.json`. | Ne cree pas une nouvelle norme ni un nouveau validateur global. |
| `registry_lineage.py` | Compare listes et lineage events fournis. | Ne lit pas le disque et ne connait pas le package. |
| `gate_validator.py` | Valide les champs deja assembles. | Ne corrige pas les preuves. |

### Contrat d'interface entre les couches

```python
def _registered_candidates_from_registry(package_dir: Path) -> list[str]:
    """Return sorted candidate_id values from REGISTER_CANDIDATE events."""

def _test_reports_gate(procedure_reports: dict) -> str:
    """Return PASS only when Test-side reports required by G7 are present."""
```

### Decisions deja actees

| Decision | Justification |
| --- | --- |
| `test_reports` devient un verdict de presence/coherence minimal. | Aucun producteur normatif explicite n'existe ; garder `True` serait un faux succes. |
| Les candidates influentes du controle G2 sont celles de `candidate_matrix["candidate_ids"]`. | C'est l'artefact runtime de la famille Test complete, deja couvert par SOP 02/03/06. |
| Le package persistant `nautilus_mvp` n'est pas regenere ici. | La regeneration depend des Lots D/E/F et appartient a la phase finale du parent. |

### Structure cible

```text
Implementation/
  examples/minimal_pilot_pipeline/build_research_package.py
  ebta_engine/tests/test_minimal_pilot_pipeline.py
  HISTORIQUE DES VERSIONS EBTA ENGINE.md
```

### Perimetre de fichiers explicite (autorises / interdits)

**Autorises (creer ou modifier)** :

```text
Implementation/examples/minimal_pilot_pipeline/build_research_package.py  MODIFIER - derivation Lot D
Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py           MODIFIER - tests ciblant Lot D
Implementation/examples/minimal_pilot_pipeline/research_package/          MODIFIER - artefact exemple regenere par le build pilote
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md                    MODIFIER - trace runtime
Implementation/TRACEABILITY_MATRIX.md                                    MODIFIER si le mapping doit etre precise
```

**Interdits (ne jamais modifier dans ce chantier)** :

```text
Protocole/                                                               NORME - intouchable
Implementation/ebta_engine/validators/gate_validator.py                  CONTRAT DEJA SUFFISANT
Implementation/ebta_engine/validators/package_validator.py               HORS PERIMETRE
Implementation/research_packages/nautilus_mvp/                          PHASE FINALE DU PARENT
Implementation/ebta_engine/package_builder/nautilus_research_package.py  TESTER SEULEMENT
.ai/checkpoint.json                                                      METTRE A JOUR UNIQUEMENT via plan.ps1
```

## 6. Decoupage en phases

### Phase 1 - Baseline et tests de contraste

Objectif : Prouver le bug et fixer les attentes avant correction.

Classification : TEST_FIXTURE

Actions :

- Ajouter un test de helper/derivation montrant qu'un registre valide mais
  incomplet par rapport a `candidate_matrix["candidate_ids"]` produit un
  `registry_review.status == "FAIL"` et un champ G2 non `PASS`.
- Ajouter un test de mapping Lot D qui compare les champs G3/G4/G5/G7/G10 de
  `gates.json` aux rapports sources.

Livrables :

- Tests rouges ou tests ecrits avant implementation, dans
  `test_minimal_pilot_pipeline.py`.

Critere de sortie :

- Les tests expriment le comportement attendu sans changer les validateurs.

### Phase 2 - Derivation des champs Lot D

Objectif : Remplacer les litteraux `True` par des verdicts derives.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ajouter les helpers de lecture `registry.jsonl` et de conversion
  `PASS/FAIL/INCONCLUSIVE`.
- Modifier `_write_reports()` et `_procedure_reports()` pour calculer
  `registry_review` a partir des candidates enregistrees reellement.
- Brancher G2/G3/G4/G5/G7/G10 sur les rapports sources.

Livrables :

- `build_research_package.py` sans litteraux `True` non derives sur les
  champs du Lot D.

Critere de sortie :

- Tests cibles minimal pilot PASS.

### Phase 3 - Validation transversale et traces

Objectif : Verifier que le chemin Nautilus herite de la correction sans
regeneration persistante, puis journaliser le changement runtime.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Executer les tests Nautilus cibles.
- Executer la suite runtime complete.
- Executer le builder pilote.
- Mettre a jour l'historique runtime et, si necessaire, la matrice de
  tracabilite.

Livrables :

- Validation documentee dans ce plan avant `/close`.

Critere de sortie :

- Toutes les commandes section 9 retournent exit code 0, ou un echec reel est
  documente et corrige avant cloture.

### Chemin critique (ordre des phases)

```mermaid
flowchart LR
    P1["Phase 1 - tests de contraste"] --> P2["Phase 2 - derivation gates"]
    P2 --> P3["Phase 3 - validation et traces"]
```

## 7. Artefacts produits

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Phase 1 | Tests Lot D | Python unittest | G2/G3/G4/G5/G7/G10 |
| Phase 2 | `reports/gates.json` dans packages generes | JSON | `gate_validator.py` |
| Phase 2 | `reports/registry_review.json` non tautologique | JSON | SOP 03 |
| Phase 3 | Historique runtime | Markdown | EBTA_Protocol_Guardian |

## 8. Invariants absolus et NO GO

### Invariants

1. Aucun champ Lot D ne doit rester un `True` litteral non derive dans
   `build_research_package.py`.
2. `registry_review` doit pouvoir echouer si `registry.jsonl` omet une
   candidate de la matrice Test.
3. Aucun verdict Nautilus ne devient une norme EBTA ; Nautilus ne fait
   qu'emprunter `pilot.build_package()`.
4. `test_reports` ne doit pas masquer l'absence des rapports Test attendus.

### NO GO

- Modifier `GATE_REQUIREMENTS` ou `VERDICT_VALUES`.
- Remplacer un `True` par un autre statut code en dur.
- Deplacer la correction vers `package_validator.py`.
- Regenerer `Implementation/research_packages/nautilus_mvp/` dans ce lot.
- Ajouter une dependance externe.

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
```

**Regle transversale bloquante** : la suite runtime complete doit rester
`PASS` avant bug-hunter, audit de conformite et `/close`.

**Premier lot executable propose** :

```text
Phase 1 - Baseline et tests de contraste
```

### Execution sans interruption

Ce plan est concu pour etre execute integralement sans retour humain, sauf si
une modification hors perimetre devient necessaire, si une source normative
contredit le plan, ou si une validation echoue pour une cause externe non
resoluble dans ce lot.

### Autorite decisionnelle accordee

L'IA peut choisir les noms exacts des helpers et les details de test tant que
le perimetre, les invariants, et les sources normatives ci-dessus sont
respectes.

### Interdiction des raccourcis (aucun faux succes)

Un echec de gate apres derivation est un resultat legitime ; il ne doit pas
etre masque en ajustant les fixtures, les seuils, ou les validateurs.

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-17 | Decoupage D/E/F et inclusion du bug G2 dans Lot D actees dans `EPIC_ATTESTATIONS_RESIDUELLES_R3`. | Autorise ce sous-chantier. |
| 2026-07-17 | `independent_registry_review`, `independent_pre_oos_approval`, G13/G14 live/post-OOS restent hors perimetre. | Interdit de construire un faux mecanisme live ou une fausse revue humaine. |

## 11. Risques et blocages connus

| Risque | Impact | Mitigation / condition de deblocage |
| --- | --- | --- |
| La correction G2 ne prouve pas une revue humaine independante | Confusion possible avec `independent_registry_review` | Le plan exclut explicitement ce champ et limite G2 a la presence/coherence des candidates enregistrees. |
| Le package genere devient `FAIL`/`INCONCLUSIVE` apres derivation | Le test historique "package PASS" peut devoir etre ajuste pour verifier un statut reel | Ne pas forcer PASS ; documenter le statut et verifier les raisons. |
| `test_reports` reste ambigu normativement | Risque de fausse procedure | Utiliser seulement un verdict minimal de presence/coherence et tracer la limite. |

## 12. Definition of Done

- [x] Phases 1 a 3 terminees.
- [x] Exit criteria de la section Triage atteints.
- [x] Aucune modification hors perimetre.
- [x] Tests section 9 executes et resultats documentes.
- [x] `bug-hunter` applique sur les fichiers touches.
- [x] `plan-conformance-audit` applique avant `/close`.
- [x] Checklist post-modification executee.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | DONE - Lot D implemente : G2/G3/G4/G5/G7-residuel/G10 derives de preuves reelles dans le builder pilote. |
| Ecarts par rapport au plan initial | Aucun ecart de fond. Precision ajoutee en cours d'execution : le package exemple minimal regenere est autorise comme artefact de preuve, sans toucher `Implementation/research_packages/nautilus_mvp/`. |
| Suites a prevoir (hors perimetre de ce plan) | Continuer l'EPIC par Lot E (`PLAN_CORRECTION_ACCES_OOS_LOT_E`), puis Lot F et regeneration finale du package persistant. |

### Resultat d'execution

| Champ | Valeur |
| --- | --- |
| Date | 2026-07-18 |
| Phases executees | Phases 1 a 3 |
| Artefact produit | Builder pilote corrige, tests Lot D, package exemple minimal regenere, historique runtime mis a jour. |
| Validation | `test_minimal_pilot_pipeline.py` PASS (6 tests) ; `test_nautilus_research_package.py` PASS (6 tests) ; suite runtime PASS (168 tests) ; build pilote PASS ; Pyrefly bug-hunter PASS (0 erreur) ; plan-conformance PASS. |
| Ecart par rapport au plan | Aucun ecart bloquant. |

### Audits pre-cloture

| Audit | Resultat | Preuve |
| --- | --- | --- |
| bug-hunter | PASS | `Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check Implementation/examples/minimal_pilot_pipeline/build_research_package.py Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py --output-format min-text` -> `INFO 0 errors`. |
| plan-conformance-audit | PASS | Exit criteria implementes : registre non tautologique, champs D sans `True` residuel, test registre incomplet, validations ciblees et suite complete PASS ; aucun non-goal viole. |

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-07-18 | Brouillon passe 1 : `test_reports` converti en verdict derive et test registre incomplete cible sur helper. | Eviter un `True` de remplacement et une preuve post-build trop tardive. |
| 2026-07-18 | Brouillon passe 2 : ajout de la validation Nautilus cible. | `nautilus_research_package.py` appelle `pilot.build_package()`. |
| 2026-07-18 | Plan passe 1 : source mise a jour vers le brouillon archive et retrait d'une decision technique du journal humain. | Eviter une source obsolete et ne pas presenter une decision d'implementation IA comme autorisation humaine. |
| 2026-07-18 | Plan passe 2 : convergence, aucun nouveau blind spot majeur. | Plan executable comme `SINGLE` pour baseline pre-implementation. |
