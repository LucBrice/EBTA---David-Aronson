# Brouillon — Lot 3 : garde d'environnement dans `long_data.py`

Track : fix
Lifecycle : INTAKE
Scope : Faire passer la suite de 219 tests a zero erreur hors du venv
Nautilus, en protegeant l'appel `importlib.metadata.version("nautilus_trader")`
dans `Implementation/ebta_engine/benchmarks/long_data.py:487`
(`_environment_report()`), sans masquer l'absence du paquet — la valeur
enregistree dans le rapport doit rester explicite.
Non-goals : Ne modifie aucun autre point de `long_data.py`. Ne modifie
aucune procedure, validator, gate ou schema. Ne rend pas la suite verte en
skippant le test — le test doit continuer a s'executer et a produire un
rapport, seul le champ `nautilus_trader_version` change de comportement.
Source : Sous-chantier 3/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`,
Phase 4. Recommandation 3 de l'audit source
`0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`.
Verrou `Implementation/` leve le 2026-08-07 pour ce seul fichier et cette
seule correction (`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md`, section 10).
Exit criteria : `python -m unittest discover -s Implementation/ebta_engine/tests
-t Implementation` retourne `219 tests, 0 error` hors venv Nautilus, et
`report["environment"]["nautilus_trader_version"]` vaut la chaine explicite
`"NOT_INSTALLED"` (jamais un champ silencieusement absent) quand le paquet
n'est pas installe.

## Cause racine (deja prouvee, pas a redemontrer)

`test_long_data_benchmark.py:105` appelle `run_benchmark`, qui appelle
`long_data.py:138 -> _environment_report() -> long_data.py:487`, ou
`importlib.metadata.version("nautilus_trader")` leve `PackageNotFoundError`
hors du venv Nautilus. L'echec est a l'execution du test, pas a l'import du
module.

## Boucle `/evaluate` d'intake (2 passes, convergee)

**Passe 1** — Verification que `_environment_report()` (ligne 483-492) est
la seule fonction concernee et que `nautilus_trader_version` (ligne 487) est
son seul appel a `importlib.metadata.version`. Grep confirme aucun autre
site du depot n'appelle `importlib.metadata.version("nautilus_trader")`.
Decision : catcher precisement `importlib.metadata.PackageNotFoundError`
(deja importe via `import importlib.metadata` en tete de fichier), jamais
`except Exception` generique — coherent avec le pattern deja juge sain par
l'audit source ailleurs dans le depot (`governance/`).

**Passe 2** — Verification qu'aucun consommateur du champ
`nautilus_trader_version` n'attend un format specifique (grep sur
`nautilus_trader_version` dans tout `Implementation/` : aucun autre usage
que sa production ligne 487 et sa consommation implicite dans le dict
`report`). La valeur `"NOT_INSTALLED"` (chaine, pas `None`) est retenue
plutot que `null` : plus explicite dans un JSON persiste, evite toute
confusion avec un champ non calcule ailleurs dans le rapport. Convergence a
2 passes sur 6 autorisees.
