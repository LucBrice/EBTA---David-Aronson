# Plan d'implementation — Hygiene `.gitignore` racine

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Coordinateur parent | `PLAN_DURCISSEMENT_CI_SUPPLY_CHAIN` `BASELINED`. |
| Predecesseur | 7A `PLAN_DURCISSEMENT_WORKFLOW_CI` `DONE`. |
| Test multi-lot | `SINGLE_CHANTIER` : politique racine et preuve partagent le meme rollback. |
| Mutation externe | Interdite ; fichiers locaux versionnes uniquement. |

## Audit IA de promotion

- [x] Bootstrap, cockpit, coordinateur et audit source relus.
- [x] Absence de `.gitignore` racine confirmee.
- [x] `Implementation/.gitignore` et fichiers suivis inspectes.
- [x] Aucun fichier suivi actuellement ignore via les regles standard.
- [x] Cas positifs et negatifs determines avant implementation.
- [x] Frontieres workflow CI, Pyrefly/Ruff, Protocole et BACKTRADER fermees.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage ; non executable avant baseline |
| Type de chantier | `SINGLE` |
| Classification | `CONTRACT_ENCODING` |
| Scope | Ajouter un `.gitignore` racine minimal et un test stdlib de ses cas positifs, negatifs et de non-masquage des fichiers suivis. |
| Non-goals | Workflow CI, settings GitHub, `.vscode`, lockfile, Dependabot, Pyrefly/Ruff, Protocole, Active et BACKTRADER. |
| Source | Coordinateur 7B ; audit de robustesse du 2026-08-08 lignes 867-897. |
| Exit criteria | Artefacts locaux cibles ignores, sources utiles non ignorees, aucun fichier suivi masque, inventaire et suite verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `DONE` |
| Date | 2026-08-09 |
| Autorite normative | Aucune. |
| Autorite executable | Regles Git locales versionnees. |
| Impact protocole | Aucun ; Guardian `CONTRACT_ENCODING`. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Partager une hygiene locale minimale sans cacher de source utile. |
| Lecture minimale | Ce plan, coordinateur, `.gitignore` existants, index Git. |
| Preuve | `git check-ignore --no-index`, controle des fichiers suivis, inventaire et suite. |
| Arret | Une regle necessite un glob large ou masque un fichier suivi/utile. |

## 1. Role et non-objectifs

Le fichier racine couvre uniquement les artefacts transverses usuels. Les
regles metier propres aux packages de recherche restent dans
`Implementation/.gitignore`. Ce plan ne generalise pas l'ignore a des
dossiers editeur ou humains.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap et cockpit vivant.
2. Coordinateur 7 et audit source.
3. `Implementation/.gitignore`.
4. Sortie `git ls-files -ci --exclude-standard`.
5. Inventaire canonique des tests.

## 3. Etat des lieux

- `.gitignore` racine absent ;
- `Implementation/.gitignore` contient `__pycache__/`, `*.py[cod]` et
  `research_packages/` ;
- aucun fichier suivi n'est ignore ;
- les reglages Claude locaux ne sont proteges que par une configuration
  utilisateur non partagee.

## 4. Gates

| Gate | PASS | Sinon |
| --- | --- | --- |
| Positif | `.env`, `.env.local`, `.claude/settings.local.json`, venv, caches, logs et temporaires ignores | FAIL |
| Exception | `.env.example` reste visible | FAIL |
| Sources | `.vscode/settings.json`, intakes, Implementation et Protocole restent visibles | FAIL |
| Suivis | `git ls-files -ci --exclude-standard` vide | FAIL |
| Regression | Ratchet, inventaire et suite canonique verts | FAIL |

## 5. Decision d'architecture

Les motifs restent explicites et limites : caches Python, environnements
virtuels nommes, `.env*` avec exception d'exemple, reglage Claude local,
artefacts OS, logs et fichiers `.tmp`. Aucun motif generique de dossier IDE,
Markdown, donnees ou resultats de recherche n'est ajoute.

Le test appelle Git lui-meme avec `--no-index`, afin de verifier la semantique
reelle des motifs plutot que de reimplementer `.gitignore` en Python.

## 6. Perimetre de fichiers

