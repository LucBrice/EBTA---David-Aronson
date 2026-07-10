# HOOK Actif : NautilusTrader MVP cloture

Le chantier mainline `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` est
clos en `DONE` depuis le 2026-07-10.

Source technique archivee :

```text
.ai/archive/20260710_PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md
```

Plan de correction applique :

```text
.ai/backlog/fixes/PLAN_CORRECTION_NAUTILUS_MULTIFOLD_ROBUSTESSE.md
```

## Etat courant

`NAUTILUS_PHASE_5_N4_N5_MULTIFOLD` et `NAUTILUS_PHASE_6_CUTOVER` sont `DONE`.
La correction du 2026-07-10 a remplace l'etat faux `DONE` mono-fold par un
package Nautilus multi-fold reel :

- `Implementation/ebta_engine/data/walk_forward.py` fournit le
  `WalkForwardSplitter` SOP 04 ;
- `Implementation/ebta_engine/risk/robustness.py` fournit les scenarios de
  robustesse pre-OOS SOP 05 ;
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
  orchestre K=2 folds reels sans transmettre Train/Test/OOS au runner Nautilus ;
- `Implementation/research_packages/nautilus_mvp` est reconstruit et valide
  avec `validate_package_dir()` en `PASS`.

## Validations finales

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
# PASS - 110 tests

.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
# PASS - Implementation/research_packages/nautilus_mvp

python -c "from pathlib import Path; from ebta_engine.validators.package_validator import validate_package_dir; print(validate_package_dir(Path('research_packages/nautilus_mvp'))['status'])"
# PASS
```

Les schemas `.ai/checkpoint.json` et `Implementation/Active/tracking.json` sont
valides. `.ai/checkpoint.json::active_workstream_id` est `null` apres
`.ai/tools/plan.ps1 close`.

## Invariants maintenus

- Aucune modification de `Protocole/`.
- Aucune modification de `procedures/`, `validators/`, `governance/` ou
  `manifests/`.
- Les dossiers natifs orphelins `backtest/`, `features/`, `metrics/` et
  `trading_signals/` ont ete retires.
- BACKTRADER reste hors scope.

## Reprise future

Pour toute suite, repartir de `.ai/checkpoint.json` et ouvrir un nouveau
workstream. Ne pas relancer ce chantier comme actif sauf demande explicite.
