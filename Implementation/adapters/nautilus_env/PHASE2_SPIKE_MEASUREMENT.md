# Nautilus Phase 2 Spike Measurement

## Status

| Field | Value |
| --- | --- |
| Date | 2026-07-09 |
| Runtime | `nautilus_trader==1.230.0` |
| Scope | Phase 2 deterministic golden case |
| Classification | ADAPTER_MAPPING / TEST_FIXTURE |
| Protocol impact | NONE |

## Environment

The reproducible setup script is versioned at
`Implementation/adapters/nautilus_env/setup_env.ps1`.

The target short-path convention maps `N:` to the repository root and creates
the venv at `N:\Implementation\.venv-nautilus` by default. The local spike
measurement reused the already installed compatibility venv through:

```powershell
.\Implementation\adapters\nautilus_env\setup_env.ps1 `
  -VenvRelativePath "Implementation\adapters\nautilus_env\venv" `
  -SkipInstall
```

This keeps the Phase 2 proof on the installed `nautilus_trader==1.230.0`
environment without introducing a second heavy venv into the working tree.

## Golden Case

The measured runner is:

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe `
  .\Implementation\adapters\nautilus_env\run_golden_case.py
```

It executes one deterministic candidate on one toy fold and returns a
`SimulationResult` matching
`Implementation/ebta_engine/tests/fixtures/nautilus_golden_case/expected_result.py`.

Observed deterministic facts:

- `BacktestEngine` instantiates and runs.
- The first market buy fills at the close of the first bar: `101.0`.
- The closing order fills at the close of the third bar: `103.0`.
- Total costs are zero because the instrument is constructed with
  `maker_fee=0` and `taker_fee=0`.
- Realized PnL is `2.0`.
- NAV path is `[1000.0, 1001.0, 1002.0]`.

## Timing

Measured command:

```powershell
Measure-Command {
  .\Implementation\adapters\nautilus_env\venv\Scripts\python.exe `
    .\Implementation\adapters\nautilus_env\run_golden_case.py | Out-Null
}
```

Observed wall-clock time:

```text
TotalSeconds      2.22
TotalMilliseconds 2224.64
```

The command emitted only `Pandas4Warning` warnings from Nautilus internals
around `Timestamp.utcnow`; the run itself passed.

## K x (M+1) Extrapolation

The current pilot input file declares exactly one walk-forward fold:

```text
K = 1
```

The Nautilus pivot decision E11 fixes the Phase 2 candidate count at:

```text
M = 16
```

The Phase 2 upper-bound call count is therefore:

```text
K x (M + 1) = 1 x 17 = 17 runs
```

Using the measured single-run wall-clock time:

```text
17 x 2.22464 s = 37.81888 s
```

This is a spike extrapolation, not a production benchmark. It includes Python
startup/import overhead for each isolated run and does not assume
parallelization, streaming, data reuse, or warm engine reuse.

## Decision

Phase 2 establishes feasibility for a Nautilus-backed `SimulationResult` and
does not yet justify adding streaming complexity. Revisit `engine.run(streaming=True)`
only if Phase 5 multi-fold orchestration shows a real runtime bottleneck on the
full EBTA data and candidate set.
