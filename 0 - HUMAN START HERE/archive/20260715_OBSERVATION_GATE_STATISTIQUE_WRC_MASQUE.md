# Observation — le verdict WRC reel est calcule puis ignore par les gates incubation/economique

> Note d'intake, pas un plan. Deposee ici pour audit et structuration, suite
> a la question "c'est quoi la suite apres R4 ?" (2026-07-15) et a la
> cartographie de code demandee sur le risque `R3 — Preuve vs attestation`
> de `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md`.

## Constat

`_procedure_reports()` dans
`Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
(fonction partagee par le pipeline pilote classique ET par le chemin de
production Nautilus, via `pilot.build_package()`) calcule un vrai verdict
WRC :

```python
wrc = wrc_test(
    candidate_returns,
    replications=statistical_plan["wrc_bootstrap_replications"],
    mean_block_length=statistical_plan["wrc_mean_block_length"],
    seed=statistical_plan["wrc_seed"],
    alpha=statistical_plan["wrc_alpha"],
)
```

(ligne ~372-378, verdict reel `"PASS"`/`"FAIL"` selon `pvalue < alpha`, voir
`procedures/wrc.py` ligne 48). Mais ce verdict reel n'est jamais reutilise
pour les deux gates qui en dependent normativement :

1. Ligne ~404, `incubation_gate({"statistical_status": "PASS", ...})` — le
   literal `"PASS"` est code en dur, au lieu de `wrc["verdict"]`.
2. `pilot_inputs["economic_gate"]["statistical_status"]` est deja fige a
   `"PASS"` en amont (cote Nautilus :
   `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
   ligne ~265, `economic_gate_evidence(statistical_status="PASS", ...)`),
   jamais recroise avec `wrc["verdict"]` reellement calcule juste apres
   dans `_procedure_reports()`.

`incubation_gate()` (`procedures/lifecycle.py` ligne 13) et
`economic_gate_report()` (`procedures/economic_gate.py` ligne 13) sont tous
deux de vrais agregateurs correctement ecrits (comparaison stricte
`evidence.get(key) != expected`, cascade de statuts) — le defaut n'est pas
dans la logique de gate, il est dans l'entree qui lui est fournie.

**Consequence concrete** : un candidat qui echoue reellement au test WRC
(bruit statistique, aucun signal reel apres correction de test multiple)
obtiendrait quand meme `incubation_gate.status == "PASS"` et
`economic_gate.global_status` potentiellement `"PASS"` aujourd'hui, sur le
chemin de production reel — le meme type de defaut (gate qui ne peut jamais
rejeter) deja corrige une fois pour le gate economique par
`.ai/archive/20260710_PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md`, mais
qui subsiste ici pour le gate statistique.

## Ce que cette note ne fait PAS

- Ne propose aucune reecriture de `procedures/wrc.py`,
  `procedures/economic_gate.py`, ou `procedures/lifecycle.py` — ces trois
  modules sont deja corrects et testes ; le defaut est en amont, a
  l'endroit ou leurs entrees sont assemblees.
- Ne couvre pas la refonte complete des ~35 booleens de `gates.json`
  auto-attestes dans `_write_reports()` (ex. `kill_switch`, `live_approval`,
  `independent_pre_oos_approval`) — la plupart sont des attestations de
  gouvernance legitimes necessitant un vrai mecanisme de decision humaine,
  pas un calcul derivable du code ; sujet a traiter dans un chantier
  separe, plus tard, si l'humain le priorise.
- Ne decide d'aucun seuil ni d'aucune calibration.

## Suite proposee

Transformer cette observation en plan `fix` cible (perimetre : la fonction
`_procedure_reports()` et son usage du verdict WRC reel dans les deux
gates concernes), avec preuve de non-regression par candidat synthetique a
verite connue (WRC FAIL), suivant le patron deja utilise par
`.ai/archive/20260710_PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md`.
