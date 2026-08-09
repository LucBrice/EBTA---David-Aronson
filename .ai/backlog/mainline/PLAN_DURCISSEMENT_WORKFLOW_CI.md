# Plan d'implementation — Durcissement du workflow CI

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Coordinateur parent | `PLAN_DURCISSEMENT_CI_SUPPLY_CHAIN` `BASELINED`, jamais active directement. |
| Workstream actif concurrent | Aucun. |
| Test multi-lot | `SINGLE_CHANTIER` : permissions, pins et ratchet portent le meme rollback workflow. |
| Mutation GitHub externe | Interdite ; seuls fichiers versionnes locaux. |

## Audit IA de promotion

- [x] Workflow, audit source et coordinateur lus.
- [x] Tags d'actions resolus sur les depots officiels par `git ls-remote`.
- [x] Trois installations pip directes inventoriees.
- [x] Suite et validations JSON existantes preservees.
- [x] Frontieres 7B/8/9/10 fermees.
- [x] Baseline : 274 tests `OK`.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage ; non executable avant baseline |
| Type de chantier | `SINGLE` |
| Classification | `CONTRACT_ENCODING` |
| Scope | Encoder least privilege et reproductibilite directe du workflow CI, avec test de non-regression stdlib. |
| Non-goals | Aucun setting GitHub, push, nouveau job/outillage, lock transitif, Dependabot, cache, Pyrefly, Ruff, gitignore, chemin d'etat, Protocole ou BACKTRADER. |
| Source | Coordinateur 7, audit du 2026-08-08 lignes 869-874. |
| Exit criteria | Actions couvertes sur SHA exact commente, `contents: read`, credentials non persistes, trois pins pip exacts, suite/JSON steps conserves, ratchet et suite verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date | 2026-08-09 |
| Autorite normative | Aucune. |
| Autorite executable | `.github/workflows/ebta-runtime-suite.yml`. |
| Impact protocole | Aucun ; Guardian `CONTRACT_ENCODING`. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Eliminer les tags/actions et installations directes flottantes sans changer la mission du job. |
| Lecture minimale | Workflow, ce plan, audit source et test inventory. |
| Preuve | Test ratchet exact, parse YAML local, suite canonique. |
| Arret | Pin incompatible ou besoin de mutation GitHub externe. |

## 1. Role et non-objectifs

Le workflow reste la source de verdict independante existante. Ce plan ne
change ni ses triggers, ni `ubuntu-latest`, ni Python 3.13, ni les commandes
unittest/schema. Il durcit seulement les dependances et autorisations deja
consommees.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap/cockpit et coordinateur 7.
2. `.github/workflows/ebta-runtime-suite.yml` integral.
3. Audit source lignes 749-765 et 867-897.
4. Inventaire canonique des tests.

## 3. Etat des lieux

| Element | Actuel | Cible |
| --- | --- | --- |
| Checkout | `actions/checkout@v4` | `11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2` |
| Setup Python | `actions/setup-python@v5` | `a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0` |
| Permissions | implicites | `contents: read` au workflow |
| Credentials | comportement action par defaut | `persist-credentials: false` |
| jsonschema | flottant | `4.23.0` |
| numpy | flottant | `2.2.6` |
| pandas | flottant | `2.3.3` |

Les SHA ont ete resolus sur les remotes officiels le 2026-08-09. Les versions
Python sont observees sous Python 3.13 et la suite locale est verte.

## 4. Gates

| Gate | PASS | Sinon |
| --- | --- | --- |
| Actions | Deux SHA 40 hex exacts et commentaires de version | FAIL ratchet |
| Tags | Aucun `uses: ...@vN/main/master` | FAIL ratchet |
| Permissions | Workflow `contents: read` | FAIL ratchet |
| Credentials | Checkout `persist-credentials: false` | FAIL ratchet |
| Pip | Trois versions exactes via `python -m pip` | FAIL ratchet |
| Fonctionnel | Steps unittest + deux validations JSON inchanges | FAIL ratchet/suite |

## 5. Decision d'architecture

Les pins sont conserves directement dans le workflow, comme l'audit le
demande, plutot que d'introduire un gestionnaire ou lockfile supplementaire.
Le test stdlib du depot duplique intentionnellement les valeurs attendues :
toute mise a jour devient un diff a deux endroits, donc une decision visible.
Les commentaires de versions rendent les SHA revus humainement.

## 6. Perimetre de fichiers

Autorises :

