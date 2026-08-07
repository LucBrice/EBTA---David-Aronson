# Plan — Lot 3 : garde d'environnement dans `long_data.py`

Sous-chantier 3/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`.

---

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Non — sous-chantier du chantier mere `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE` (`BASELINED`). |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Oui, en principe : `.ai/governance/AI_MODIFICATION_CHECKLIST.md` interdit de modifier `Implementation/` sans decision humaine explicite. **Leve le 2026-08-07** pour ce seul fichier (`long_data.py`) et cette seule correction (chantier mere, section 10). |
| Ce plan a-t-il besoin d'une decision humaine explicite pour lever ce verrou avant d'etre routable via `/start` ? | Non — deja levee et journalisee. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. |

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif.
- [x] Bandeau de statut (section 0) rempli et verifie contre l'etat machine reel.
- [x] Ce plan a ete ECRIT COMME NOUVEAU FICHIER dans `.ai/backlog/fixes/`.
- [x] Chantier classe `fix` — sous-chantier de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`.
- [x] Autorite normative applicable identifiee : aucune regle scientifique
      EBTA touchee ; autorite executable `Implementation/ebta_engine/benchmarks/long_data.py`.
- [x] Perimetre de fichiers autorises/interdits explicite (section 5).
- [x] Aucune modification hors perimetre requise.
- [x] Prerequis factuels : verrou `Implementation/` leve pour ce seul fichier
      (journal section 10 du chantier mere), aucun autre prerequis manquant.
