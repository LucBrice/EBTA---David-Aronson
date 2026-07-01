# TEMPLATE - Dérogation méthodologique EBTA

## Métadonnées

```text
derogation_id:
project_id:
research_family_id:
process_version_id:
requested_at:
requested_by:
protocol_version:
related_sop:
affected_gate:
```

## Demande

```text
requested_exception:
objective_constraint:
scope_limit:
time_limit:
affected_artifacts:
affected_decisions:
```

## Conditions d'admissibilité

```text
documented_before_affected_decision: true | false
independent_of_observed_result: true | false
no_oos_repair_effect: true | false
no_metric_or_hurdle_repair: true | false
no_candidate_family_reduction: true | false
reviewer_independent: true | false
```

## Interdictions absolues

La dérogation est irrecevable si elle vise à :

- réouvrir un OOS consommé ;
- retirer un run, actif, fold ou incident défavorable ;
- changer une métrique, un hurdle, un benchmark, un coût ou un scénario après résultat ;
- transformer `FAIL`, `INCONCLUSIVE`, `NOT_VALIDATED` ou `REJECTED_ECONOMIC` en `PASS` ;
- justifier une réparation conçue après exposition à un résultat sensible ;
- remplacer une preuve manquante par une opinion.

## Décision

```text
decision: APPROVED | REJECTED | INCONCLUSIVE
reviewer:
approved_by:
decision_at:
conditions:
expiration:
registry_event_id:
evidence_paths:
evidence_hashes:
```

## Note normative

Une dérogation approuvée limite un écart documenté. Elle ne restaure jamais la
virginité d'une donnée, ne réduit jamais une famille statistique et ne répare
jamais un résultat observé.
