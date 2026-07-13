# Observation — Gate economique de production : booleens codes en dur a `True`

> Note d'intake, pas un plan. Depose ici pour triage humain futur, suite a
> l'experience controlee de discrimination des gates
> (`.ai/backlog/annexes/PLAN_EXPERIENCE_CONTROLEE_DISCRIMINATION_GATES.md`,
> cloturee `DONE` le 2026-07-10).

## Constat

`Implementation/ebta_engine/package_builder/nautilus_research_package.py`
(chemin de production du package Nautilus MVP) code ses cinq booleens de
gate economique en dur a `True` avant d'appeler
`SimulationResult.economic_gate_evidence()` :

```python
inputs["economic_gate"] = selected_oos.economic_gate_evidence(
    ...
    return_hurdle_pass=True,
    drawdown_pass=True,
    capacity_pass=True,
    costs_pass=True,
    execution_pass=True,
)
```

`procedures/economic_gate.py::economic_gate_report()` n'agrege que des
booleens deja fournis par l'appelant — il ne les calcule jamais lui-meme
depuis `thresholds`/`observed_values`. Consequence : dans l'etat actuel du
code de production, **le gate economique du package MVP ne peut jamais
rejeter un candidat**, quel que soit son rendement, ses couts ou son
drawdown reels.

## Preuve

L'experience controlee (`.ai/backlog/annexes/PLAN_EXPERIENCE_CONTROLEE_DISCRIMINATION_GATES.md`,
section 4 et section 14) a construit, dans son propre module isole
(`examples/controlled_experiments/gate_discrimination_experiment.py`), une
fonction `compute_economic_pass_flags()` qui calcule honnetement ces cinq
booleens depuis un `SimulationResult` reel, et un test de contraste
permanent (`tests/test_gate_discrimination_experiment.py::test_hardcoded_true_flags_would_let_same_loser_pass`)
qui prouve mecaniquement qu'un candidat perdant a verite connue obtiendrait
`PASS` avec les booleens de production actuels, et `REJECTED_ECONOMIC` avec
un calcul honnete.

## Ce que cette note ne fait PAS

- Elle ne modifie pas `package_builder/nautilus_research_package.py`
  (explicitement hors perimetre du plan qui l'a decouverte).
- Elle ne propose pas de seuils de production — ce choix (SOP 08 : hurdle
  de rendement, drawdown maximal, couts maximaux, capacite) est une
  decision de calibration qui appartient a l'humain, pas a une IA.
- Elle ne cree pas de chantier actif : ce fichier reste `INTAKE`, non
  executable, tant qu'un humain ne l'a pas audite et route vers
  `.ai/backlog/` (mainline, annexe ou fix) selon `.ai/README.md`.

## Question ouverte pour l'humain

Faut-il corriger `nautilus_research_package.py` pour qu'il calcule
reellement ces cinq booleens (en reutilisant `compute_economic_pass_flags()`
ou une fonction equivalente placee dans `package_builder/`), avec quels
seuils de production (SOP 08) ? Ou le MVP reste-t-il volontairement
"tout passe" tant qu'aucune vraie campagne de recherche n'est lancee
dessus ?
