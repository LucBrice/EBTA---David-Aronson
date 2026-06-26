# Minimal EBTA Pilot Pipeline

This example is a local pilot pipeline for `EBTA-ENGINE-0.1.0`.

It does not define EBTA methodology and does not read or write `BACKTRADER`.
Its only role is to prove that a small deterministic research workflow can
produce a `research_package/` accepted by `validate_package_dir()`.

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
