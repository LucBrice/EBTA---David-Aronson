# Audit de conformite — PLAN_PYREFLY_CI_NOTEBOOK

Date : 2026-08-09

## Verdict

PASS — tous les exit criteria du lot 9 sont livres sans venv Nautilus ni
changement runtime.

## Matrice de conformite

| Critere | Preuve | Verdict |
| --- | --- | --- |
| Pin Pyrefly | `pyrefly==1.1.1` dans l'ensemble exact | PASS |
| Interpreteur CI | `--python-interpreter-path python` | PASS |
| Frontiere Nautilus | `--replace-imports-with-any "nautilus_trader.*"` | PASS |
| Couverture | Moteur et notebooks explicitement passes | PASS |
| Notebook | `TemporaryDirectory` et `package_dir=Path(temp_dir)` | PASS |
| Effet de bord | Aucun package persistant choisi par le notebook | PASS |
| Type-check | Venv CI equivalent, 0 erreur | PASS |
| Ratchet | 7 tests CI, dont retrait du gate hostile | PASS |
| Regression | Inventaire et 291 tests canoniques OK | PASS |
| YAML | Parse local PASS | PASS |
| Scope | pyproject, runtime, Ruff, Protocole, Active et BACKTRADER intacts | PASS |

## Ecart

Aucun ecart dans le depot. Le run GitHub externe reste non execute et non
revendique faute de push autorise.
