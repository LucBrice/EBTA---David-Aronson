# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is not a conventional application codebase. It is **EBTA** (Evidence-Based Technical Analysis, after David Aronson), a governed system with two layers:

1. `Protocole/` — the frozen, normative methodology (statistical/scientific rules for validating trading strategies: WRC/SPA/Romano-Wolf multiple-testing correction, walk-forward segmentation, OOS governance, bias governance, etc.). This is documentation, not code, but it is the **highest authority in the repo**.
2. `Implementation/ebta_engine/` — a Python 3, standard-library-only runtime that mechanically enforces the rules in `Protocole/` (schemas, validators, gates, manifests). It has no external dependencies and no database; persistence is explicit files inside a "research package".

Everything else (`.ai/`, `.agents/`, `.codex/`, `0 - HUMAN START HERE/`) is AI-facing project-management scaffolding layered on top, not project code.

## Mandatory read order before any substantive change

Before doing real work in this repo, read in this order (per `AGENTS.md`):

1. `AGENTS.md` (root)
2. `.ai/README.md`
3. `.ai/checkpoint.json` — machine-readable current state (active workstream, active hook/tracking paths, risks)
4. The active hook file declared in `.ai/checkpoint.json` at `active_paths.active_hook_path` (currently `Implementation/Active/HOOK.md`) and the active tracking file at `active_paths.active_tracking_path` (currently `Implementation/Active/tracking.json`)
5. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` if the task touches EBTA protocol, methodology, normative rules, or scientific decisions
6. `.ai/governance/AI_MODIFICATION_CHECKLIST.md` before any normative, structural, or implementation-impacting modification

This read order is not optional ceremony — `.ai/checkpoint.json` is the single source of truth for what workstream is active and what must not be touched yet (e.g. BACKTRADER must not be integrated/modified before its local governance is read, per risk `R2`).

## Authority hierarchy (do not violate)

```
1. Protocole/MANIFESTE DE GEL EBTA.md
2. Protocole/PROTOCOLE EBTA.md
3. Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md
4. Individual SOPs (Protocole/SOP 01 ... SOP 13)
5. Protocole/PAQUET D'EXECUTION EBTA.md
6. Implementation/
7. External adapters (e.g. BACKTRADER)
```

Rules that follow from this:
- If the runtime (`Implementation/`) contradicts `Protocole/`, the runtime is wrong — fix the runtime, never silently reinterpret the protocol.
- If a rule is missing, the runtime must block or return `INCONCLUSIVE` / `DEFERRED_REQUIRES_PIPELINE_DATA` rather than guess.
- `.ai/`, `.agents/`, `.codex/` are **never** allowed to become a competing source of scientific or project-state truth. `.ai/governance/` is procedural (how an AI should classify/apply changes), not scientific authority.
- Directory roles are fixed and must not be moved: `Protocole/` (normative), `Implementation/` (executable derivative), `Implementation/Active/` (micro runtime cockpit), `.ai/` (AI cockpit: macro relay, checkpoint, backlog, archive), `0 - HUMAN START HERE/` (human intake, never directly executable), `.agents/` and `.codex/` (non-normative tooling/adapters only).

## Modifications forbidden without an explicit human decision

(from `.ai/governance/AI_MODIFICATION_CHECKLIST.md`)
- Rewriting the EBTA protocol or SOPs, or changing the protocol's scientific hierarchy.
- Moving `.agents/`, `.codex/`, `Protocole/`, or `Implementation/`.
- Introducing RAG, embeddings, a vector database, or autonomous agents.
- Adding technical dependencies (the engine is stdlib-only by design).
- Modifying implementation code except when strictly required to update a documentary trace.

## Human/AI workflow commands

Conversational commands the user may type — these drive `.ai/tools/plan.ps1`, the mechanical backend for backlog state (it does not do semantic audit; the AI must audit/structure first):

- `/start "0 - HUMAN START HERE/PLAN.md"` — audit a raw human draft, structure it if needed, route it to `.ai/backlog/mainline|annexes|fixes/`, then call `.ai/tools/plan.ps1 start -Audited` (this requires the plan to already have `Track`, `Lifecycle`, `Scope`, `Non-goals`, `Source`, `Exit criteria` sections).
- Between `/start` and `/continue`: run an architecture-refinement loop on the plan via `code-architecture-evaluator` (`/evaluate`) — fix what it flags, re-run, repeat up to 3-4 passes max, then commit the refined plan as a pre-implementation baseline (topic-scoped commit matching this repo's existing style, e.g. commit `184b013`). Only then does `/continue` begin implementation.
- `/continue PLAN_ID` — resume a workstream (`.ai/tools/plan.ps1 continue`).
- `/close PLAN_ID` — first apply `.agents/skills/bug-hunter/SKILL.md` on the workstream's touched files and `.agents/skills/plan-conformance-audit/SKILL.md` against its Exit criteria; only close and archive with `.ai/tools/plan.ps1 close` if bug-hunter reports zero open confirmed bugs and no Exit criterion is reported missing.

Workstream lifecycle: `INTAKE -> TRIAGED -> PLANNED -> ACTIVE -> BLOCKED/DONE/REJECTED/SUPERSEDED -> ARCHIVED`. Files dropped in `0 - HUMAN START HERE/` are always `INTAKE` and not executable until audited and routed.

## Commands

Run the full runtime test suite (from repo root):

```powershell
python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation
```

Run a single test file or case:

```powershell
python -m unittest Implementation.ebta_engine.tests.test_gates
python -m unittest Implementation.ebta_engine.tests.test_gates.TestGateName.test_method_name
```

Run the minimal pilot pipeline (builds a full `research_package` end-to-end and exercises the engine as a whole):

```powershell
python Implementation/examples/minimal_pilot_pipeline/build_research_package.py
```

Validate the JSON project-state files after editing them:

```powershell
python -m json.tool .ai\checkpoint.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -m json.tool Implementation\Active\tracking.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
```

There is no build step, linter, or package manifest — the engine is Python 3 standard library only (no `requirements.txt`/`pyproject.toml` by design; do not add dependencies without an explicit human decision, see above).

## `Implementation/ebta_engine/` architecture

- `procedures/` — deterministic calculation procedures derived from the protocol (`wrc.py` = White's Reality Check, `detrending.py`, `bootstrap.py`, `walk_forward.py`, `zero_centering.py`, `oos_confidence_interval.py`, etc.). Each corresponds to a specific SOP; see `Implementation/PROCEDURE_CALCULATION_MAP.md` for the SOP-to-file mapping.
- `governance/` — the "G-BIAS" runtime layer (SOP 13): bias registry/schema, append-only incident logger, pre-OOS checkers (registry completeness, candidate family, metric lock, robustness), the OOS access guard (blocks/burns on unauthorized access), and `bias_gate.py`, the aggregate gate producing `PASS`/`FAIL`/`INCONCLUSIVE`/`BURNED`.
- `validators/` — schema and package validation ("the customs check"): `package_validator.py`, `gate_validator.py`, `invariant_validator.py`, `registry_append_only_validator.py`.
- `schemas/` — JSON Schemas for every artifact type (config, registry events, OOS access events, walk-forward declaration, robustness plan, reproducibility manifest, etc.), validated by a small internal validator restricted to the keywords actually used (no external `jsonschema` dependency in the runtime itself, only in test/CI tooling).
- `manifests/` — SHA-256 manifest generation/verification ("the notary") proving package integrity.
- `adapters/` — boundary code for external engines (currently `backtrader_mapping.py`). An adapter treats external output as untrusted, maps it into EBTA artifacts, and lets the core validate the contract — it never silently "fixes" mapping errors or imports the external tool's conventions as EBTA norms.
- `persistence.py` — explicit file-based read/write of research package artifacts (no DB).
- `constants.py` — canonical status/version enums sourced from `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
- `tests/` + `fixtures/` — `unittest`-based suite; fixtures include intentionally invalid packages (`fixtures/invalid_invariants`, `invalid_missing_required`, `invalid_rejection_tests`) to test gate rejection paths, plus `fixtures/valid_minimal`.
- `migrations/` — deterministic, tested schema migrations with no change in normative meaning and no information loss without an explicit decision.

