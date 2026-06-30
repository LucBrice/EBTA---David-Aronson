# Installation du hook git pre-commit EBTA

Ce hook detecte un `.ai/checkpoint.json` stale avant tout commit touchant les
fichiers du cockpit IA actif (`.ai/README.md`, `.ai/checkpoint.json`,
`.ai/checkpoint.schema.json`, `.ai/backlog/`, `.ai/tools/`).

## Pourquoi ce hook existe

L'audit externe (2026-06-29) a identifie le risque R3 : une IA peut reprendre
le relais sur un checkpoint dont updated_at est en retard sur la realite du
repo. Ce hook bloque le commit si le checkpoint n'a pas ete mis a jour.

## Installation (une seule fois par clone)

```powershell
# Depuis la racine du repo
Copy-Item ".git\hooks\pre-commit" ".git\hooks\pre-commit.bak" -ErrorAction SilentlyContinue
# Le hook est deja en place si vous clonez apres cette date.
# S'il est absent, le recreer avec la commande suivante :
python -c "import sys; open('.git/hooks/pre-commit', 'w').write(open('Implementation/Active/pre_commit_hook.py').read())"
```

Si Python n'est pas dans le PATH, adapter le chemin.

## Comportement

- Le hook s'active si `.ai/checkpoint.json` ou un fichier de gouvernance `.ai/`
  est en staging.
- Si checkpoint.updated_at est anterieur ou egal au timestamp du dernier
  commit, le hook bloque avec un message explicite.
- Le hook ne valide pas le contenu du checkpoint, seulement sa fraicheur.

## Contournement (urgence uniquement)

```powershell
git commit --no-verify
```

**A utiliser uniquement en urgence, avec une entree de justification dans
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md.**

## Sources de controle

- `AGENTS.md` pour le bootstrap IA officiel.
- `.ai/README.md` pour les regles stables du cockpit IA.
- `.ai/checkpoint.json` champ `updated_at`.
- `.ai/checkpoint.schema.json` pour la structure du checkpoint.
- Audit externe 2026-06-29, point P2.
