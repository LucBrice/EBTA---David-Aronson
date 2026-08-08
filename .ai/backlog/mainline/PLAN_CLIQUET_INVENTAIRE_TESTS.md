# Plan — Cliquet versionne de l'inventaire unittest

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Perimetre deja couvert ? | Non. Le parent coordonne le lot ; aucun inventaire equivalent n'existe. |
| Verrou actif ? | Non ; deux fixtures nouvelles seulement. |
| Decision humaine requise ? | Non tant que la CI et les tests existants restent intacts. |
| Remplacement ? | Non, sous-chantier 2/7. |
| Test multi-lot | `SINGLE` : le snapshot et son garde sont inutiles separement et partagent un seul critere d'egalite exacte. |

## Audit IA de promotion

- [x] Bootstrap, etat vivant, parent, gouvernance et workflows lus.
- [x] Topologie `unittest discover` verifiee : 245 IDs, tous uniques.
- [x] Absence d'inventaire existant verifiee par recherche.
- [x] Deux passes intake convergentes.
- [x] Limite d'auto-suppression documentee sans fausse garantie.
- [x] Perimetre ferme a deux nouveaux fichiers de test.

### Journal de convergence de l'intake

| Passe | Verification | Correction | Resultat |
| --- | --- | --- | --- |
| 1 | Aplatissement reel de la suite canonique. | Snapshot initial porte a 246 IDs pour inclure le futur garde lui-meme. | Angle mort corrige. |
| 2 | Analyse de la suppression simultanee garde + inventaire. | Garantie limitee aux derives lorsque le garde s'execute ; aucune extension CI. | Aucun nouvel angle mort majeur ; convergence. |

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage |
| Type de chantier | `SINGLE` |
| Scope | Versionner les IDs unittest et exiger leur egalite exacte avec la decouverte canonique. |
| Non-goals | Pas de CI, production, protocole, schema ou test existant modifie ; aucune resistance revendiquee contre la suppression volontaire simultanee du mecanisme. |
| Source | Sous-chantier 2/7 de `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA`. |
| Exit criteria | Deux nouveaux fichiers seulement ; inventaire exact/unique/trie/auto-inclusif ; test cible et suite complete passent ; ajout et retrait simules sont rejetes ; audits sans finding bloquant. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `EN_COURS` — implementation et audits termines, fermeture en attente |
| Date de creation | 2026-08-08 |
| Date d'activation | 2026-08-08 |
| Autorite normative | Aucune regle scientifique nouvelle ; `Protocole/` reste inchange. |
| Autorite executable | Chargeur stdlib `unittest` et commande canonique du workflow CI. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune. |

## Carte d'execution IA

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Ajouter un snapshot de 246 IDs et un garde d'egalite exacte. |
| Autorite et lecture minimale | Bootstrap -> parent -> plan -> workflow core-engine -> tests vivants -> CI canonique. |
| Perimetre autorise | `test_inventory.txt` et `test_test_inventory.py`. |
| Interdits absolus | Modifier un test existant, la CI, la production ou masquer une difference attendu/reel. |
| Phase de reprise | Phase 1 apres baseline et `continue`. |
| Preuve attendue | 1 test cible, suite complete >=246, deux mutations d'inventaire rejetees. |
| Arret et escalade | Le garde exige une modification hors des deux fichiers ou la decouverte canonique n'est pas stable. |

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `unittest discover` | Source executable des IDs actuels. |
| `test_inventory.txt` | Snapshot derive, relisible en diff. |
| `test_test_inventory.py` | Compare le snapshot a la decouverte. |
| Ce plan | Borne la livraison, sans devenir une liste d'autorite concurrente. |

Non-objectifs : ne pas compter la couverture, migrer vers pytest, modifier la CI, proteger contre un acteur qui supprime aussi le garde, ni modifier la doctrine EBTA.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, checkpoint/hook/tracking.
2. Checklist de gouvernance et workflows `common`/`core-engine`.
3. Epic parent et present plan.
4. `.github/workflows/ebta-runtime-suite.yml` pour la commande canonique seulement.
5. Arborescence et IDs reels de `Implementation/ebta_engine/tests/`.

Hierarchie : commandes/workflows du repo -> plan baseline -> garde -> snapshot derive.

## 3. Table des gates

| Gate | Question | Echec |
| --- | --- | --- |
| I1 | Snapshot trie et sans doublon ? | Assertion explicite. |
| I2 | Snapshot egal a la decouverte canonique ? | IDs manquants/inattendus affiches. |
| I3 | Test cible et suite complete passent ? | Lot non cloturable. |
| I4 | Scenarios hostiles sont rejetes ? | Audit adversarial bloque. |

## 4. Etat des lieux

