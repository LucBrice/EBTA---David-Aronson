# Native Engine Procedure Mapping

## Status

| Field | Value |
| --- | --- |
| Status | ACTIVE - NATIVE_ENGINE_MAPPING |
| Runtime | EBTA-ENGINE-0.1.x |
| Scope | Native backtest engine through Phase 8 MVP |
| BACKTRADER role | REFERENCE_ONLY |
| Impact protocol | NONE |

## Function

This document replaces the former external-engine contract. The EBTA native
engine is now responsible for producing the artifacts consumed by the existing
EBTA procedures and validators.

BACKTRADER can be read as historical reference after local governance is read,
but it is not a runtime dependency and does not produce EBTA verdicts.

## Native Outputs

| Native output | EBTA artifact | Consuming procedure |
| --- | --- | --- |
| Pre-registered native MVP configuration | `config.json`, search metadata | `search_space`, `walk_forward`, `sealing` |
| StrategyPayload grid, asset x payload | `registry.jsonl`, candidate family | `registry_lineage`, `candidate_matrix` |
| Native Train scores | `reports/optimization_log.json` | `optimization` |
| Native Test scores | `reports/complexity_selection.json` | `complexity_selection` |
| Complete Test family returns | `reports/candidate_matrix.json`, `reports/wrc.json` | `candidate_matrix`, `detrending`, `zero_centering`, `wrc` |
| Native OOS portfolio series | `series/oos_primary_returns.json`, `reports/oos.json` | `oos_confidence_interval` |
| Orders, fills, positions, NAV and costs | `reports/execution.json`, `reports/economic.json` | `returns`, `detrending`, `economic_gate` |
| Local CSV availability and checksum report | `reports/data_availability.json` | `data_availability` |
| Fold schedule with purge, embargo and warm-up | `reports/fold_schedule.json` | `walk_forward` |
| Robustness scenario matrix | `reports/robustness.json` | `robustness` |
| Pre-OOS package hash and approval | `reports/reproduction.json`, access gate evidence | `sealing`, `oos_access` |
| OOS access events | `oos_access_log.jsonl` | `oos_access`, package validators |
| Lifecycle, paper and deployment states | lifecycle reports | `lifecycle` |

## Component Decisions

| Component | Decision | Rationale |
| --- | --- | --- |
| `data/loaders.py` BACKTRADER | REWRITE | Native loader reads local CSV OHLCV directly and records source metadata/checksums. |
| `data/pipeline.py` BACKTRADER | REJECT | Sectional data lake and Joblib cache are not EBTA source-of-truth boundaries. |
| `features/entry_signal.py` BACKTRADER | ADAPT | Liquidity sweep decomposition is reference material; native implementation must remain causal and cache-independent. |
| `features/filters.py` BACKTRADER | ADAPT | Session and MTF ideas are reusable as specifications, not as imported runtime code. |
| `strategies/sweep_lq.py` BACKTRADER | ADAPT | Payloads E-I are decomposed into `StrategyPayload` candidates. |
| `backtest/` BACKTRADER | REWRITE | Native execution must produce EBTA artifacts without stubs or BACKTRADER conventions. |
| `risk/` BACKTRADER | REWRITE | Native MVP uses explicit sizing/risk helpers and must later expand under EBTA governance. |
| `metrics/` BACKTRADER | REWRITE | EBTA procedures and validators remain the verdict source. |
| `viz/` BACKTRADER | REJECT | Visualization is not a business-calculation or verdict source. |
| `adapters/backtrader_mapping.py` EBTA | ADAPT | Retained only as a future boundary contract; not used by the native runtime. |

## Contract Errors

| Error | Expected handling |
| --- | --- |
| Missing native artifact | Raise a contract error; do not synthesize a favorable artifact |
| OOS data supplied to optimization or Test tie-break | Reject as methodological violation |
| Winner-only Test matrix | Reject before WRC |
| Missing strategy x asset candidate | `FAIL` or `INCONCLUSIVE` according to registry evidence |
| WRC Test bootstrap reused for OOS IC | Reject before OOS report |
| OOS access before `PRE_OOS_SEALED` | Deny access |
| Economic gate merged into statistical gate | Reject report structure |
| Notebook-produced verdict | Reject; notebooks may orchestrate only |
| BACKTRADER verdict imported into EBTA | Reject; EBTA validators are the verdict authority |

## Phase 8 Boundary

Phase 8 ends with:

- native modules under `Implementation/ebta_engine/` able to generate a valid
  MVP `research_package`;
- package output written under ignored `Implementation/research_packages/`;
- notebooks under `Implementation/notebooks/` orchestrating code only;
- no `Protocole/` modification;
- no BACKTRADER repository modification;
- no BACKTRADER runtime dependency.
