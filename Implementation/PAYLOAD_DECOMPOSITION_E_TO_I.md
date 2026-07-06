# Payload Decomposition E to I

## Status

| Field | Value |
| --- | --- |
| Status | ACTIVE - PHASE_1_AUDIT |
| Date | 2026-07-02 |
| BACKTRADER access | READ_ONLY authorized by user decision `1A` |
| EBTA runtime impact | Native rewrite specification |
| Protocol impact | NONE |

## Provenance

The payload identifiers `E`, `F`, `G`, `H`, `I` were first introduced in the
2026-07-02 user/Codex planning discussion. The read-only BACKTRADER audit then
confirmed their implementation locus in:

```text
D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\strategies\sweep_lq.py
```

The payloads are treated as historical reference material only. EBTA re-expresses
them as pre-registered `StrategyPayload` candidates.

## Shared Family

| Dimension | Native EBTA value |
| --- | --- |
| Strategy family | `liquidity_sweep_confirmation` |
| Base entry | M15 liquidity levels, M1 sweep/engulfing, strict M3 close confirmation |
| Timeframe | `3min` decision frame with M1/M3/M15 inputs |
| Direction | `long_short` |
| Horizon | `10` M3 bars |
| Expiry | `3` days |
| LQ timeframe | `15` minutes |
| Sweep window | `240` minutes |
| Candidate unit | `asset x payload_code` |

## Payload Table

| Payload | Bias filter | Time/session filter | EBTA interpretation |
| --- | --- | --- | --- |
| E | none | none / all | Confirmation-only liquidity sweep baseline |
| F | directional MTF bias | none / all | E plus directional higher-timeframe bias |
| G | directional MTF bias | Asia | F plus Asia session mask |
| H | directional MTF bias | London | F plus London session mask |
| I | directional MTF bias | US | F plus US session mask |

## MVP Candidate Matrix

| Asset | Payloads | Candidate count |
| --- | --- | --- |
| NASDAQ | E, F, G, H, I | 5 |
| XAUUSD | E, F, G, H, I | 5 |
| Total | 2 assets x 5 payloads | 10 |

Winner-only selection is forbidden. The native engine must emit all 10 candidates
into `registry.jsonl`, `reports/search_space.json`,
`reports/candidate_matrix.json`, and WRC evidence.

## BACKTRADER Reference Notes

- `strategies/sweep_lq.py` defines E-I as a family around `SweepLQ`.
- Payload E uses `df_m15`, `df_m1`, `df_m3` without MTF bias.
- Payload F adds directional MTF bias.
- Payloads G/H/I add Asia/London/US session filters respectively.
- The reference implementation depends on `features/entry_signal.py`,
  `features/filters.py`, and `features/core.py`.
- The EBTA native MVP rewrites behavior; it does not import these modules.

## Forbidden Imports

- No BACKTRADER runtime dependency.
- No section pipeline S1-S9.
- No BACKTRADER verdicts.
- No stubs or hardcoded favorable PnL.
- No cache identity that omits asset/content identity.
