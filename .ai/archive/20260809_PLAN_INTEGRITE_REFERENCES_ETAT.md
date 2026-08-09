# Plan d'implementation — Integrite des references d'etat

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Parent | `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA` `BASELINED`, enfants 1-7 `DONE`. |
| Test multi-lot | `SINGLE_CHANTIER` : corrections de donnees et ratchet partagent le meme invariant de resolution. |
| Exception historique | Une seule : plan RAG `REJECTED`, supprime manuellement et closure_reason explicite. |
| Mutation normative | Aucune ; etat de gouvernance/runtime seulement. |

## Audit IA de promotion

- [x] Bootstrap, cockpit, schemas, proprietaires et audit source relus.
- [x] Toutes les references `source_path`, `original_draft_path` et `active_runtime_path` inventoriees.
- [x] Deux pointeurs obsoletes vers des archives existantes confirmes.
- [x] Absence RAG confrontee au lifecycle `REJECTED` et au motif de cloture.
- [x] `active_scope` distingue chemins (slash) et description textuelle.
- [x] Appelants `plan.ps1` verifies ; aucune migration schema requise.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage ; non executable avant baseline |
| Type de chantier | `SINGLE` |
| Classification | `CONTRACT_ENCODING` |
| Scope | Corriger deux references archivables et bloquer les references mortes futures du checkpoint/tracking dans le pre-commit. |
| Non-goals | Aucun faux artefact RAG, aucune migration schema, aucun changement de workflow state, Protocole, BACKTRADER, Pyrefly/Ruff CI ou setting GitHub. |
| Source | Epic parent enfant 8/10 ; audit du 2026-08-08 lignes 570-613, 707-755 et 875-884. |
| Exit criteria | Deux pointeurs corriges, exception RAG exacte et explicite, garde fail-closed/stale, hook et suite verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `DONE` |
| Date | 2026-08-09 |
| Autorite normative | Aucune. |
| Autorite de donnees | `.ai/checkpoint.json` pour macro ; `Implementation/Active/tracking.json` pour micro. |
| Impact protocole | Aucun ; Guardian `CONTRACT_ENCODING`. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Rendre une reference morte impossible a committer silencieusement. |
| Lecture minimale | Checkpoint/tracking/schemas, hook/tests, plans archives cibles. |
| Preuve | Scan exhaustif, tests hostiles, hook cible, inventaire et suite. |
| Arret | Ambiguite sur la nature d'un champ ou besoin de fabriquer un artefact absent. |

## 1. Role et non-objectifs

Le garde valide l'existence et la surete lexicale des chemins, pas leur
contenu semantique. Il ne cree aucune nouvelle source d'etat. Les corrections
restent dans les deux proprietaires existants.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap/cockpit, parent et audit source.
2. Checkpoint, tracking et leurs schemas.
3. `plan.ps1`, `pre_commit_hook.py`, documentation d'installation et tests.
4. Les trois workstreams/archives concernes.

## 3. Etat des lieux

| Reference | Etat | Decision |
| --- | --- | --- |
| Biais EBTA `source_path` | backlog absent, archive `20260701_...` presente | Corriger vers l'archive. |
| Tracking plan Nautilus | backlog absent, archive `20260710_...` presente et deja pointee par HOOK/checkpoint | Corriger vers l'archive. |
| RAG rejete `source_path` | fichier supprime manuellement, motif explicite | Conserver l'absence ; exception exacte auditable. |

Tous les autres champs `*_path`, `hook_file` et elements path-like de
`active_scope` resolvent actuellement.

## 4. Gates

| Gate | PASS | Sinon |
| --- | --- | --- |
| Surete | Chemin relatif, sans `..`, dans le depot | FAIL |
| Existence | Fichier ou dossier cible existe | FAIL |
| Exception | Tuple ID/champ/chemin/lifecycle/motif exacte | FAIL |
| Stale exception | Exception encore consommee par une absence | Sinon FAIL |
| Integration | Controle execute par `main()` pour tout commit non vide | FAIL |
| Regression | Tests/inventaire/suite et deux schemas verts | FAIL |

## 5. Decision d'architecture

Le garde vit dans `pre_commit_hook.py`, deja source versionnee du hook, plutot
que dans un nouveau script concurrent. Il parcourt recursivement les cles
`*_path` du checkpoint, puis `hook_file` et les chaines de `active_scope`
contenant un separateur de chemin. Les descriptions libres sans slash ne
sont pas traitees comme chemins.

L'exception RAG est une constante exacte incluant ID, champ, valeur,
lifecycle et fragment attendu du `closure_reason`. Si le fichier reapparait,
si l'entree disparait ou si un attribut change, l'exception devient stale et
le commit echoue : elle ne peut pas devenir un trou generique.

## 6. Perimetre de fichiers

Autorises :

