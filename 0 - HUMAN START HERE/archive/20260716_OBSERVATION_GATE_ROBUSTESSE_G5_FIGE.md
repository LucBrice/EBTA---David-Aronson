# Observation — le verdict de robustesse pre-OOS reel est calcule puis ignore par gates.json (G5)

> Note d'intake, pas un plan. Deposee ici pour audit et structuration, suite
> a la question "c'est quoi la suite des travaux ?" (2026-07-15) et au
> risque `R3 — Preuve vs attestation` de
> `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` (section "Suite
> proposee"), qui identifie explicitement ce point comme suite residuelle
> apres la cloture de
> `.ai/archive/20260715_PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE.md`.

## Constat

`_write_reports()` dans
`Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
(fonction partagee par le pipeline pilote classique ET par le chemin de
production Nautilus, via `pilot.build_package()`) construit le dict `gates`
consomme par `validators/gate_validator.py::gate_report()`. Deux champs
voisins du meme dict recoivent un traitement different, verifie directement
dans le code le 2026-07-15 :

```python
"wrc_status": procedure_reports["wrc"]["verdict"],       # ligne 211 — reel
...
"pre_oos_robustness_verdict": "PASS",                     # ligne 215 — code en dur
```

`procedure_reports["robustness"]` existe pourtant deja, calcule juste avant
dans `_procedure_reports()` (ligne ~390) :

```python
robustness = robustness_verdict(pilot_inputs["robustness_plan"]["scenarios"])
```

qui route (`procedures/robustness.py` ligne 260-266) vers
`pre_oos_robustness_verdict()`, une fonction reelle (SOP 05 / DN-030) qui
retourne `status: "FAIL"` des qu'un scenario **bloquant** (`CENTRAL` ou
`PLAUSIBLE_BASE`) ne `PASS`e pas — verdict atteignable en production : côté
Nautilus, `risk/robustness.py::compute_robustness_scenarios()` produit
`scenario_verdict="REJECTED_ECONOMIC"` des que `mean_return` d'un scenario
passe sous `minimum_mean_return` (ligne 51), ce qui n'est pas dans
`_PASS_VERDICTS`.

Ce meme `procedure_reports["robustness"]["status"]` **est** deja utilise
honnetement ailleurs dans le meme fichier :
- `robustness.json` (ligne 303) le reporte tel quel ;
- `incubation_gate.json::robustness_status` (ligne 410) le reporte tel quel,
  et `procedures/lifecycle.py::incubation_gate()` (comparaison stricte
  `!= "PASS"`) fait deja basculer `incubation_gate.status` en `FAIL` si la
  robustesse reelle echoue — ce canal-la est deja honnete, et
  `validators/package_validator.py::_semantic_consistency_errors()` lit deja
  `incubation_gate.status` (verifie le 2026-07-15, voir
  `.ai/archive/20260715_PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE.md`).

Le defaut est donc plus etroit que pour le WRC (deja corrige) : ce n'est
**pas** un angle mort complet du statut global de package — un vrai `FAIL`
de robustesse atteint deja `incubation_gate.json` et donc
`validate_package_dir()["status"]`. Le defaut reel est que **G5
specifiquement**, dans `gates.json`/`gate_report()`, reste une attestation
fausse : `validators/gate_validator.py::_requirement_satisfied()` verifie
deja la valeur des champs de verdict connus (corrige par
`.ai/archive/20260715_PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE.md`),
mais cette correction est neutralisee pour G5 par une entree fabriquee en
amont. Un lecteur qui consulte `gates.json` ou `gate_report()` gate par
gate (plutot que le seul champ `status` agrege) voit G5 = `PASS` meme quand
la robustesse pre-OOS reelle a echoue — la meme categorie de defaut
(attestation deconnectee du calcul) que le WRC, a l'endroit exact que
`.ai/archive/20260715_PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE.md`
avait deja identifie et explicitement laisse hors perimetre (section "Non-
goals" de ce plan-la).

## Ce que cette note ne fait PAS

- Ne propose aucune reecriture de `procedures/robustness.py`,
  `risk/robustness.py`, `procedures/lifecycle.py`,
  `validators/gate_validator.py`, ou `validators/package_validator.py` —
  ces cinq modules sont deja corrects et testes ; le defaut est en amont, a
  l'endroit ou l'entree de `gates.json` est assemblee dans `_write_reports()`.
- Ne touche pas au fait que `robustness_verdict()` route sans
  `preregistered_catalogue` (verification de couverture DN-030 non
  activee) — sujet distinct, a evaluer separement si priorise.
- Ne couvre pas le risque `R6` de l'audit (les trois scenarios
  CENTRAL/PLAUSIBLE/EXTREME recoivent aujourd'hui les memes donnees,
  aucun choc reel de cout/slippage/latence n'est applique) — meme si un
  gate G5 honnete est un prealable utile a R6, R6 reste un chantier
  distinct de calibration, pas un defaut de lecture.
- Ne couvre pas la refonte des ~35 autres booleens d'attestation de
  `gates.json` (`kill_switch`, `live_approval`,
  `independent_pre_oos_approval`, etc.) — attestations de gouvernance
  necessitant un vrai mecanisme de decision humaine, hors perimetre ici.
- Ne decide d'aucun seuil ni d'aucune calibration.

## Suite proposee

Transformer cette observation en plan `fix` cible et minimal : remplacer
`"pre_oos_robustness_verdict": "PASS"` (ligne ~215) par
`"pre_oos_robustness_verdict": procedure_reports["robustness"]["status"]`,
exactement le meme patron deja applique a `wrc_status` (ligne 211). Preuve
de non-regression par fixture a verite connue (scenario bloquant CENTRAL ou
PLAUSIBLE_BASE force sous son `minimum_mean_return`, verdict
`REJECTED_ECONOMIC`), suivant le patron deja utilise par
`.ai/archive/20260715_PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE.md` et
`.ai/archive/20260715_PLAN_CORRECTION_VALIDATORS_STATUT_GLOBAL_PACKAGE.md` :
asserter que `gates.json::pre_oos_robustness_verdict == "FAIL"` et que
`gate_report()` classe G5 comme non-`PASS`, sur le chemin de production
Nautilus reel.
