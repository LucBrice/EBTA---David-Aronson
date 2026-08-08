# Plan — Tests WRC de regression nulle et metamorphique

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Un chantier couvre-t-il deja ce perimetre ? | Le parent `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA` coordonne ce lot sans l'implementer. Aucun autre workstream ne possede ces tests. |
| Un verrou bloque-t-il le routage ? | Non. Le lot ajoute uniquement une fixture de test et ne change ni methode ni seuil. |
| Une decision humaine supplementaire est-elle requise ? | Non tant que `Protocole/` et `procedures/wrc.py` restent intacts. Toute necessite de les modifier bloque le lot. |
| Ce plan remplace-t-il un chantier existant ? | Non. Sous-chantier 1/7 du parent. |
| Test multi-lot | `SINGLE` : les trois controles partagent un seul fichier, un meme objet WRC et un critere de sortie commun ; aucun n'est clos avant que le module cible et la suite complete passent ensemble. |

## Audit IA de promotion

- [x] Etat vivant, gouvernance, parent et workflows lus.
- [x] SOP 02 lue integralement ; DN-008, DN-009 et DN-018 recoupes.
- [x] `wrc.py`, `bootstrap.py` et les tests WRC existants lus directement.
- [x] Deux passes d'evaluation de l'intake executees et corrigees.
- [x] Parametres de fixture mesures localement sans modifier le depot.
- [x] Perimetre ferme a un seul nouveau fichier runtime.
- [x] Aucune dependance, modification normative ou mutation externe.

### Journal de convergence de l'intake

| Passe | Verification | Correction | Resultat |
| --- | --- | --- | --- |
| 1 | Simulation de 40 nulles avec 4 candidates et lecture du contrat de test. | La matrice initiale de 128 observations donnait 9 `PASS` ; passage a 252 observations, 499 repetitions et bloc moyen 5, donnant 3 `PASS` deterministes. Commande cible alignee sur `unittest discover -t Implementation`. | Nouveaux problemes corriges. |
| 2 | Verification de l'invariance au renommage et de l'extension de famille. | Abandon de toute affirmation universelle ; fixture controlee avec `p=0.046/PASS` pour 2 candidates et `p=0.174/FAIL` pour 10 candidates, a colonnes de base et indices inchanges. | Aucun nouvel angle mort majeur ; convergence. |

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage |
| Type de chantier | `SINGLE` |
| Scope | Ajouter un module `unittest` deterministe couvrant une nulle gaussienne versionnee, l'invariance au renommage et une extension controlee de famille WRC. |
| Non-goals | Aucun changement de `wrc.py`, bootstrap, SOP, alpha, repetitions normatives, gate, schema, exemple, notebook ou adaptateur ; aucune certification universelle de calibration. |
| Source | Sous-chantier 1/7 de `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA`, audit du 2026-08-08. |
| Exit criteria | Le nouveau module et la suite canonique passent ; seul le fichier de test autorise est modifie dans `Implementation/`; les trois audits de fermeture requis sont sans finding bloquant. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `EN_COURS` — implementation et validations terminees, fermeture en attente |
| Date de creation | 2026-08-08 |
| Date d'activation | 2026-08-08 |
| Autorite normative | SOP 02 ; registre DN-008, DN-009, DN-018. |
| Autorite executable | `Implementation/ebta_engine/procedures/wrc.py` et `bootstrap.py`, lus mais interdits de modification. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune. |

## Carte d'execution IA

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Creer trois regressions deterministes WRC dans un seul nouveau module de tests. |
| Autorite et lecture minimale | Bootstrap repo -> parent -> ce plan -> SOP 02 sections 6-9, 13-15, 18 -> `wrc.py` -> tests WRC existants. |
| Perimetre autorise | `Implementation/ebta_engine/tests/test_wrc_calibration_metamorphic.py` uniquement pour le runtime. |
| Interdits absolus | Modifier production/protocole, inventer un seuil scientifique, utiliser une source aleatoire non seedee, presenter le cliquet comme certification. |
| Phase de reprise | Phase 1 apres baseline et `plan.ps1 continue`. |
| Preuve attendue | Trois tests cibles puis 245 tests ou davantage dans la suite complete, tous `OK`. |
| Arret et escalade | Le fichier unique ne suffit pas, une assertion exige une nouvelle doctrine, ou le comportement courant contredit les valeurs mesurees. |

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| SOP 02 | Definit WRC, alpha, bootstrap, verdicts et reproductibilite. |
| `wrc.py` | Implementation existante sous test, non modifiee. |
| Nouveau module | Garde de regression executable, non autorite scientifique. |
| Ce plan | Contrat d'implementation borne. |

