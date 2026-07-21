# R5/R6 integrated pre-OOS validation

Date: 2026-07-21  
Scope: `PRE_OOS_BENCHMARK`  
OOS segments opened: **0**

The real Nautilus path executed 16 candidates over two folds, hence 32 Test
segments per scenario and 96 segment executions across the three calibrated
scenarios. CENTRAL used 46,080 NAV observations, 42 orders and USD 11.564 of
explicit spread cost. Its NAV reconciliation passed.

| Scenario | Spread basis | Mean return | Hurdle | Verdict |
|---|---|---:|---:|---|
| CENTRAL | p50 | 2.858028194100337e-07 | 0.0 | PASS |
| PLAUSIBLE_BASE | p95 | -3.961375059518784e-08 | 0.0 | REJECTED_ECONOMIC |
| EXTREME | p99 | -4.795326181675023e-08 | 0.0 | REJECTED_ECONOMIC |

The contrast is derived from three executions, not from relabeling one result.
Native one-tick slippage is embedded in Nautilus fill prices; the separate
monetary overlay is the spread ledger. Published fill rates remain evidence
only and are not misrepresented as `prob_fill_on_limit`.

The full package is intentionally deferred to the EPIC's global gate after Lot
3 replaces residual auto-attestations with the explicit human evidence inputs
selected in decision `3A`.
