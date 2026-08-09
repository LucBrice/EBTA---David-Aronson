# Plan d'implementation — Pyrefly CI et correction notebook

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Parent | Epic post-audit `BASELINED`, enfants 1-8 `DONE`. |
| Test multi-lot | `SINGLE_CHANTIER` : correction et gate Pyrefly partagent le meme critere zero erreur. |
| Venv Nautilus CI | Interdit ; import remplace par `Any`. |
| Ruff | Hors scope, reserve a l'enfant 10. |

## Audit IA de promotion

- [x] Workflow, pyproject, notebook et signature cible lus.
- [x] Pyrefly local 1.1.1 confirme.
- [x] Diagnostic `package_dir` reproduit avec la commande portable cible.
- [x] Dependances CI existantes distinguees du venv Nautilus lourd.
- [x] Ratchet supply-chain existant identifie et inclus au scope.
- [x] Correction notebook sans package durable choisie.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage ; non executable avant baseline |
| Type de chantier | `SINGLE` |
| Classification | `CONTRACT_ENCODING` |
| Scope | Epingler/executer Pyrefly en CI sur moteur + notebooks, neutraliser seulement Nautilus et corriger l'appel notebook. |
| Non-goals | Venv Nautilus en CI, Ruff, changement de signature runtime, dependance moteur, Protocole, BACKTRADER, settings GitHub. |
| Source | Epic parent enfant 9/10 ; audit du 2026-08-08 lignes 486-492, 701-705, 756-760 et 885-891. |
| Exit criteria | Pyrefly pinne, commande portable exacte, notebook type-correct sans sortie durable, ratchet et suite verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `DONE` |
| Date | 2026-08-09 |
| Autorite normative | Aucune. |
| Autorite executable | Workflow CI et code notebook. |
| Impact protocole | Aucun ; Guardian `CONTRACT_ENCODING`. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Rendre le type-check mecanique et independant du rapport bug-hunter. |
| Lecture minimale | Ce plan, workflow, pyproject, notebook, fonction appelee et test supply-chain. |
| Preuve | Pyrefly en environnement CI equivalent, ratchet, inventaire et suite. |
| Arret | Besoin d'installer Nautilus en CI ou diagnostic interne hors scope massif. |

## 1. Role et non-objectifs

Pyrefly devient un gate technique additionnel, jamais une preuve de validite
scientifique. Il ne remplace ni les tests, ni bug-hunter, ni les gardes de
verdict.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap/cockpit, parent et audit source.
2. Workflow CI et ratchet supply-chain.
3. `pyproject.toml` et aide Pyrefly 1.1.1.
4. Notebook et signature `build_nautilus_inputs`.

## 3. Etat des lieux

- Pyrefly 1.1.1 est present dans le venv local ;
- `python-interpreter-path` du pyproject est Windows/local et doit etre
  surcharge par `--python-interpreter-path python` en CI ;
- le workflow installe deja jsonschema/numpy/pandas ;
- Nautilus n'est volontairement pas installe en CI ;
- le notebook appelle `build_nautilus_inputs()` sans son argument requis.

## 4. Gates

| Gate | PASS | Sinon |
| --- | --- | --- |
| Pin | `pyrefly==1.1.1` dans l'ensemble exact des installs | FAIL |
| Portabilite | `--python-interpreter-path python` | FAIL |
| Frontiere | `--replace-imports-with-any "nautilus_trader.*"` uniquement | FAIL |
| Couverture | `Implementation/ebta_engine` et `Implementation/notebooks` | FAIL |
| Notebook | `package_dir=Path(temp_dir)` dans `TemporaryDirectory` | FAIL |
| Regression | Pyrefly 0, ratchet/inventaire/suite verts | FAIL |

## 5. Decision d'architecture

Le workflow installe Pyrefly comme outillage CI direct, apres les dependances
deja presentes, puis execute `python -m pyrefly`. La CLI surcharge le chemin
d'interpreteur local sans modifier le pyproject utile aux developpeurs.

Le notebook cree un `TemporaryDirectory` dans sa cellule et passe
`Path(temp_dir)` : l'appel est type-correct et son execution exploratoire ne
modifie aucun package persistant.

## 6. Perimetre de fichiers

Autorises :