Non-objectifs : ne pas corriger ou refondre le WRC, ne pas estimer une erreur de type I publiable, ne pas remplacer les validations scientifiques du protocole, ne pas ouvrir l'OOS.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, checkpoint/hook/tracking.
2. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
3. `.ai/workflows/common/WORKFLOW.md` et `core-engine/WORKFLOW.md`.
4. Plan parent et present plan.
5. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
6. `Protocole/SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`.
7. `Implementation/ebta_engine/procedures/wrc.py`, `bootstrap.py`, `zero_centering.py` et `tests/test_procedure_wrc.py`.

Hierarchie : `Protocole/` -> decisions humaines -> plan baseline -> `Implementation/` -> fixture.

## 3. Table des gates

| Ordre | Gate | Sortie si echec |
| --- | --- | --- |
| T1 | La nulle versionnee ne depasse pas 3 `PASS` sur 40. | Test rouge ; ne pas modifier la norme ni masquer l'echec. |
| T2 | Renommer les candidates ne change pas la statistique ni le verdict. | Test rouge. |
| T3 | L'extension controlee ne rend pas la p-value ou le verdict plus favorable. | Test rouge. |
| T4 | Suite complete et audits de fermeture passent. | Workstream non cloturable. |

## 4. Etat des lieux

### Existe deja

| Module | Role verifie | Suffisant ? |
| --- | --- | --- |
| `procedures/wrc.py` | Calcule statistique max, bootstrap conjoint zero-centered, p-value corrigee et verdict strict. | Oui, cible de test ; ne pas dupliquer. |
| `procedures/bootstrap.py` | Indices stationnaires communs et reproductibles. | Oui. |
| `tests/test_procedure_wrc.py` | Cas positif reproductible, famille complete, echec primaire et tests secondaires. | Non pour les trois regressions de ce lot. |

### Manque reel

Un module de test separe, lisible et sans helper de production, qui encode les trois fixtures versionnees et leur portee limitee.

## 5. Decision d'architecture

Le test reste separe de `test_procedure_wrc.py` pour rendre sa nature de garde post-audit identifiable et permettre une commande cible stable. Il appelle uniquement l'API publique `wrc_test`; aucun helper de production ni nouvelle abstraction n'est cree.

### Contrats des fixtures

```python
def build_null_family(data_seed: int) -> dict[str, list[float]]:
    """Quatre colonnes gaussiennes independantes, 252 observations."""

def build_family_expansion_fixture() -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    """Deux colonnes de base inchangees, puis huit colonnes nulles ajoutees."""
```

### Perimetre explicite

Autorise :

```text
Implementation/ebta_engine/tests/test_wrc_calibration_metamorphic.py [CREER]
```

Interdits :

```text
Protocole/
Implementation/ebta_engine/procedures/
Implementation/ebta_engine/schemas/
Implementation/ebta_engine/governance/
Implementation/ebta_engine/validators/
Implementation/ebta_engine/manifests/
Implementation/examples/
Implementation/notebooks/
BACKTRADER/
```

## 6. Decoupage en phases

### Phase 1 - Fixtures deterministes

Objectif : coder les constructeurs de donnees et le controle nul dans le seul fichier autorise.

Classification : TEST_FIXTURE

Actions :

- utiliser `random.Random` local, sans etat global ;
- executer 40 runs WRC avec les parametres figes ;
- compter les verdicts `PASS` et exiger `<= 3`.

Livrables :

- helper nul et premier test.

Critere de sortie :

- le test cible passe et reproduit le compte observe sans modifier la production.

### Phase 2 - Metamorphismes controles

Objectif : ajouter l'invariance au renommage et l'extension de famille.

Classification : TEST_FIXTURE