| Element | Etat verifie | Decision |
| --- | --- | --- |
| Suite canonique | 245 IDs uniques apres le lot WRC. | Reutiliser `TestLoader.discover`. |
| Inventaire | Aucun fichier ou helper equivalent. | Creer deux fixtures. |
| CI | Lance deja la suite canonique. | Ne pas modifier. |

Manque : un signal executable lorsqu'un ID change, avec une mise a jour de snapshot visible dans le meme diff si le changement est volontaire.

## 5. Decision d'architecture

Un fichier texte trié est choisi plutot qu'un compte global : il montre exactement quel test a disparu ou apparu. Le garde utilise `Path(__file__)` pour resoudre le repertoire et le top-level, puis aplatit recursivement les `TestSuite` sans les executer.

```python
def iter_test_ids(suite: unittest.TestSuite) -> Iterator[str]: ...
def discover_test_ids() -> list[str]: ...
```

Le message d'echec calcule `missing = expected - actual` et `unexpected = actual - expected`.

### Perimetre explicite

Autorises :

```text
Implementation/ebta_engine/tests/test_inventory.txt         [CREER]
Implementation/ebta_engine/tests/test_test_inventory.py     [CREER]
```

Interdits :

```text
Implementation/ebta_engine/tests/test_*.py                  [tous les fichiers existants]
.github/
Protocole/
Implementation/ebta_engine/ hors tests
Implementation/examples/
Implementation/notebooks/
Implementation/adapters/
BACKTRADER/
```

## 6. Decoupage en phases

### Phase 1 - Garde de decouverte

Objectif : creer le garde qui reproduit la topologie canonique.

Classification : TEST_FIXTURE

Actions :

- resoudre `tests/` et `Implementation/` depuis `__file__` ;
- aplatir les suites et produire une liste triee d'IDs ;
- valider ordre, unicite et egalite exacte au snapshot.

Livrables :

- `test_test_inventory.py`.

Critere de sortie :

- le garde decouvre son propre ID et fournit un message missing/unexpected.

### Phase 2 - Snapshot initial

Objectif : versionner l'etat exact apres ajout du garde.

Classification : TEST_FIXTURE

Actions :

- generer la liste logique des 246 IDs ;
- l'ajouter avec `apply_patch`, une ligne par ID ;
- verifier ordre et absence de doublon.

Livrables :

- `test_inventory.txt` contenant 246 IDs.

Critere de sortie :

- le test cible passe et `countTestCases()` vaut au moins 246.

### Phase 3 - Adversarial et non-regression

Objectif : prouver que le garde rejette les derives et ne casse pas la suite.

Classification : TEST_FIXTURE

Actions :

- simuler un ID attendu manquant puis un ID inattendu ;
- executer test cible et suite complete ;
- appliquer les audits core-engine.

Livrables :

- preuves persistées dans ce plan.

Critere de sortie :

- deux scenarios hostiles rejetes, suite complete verte et audits sans finding bloquant.

## 7. Artefacts produits

| Artefact | Format | Autorite |
| --- | --- | --- |
| `test_inventory.txt` | texte trie | derive de la decouverte |
| `test_test_inventory.py` | unittest stdlib | garde executable |
| rapports | Markdown dans ce plan | preuves workflow |

## 8. Invariants absolus et NO GO

### Invariants

1. Le snapshot contient des IDs, pas seulement un compte.
2. Il inclut le garde lui-meme.
3. Tout ajout et toute suppression sont visibles.
4. La mise a jour volontaire du snapshot reste une revue de diff, pas une preuve automatique de legitimite.
5. Aucun autre fichier de test n'est modifie.

### NO GO

