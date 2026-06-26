# External Engine Procedure Mapping

## Status

| Field | Value |
| --- | --- |
| Status | ACTIVE - PRE_ADAPTER_MAPPING |
| Runtime | EBTA-ENGINE-0.1.0 |
| Scope | Phase 8 pre-adaptation |
| External repo access | FORBIDDEN_IN_THIS_LOT |
| Impact protocol | NONE |

## Function

This document lists the outputs that a future external engine, including
BACKTRADER, must provide to feed the EBTA procedure modules.

It does not describe the current BACKTRADER repository and was produced without
reading or modifying that repository.

## Required External Outputs

| External output | EBTA target | Consuming procedure |
| --- | --- | --- |
| Pre-registered configuration | `config.json`, search metadata | `search_space`, `walk_forward`, `sealing` |
| Candidate catalogue and registry events | `registry.jsonl`, candidate family | `registry_lineage`, `candidate_matrix` |
| Train candidate scores | `reports/optimization_log.json` | `optimization` |
| Test candidate scores | `reports/complexity_selection.json` | `complexity_selection` |
| Candidate daily Test series | `reports/candidate_matrix.json`, `reports/wrc.json` | `candidate_matrix`, `detrending`, `zero_centering`, `wrc` |
| OOS daily portfolio series | `series/oos_primary_returns.json`, `reports/oos.json` | `oos_confidence_interval` |
| NAV, costs, cash, exposure and benchmark series | `reports/execution.json`, `reports/economic.json` | `returns`, `detrending`, `economic_gate` |
| Data availability timestamps | `reports/data_availability.json` | `data_availability` |
| Fold schedule with purge, embargo and warm-up | `reports/fold_schedule.json` | `walk_forward` |
| Robustness scenario matrix | `reports/robustness.json` | `robustness` |
| Pre-OOS package hash and approval | `reports/reproduction.json`, access gate evidence | `sealing`, `oos_access` |
| OOS access events | `oos_access_log.jsonl` | `oos_access`, package validators |
| Lifecycle, paper and deployment states | lifecycle reports | `lifecycle` |

## Contract Errors

| Error | Expected handling |
| --- | --- |
| Missing required external output | Raise a contract error; do not synthesize a favorable artifact |
| OOS data supplied to optimization or Test tie-break | Reject as methodological violation |
| Winner-only Test matrix | Reject before WRC |
| Missing influential candidate | `FAIL` or `INCONCLUSIVE` according to registry evidence |
| WRC Test bootstrap reused for OOS IC | Reject before OOS report |
| OOS access before `PRE_OOS_SEALED` | Deny access |
| Economic gate merged into statistical gate | Reject report structure |
| Incubation before `VALIDATION_READY` | Reject lifecycle transition |

## Phase 8 Boundary

Phase 8 ends here for this execution:

- no BACKTRADER repository read;
- no BACKTRADER file modified;
- no BACKTRADER convention imported into EBTA core;
- future work starts by reading BACKTRADER governance, then mapping its actual
  outputs to this contract.
