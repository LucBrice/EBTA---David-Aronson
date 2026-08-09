# Audit bug-hunter — PLAN_PYREFLY_CI_NOTEBOOK

Date : 2026-08-09

## Verdict

PASS — zero erreur Pyrefly dans l'environnement equivalent au runner CI.

## Preuves

- Venv Python 3.13 temporaire avec jsonschema 4.23.0, numpy 2.2.6,
  pandas 2.3.3 et Pyrefly 1.1.1.
- Commande portable moteur + notebooks, Nautilus remplace par `Any` :
  0 erreur (1 import externe supprime, warnings non bloquants non affiches).
- 7 tests CI et inventaire : `OK`.
- Suite canonique : 291 tests `OK`, 1 skipped.
- Workflow : `YAML_PASS`.

## Analyse

Le diagnostic initial `package_dir` a disparu apres correction de l'appel.
Aucun `type: ignore`, exclusion du notebook ou remplacement d'un module EBTA
n'a ete utilise. Le seul remplacement vise `nautilus_trader.*`, absent du
runner par decision d'architecture.

## Limite

La preuve est locale dans un environnement equivalent ; aucun run GitHub
distant n'est affirme sans publication.