- [x] Etat des lieux (section 4) verifie par lecture directe du code
      (`_environment_report()` ligne 483-492, seul appelant de
      `importlib.metadata.version("nautilus_trader")` dans tout le depot,
      confirme par grep).

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Proteger `importlib.metadata.version("nautilus_trader")` dans `_environment_report()` (`long_data.py:487`) pour que la suite de tests passe a zero erreur hors du venv Nautilus, sans masquer l'absence du paquet. |
| Non-goals | Ne modifie aucun autre point de `long_data.py`. Ne modifie aucune procedure, validator, gate ou schema. Ne skip pas le test — il continue de s'executer et de produire un rapport complet. |
| Source | Sous-chantier 3/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`, Phase 4. Recommandation 3 de l'audit source `0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`. Verrou `Implementation/` leve le 2026-08-07 (chantier mere, section 10). |
| Exit criteria | (1) `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation` retourne `219 tests, 0 error` (skips autorises) hors venv Nautilus ; (2) `report["environment"]["nautilus_trader_version"]` vaut la chaine explicite `"NOT_INSTALLED"` (jamais un champ absent) quand le paquet n'est pas installe ; (3) aucune autre modification de `Implementation/` que ce fichier. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date de creation | 2026-08-07 |
| Date d'activation | - |
| Autorite normative | Aucune (hors perimetre EBTA scientifique — correction technique locale). |
| Autorite executable | `Implementation/ebta_engine/benchmarks/long_data.py`. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune (le venv Nautilus reste optionnel ; cette correction rend son absence explicite, pas obligatoire). |

## Carte d'execution IA (lecture prioritaire pour `/continue`)

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | `_environment_report()` retourne `"NOT_INSTALLED"` pour `nautilus_trader_version` au lieu de lever `PackageNotFoundError`, hors venv Nautilus. |
| Autorite et lecture minimale | 1. Ce document ; 2. `Implementation/ebta_engine/benchmarks/long_data.py` lignes 1-30 (imports) et 483-492 (`_environment_report`) ; 3. `Implementation/ebta_engine/tests/test_long_data_benchmark.py`. |
| Perimetre autorise | `Implementation/ebta_engine/benchmarks/long_data.py` (uniquement `_environment_report()`), plus les fichiers de plan de ce lot. |
| Interdits absolus | Toute autre fonction de `long_data.py`. Toute modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `adapters/`. Catcher `Exception` generique au lieu de `PackageNotFoundError` precis. |
| Phase de reprise | Phase 1 (implementation unique). |
| Preuve attendue | `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation` -> `219 tests`, `0 error` (hors venv Nautilus). |
| Arret et escalade | Aucune attendue — verrou deja leve, aucune decision en suspens. |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `Protocole/` | Hors perimetre total. |
| `Implementation/ebta_engine/benchmarks/long_data.py` | Cible unique de ce lot. |
| Ce plan | Carte d'implementation de la garde d'environnement. |

Non-objectifs :

- ne pas reecrire l'autorite normative du projet ;
- ne pas introduire de regle, seuil ou statut absent de cette autorite ;
- ne pas faire du venv Nautilus une dependance obligatoire de la suite de
  tests stdlib-only ;
- ne pas skipper silencieusement le test concerne.

---

## 2. Contexte obligatoire a lire avant de coder

1. `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md` section 10 — levee du verrou
   pour ce fichier precis.
2. `Implementation/ebta_engine/benchmarks/long_data.py` lignes 1-30
   (imports, `importlib.metadata` deja importe) et 483-492
   (`_environment_report`).
3. `Implementation/ebta_engine/tests/test_long_data_benchmark.py` ligne 105
   (`run_benchmark` appele, chemin d'erreur reel).

**Hierarchie d'autorite applicable a ce chantier** :

```text
1. Protocole/ (non touche)
2. Implementation/ebta_engine/benchmarks/long_data.py (cible unique, verrou leve)
3. Le reste de Implementation/ (non touche)
```

Regle : si le paquet Nautilus est absent, la fonction doit retourner une
valeur explicite plutot que de deviner ou de crasher silencieusement dans
un contexte englobant.

---

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

| Module actuel | Chemin | Role reel (verifie, pas suppose) | Suffisant pour l'objectif ? |
| --- | --- | --- | --- |
| `_environment_report()` | `Implementation/ebta_engine/benchmarks/long_data.py:483-492` | Construit un dict d'informations d'environnement (version Python, OS, CPU, memoire) inclus dans le rapport de benchmark. Ligne 487 appelle `importlib.metadata.version("nautilus_trader")` sans garde. | ⚠️ a corriger — un seul appel non protege |
| Import `importlib.metadata` | `long_data.py:8` | Deja importe en tete de fichier. | ✅ suffisant — pas de nouvel import necessaire |

### Ce qui manque reellement

| Brique manquante | Module a creer/modifier | Source de la regle | Ce qui existe deja et doit etre reutilise |
| --- | --- | --- | --- |
| Garde `PackageNotFoundError` | `_environment_report()` (MODIFIER) | Audit source recommandation 3 ; decision humaine section 10 du chantier mere | `importlib.metadata` deja importe |

---

## 5. Decision d'architecture

Principe directeur : la valeur du champ doit rester explicite dans le
rapport persiste, jamais silencieusement absente.

- Raison 1 — catcher precisement `importlib.metadata.PackageNotFoundError`,
  jamais `except Exception` generique : coherent avec le seul pattern deja
  juge sain par l'audit source dans `governance/` (echec explicite, jamais
  un defaut positif implicite qui masquerait une autre cause d'echec).
- Raison 2 — valeur sentinelle `"NOT_INSTALLED"` (chaine), pas `None` :
  plus explicite dans un JSON persiste, distingue "paquet absent, verifie"
  de "champ non calcule".

### Decisions deja actees

| Decision | Justification |
| --- | --- |
| `"NOT_INSTALLED"` plutot que `null` | Le chantier mere autorise les deux (`null` / `"NOT_INSTALLED"`) ; la chaine explicite est retenue pour eviter toute confusion avec un champ manquant ailleurs dans le rapport JSON. |
| Catch cible sur `PackageNotFoundError`, jamais `Exception` | Toute autre exception (ex. erreur reseau improbable de `importlib.metadata`) doit continuer a remonter — masquer une cause differente serait un `SILENT_FALLBACK`. |

### Perimetre de fichiers explicite (autorises / interdits)

**Autorises (creer ou modifier)** :

```text
Implementation/ebta_engine/benchmarks/long_data.py    [MODIFIER - Phase 1, _environment_report() uniquement]
0 - HUMAN START HERE/PLAN_GARDE_ENVIRONNEMENT_BENCHMARK_NAUTILUS.md [CREER - brouillon, archive par plan.ps1]
.ai/backlog/fixes/PLAN_GARDE_ENVIRONNEMENT_BENCHMARK_NAUTILUS.md    [CREER - ce fichier]
.ai/checkpoint.json                                    [MODIFIER - uniquement via plan.ps1]
```

**Interdits (ne jamais modifier dans ce chantier)** :

```text
Protocole/                                    [NORME - intouchable]
Implementation/ebta_engine/ (hors long_data.py) [VERROU NON LEVE pour le reste de Implementation/]
Implementation/ebta_engine/tests/test_long_data_benchmark.py [NE PAS AFFAIBLIR - aucune modification requise]
.ai/checkpoint.schema.json                     [CONTRAT GELE]
```

---

## 6. Decoupage en phases

### Phase 1 - Proteger `_environment_report()`

Objectif : `nautilus_trader_version` vaut `"NOT_INSTALLED"` quand le paquet
est absent, au lieu de faire echouer l'appelant.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Encadrer `importlib.metadata.version("nautilus_trader")` d'un
  `try`/`except importlib.metadata.PackageNotFoundError`, retournant
  `"NOT_INSTALLED"` dans le dict en cas d'exception.

Livrables :

- `Implementation/ebta_engine/benchmarks/long_data.py` corrige.

Critere de sortie :

- `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation`
  retourne `219 tests`, `0 error` hors venv Nautilus.

### Chemin critique (ordre des phases)

```mermaid
flowchart LR
    P1["Phase 1 - garde PackageNotFoundError"] --> FIN["Termine"]