- Exclure silencieusement un test difficile a importer.
- Trier ou dedupliquer seulement la liste attendue de facon a masquer un doublon.
- Modifier la CI ou un test existant.
- Presenter le garde comme inviolable apres sa propre suppression.
- Remplacer une erreur de decouverte par une liste vide plausible.

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_test_inventory.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check -- Implementation\ebta_engine\tests\test_test_inventory.py Implementation\ebta_engine\tests\test_inventory.txt
```

Premier lot executable : garde de decouverte, puis snapshot calcule apres que son ID existe.

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | `/continue` du parent. | Autorise le cycle enfant borne. |
| 2026-08-08 | Cliquet d'inventaire retenu par l'audit. | Rend les suppressions visibles sans revendiquer une protection absolue. |

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Auto-suppression du garde | CI verte si les deux fichiers disparaissent. | Limite explicite ; diff humain et futurs garde-fous CI restent distincts. |
| Import dependant du cwd | Faux IDs ou erreur. | Chemins absolus derives de `__file__`, top-level explicite. |
| Inventaire verbeux | Diff de 246 lignes. | Une ligne par ID, ordre stable, aucun metadata. |
| Ajout legitime bloque | Friction volontaire. | Mettre a jour le snapshot dans le meme commit et revoir le diff. |

## 12. Definition of Done

- [x] Deux fichiers nouveaux seulement.
- [x] Inventaire exact, trie, unique, auto-inclusif.
- [x] Garde affiche missing/unexpected.
- [x] Test cible et suite >=246 passent.
- [x] Deux scenarios adversariaux rejetes.
- [x] Audits core-engine sans finding bloquant.
- [x] Etat JSON valide.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | A remplir. |
| Ecart | Aucun attendu. |
| Suite | Retour parent puis `PLAN_GARDE_LITTERAUX_VERDICT`. |

## 14. Journal d'audits post-route

| Passe | Verification | Correction | Resultat |
| --- | --- | --- | --- |
| 1 | Relecture du plan normalise contre le comportement de `unittest.TestLoader.discover`. | Le garde ne filtrera pas les objets `_FailedTest` : une erreur d'import doit produire un ID inattendu et des IDs attendus manquants, donc echouer en fermeture prudente. | Precision fail-closed ajoutee, aucun changement de scope. |
| 2 | Recalcul de cardinalite et verification des chemins : 245 IDs vivants, `test_inventory.txt` non decouvert, un seul futur `TestCase` ajoute. | Total attendu confirme a 246 ; resolution `tests_dir = Path(__file__).resolve().parent` et `top_level = tests_dir.parents[1]`. | Aucun nouvel angle mort majeur ; convergence. |

## 15. Resultat d'execution du 2026-08-08

| Champ | Valeur |
| --- | --- |
| Fichiers crees | `test_test_inventory.py`, `test_inventory.txt` |
| Snapshot | 246 lignes, 246 uniques, trie, ID du garde present |
| Test cible | `Ran 1 test ... OK` |
| Suite complete | `Ran 246 tests ... OK` |
| Ecart | Aucun ; aucun test existant ni fichier CI modifie. |

## Preuve bug-hunter

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check Implementation\ebta_engine\tests\test_test_inventory.py --output-format min-text
```

Resultat : `INFO 0 errors`. Aucun signal de typage a trier.

## Preuve adversarial-tester

Le helper `_load_expected_ids` a ete remplace temporairement en memoire, sans
ecriture de fichier, pour trois entrees hostiles :

| Entree hostile | Observation | Classement |
| --- | --- | --- |
| Snapshot prive d'un ID reel | 1 assertion failure, 0 erreur | `PASS_ADVERSARIAL` |
| Snapshot contenant un ID inexistant | 1 assertion failure, 0 erreur | `PASS_ADVERSARIAL` |
| Snapshot contenant un doublon | 1 assertion failure, 0 erreur | `PASS_ADVERSARIAL` |

Le garde echoue explicitement ; aucun repli vers une liste vide ou un succes
plausible. Aucun `FALSE_SUCCESS` ou `SILENT_FALLBACK` detecte. La suppression
simultanee du garde et du snapshot reste le residu explicite du plan, pas une
garantie simulee.

## Preuve EBTA Protocol Guardian

Ce lot est procedural et derive uniquement la liste des tests decouverts. Il
ne modifie aucun calcul, seuil, verdict, gate ou document sous `Protocole/`.
L'inventaire ne devient pas une autorite scientifique et ne remplace pas la
suite elle-meme. Verdict : `CONFORME — TEST_FIXTURE`.

## Preuve plan-conformance-audit

Fenetre : baseline `dbb4095`, activation apres `f148835`, etat courant avant
cloture.

| Critere | Classement | Preuve |
| --- | --- | --- |
| Deux fichiers nouveaux seulement | `IMPLEMENTE` | `git status --short -- Implementation` liste uniquement les deux chemins autorises. |
| Inventaire exact, trie, unique et auto-inclusif | `IMPLEMENTE` | 246 lignes, 246 uniques, ordre vrai, ID du garde present ; test cible `OK`. |
| Ajout/retrait rendus visibles | `IMPLEMENTE` | Scenarios hostile manquant, inattendu et doublon echouent par assertion. |
| Suite complete verte | `IMPLEMENTE` | `Ran 246 tests ... OK`. |
| Non-goals respectes | `IMPLEMENTE` | Aucun diff CI, production, protocole ou test existant. |
| Audits sans finding bloquant | `IMPLEMENTE` | Pyrefly 0 ; adversarial 3/3 ; present audit. |

Verdict : `PASS`, 6/6 criteres implementes, aucun extra et aucun Non-goal
viole. La cloture peut franchir `READY_TO_CLOSE`.
