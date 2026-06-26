# Procedure Calculation Map

## Status

| Field | Value |
| --- | --- |
| Status | ACTIVE - PROCEDURE_MAP |
| Runtime | EBTA-ENGINE-0.1.0 |
| Plan | `Implementation/Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md` |
| Authority | `Protocole/` frozen as `EBTA-DOC-1.0` |
| Impact protocol | NONE |

## Function

This map links each runtime procedure to its owner SOP, expected inputs,
expected outputs, generated artifacts, and EBTA prohibitions.

It is an implementation handoff. It does not create new EBTA rules.

## Procedure Map

| Procedure | Owner SOP / DN | Inputs | Outputs | Runtime artifacts | EBTA prohibitions |
| --- | --- | --- | --- | --- | --- |
| `search_space` | SOP 03, SOP 06, DN-005 to DN-007 | Pre-registered candidate space, fold id, train segment id, parameter grid | Canonical candidate specifications and search-space snapshot | `reports/search_space.json` | No ex post candidate merge; no OOS input |
| `optimization` | SOP 06, DN-012, DN-013 | Search-space snapshot, Train_k observations, pre-registered objective | Deterministic optimization log and representative candidates | `reports/optimization_log.json` | No Test/OOS fitting; no hidden failed runs |
| `ml_manifest` | SOP 06, SOP 09A, DN-026 | Feature list, model spec, seeds, train segment id, hyperparameters | Reproducible ML manifest | `reports/ml_manifest.json` | No feature unavailable at decision time; no unlogged seed |
| `complexity_selection` | SOP 06, DN-012, DN-013 | Representative candidates, Test_k scores, tie-break rule | Selected candidate or `NO_MODEL` / `STOP_PROCESS` | `reports/complexity_selection.json` | No OOS tie-break; no discretionary override |
| `candidate_matrix` | SOP 02, SOP 03, SOP 06, DN-007, DN-008 | Full applicable candidate list, Test_k series by candidate | Complete matrix for WRC family | `reports/candidate_matrix.json` | No winner-only matrix; no omitted influential candidate |
| `returns` | SOP 08, SOP 09B, DN-014, DN-015, DN-028 | Prices or PnL observations, costs, calendar | Net log-return series and NAV path | `series/*`, `reports/execution.json` | No skipped no-exposure days; no gross/net confusion |
| `detrending` | SOP 07, DN-016, DN-017, DN-026 | Evaluation returns, benchmark returns, exposure weights, fit segment | Detrended evaluation series | `reports/detrending.json` | No signal generation from detrended data; no non-Train fit when learning parameters |
| `zero_centering` | SOP 07, SOP 02, DN-018 | Test candidate matrix | Zero-centered matrix for WRC H0 | `reports/wrc.json` | No zero-centering for OOS estimation |
| `bootstrap` | SOP 01, SOP 02, DN-020, DN-022 | Time series or matrix, block settings, seed, bootstrap purpose | Reproducible stationary-block resamples | `reports/wrc.json`, `reports/oos.json` | No reuse of WRC Test distribution for OOS IC |
| `wrc` | SOP 02, DN-008 to DN-011 | Complete zero-centered Test matrix, observed Test matrix, alpha, seed | WRC statistic, bootstrap distribution, p-value, verdict, **family_catalogue_hash** (DN-008) | `reports/wrc.json` | No SPA override; no testing only the selected winner; family hash must be recorded |
| `oos_confidence_interval` | SOP 01, DN-019 to DN-022 | Concatenated OOS series, OOS bootstrap settings, seed, **power target, stop criterion** | OOS estimate, one-sided lower confidence bound, **power_check**, verdict inputs | `reports/oos.json` | No WRC bootstrap source; no OOS selection; verdict at preregistered stop point only (DN-004) |
| `data_availability` | SOP 09A, DN-025 | Data availability timestamps, decision timestamps | Availability validation report | `reports/data_availability.json` | No decision using unavailable data |
| `walk_forward` | SOP 04, DN-001 to DN-004, DN-027 | Fold schedule, purge, embargo, warm-up, **information_stop_criterion** | Validated fold schedule — **preventive OOS overlap check at construction time** | `reports/fold_schedule.json` | No overlapping OOS; no final extra holdout; no opportunistic fold additions (DN-004) |
| `registry_lineage` | SOP 03, DN-005 to DN-008, DN-034 | Registry events, influential candidate list | Registry coverage and lineage report | `reports/registry_review.json` | No omitted influential candidate; no retrospective universe reduction |
| `registry_append_only` | SOP 03, DN-005 to DN-008 | Ordered registry event list with chain_hash | Append-only validation report — chain integrity + no retro-dedup + family completeness | `reports/registry_review.json` | No delete; no retroactive deduplication (DN-006); WRC must cover complete family (DN-008) |
| `robustness` | SOP 05, DN-030, DN-031 | **Pre-OOS**: robustness plan, stress results by classification (CENTRAL/PLAUSIBLE_BASE/EXTREME); **Post-OOS**: diagnostic-only scenarios | **pre_oos_robustness_verdict** or **post_oos_diagnostic_report** | `reports/robustness.json` | No decision robustness on observed OOS (DN-030); no repair/reselection after OOS (DN-031) |
| `sealing` | SOP 10, SOP 12, DN-032, DN-038 | Package stage, manifest hash, approvals | Pre-OOS sealing report | `reports/reproduction.json` | No OOS opening before `PRE_OOS_SEALED` |
| `oos_access` | SOP 10, DN-032, DN-033 | OOS access request, sealing state, authorization | OOS access decision and log entry | `oos_access_log.jsonl` | No unauthorized OOS read; no silent same-OOS rerun |
| `economic_gate` | SOP 08, SOP 09B, DN-023, DN-024, DN-028, DN-029 | NAV, costs, capacity, hurdle settings | Separate economic gate verdict | `reports/economic.json` | No economic gate replacing statistical gate |
| `monitoring` | SOP 11, DN-037 | Monitoring plan, consultation log with alpha-spent tracking | Monitoring plan validation + consultation log validation | `reports/monitoring.json` | No uncontrolled repeated testing; max consultations enforced; no repair during monitoring |
| `incubation_report` | SOP 11, DN-035, DN-036 | Paper-trading report (signals, execution, costs, risks, incidents) or live deployment report | Incubation/live compliance validation | `reports/incubation.json` | No incubation before VALIDATION_READY; no alpha repair during incubation (DN-035) |
| `reproduction_report` | SOP 12, DN-039, INV-016 | Reproduction report from independent party + original manifest | Hash comparison + environment + command validation | `reports/reproduction.json` | No automated self-reproduction (circular); tolerances must be declared ex ante |
| `lifecycle` | SOP 11, SOP 12, DN-035 to DN-041 | Package stages, incubation/live approvals, monitoring events | Incubation, deployment, lifecycle status report | `reports/incubation.json`, lifecycle archive metadata | No incubation before `VALIDATION_READY`; no live before `DEPLOYMENT_CERTIFIED` |

