# Brouillon — Lot 2 : etendre `pre-commit` et ajouter `pre-push`

Track : fix
Lifecycle : INTAKE
Scope : Etendre `Implementation/Active/pre_commit_hook.py` a la validation de
schema JSON de `checkpoint.json`/`tracking.json` avant tout commit qui les
touche, et creer la source versionnee d'un hook `pre-push`
(`Implementation/Active/pre_push_hook.py`) executant la suite de tests
canonique avant tout push, puis installer les deux copies et verifier leur
identite avec la source.
Non-goals : Ne modifie jamais `.git/hooks/*` directement — seulement la
source versionnee, ensuite reinstallee. Ne rend `jsonschema` obligatoire
pour committer localement (seul le runner CI, lot 6, est autorise a
l'installer). N'ajoute aucune verification Pyrefly au hook (trop lent pour
`pre-commit`, hors perimetre de `pre-push` qui ne fait que la suite
canonique).
Source : Sous-chantier 2/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`,
Phase 3. Recommandation 2 de l'audit source
`0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`.
Depend du lot 3 (`DONE`) : la suite doit etre verte avant qu'un hook
`pre-push` bloquant existe, sinon il est ignore/contourne des sa premiere
execution.
Exit criteria : (1) un `checkpoint.json` volontairement invalide (viole son
schema) est bloque au commit ; (2) un `tracking.json` volontairement invalide
est bloque au commit ; (3) un test volontairement casse est bloque au push ;
(4) la copie installee de chaque hook est identique octet-pour-octet a sa
source versionnee ; (5) `python -m unittest discover -s
Implementation/ebta_engine/tests -t Implementation` retourne `0 error`.

## Contraintes techniques deja etablies (a respecter)

1. `jsonschema` n'est autorise que cote CI (decision humaine section 10 du
   chantier mere) — le hook local doit fonctionner sans, avec repli sur le
   validateur interne `ebta_engine.schema_validation` et un avertissement
   explicite de couverture partielle si `jsonschema` est absent.
2. Deux hooks distincts (pas un seul surcharge) : `pre-commit` reste rapide
   (< 1 s), `pre-push` porte la suite complete (~45-50 s), car les commits
   sont frequents et les push rares.
3. Le lot 3 doit etre livre avant : verifie, deja `DONE`.
4. `Implementation/Active/pre_commit_hook.py` est la source versionnee ;
   `.git/hooks/pre-commit` est la copie installee, jamais modifiee
   directement.

## Boucle `/evaluate` d'intake (2 passes, convergee)

**Passe 1** — Verification du format des schemas cibles : `checkpoint.schema.json`
et `tracking.schema.json` utilisent tous deux `pattern`, `format`,
`uniqueItems` — hors du sous-ensemble supporte par le validateur interne
`ebta_engine.schema_validation` (documente : `type, required, properties,
items, enum, additionalProperties, minItems` seulement). Confirme que
`jsonschema` (deja installe dans cet environnement, verifie par
`pip show jsonschema` -> 4.23.0) doit rester le validateur prioritaire, avec
repli explicite plutot que silencieux.

**Passe 2** — Verification qu'aucun appelant/test existant ne serait casse
par l'extension du hook (le hook n'a aujourd'hui aucun test — zero risque
de regression testee, mais aussi zero garde-fou existant : un harnais de
test complet est ajoute par ce lot, pas seulement le code du hook). Les
worktrees git partagent le meme repertoire `.git/hooks` (verifie via `git
rev-parse --git-common-dir`) : une seule installation suffit par clone,
documente dans `INSTALL_GIT_HOOK.md`. Convergence a 2 passes sur 6
autorisees.
