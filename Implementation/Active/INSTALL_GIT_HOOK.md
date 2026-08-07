# Installation des hooks git EBTA

Deux hooks versionnes protegent ce depot :

| Hook | Source versionnee | Declencheur | Duree typique |
| --- | --- | --- | --- |
| `pre-commit` | `Implementation/Active/pre_commit_hook.py` | Un commit qui touche le cockpit IA (`.ai/README.md`, `.ai/checkpoint.json`, `.ai/checkpoint.schema.json`, `.ai/backlog/`, `.ai/tools/`) ou `.ai/checkpoint.json`/`Implementation/Active/tracking.json` specifiquement | < 1 s |
| `pre-push` | `Implementation/Active/pre_push_hook.py` | Tout push, sans condition | ~45-50 s (suite complete) |

## Pourquoi deux hooks distincts, pas un seul

- `pre-commit` s'active uniquement si un fichier du cockpit IA est stage :
  un commit purement `Implementation/` (le risque prioritaire de ce depot,
  l'erreur d'un agent de codage) ne le declenche pas. La suite de tests
  complete est trop lente (~45-50 s) pour tourner a chaque commit (frequent).
- `pre-push` tourne sur **tout** push, sans condition, et ferme exactement
  cet ecart : peu importe ce qui a change, la suite de reference doit passer
  avant qu'un push quitte la machine. Les push sont rares ; le cout est
  acceptable a cette frequence.
- Les deux restent des garde-fous locaux, contournables par
  `--no-verify` sans laisser de trace. Le verdict independant que l'agent ne
  controle pas est la CI GitHub (`PLAN_CI_GITHUB_VERDICT_INDEPENDANT`), pas
  ces hooks.

## Ce que `pre-commit` verifie

1. **Fraicheur de `checkpoint.json`** (comportement historique, inchange) :
   si `checkpoint.updated_at` est anterieur au dernier commit alors qu'un
   fichier du cockpit IA est stage, le commit est bloque.
2. **Schema JSON de `checkpoint.json`/`tracking.json`** (nouveau) : si l'un
   de ces deux fichiers est stage, son contenu doit satisfaire son schema
   (`checkpoint.schema.json`/`tracking.schema.json`). Utilise `jsonschema`
   (couverture complete, y compris `pattern`/`format`/`uniqueItems`/
   `maxItems`) s'il est installe ; sinon, se replie sur le validateur
   interne `ebta_engine.schema_validation` avec un avertissement explicite
   de couverture partielle (`pattern`/`format`/`uniqueItems`/`maxItems` non
   verifies par le repli). `jsonschema` n'est **pas** une dependance
   requise pour cloner et committer dans ce depot — seul le runner CI est
   autorise a l'installer (decision humaine du 2026-08-07,
   `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md` section 10).

## Ce que `pre-push` verifie

Execute `python -m unittest discover -s Implementation/ebta_engine/tests -t
Implementation` (la commande canonique de ce depot) avant tout push. Un
echec bloque le push.

## Installation (une seule fois par clone)

```powershell
# Depuis la racine du repo. Copie binaire (mode 'rb'/'wb') pour eviter toute
# translation de fin de ligne silencieuse entre la source et la copie
# installee (une copie texte convertit LF -> CRLF sur Windows, ce qui rend
# "git diff --no-index" ci-dessous bruyant sans changer le comportement).
python -c "import shutil; shutil.copy2('Implementation/Active/pre_commit_hook.py', '.git/hooks/pre-commit')"
python -c "import shutil; shutil.copy2('Implementation/Active/pre_push_hook.py', '.git/hooks/pre-push')"
```

Si Python n'est pas dans le PATH, adapter le chemin. Sur un depot utilisant
des worktrees git, les hooks sont partages par tous les worktrees (ils
vivent dans le repertoire `.git` commun, pas dans le `.git` par worktree) :
une seule installation suffit pour tous les worktrees d'un meme clone.

Verifier apres installation que la copie installee correspond exactement a
la source versionnee (aucune derive silencieuse) :

```powershell
git diff --no-index Implementation/Active/pre_commit_hook.py "$(git rev-parse --git-common-dir)/hooks/pre-commit"
git diff --no-index Implementation/Active/pre_push_hook.py "$(git rev-parse --git-common-dir)/hooks/pre-push"
```

Une sortie vide sur les deux commandes confirme l'identite.

## Comportement de `pre-commit` (fraicheur)

- Le hook s'active si `.ai/checkpoint.json` ou un fichier de gouvernance `.ai/`
  est en staging.
- Si checkpoint.updated_at est anterieur ou egal au timestamp du dernier
  commit, le hook bloque avec un message explicite.
- Le hook ne valide pas semantiquement le contenu du checkpoint au-dela de
  son schema (voir ci-dessus) et de sa fraicheur.

## Contournement (urgence uniquement)

```powershell
git commit --no-verify
git push --no-verify
```

**A utiliser uniquement en urgence, avec une entree de justification dans
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md.** Ce contournement
ne laisse aucune trace mecanique — c'est exactement la limite que la CI
GitHub (`PLAN_CI_GITHUB_VERDICT_INDEPENDANT`) est concue pour combler.

## Sources de controle

- `AGENTS.md` pour le bootstrap IA officiel.
- `.ai/README.md` pour les regles stables du cockpit IA.
- `.ai/checkpoint.json` champ `updated_at`.
- `.ai/checkpoint.schema.json` / `Implementation/Active/tracking.schema.json`
  pour la structure des fichiers d'etat.
- Audit externe 2026-06-29, point P2 (hook pre-commit original).
- `0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`,
  recommandation 2 (extension schema + hook pre-push).