```text
.ai/checkpoint.json
Implementation/Active/tracking.json
Implementation/Active/pre_commit_hook.py
Implementation/Active/INSTALL_GIT_HOOK.md
Implementation/ebta_engine/tests/test_git_hooks.py
Implementation/ebta_engine/tests/test_inventory.txt
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md
.ai/backlog/mainline/PLAN_INTEGRITE_REFERENCES_ETAT.md
.ai/archive/20260809_PLAN_INTEGRITE_REFERENCES_ETAT.md
0 - HUMAN START HERE/archive/20260809_PLAN_INTEGRITE_REFERENCES_ETAT.md
0 - HUMAN START HERE/AUDIT_BUG_HUNTER_PLAN_INTEGRITE_REFERENCES_ETAT_2026-08-09.md
0 - HUMAN START HERE/AUDIT_ADVERSARIAL_PLAN_INTEGRITE_REFERENCES_ETAT_2026-08-09.md
0 - HUMAN START HERE/AUDIT_CONFORMITE_PLAN_INTEGRITE_REFERENCES_ETAT_2026-08-09.md
```

Interdits : schemas JSON, `plan.ps1`, workflow contracts, autres fichiers
Active, Protocole, BACKTRADER, CI Pyrefly/Ruff et settings GitHub.

## 7. Decoupage en phases

### Phase 1 — Donnees

Corriger les deux chemins vers leurs archives existantes et dater le tracking.

### Phase 2 — Garde

Ajouter le scan, l'exception exacte, les diagnostics et l'appel dans `main()`.
Documenter que le hook s'execute desormais sur tout commit non vide.

### Phase 3 — Ratchet et verification

Tester chemins valides, absents, absolus/traversants, exception consommee et
stale, tracking path-like/prose, puis executer suite et audits.

## 8. Invariants et NO GO

1. Checkpoint et tracking restent les seuls proprietaires de leurs etats.
2. Aucun chemin absolu ou traversal n'est accepte.
3. Une absence historique n'est jamais transformee en fichier fictif.
4. Une closure_reason arbitraire ne cree pas une exception.
5. Le garde s'execute meme si le commit deplace un fichier reference sans
   modifier le JSON.

NO GO : schema nullable, allowlist par lifecycle generique, warning-only sur
un nouveau chemin mort, auto-correction, creation de tombstone RAG.

## 9. Verification a chaque etape

```powershell
python -m unittest Implementation.ebta_engine.tests.test_git_hooks
python -m unittest Implementation.ebta_engine.tests.test_test_inventory
python -m jsonschema -i .ai/checkpoint.json .ai/checkpoint.schema.json
python -m jsonschema -i Implementation/Active/tracking.json Implementation/Active/tracking.schema.json
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | Audit consolide. | Corriger deux pointeurs et documenter, sans falsifier, l'absence RAG. |
| 2026-08-09 | `/continue` persistant. | Autorise l'enfant 8 local, pas de nouveau contrat normatif. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| Exception trop large | Tuple complete et stale-check. |
| Faux positif sur texte libre | `active_scope` path-like seulement si slash/backslash. |
| Deplacement non detecte | Scan sur tout commit non vide. |
| Cout du hook | Deux petits JSON et tests cibles ; mesurer l'execution. |
| Etat invalide avant le garde | Parse JSON fail-closed ; schema reste controle separement. |

## 12. Definition of Done

- [x] Deux pointeurs corriges vers archives existantes.
- [x] Exception RAG exacte, expliquee et stale-checkee.
- [x] Chemins absents/dangereux bloquants dans le hook.
- [x] Documentation d'installation coherente.
- [x] Ratchet, inventaire, schemas et suite complete verts.
- [x] Audits sans finding bloquant.
- [x] Aucun fichier interdit touche.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | Scan reel : 0 erreur, 1 absence historique documentee ; 26 tests hook + inventaire verts ; suite canonique 289 tests `OK` (1 skipped) ; deux schemas PASS ; Pyrefly portable 0 erreur. |
| Ecart | Aucun. Le scan Pyrefly brut du venv allégé conserve 2 `missing-import` jsonschema preexistants ; l'option portable autorisee les neutralise sans masquer les diagnostics internes. |
| Suite | Enfant 9/10 `PLAN_PYREFLY_CI_NOTEBOOK`. |

## 14. Journal d'audits post-route

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Option schema nullable confrontee a `plan.ps1` et a l'autorite du checkpoint. | Rejetee : elle elargirait le contrat pour un seul cas historique et fragiliserait les appelants. |
| 2 | Exception generique par lifecycle confrontee aux contournements. | Rejetee : exception exacte avec motif et stale-check ; scan sur tout commit. Convergence. |

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Releve exhaustif des chemins et archives. | Trois anomalies classees : deux corrections, une absence expliquee. |
| 2 | Schemas, outils et hook confrontes au design. | Aucun schema/outillage workflow modifie ; garde fail-closed converge. |