A "research package" — the artifact this whole engine validates — has the shape:

```
research_package/
  config.json
  registry.jsonl         # append-only
  oos_access_log.jsonl   # append-only
  reports/
  series/
  manifests/
```

Version compatibility is tracked explicitly: `Protocole` version (currently `EBTA-DOC-1.1`) is normative and versions independently from `EBTA-ENGINE` (currently `0.1.0`) and `schema_version` (currently `1.0.0`, on every persisted artifact). A package with an unsupported schema version must be rejected, not coerced.

## Current state / active workstream

Check `.ai/checkpoint.json` for the live answer — do not trust this section once it goes stale. As of the last update, `STEP_3_BACKTRADER_INTEGRATION` is pending, and a draft plan at `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF.md` is under discussion proposing that EBTA become a fully native backtesting engine (with BACKTRADER downgraded to a read-only reference for porting useful components, not something to integrate durably). This is a draft, not a decision — do not act on it as though it were settled.

## Practical notes

- Files are largely written in French (protocol, SOPs, governance docs); code (Python identifiers, docstrings, test names) is in English.
- JSON project-state files (`.ai/checkpoint.json`, `Implementation/Active/tracking.json`) are schema-constrained (`checkpoint.schema.json`, `tracking.schema.json`) — validate against the schema after any manual edit, not just JSON syntax.
- Two append-only logs exist by contract (`registry.jsonl`, `oos_access_log.jsonl`) — the runtime treats them as untrusted input and validates them with `registry_append_only_validator.py`; never rewrite or truncate them to "fix" data.
- After any change touching `Implementation/`, `Protocole/`, or `.ai/`, follow the post-modification checklist in `.ai/governance/AI_MODIFICATION_CHECKLIST.md`: summarize files changed and why, list files deliberately left unchanged, list unresolved conflicts, list remaining human decisions, and run the relevant validation commands above.
- Before declaring any `Implementation/ebta_engine/` code change done, apply `.agents/skills/bug-hunter/SKILL.md` on the touched files (Pyrefly is installed as a dev CLI in `Implementation/adapters/nautilus_env/venv`). A confirmed real bug it finds must be fixed or explicitly escalated before the task counts as complete.