```text
.github/workflows/ebta-runtime-suite.yml
Implementation/ebta_engine/tests/test_ci_supply_chain.py
Implementation/ebta_engine/tests/test_inventory.txt
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md
.ai/backlog/mainline/PLAN_DURCISSEMENT_WORKFLOW_CI.md
.ai/archive/20260809_PLAN_DURCISSEMENT_WORKFLOW_CI.md
.ai/checkpoint.json
0 - HUMAN START HERE/archive/20260809_PLAN_DURCISSEMENT_WORKFLOW_CI.md
0 - HUMAN START HERE/AUDIT_BUG_HUNTER_PLAN_DURCISSEMENT_WORKFLOW_CI_2026-08-09.md
0 - HUMAN START HERE/AUDIT_ADVERSARIAL_PLAN_DURCISSEMENT_WORKFLOW_CI_2026-08-09.md
0 - HUMAN START HERE/AUDIT_CONFORMITE_PLAN_DURCISSEMENT_WORKFLOW_CI_2026-08-09.md
```

Interdits : `.gitignore`, autres workflows, GitHub settings, `pyproject.toml`,
Implementation hors tests/inventaire/historique, Protocole, Active,
BACKTRADER.

## 7. Decoupage en phases

### Phase 1 — Workflow

- permissions minimales ;
- SHA officiels commentes ;
- credentials non persistants ;
- pins exacts avec `python -m pip`.

### Phase 2 — Ratchet

- verifier les deux lignes `uses` exactes ;
- refuser tags/branches mutables ;
- comparer l'ensemble complet des lignes `uses` et `pip install` aux valeurs
  attendues afin qu'une entree flottante additionnelle echoue aussi ;
- verifier permissions, credentials, pins et conservation des trois commandes
  de preuve (suite + deux schemas).

### Phase 3 — Verification

- parse YAML avec l'outil local disponible ;
- tests cibles/inventaire/suite ;
- audits de fermeture.

## 8. Invariants et NO GO

1. Les triggers `push`/`workflow_dispatch` restent.
2. Le runner et Python restent inchanges.
3. Aucun step de preuve n'est retire ou affaibli.
4. Aucun secret ou droit d'ecriture n'est ajoute.
5. Une mise a jour future de SHA/version exige la mise a jour visible du test.

NO GO : curl/script distant, tag mutable, installation `latest`, cache,
nouvel outil, matrice, settings GitHub, push.

## 9. Verification a chaque etape

```powershell
python -c "import yaml; yaml.safe_load(open('.github/workflows/ebta-runtime-suite.yml', encoding='utf-8')); print('YAML_PASS')"
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_ci_supply_chain.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_test_inventory.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | Audit consolide. | Retient pins actions/dependances et permissions minimales ; rejette les outils additionnels. |
| 2026-08-09 | `/continue` persistant. | Autorise le cycle local 7A, pas les settings GitHub. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| SHA opaque | Commentaire tag + ratchet exact. |
| Dependances incompatibles | Versions deja executees sous Python 3.13 ; suite complete. |
| YAML casse | Parse local + test textuel + futur run GitHub apres publication humaine. |
| Faux sentiment de supply-chain totale | Non-goal explicite : pas de lock transitif/SBOM/audit de vulnerabilites. |

## 12. Definition of Done

- [ ] Deux actions sur SHA exact commente.
- [ ] Permissions read-only et credentials non persistants.
- [ ] Trois dependances directes exactement versionnees.
- [ ] Steps de preuve existants conserves.
- [ ] Ratchet, inventaire et suite complete verts.
- [ ] Audits sans finding bloquant.
- [ ] Aucun fichier interdit ou setting externe touche.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | A renseigner. |
| Ecart | A renseigner. |
| Suite | 7B `PLAN_HYGIENE_GITIGNORE_RACINE`. |

## 14. Journal d'audits post-route

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Plan route confronte aux possibilites de contournement par ajout d'une ligne `uses` ou `pip install`. | Ratchet renforce par egalite d'ensemble, pas simple presence des pins attendus. Aucun fichier ajoute au scope. |
| 2 | Relecture des triggers, runner/Python, suite unittest, deux validations JSON et frontieres externes. | Tous restent explicitement conserves ; test stdlib ne depend pas de PyYAML en CI et le parse YAML local reste une preuve additionnelle. Convergence. |

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Workflow et audit source relus. | Scope exact pins/permissions/ratchet. |
| 2 | SHA officiels et versions Python verifies. | Valeurs cibles fixees. |
| 3 | Frontieres enfants relues. | Aucun chevauchement 7B/8/9/10 ; convergence. |
