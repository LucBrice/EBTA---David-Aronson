# R5/R6 execution calibration

As of: 2026-07-21

## NASDAQ local tick evidence

- Classification: `UNVERIFIED_LOCAL_EXPORT`
- Period: 2023-01-01 to 2025-12-31
- Files: 36
- Rows: 181713218 valid / 181713218 total
- Invalid prices: 0
- Crossed markets: 0
- Spread p50/p95/p99 (points): 1.502000 / 3.515000 / 3.558000

## Descriptive broker proxies

| Series | N | Mean | p50 | p95 | p99 | Unit |
|---|---:|---:|---:|---:|---:|---|
| NASDAQ_SPREAD_POINTS | 4 | 1.251750 | 1.100000 | 1.715950 | 1.788790 | index_point |
| XAUUSD_SPREAD_POINTS | 4 | 0.167500 | 0.150000 | 0.285000 | 0.297000 | gold_point |
| BROKER_EXECUTION_LATENCY_MS | 4 | 26.175000 | 25.350000 | 48.500000 | 49.700000 | millisecond |
| INDEX_ADVERSE_SLIPPAGE_PROBABILITY | 1 | 0.320000 | 0.320000 | 0.320000 | 0.320000 | probability |
| BROKER_FILL_RATE_PERCENT | 3 | 99.363333 | 99.320000 | 99.752000 | 99.790400 | percent |
| STANDARD_CFD_COMMISSION_RATE | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | notional_fraction |

## Limitations

- The NASDAQ local export has no externally attested provider provenance.
- Broker samples mix published averages, minimums, medians, and bounds; cross-broker quantiles are descriptive proxies with small N.
- Broker latency is not end-to-end latency from the EBTA execution machine.
- The adverse slippage probability is an aggregate IG index-stop proxy, not an asset-specific observed distribution.
- Published overall fill rates are retained as evidence but are not mapped to prob_fill_on_limit because the contracts are not equivalent.
- XAUUSD spread is BROKER_PROXY because no local ask/bid tick source is available.