```

---

## 7. Artefacts produits

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Phase 1 | `long_data.py` corrige | Python | Audit source recommandation 3 |

---

## 8. Invariants absolus et NO GO

### Invariants (non negociables)

1. Seule `PackageNotFoundError` est capturee, jamais `Exception` generique.
2. La valeur retournee en absence du paquet est une chaine explicite
   (`"NOT_INSTALLED"`), jamais un champ omis ni `null` implicite par accident.

### NO GO

- Catcher `Exception` generique.
- Skipper le test au lieu de le laisser s'executer et produire un rapport.
- Modifier tout autre fichier sous `Implementation/`.

---

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation
```

**Regle transversale bloquante** : la suite complete doit passer a
`219 tests, 0 error` (skips autorises) hors venv Nautilus, sans regression
sur les 218 tests deja verts.

**Notes de portabilite / caveats connus** :

- La correction ne rend pas Nautilus optionnel pour les tests qui en ont
  reellement besoin (aucun test de ce type n'existe aujourd'hui, verifie
  par le lot 5 refuse) — elle rend uniquement ce rapport d'environnement
  robuste a son absence.

**Premier lot executable propose** :

```text
Phase 1 - garde try/except dans _environment_report()
```

### Execution sans interruption

Ce plan s'execute integralement en une seule phase, sans decision humaine en
attente (verrou deja leve).

### Autorite decisionnelle accordee

L'IA qui execute ce plan decide seule des details d'implementation dans le
perimetre de la section 5.

### Interdiction des raccourcis (aucun faux succes)

- Ne jamais elargir le catch a `Exception` pour "faire passer" le test plus
  largement que necessaire.
- Ne jamais presenter `"NOT_INSTALLED"` comme une preuve que Nautilus
  fonctionne — c'est une preuve d'absence, pas de fonctionnement.

---

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-07 | **Verrou `Implementation/` leve pour le lot 3.** Autorise la modification de `Implementation/ebta_engine/benchmarks/long_data.py` pour y ajouter la garde d'environnement (journalise dans `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md`, section 10). | Autorise ce seul fichier, pour cette seule correction. La garde doit enregistrer une valeur explicite (`null` / `"NOT_INSTALLED"`) et ne jamais masquer l'absence du paquet. |

