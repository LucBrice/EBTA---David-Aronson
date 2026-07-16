# Lot C — Brancher les attestations mecaniques deja calculees (G1/G7/G11/G12/G13)

> Note d'intake, sous-chantier 1/3 de
> `.ai/backlog/fixes/EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES.md`
> (chantier mere de suivi). Issue du Lot C de l'observation
> `0 - HUMAN START HERE/archive/20260716_OBSERVATION_GATES_ATTESTATIONS_RESIDUELLES.md`,
> deja convergee apres 3 passes `/evaluate`. Meme nature de defaut, meme
> patron de correction que
> `.ai/archive/20260716_PLAN_CORRECTION_GATE_STATISTIQUE_OOS_MASQUE.md`
> (Lot A1, deja `DONE`), applique ici a 6 champs de gouvernance
> supplementaires (G1, G7, G11, G12, G13) plutot qu'au gate OOS (G9).

## Constat verifie en session (2026-07-17)

`Implementation/examples/minimal_pilot_pipeline/build_research_package.py::_write_reports()`
(lignes 195-254) ecrit ~12 champs `gates.json` en litteral `True`, alors que
`_procedure_reports()` (lignes 339-460, meme fichier) a **deja calcule** un
vrai `status` pour chacun d'eux, via des fonctions deja testees et deja
appelees avec les vraies entrees :

| Champ `gates.json` (actuellement `True` en dur) | Gate | Source deja calculee | Verifie (valeurs possibles) |
| --- | --- | --- | --- |
| `data_snapshots`, `availability_timestamps`, `anti_leakage_report` | G1 | `procedure_reports["data_availability"]["status"]` (`validate_availability()`, `procedures/data_availability.py:13,22`) | `PASS`/`FAIL` uniquement |
| `pre_oos_manifest`, `frozen_config` | G7 | `procedure_reports["sealing"]["status"]` (`validate_pre_oos_seal()`, `procedures/sealing.py:10,20`) | `PASS`/`FAIL` uniquement |
| `validation_ready_manifest`, `reproduction_report`, `incubation_approval` | G11 | `procedure_reports["reproduction_validation"]["status"]` (`validate_reproduction_report()`, `procedures/reproduction_report.py`) | `PASS`/`FAIL`/`INCONCLUSIVE` |
| `monitoring_plan` | G12 | `procedure_reports["monitoring_plan"]["status"]` (`validate_monitoring_plan()`, `procedures/monitoring.py:28`) | `PASS`/`FAIL`/`INCONCLUSIVE` |
| `paper_trading_log` | G12 | `procedure_reports["monitoring_consultation_log"]["status"]` (`validate_consultation_log()`, `procedures/monitoring.py:87`) | `PASS`/`FAIL` (verifie : `_monitoring_result()` ligne 191-198 ne produit que ces deux valeurs pour ce chemin) |
| `incubation_report` | G12 | `procedure_reports["incubation_report"]["status"]` (`validate_incubation_report()`, `procedures/incubation_report.py:21-126`) | `PASS`/`FAIL`/`INCONCLUSIVE` (verifie explicitement : le `"WATCH"` possible reste dans le sous-champ `verdict` du rapport source, jamais dans `status` lui-meme — ligne 120-121 ne retourne que `"PASS"`/`"FAIL"`, ligne 47-50 `"INCONCLUSIVE"` si rapport vide) |
| `deployment_certified_manifest` | G13 | `procedure_reports["deployment_gate"]["status"]` (`deployment_gate()`, `procedures/lifecycle.py:30-40`) | `PASS`/`FAIL` uniquement |

**Point important verifie en session, absent de l'observation source** : les
6 statuts ci-dessus sont **tous** deja confines a
`{"PASS", "FAIL", "INCONCLUSIVE"}` — contrairement au cas G9/Lot A1 ou
`"NOT_VALIDATED"` sortait de cet ensemble et exigeait une fonction de
normalisation dediee (`_g9_gate_value()`). Ici, aucune valeur hors-catalogue
ne peut remonter : le branchement peut donc etre une simple lecture directe
du `status`, sans normalisation supplementaire — plus simple que le patron
G9, pas plus risque.

## Ce qui n'est PAS dans ce lot

- G2 `independent_registry_review` (tautologique, decision de source de
  verite non tranchee) — reste hors perimetre par decision humaine du
  2026-07-16.
- G7 `independent_pre_oos_approval`, G13 `kill_switch`/`live_approval`, G14
  (`retention_policy`/`incident_log`) — attestations humaines legitimes,
  aucune procedure ne peut les calculer depuis une simulation.
- G9 `power_report` (Lot A2, calcul manquant, sous-chantier separe) et G6
  `execution_report`/`nav_reconciliation` (Lot B, decision de seuil requise,
  sous-chantier separe).
- `nautilus_research_package.py` : verifie par grep (`data_availability`,
  `sealing`, `reproduction`, `monitoring`, `incubation`, `deployment_gate`)
  — aucun champ Lot C n'y est fige en amont, seules des entrees `inputs[...]`
  alimentant `_procedure_reports()` y sont ajustees. Aucune modification
  necessaire dans ce fichier pour ce lot.

## Perimetre pressenti

**Autorises** : `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
(`_write_reports()`, partage pilote + production Nautilus) ;
`Implementation/ebta_engine/tests/test_gates.py` (tests au meme patron que
G9) ; `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`
(assertion d'integration additionnelle) ; `Implementation/HISTORIQUE DES
VERSIONS EBTA ENGINE.md` (entree si le M1 courant bascule).

**Interdits** : `Protocole/`, tout fichier sous `procedures/` (les 7
fonctions citees sont deja correctes, seul leur resultat doit etre
branche), `validators/`, `governance/`, `manifests/`,
`package_builder/nautilus_research_package.py` (aucune modification requise,
verifie ci-dessus).

## Suite immediate

Ce lot est pret pour `/start` immediatement (aucune decision humaine
requise, methode identique au patron G9 deja valide). Une fois clos, le
sous-chantier Lot A2 (fonction de puissance atteinte) sera redige et route
a son tour, selon l'ordre acte dans le chantier mere.