```text
.github/workflows/ebta-runtime-suite.yml
Implementation/notebooks/03_candidate_matrix_build.ipynb
Implementation/ebta_engine/tests/test_ci_supply_chain.py
Implementation/ebta_engine/tests/test_inventory.txt
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md
.ai/backlog/mainline/PLAN_PYREFLY_CI_NOTEBOOK.md
.ai/archive/20260809_PLAN_PYREFLY_CI_NOTEBOOK.md
.ai/checkpoint.json
0 - HUMAN START HERE/archive/20260809_PLAN_PYREFLY_CI_NOTEBOOK.md
0 - HUMAN START HERE/archive/AUDIT_BUG_HUNTER_PLAN_PYREFLY_CI_NOTEBOOK_2026-08-09.md
0 - HUMAN START HERE/archive/AUDIT_ADVERSARIAL_PLAN_PYREFLY_CI_NOTEBOOK_2026-08-09.md
0 - HUMAN START HERE/archive/AUDIT_CONFORMITE_PLAN_PYREFLY_CI_NOTEBOOK_2026-08-09.md
```

Interdits : `pyproject.toml`, requirements Nautilus, runtime Python, Ruff,
Protocole, Active, BACKTRADER et settings GitHub.

## 7. Decoupage en phases

### Phase 1 — Correction notebook

Ajouter le contexte temporaire et l'argument requis.

### Phase 2 — CI et ratchet

Ajouter pin/step Pyrefly et etendre l'ensemble exact supply-chain ainsi que
les mutations hostiles au retrait/affaiblissement du gate.

### Phase 3 — Verification

Executer Pyrefly dans un environnement equivalent CI, tests, inventaire,
suite et audits.

## 8. Invariants et NO GO

1. La CI n'installe jamais `nautilus_trader`.
2. `jsonschema`, numpy et pandas restent pins identiques.
3. Une erreur interne Pyrefly reste bloquante.
4. Le notebook n'ecrit pas dans `research_packages/` par defaut.
5. Ruff et ses 26 findings restent intacts pour le lot 10.

NO GO : ignore global de `ebta_engine`, `# type: ignore` sur l'appel, retrait
des notebooks, chemin Windows en CI, installation du venv lourd.

## 9. Verification a chaque etape

```powershell
python -m pyrefly check --python-interpreter-path python --replace-imports-with-any "nautilus_trader.*" Implementation/ebta_engine Implementation/notebooks
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_ci_supply_chain.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_test_inventory.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | Audit consolide. | Pyrefly CI sans venv Nautilus et correction du bug notebook. |
| 2026-08-09 | `/continue` persistant. | Autorise l'enfant 9 local. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| Config Windows casse Linux | Override CLI explicite et test exact. |
| Faux zero par ignore large | Remplacement limite a `nautilus_trader.*`; deux racines explicites. |
| Dependances CI flottantes | Pin 1.1.1 integre a l'ensemble exact existant. |
| Notebook pollue le depot | Repertoire temporaire. |
| CI non executee localement | Environnement temporaire equivalent ; run distant non revendique avant push. |

## 12. Definition of Done

- [x] Notebook corrige sans artefact durable.
- [x] Pyrefly 1.1.1 epingle et execute en CI.
- [x] Interpreteur CI et frontiere Nautilus explicites.
- [x] Ratchet refuse retrait/affaiblissement du gate.
- [x] Pyrefly, inventaire et suite complete verts.
- [x] Audits sans finding bloquant.
- [x] Aucun fichier interdit touche.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | Venv CI equivalent : Pyrefly 1.1.1, 0 erreur ; 7 tests CI + inventaire verts ; YAML_PASS ; suite canonique 291 tests `OK` (1 skipped). |
| Ecart | Aucun fichier du depot. Le run GitHub distant n'est pas revendique sans push. Le venv temporaire de preuve reste sous Temp car sa suppression a ete refusee par la politique d'execution. |
| Suite | Enfant 10/10 `PLAN_RUFF_CI_BUGS_CIBLES`. |

## 14. Journal d'audits post-route

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Commande confrontee au pyproject Windows et au venv de 2,6 Go. | Override `python`, Nautilus remplace, aucun changement pyproject/venv. |
| 2 | Correction notebook confrontee aux effets de bord et au ratchet CI. | TemporaryDirectory, ensemble installs exact et step exact. Convergence. |

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Diagnostic et version reproduits. | Une erreur interne notebook confirmee. |
| 2 | Environnement CI et frontieres relus. | Pin/commande/correction atomiques ; convergence. |
