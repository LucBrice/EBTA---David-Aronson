# TEMPLATE - Incident de biais EBTA

## Métadonnées

```text
incident_id:
project_id:
research_family_id:
candidate_id:
process_version_id:
fold_id:
oos_segment_id:
detected_at:
detected_by:
reported_by:
protocol_version:
related_sop:
```

## Classification

```text
bias_category:
severity_level:
status: OPEN | UNDER_REVIEW | RESOLVED | FAIL | INCONCLUSIVE | BURNED
information_exposure: NONE | TEST | OOS | ECONOMIC | ROBUSTNESS | REPRODUCTION | LIVE
affected_gate:
affected_artifacts:
```

## Description factuelle

```text
what_happened:
when_it_happened:
who_or_tool_was_involved:
what_information_was_visible:
what_decision_could_be_influenced:
```

## Analyse d'impact

```text
candidate_family_impact:
metric_or_hurdle_impact:
robustness_impact:
oos_virginity_impact:
reproducibility_impact:
archive_impact:
ai_or_external_tool_impact:
```

## Mesures immédiates

```text
freeze_required:
access_suspended:
new_candidate_or_version_required:
oos_burned:
artifacts_to_preserve:
```

## Revue indépendante

```text
reviewer:
review_started_at:
review_completed_at:
evidence_paths:
evidence_hashes:
review_decision:
review_rationale:
```

## Décision G-BIAS

```text
gbias_status: PASS | FAIL | INCONCLUSIVE | BURNED
conditions_before_reopen:
required_registry_events:
required_package_updates:
approved_by:
approved_at:
```

## Note normative

Un incident ne doit jamais être supprimé. Toute correction est un nouvel
événement append-only lié à cet incident.