## Phase Coverage

| Phase | Procedures |
| --- | --- |
| Phase 2 | `search_space`, `optimization`, `ml_manifest`, `complexity_selection`, `candidate_matrix` |
| Phase 3 | `returns`, `detrending` |
| Phase 4 | `zero_centering`, `bootstrap`, `wrc` (+ family_catalogue_hash A5) |
| Phase 5 | `oos_confidence_interval` (+ power validation B5) |
| Phase 6 | `data_availability`, `walk_forward` (+ preventive OOS C3), `registry_lineage`, `registry_append_only` (A1), `robustness` (+ CENTRAL/PLAUSIBLE_BASE/EXTREME A2), `sealing`, `oos_access`, `economic_gate`, `monitoring` (B2), `incubation_report` (B3), `reproduction_report` (B4), `lifecycle` |
| Phase 7 | Pipeline pilot reports produced from procedure modules |
| Phase 8 | External engine output mapping to procedure inputs |

## Schemas ajoutees (lot audit exhaustivite 2026-06-26)

| Schema | Gate / SOP | Angle mort corrige |
| --- | --- | --- |
| `execution_journal_event.schema.json` | G6 / SOP 09B | A3 |
| `pit_data_declaration.schema.json` | G1 / SOP 09A | A4 |
| `walk_forward_declaration.schema.json` | G3 / SOP 04 | A4 |
| `robustness_plan.schema.json` | G5 / SOP 05 | A4 |
| `incubation_plan.schema.json` | G12-G13 / SOP 11 | A4 |
| `reproduction_report.schema.json` | G11 / SOP 12 | B4 |
| `lifecycle_archive.schema.json` | G14 / SOP 12 | C2 |