Actions :

- comparer uniquement les champs invariants au renommage ;
- construire la famille 2 puis 10 candidates avec les deux colonnes de base identiques ;
- verifier `p_extended >= p_base` et interdire `FAIL -> PASS`.

Livrables :

- deux tests supplementaires dans le meme fichier.

Critere de sortie :

- les trois tests passent ensemble et restent deterministes lors de deux executions consecutives.

### Phase 3 - Non-regression et audits

Objectif : prouver l'absence de regression et de faux succes dans le lot.

Classification : TEST_FIXTURE

Actions :

- executer test cible et suite complete ;
- appliquer `bug-hunter`, `adversarial-tester` et `plan-conformance-audit` ;
- corriger uniquement dans le perimetre ou escalader.

Livrables :

- preuves de test et rapports de fermeture dans ce plan.

Critere de sortie :

- tous les controles sont verts, sans finding bloquant ni fichier runtime hors scope.

## 7. Artefacts produits

| Etape | Artefact | Format | Source |
| --- | --- | --- | --- |
| Phases 1-2 | `test_wrc_calibration_metamorphic.py` | unittest stdlib | SOP 02 + audit parent |
| Phase 3 | Resultats commandes et rapports | sections Markdown de ce plan | workflow core-engine |

## 8. Invariants absolus et NO GO

### Invariants

1. `alpha=0.05` est lu comme autorite normative, jamais redéfini par le test.
2. Les 499 repetitions et le seuil `<=3/40` appartiennent seulement a la fixture.
3. Les seeds, colonnes de base et parametres sont explicites et reproductibles.
4. Les champs dependants des IDs ne sont pas declares invariants au renommage.
5. Un echec n'autorise aucune modification hors scope ni affaiblissement du test.

### NO GO

- Modifier `wrc.py`, le bootstrap, la SOP ou un schema.
- Utiliser `random` global ou une seed implicite.
- Tester seulement un exemple favorable sans controle negatif.
- Affirmer que `<=3/40` certifie le taux de type I du WRC.
- Changer les seeds apres observation pour obtenir un vert.
- Transformer un `FAIL` scientifique en `PASS`.

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_wrc_calibration_metamorphic.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check -- Implementation\ebta_engine\tests\test_wrc_calibration_metamorphic.py
```

La Phase 2 exige deux executions cibles consecutives identiques. La Phase 3 exige la suite complete. Aucun mock de `wrc_test` n'est autorise.

Premier lot executable : creation du fichier de test et controle nul.

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | `/continue` du parent multi-lot. | Autorise l'ouverture et l'execution gouvernee des enfants, pas une modification normative. |
| 2026-08-08 | Priorite au faux succes statistique dans l'audit source. | Place ce lot en premier. |

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Surinterpreter 40 fixtures | Fausse garantie scientifique. | Noms, commentaires et assertions parlent de regression deterministe seulement. |
| Fragilite aux versions Python | Variation de `random.gauss` ou de flottants. | CI Python 3.13 existante ; seeds et parametres visibles ; toute derive doit etre auditee, pas acceptee automatiquement. |
| Runtime du test | Suite ralentie. | `run_secondary=False`, 499 repetitions ; mesure exploratoire inferieure a quelques secondes. |
| Monotonie trop generale | Test faux pour une autre famille. | Assertion limitee a la fixture controlee versionnee. |

## 12. Definition of Done

- [x] Un seul nouveau fichier runtime, dans le perimetre autorise.
- [x] Controle nul, renommage et extension de famille implementes.
- [x] Deux executions cibles consecutives passent.
- [x] Suite complete passe avec au moins 245 tests.
- [x] Aucun changement de production ou de protocole.
- [x] `bug-hunter`, `adversarial-tester`, `plan-conformance-audit` sans finding bloquant.
- [x] JSON d'etat valides apres transitions.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | A remplir lors de `/close`. |
| Ecarts | Aucun attendu. |
| Suite | Retour au parent puis `PLAN_CLIQUET_INVENTAIRE_TESTS`. |

## 14. Journal d'audits post-route

| Passe | Verification | Correction | Resultat |
| --- | --- | --- | --- |
| 1 | Relecture du plan normalise contre le code, la SOP 02, le workflow `core-engine` et le nombre de tests attendu. | La preuve minimale est passee de 243 a 245 tests : le fichier doit contenir trois cas cibles, pas un seul. | Nouvel ecart mineur corrige. |
| 2 | Prototype exact des trois fixtures execute deux fois sans ecriture : nulle `3/40`, base `0.046/PASS`, famille etendue `0.174/FAIL`, invariance au renommage vraie lors des deux runs. | Aucune. Les valeurs restent des preuves de fixture et ne sont pas transformees en constantes normatives. | Aucun nouvel angle mort majeur ; convergence. |

## 15. Resultat d'execution du 2026-08-08

| Champ | Valeur |
| --- | --- |
| Fichier runtime cree | `Implementation/ebta_engine/tests/test_wrc_calibration_metamorphic.py` |
| Tests cibles | Deux executions consecutives : `Ran 3 tests ... OK` |
| Suite complete | `Ran 245 tests ... OK` |
| Hygiene | `git diff --check` PASS |
| Ecart | Aucun. `wrc.py`, bootstrap et `Protocole/` inchanges. |

## Preuve bug-hunter

Commande cible :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check Implementation\ebta_engine\tests\test_wrc_calibration_metamorphic.py --output-format min-text
```

