# Brouillon — Phase 1 gouvernance déclarative et preuve de session

## But

Exécuter la Phase 1 de la feuille de route issue du brouillon archivé du
2026-07-29, désormais débloquée par la clôture `DONE` de la Phase 0 :

1. créer un `POLICIES.md` minimal et déclaratif qui consolide, sans les
   remplacer, les autorisations déjà dispersées dans `AGENTS.md` et
   `.ai/governance/` ;
2. créer un gabarit structuré de preuve de session portant au minimum
   `task_id`, `objective`, `tests_executed`, `claims` et `evidence`.

## Résultat du test multi-lot

`MULTI_LOT` : les deux artefacts ont des critères de sortie indépendants,
peuvent être livrés dans un ordre différent et un blocage de l'un n'empêche pas
l'autre d'avancer. Ils doivent donc suivre deux cycles séparés.

## Lots proposés

| # | ID | Livrable |
| --- | --- | --- |
| 1 | `PLAN_POLICIES_DECLARATIF_IA` | `POLICIES.md` à la racine, table Action / Autorisée ? / Conditions / Validation requise, pointeurs vers les autorités existantes. |
| 2 | `PLAN_GABARIT_PREUVE_SESSION_IA` | `.ai/governance/TEMPLATE_PREUVE_SESSION_IA.json`, JSON valide et copiable avec champs fixes `task_id`, `objective`, `tests_executed`, `claims`, `evidence`, risques et portée ; mise à jour du README de gouvernance. |

Le chantier mère coordonne seulement ces deux lots. Il ne crée aucun artefact
de fond et ne modifie pas le protocole.

## Garde-fous

- `POLICIES.md` est un index déclaratif, jamais une autorité scientifique ni
  un Policy Engine mécanisé.
- Le gabarit de preuve ne devient ni un checkpoint, ni un journal runtime, ni
  une obligation mécanique non implémentée. `python -m json.tool` prouve
  uniquement sa forme JSON, pas la véracité d'une preuve remplie.
- Aucune règle nouvelle n'est inventée : chaque ligne de policy cite sa source.
- Aucun changement dans `Protocole/` ou `Implementation/`.
- `.ai/lessons-learned/` reste hors scope : la feuille de route Phase 1 ne
  retient que `POLICIES.md` et la preuve de session.

## Journal `/evaluate`

| Passe | Résultat |
| --- | --- |
| 1 | Format et autorité clarifiés : template JSON documentaire sous `.ai/governance/`, sans faux gate mécanique ; périmètre du lot 2 fixé au template et au README. |
| 2 | Convergence : séparation des deux lots confirmée ; `lessons-learned/`, Policy Engine mécanisé, workflows interface et toute mutation runtime explicitement hors scope. Aucun nouvel angle mort majeur. |
