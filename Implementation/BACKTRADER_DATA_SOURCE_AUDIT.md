# BACKTRADER Data Source Audit

## Status

| Field | Value |
| --- | --- |
| Status | ACTIVE - PHASE_1_AUDIT |
| Date | 2026-07-02 |
| Human decision | `2B` data source path supplied |
| Data root | `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\Data` |
| BACKTRADER role | REFERENCE_ONLY |
| Protocol impact | NONE |

## Source Folders

| Asset | Folder | File count | First file | Last file |
| --- | --- | ---: | --- | --- |
| XAUUSD | `XAUUSD 1m` | 72 | `XAUUSD-m1-bid-2020-01-01-2020-01-31.csv` | `XAUUSD-m1-bid-2025-12-01-2025-12-31.csv` |
| NASDAQ | `NASDAQ 1m` | 72 | `USATECH.IDXUSD-m1-bid-2020-01-01-2020-01-31.csv` | `USATECH.IDXUSD-m1-bid-2025-12-01-2025-12-31.csv` |

## CSV Format

Observed header:

```text
timestamp,open,high,low,close,volume
```

Observed first rows:

```text
XAUUSD  2020-01-01T00:00:00Z,1516.915,1516.915,1516.915,1516.915,0.0
NASDAQ  2020-01-01T00:00:00Z,8744.58,8744.58,8744.58,8744.58,0.0
```

Observed last rows:

```text
XAUUSD  2025-12-30T23:59:00Z,4338.608,4339.248,4338.078,4338.655,17079.999670386314
NASDAQ  2025-12-30T23:59:00Z,25450.279,25451.066,25449.87,25450.588,461.9999963324517
```

The filenames and BACKTRADER loader conventions identify these as 1-minute bid
OHLCV CSV exports. The vendor/licence are not encoded in the files inspected
here and remain `UNVERIFIED_LOCAL_EXPORT`.

## BACKTRADER Loader Reference

Read-only audit of:

```text
BACKTRADER\data\loaders.py
BACKTRADER\data\pipeline.py
```

Findings:

- `loaders.py` hardcodes the same `Data` root supplied by the user.
- Required columns are `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Timestamps are parsed with `utc=True`.
- `pipeline.py` resamples OHLCV by timeframe using first/high/low/last/sum.
- The historical BACKTRADER cache is Joblib-based and not reused by EBTA.

## Native MVP Data Window

For the first EBTA-native package proof, the engine uses a deterministic subset:

```text
2020-01-01T00:00:00Z -> 2020-01-03T23:59:00Z
```

This subset proves architecture and package generation. Expanding to the full
2020-2025 local history is a separate research decision.

## Licence And Provenance Gaps

| Item | Status |
| --- | --- |
| Local path | CONFIRMED |
| CSV schema | CONFIRMED |
| UTC timestamp convention | CONFIRMED |
| Asset coverage | CONFIRMED for XAUUSD and NASDAQ folders |
| Temporal coverage | CONFIRMED by filenames and sampled first/last rows |
| Vendor/broker licence | UNVERIFIED_LOCAL_EXPORT |
| Runtime dependency on BACKTRADER | REJECTED |