Resultat : `INFO 0 errors`. Aucun diagnostic, faux positif ou vrai bug a
trier. La suite complete reste `245 tests, OK`.

## Preuve adversarial-tester

Trois mutations hostiles ont ete injectees par `unittest.mock.patch` sans
modifier le depot :

| Scenario hostile | Attendu | Observe | Classement |
| --- | --- | --- | --- |
| `wrc_test` renvoie toujours `PASS` sur les 40 nulles | Le controle nul echoue. | 1 assertion failure, 0 erreur. | `PASS_ADVERSARIAL` |
| Le resultat depend seulement du nom des candidates | L'invariance au renommage echoue. | 1 assertion failure, 0 erreur. | `PASS_ADVERSARIAL` |
| L'extension de famille produit un `PASS` avec une p-value plus faible | Le controle d'extension echoue. | 1 assertion failure, 0 erreur. | `PASS_ADVERSARIAL` |

Aucun `FALSE_SUCCESS`, `SILENT_FALLBACK` ou `NORMATIVE_GAP` detecte dans le
diff du lot.

## Preuve EBTA Protocol Guardian

- La SOP 02 conserve son autorite : `alpha=0,05`, bootstrap stationnaire
  conjoint, zero-centering et `B=5000` pour un run EBTA reel.
- Les `499` repetitions, les seeds et `<=3/40` sont explicitement limites a
  une fixture de regression ; ils ne produisent aucun gate ou seuil
  methodologique nouveau.
- Aucun fichier de `Protocole/`, aucune procedure et aucun verdict runtime ne
  sont modifies.

Verdict : `CONFORME — TEST_FIXTURE`, confiance haute sur le perimetre lu.

## Preuve plan-conformance-audit

Fenetre : baseline `9b4772c`, activation enregistree apres `99a0a52`, etat
de travail courant avant cloture.

| Critere | Classement | Preuve |
| --- | --- | --- |
| Nouveau module cible et suite canonique passent | `IMPLEMENTE` | Deux runs cibles `3 tests OK`; suite `245 tests OK`. |
| Seul le fichier runtime autorise est touche | `IMPLEMENTE` | `git status --short -- Implementation` ne liste que `test_wrc_calibration_metamorphic.py`. |
| Trois controles livres | `IMPLEMENTE` | Trois methodes decouvertes par `unittest`, couvrant nulle, renommage et extension. |
| Audits de fermeture sans finding bloquant | `IMPLEMENTE` | Sections `Preuve bug-hunter`, `Preuve adversarial-tester` et present audit. |
| Non-goals respectes | `IMPLEMENTE` | Aucun diff dans `Protocole/`, `procedures/`, schemas, exemples, notebooks ou adaptateurs. |

Verdict : `PASS`, 5/5 criteres implementes, aucun extra runtime et aucun
Non-goal viole. La cloture peut franchir `READY_TO_CLOSE`.
