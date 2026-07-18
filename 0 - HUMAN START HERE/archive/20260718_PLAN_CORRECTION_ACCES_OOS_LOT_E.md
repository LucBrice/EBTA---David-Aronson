# Brouillon — Lot E : G8 acces OOS et correction du bug wrc_pass fige

## Origine

Ce brouillon est le sous-chantier 2/4 de
`EPIC_ATTESTATIONS_RESIDUELLES_R3`. Le chantier mere a cloture le Lot D le
2026-07-18 et pointe maintenant ce Lot E comme prochaine etape executable.

## Constat verifie dans le code

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
  conserve encore trois champs G8 en litteraux `True` dans `gates.json` :
  `oos_access_log`, `opening_authorization`,
  `single_oos_execution_log`.
- `_oos_access_request()` force encore `"wrc_pass": True`.
- `Implementation/ebta_engine/procedures/oos_access.py::authorize_oos_access()`
  sait deja refuser l'acces OOS si un des flags requis est faux, dont
  `wrc_pass`.
- Le package persistant `Implementation/research_packages/nautilus_mvp`
  contient actuellement `reports/wrc.json::verdict = "FAIL"` mais
  `reports/oos_access_decision.json::status = "AUTHORIZED"`, ce qui prouve
  le bug de propagation.

## Objectif

Corriger le chemin pilote/production qui fabrique l'autorisation OOS :

- `wrc_pass` doit deriver du verdict WRC reel ;
- les champs G8 de `gates.json` doivent deriver du rapport reel
  `oos_access_decision`, pas de litteraux `True` ;
- un test de contraste doit prouver que WRC `FAIL` entraine
  `oos_access_decision.status = "DENIED"` et que G8 n'est plus `PASS`.

## Perimetre autorise

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`
- `Implementation/ebta_engine/tests/test_nautilus_research_package.py`
- `Implementation/examples/minimal_pilot_pipeline/research_package/`
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`
- fichiers `.ai/` modifies mecaniquement par `plan.ps1`

## Non-objectifs

- Ne pas modifier `Protocole/`.
- Ne pas modifier `validators/gate_validator.py::GATE_REQUIREMENTS` ni
  `VERDICT_VALUES`.
- Ne pas ouvrir l'OOS ni inventer une nouvelle regle d'autorisation.
- Ne pas regenerer `Implementation/research_packages/nautilus_mvp` dans ce
  lot ; la regeneration persistante reste Phase 4 du chantier mere.
- Ne pas traiter Lot F (`invariant_evidence.json`).

## Verification attendue

- Test cible minimal pilot.
- Test cible Nautilus prouvant WRC FAIL -> OOS DENIED.
- Suite runtime complete.
- Build du package pilote minimal.
- Bug-hunter Pyrefly sur les fichiers touches.
- Audit de conformite du plan avant cloture.

## Notes d'audit

- Passe `/evaluate` 1 executee le 2026-07-18 : angle mort identifie, le
  contraste ne doit pas rester limite au helper `_oos_access_request()` mais
  couvrir le chemin `build_nautilus_research_package()` via le runner WRC
  FAIL deja present dans `test_nautilus_research_package.py`.
- Passe `/evaluate` 2 executee le 2026-07-18 : convergence. Aucun nouveau
  blind spot majeur ; le perimetre reste `SINGLE`, sans changement normatif
  ni regeneration du package persistant.
