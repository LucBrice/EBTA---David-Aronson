# Minimal EBTA Pilot Pipeline

This example is a local pilot pipeline for `EBTA-ENGINE-0.1.0`.

It does not define EBTA methodology and does not read or write `BACKTRADER`.
Its only role is to prove that a small deterministic research workflow can
produce a `research_package/` accepted by `validate_package_dir()`.

## Inputs

The pilot input contract is explicit and local:

```text
Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json
```

It defines the preregistered pilot identifiers, PIT snapshot, Walk-Forward
schedule, candidate grid, statistical plan, robustness scenarios, OOS access
event, OOS series, and compact procedure inputs used by the example.

The expected package shape is:

```text
Implementation/examples/minimal_pilot_pipeline/inputs/package_shape.json
```

The shape lists the artifacts that must be present in the generated
`research_package/` and then referenced by the reproducibility manifest. The
runtime validator remains the authority for PASS/FAIL.

## Run

From the repository root:

```powershell
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
```

The command recreates:

```text
Implementation/examples/minimal_pilot_pipeline/research_package/
```

Expected terminal status:

```text
PASS
```

## Boundary

- Normative source: `Protocole/PAQUET D'EXECUTION EBTA.md` sections 2, 3, 5, 6.
- Runtime control bench: `Implementation/ebta_engine/`.
- Package validator: `ebta_engine.validators.package_validator.validate_package_dir`.
- Protocol impact: none.
