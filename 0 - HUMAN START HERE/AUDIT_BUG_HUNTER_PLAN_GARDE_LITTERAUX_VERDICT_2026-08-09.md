# Audit bug-hunter — Garde AST des litteraux de verdict

## Verdict

`PASS` — Pyrefly retourne 0 erreur apres correction de quatre vrais defauts
de contrat de typage dans le nouveau scanner.

## Perimetre

- `Implementation/ebta_engine/validators/verdict_literal_guard.py` ;
- `Implementation/ebta_engine/tests/test_verdict_literal_guard.py`.

## Diagnostics et corrections

| Diagnostic | Classe | Cause | Correction |
| --- | --- | --- | --- |
| Trois erreurs `AST` vs `Constant` | VRAI BUG | `_is_positive_literal` ne declarait pas son narrowing, donc les acces `value` et appels types n'etaient pas garantis. | Retour annote `TypeGuard[ast.Constant]`. |
| `str.join(list[str | None])` | VRAI BUG | La comprehension avec walrus conservait un `None` possible de `_target_key`. | Boucle explicite, garde `is not None`, liste `str`. |

Aucun `Any` n'a ete ajoute pour masquer les diagnostics et aucun comportement
runtime n'a change.

## Preuve

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check Implementation\ebta_engine\validators\verdict_literal_guard.py Implementation\ebta_engine\tests\test_verdict_literal_guard.py --output-format min-text
```

Resultat final : `INFO 0 errors`.

Les 8 tests cibles passent sans `SKIP` et la suite complete execute 274 tests :
`OK`.
