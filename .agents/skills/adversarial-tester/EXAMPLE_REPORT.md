# Exemple de rapport — `_call_float`

## Perimetre

- Point examine :
  `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::_call_float`
  (lignes 163-174 au 2026-07-29).
- Appelants critiques : `_record_nav_snapshot`, puis reconciliation NAV et
  gate G6.
- Source de l'analyse :
  `0 - HUMAN START HERE/archive/20260729_PROPOSITION_FORMALISATION_WORKFLOWS_IA_ADVERSARIAL_EXPERT_PANEL.md`.

## Scenario adversarial

| Element | Preuve |
| --- | --- |
| Entree hostile | La methode externe leve une exception, ou renvoie une valeur impossible a convertir en nombre. |
| Echec attendu | L'extraction refuse explicitement la valeur et empeche le calcul d'un verdict fonde sur une NAV inconnue. |
| Observation actuelle | Les deux branches `except Exception` retournent `0.0`. |
| Effet aval | `0.0` est un nombre plausible ; il alimente `equity` ou `net_exposure`, les snapshots NAV, puis la reconciliation et G6. |
| Controle entree | **FAIL** — l'erreur n'est pas rejetee au point d'entree. |
| Controle resultat | **FAIL/INCONCLUSIVE** — le pipeline peut produire un resultat a partir d'une mesure fabriquee. |
| Classification | `FALSE_SUCCESS` et `SILENT_FALLBACK`. |

## Verdict

**BLOQUANT pour le chantier correctif dedie.** Ce rapport ne corrige pas le
defaut : `Implementation/` est hors perimetre du chantier de formalisation.

La decision humaine D3 est journalisee dans
`.ai/backlog/annexes/PLAN_FORMALISATION_WORKFLOWS_IA_ET_TROIS_SKILLS.md` :
un chantier `fix` separe doit porter la correction. Sa promotion mecanique
via `/start` est une suite explicite hors du present lot ; ne pas presenter
ce workstream comme deja cree dans `.ai/checkpoint.json`.

## Regression exigee du futur chantier `fix`

1. Une exception de la frontiere Nautilus doit produire un echec explicite,
   jamais `0.0`.
2. Une valeur non convertible doit produire un echec explicite.
3. Un mapping monodevise valide doit continuer a produire la valeur attendue.
4. La preuve doit couvrir le point d'entree et le resultat aval G6.

`payload_factory.py::allowed_values` n'est pas un contre-exemple : son repli
sur la valeur par defaut est le comportement voulu de `_axis_combinations`
lorsqu'un axe conditionnel n'est pas applicable.