---

## 11. Risques et blocages connus

| Risque | Impact | Mitigation / condition de deblocage |
| --- | --- | --- |
| Une autre exception (reseau, corruption de metadata) masquee par erreur | Cause d'echec differente cachee | Catch cible sur `PackageNotFoundError` uniquement (invariant 1) |

---

## 12. Definition of Done

- [x] Phase 1 executee et verifiee (section 9).
- [x] Exit criteria de la section Triage atteint et verifiable.
- [x] Aucune modification hors perimetre (section 5).
- [x] Aucune regression sur la suite de tests existante.
- [x] Checklist post-modification du projet executee.
- [x] Aucune implementation partielle presentee comme terminee.

---

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | DONE — `_environment_report()` retourne desormais `"NOT_INSTALLED"` pour `nautilus_trader_version` hors venv Nautilus au lieu de lever `PackageNotFoundError` ; suite complete `219 tests, 0 error` (skips=6) hors venv. |
| Ecarts par rapport au plan initial | Aucun. Implementation strictement conforme a la section 5 (nouvelle fonction `_nautilus_trader_version()` extraite, seul `_environment_report()` modifie pour l'appeler). |
| Suites a prevoir (hors perimetre de ce plan) | Ce lot debloque la partie `pre-push` du lot 2 et le lot 6 (CI), tous deux conditionnes par une suite verte. Hors-scope trouve par le bug-hunter : 3 erreurs Pyrefly preexistantes (`ctypes.WinDLL` non declare par le stub, lignes 407/448-449, confirmees anterieures a ce lot via `git show d18f468`) — flagge separement, pas corrige ici (hors perimetre section 5 : "`_environment_report()` uniquement"). |

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Champ | Valeur |
| --- | --- |
| Date | 2026-08-07 |
| Phases executees | Phase 1 (unique) |
| Artefact produit | `Implementation/ebta_engine/benchmarks/long_data.py` (`_nautilus_trader_version()` nouvelle fonction, `_environment_report()` l'appelle). |
| Validation | PASS — `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation` -> `Ran 219 tests`, `OK (skipped=6)`, zero erreur. Verification directe : `_environment_report()["nautilus_trader_version"] == "NOT_INSTALLED"` hors venv Nautilus. |
| Ecart par rapport au plan | Aucun. |

#### bug-hunter (Pyrefly, fichier touche)

Environnement : `Implementation/adapters/nautilus_env/venv` (chemin standard
documente par `CLAUDE.md`) est absent de ce worktree ; Pyrefly installe a la
place via `pip install --user pyrefly` (outillage dev ponctuel, decision
humaine deja actee le 2026-07-14 pour Pyrefly en general — voir
`.agents/skills/bug-hunter/SKILL.md` — aucune dependance runtime ajoutee au
moteur, rien commite dans le depot).

```
python -m pyrefly check Implementation/ebta_engine/benchmarks/long_data.py --output-format min-text
```

Resultat : 3 erreurs, toutes sur `ctypes.WinDLL` (lignes 407, 448, 449),
**toutes preexistantes** — confirme par `git show d18f468:Implementation/ebta_engine/benchmarks/long_data.py`
(SHA de baseline de ce lot, avant implementation) : les trois lignes y sont
identiques. Triage : **FAUX POSITIF D'OUTILLAGE** — `ctypes.WinDLL` est un
attribut Windows reel et valide a l'execution (la suite complete passe,
219 tests OK) ; le stub typeshed utilise par Pyrefly ne le declare pas pour
la cible de plateforme par defaut. Meme classe que les faux positifs
numpy/pandas deja documentes par `bug-hunter/SKILL.md`. Hors perimetre de ce
lot (section 5 : `_environment_report()` uniquement, pas
`_process_tree_rss_bytes()`/`_visible_memory_bytes()`) — flagge separement
(tache de suivi spawnee), pas corrige ici pour ne pas depasser le perimetre
declare. **Zero erreur sur le code ajoute par ce lot** (`_nautilus_trader_version()`,
lignes ajoutees) : les 3 erreurs portent exclusivement sur du code
preexistant non touche.

#### adversarial-tester (cible : `_environment_report()`, ecrit un artefact persiste `reports/*.json`-like)

Le rapport de benchmark produit par `run_benchmark()` est ecrit sur disque
(`_write_json_atomic`) — dans le perimetre d'invocation recommandee du
skill (artefact persiste).

| Point teste | Entree hostile | Observation avant correction | Observation apres correction | Classification | Preuve |
| --- | --- | --- | --- | --- | --- |
| Paquet `nautilus_trader` absent | Environnement hors venv Nautilus (cas reel de ce worktree) | `PackageNotFoundError` non catchee : `run_benchmark()` levait une exception Python non geree — echec bruyant, pas un faux succes, mais un crash total du benchmark plutot qu'un rapport gracieux | `nautilus_trader_version` vaut `"NOT_INSTALLED"` ; le reste du rapport (`status`, `canonical`, `pipeline_cells`) continue de refleter les statuts reels des cellules, inchange par ce champ | `PASS_ADVERSARIAL` (apres correctif) — aucun `FALSE_SUCCESS` : le champ verite (`status`/`canonical`) ne depend jamais de `nautilus_trader_version`, verifie par lecture du code (ligne 117, 120-121) | Execution directe de `_environment_report()` ci-dessus + lecture de `run_benchmark()` lignes 117-121 |
| Exception autre que `PackageNotFoundError` (ex. metadonnees corrompues) | Non provoquee physiquement (necessiterait de corrompre l'index de paquets Python) | N/A | Continuerait de se propager sans etre masquee — catch cible exclusivement sur `PackageNotFoundError` | `PASS_ADVERSARIAL` (par lecture de code, invariant 1) | Lecture directe de `_nautilus_trader_version()` : un seul `except importlib.metadata.PackageNotFoundError` |

Aucun `FALSE_SUCCESS` ni `SILENT_FALLBACK` trouve. Le correctif transforme
un crash total (echec bruyant mais total) en un rapport complet avec un
champ informatif explicite — pas une degradation du niveau de verite du
rapport.

#### plan-conformance-audit

| Exit criterion | Classification | Preuve |
| --- | --- | --- |
| (1) `219 tests, 0 error` hors venv Nautilus | IMPLEMENTE | `python -m unittest discover ...` -> `Ran 219 tests`, `OK (skipped=6)`. |
| (2) `nautilus_trader_version` vaut `"NOT_INSTALLED"` explicite quand le paquet est absent | IMPLEMENTE | Verification directe ci-dessus. |
| (3) Aucune autre modification de `Implementation/` que ce fichier | IMPLEMENTE | `git diff --stat` limite a `Implementation/ebta_engine/benchmarks/long_data.py` (verifie avant commit). |
| Non-goals respectes (aucune autre fonction modifiee, aucun test skippe) | IMPLEMENTE | Seule `_environment_report()`/`_nautilus_trader_version()` touchees ; `test_long_data_benchmark.py` non modifie, aucun `@skip`. |

Aucun critere MANQUANT. Aucun `Non-goals` viole. Cloture autorisee.

---

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-08-07 | Boucle `/evaluate` d'intake, 2 passes convergees sur le brouillon (`0 - HUMAN START HERE/PLAN_GARDE_ENVIRONNEMENT_BENCHMARK_NAUTILUS.md`). Confirmation par grep qu'aucun autre site du depot n'appelle `importlib.metadata.version("nautilus_trader")` ni ne consomme `nautilus_trader_version` en dehors de sa production. Aucun angle mort majeur trouve. | Confirmer que la correction est strictement locale et n'a pas d'effet de bord sur un consommateur existant du champ. |