Autorises :

```text
.gitignore
Implementation/ebta_engine/tests/test_root_gitignore.py
Implementation/ebta_engine/tests/test_inventory.txt
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md
.ai/backlog/mainline/PLAN_HYGIENE_GITIGNORE_RACINE.md
.ai/archive/20260809_PLAN_HYGIENE_GITIGNORE_RACINE.md
.ai/checkpoint.json
0 - HUMAN START HERE/archive/20260809_PLAN_HYGIENE_GITIGNORE_RACINE.md
0 - HUMAN START HERE/AUDIT_BUG_HUNTER_PLAN_HYGIENE_GITIGNORE_RACINE_2026-08-09.md
0 - HUMAN START HERE/AUDIT_ADVERSARIAL_PLAN_HYGIENE_GITIGNORE_RACINE_2026-08-09.md
0 - HUMAN START HERE/AUDIT_CONFORMITE_PLAN_HYGIENE_GITIGNORE_RACINE_2026-08-09.md
```

Interdits : modification de `Implementation/.gitignore`, workflow CI,
settings GitHub, `.vscode`, pyproject, Protocole, Active et BACKTRADER.

## 7. Decoupage en phases

### Phase 1 — Politique minimale

Ajouter les motifs explicites et l'exception `.env.example`.

### Phase 2 — Ratchet Git reel

Tester des chemins inexistants avec `git check-ignore --no-index`, puis
verifier que `git ls-files -ci --exclude-standard` reste vide.

### Phase 3 — Verification

Executer tests cibles, inventaire, suite et audits de fermeture.

## 8. Invariants et NO GO

1. Aucun fichier suivi ne devient ignore.
2. `.env.example` reste versionnable.
3. `.vscode/settings.json`, Markdown humain, source Implementation et
   Protocole restent versionnables.
4. `research_packages/` reste sous l'autorite de l'ignore Implementation.
5. Aucun fichier hors scope n'est modifie.

NO GO : `.*`, `*.md`, `data/`, `results/`, `.vscode/`, `Implementation/`,
`Protocole/`, mutation externe ou suppression de regle locale existante.

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_root_gitignore.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_test_inventory.py
git ls-files -ci --exclude-standard
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | Audit consolide. | Retient une hygiene racine minimale ; exclut les mutations GitHub externes. |
| 2026-08-09 | `/continue` persistant. | Autorise le cycle local 7B. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| Glob trop large | Liste negative explicite et controle des fichiers suivis. |
| Resultat dependant du global ignore | Assertions positives et negatives sur motifs du depot ; aucune preuve tiree du seul global exclude. |
| Test hors depot Git | Echec explicite du subprocess. |
| Faux sentiment de securite | Secrets deja suivis ou historique Git explicitement hors capacite de `.gitignore`. |

## 12. Definition of Done

- [x] Politique racine minimale versionnee.
- [x] Cas positifs et negatifs prouves par Git.
- [x] Aucun fichier suivi ignore.
- [x] Ratchet, inventaire et suite complete verts.
- [x] Audits sans finding bloquant.
- [x] Aucun fichier interdit ou mutation externe touche.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | 5 tests gitignore et inventaire verts ; suite canonique 284 tests `OK` (1 skipped) ; Pyrefly 0 erreur ; 4 mutations hostiles rejetees. |
| Ecart | Aucun. Les secrets deja suivis ou presents dans l'historique Git restent hors capacite de `.gitignore`. |
| Suite | Cloture du coordinateur `PLAN_DURCISSEMENT_CI_SUPPLY_CHAIN`. |

## 14. Journal d'audits post-route

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Scope confronte aux motifs larges et aux sources utiles. | Motifs de donnees, resultats, IDE et Markdown rejetes ; liste negative explicite. |
| 2 | Preuve confrontee aux ignores globaux et aux fichiers suivis. | Git est l'oracle ; `--no-index` pour chemins fictifs et `ls-files -ci` pour suivis. Convergence. |

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Racine, ignore Implementation et index Git inspectes. | Etat de depart fixe. |
| 2 | Cas positifs/negatifs et frontieres 7A/8/9/10 relus. | Lot atomique sans chevauchement ; convergence. |
