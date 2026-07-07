# EBTA AI Bootstrap

This file is the official AI entrypoint for the EBTA repository.

## Read Order

Before any substantive action, read in this order:

1. `AGENTS.md`
2. `.ai/README.md`
3. `.ai/checkpoint.json`
4. the active hook path declared in `.ai/checkpoint.json`
5. the active tracking path declared in `.ai/checkpoint.json`
6. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` if the task touches EBTA protocol, methodology, normative rules, or scientific decisions.
7. `.ai/governance/AI_MODIFICATION_CHECKLIST.md` before any normative, structural, or implementation-impacting modification.

## Responsibility Map

- `Protocole/` is the normative EBTA authority.
- `Implementation/` is the executable translation of `Protocole/`.
- `.ai/` is the single AI cockpit: macro relay, checkpoint, backlog, archive.
- `.ai/governance/` contains AI modification governance; it is procedural, not scientific authority.
- `0 - HUMAN START HERE/` is the human intake area for raw drafts.
- `Implementation/Active/` contains the micro runtime cockpit: active hook and tracking state.
- `.agents/` is historical/tooling support only; it is not a project-state authority.
- `.codex/` is a Codex adapter area only; it is not normative.

## Operating Rules

- Do not create competing sources of truth.
- Do not modify `Protocole/` unless the task explicitly requires protocol work.
- Read `.ai/governance/` before any normative, structural, or implementation-impacting modification.
- Do not modify BACKTRADER before reading its local governance and receiving explicit scope.
- Keep `AGENTS.md` thin. Put AI project state in `.ai/`, not in parallel state folders.
- Human drafts enter through `0 - HUMAN START HERE/` and are never executable by default.
- If active hook or tracking paths change, update `.ai/checkpoint.json` first; update `.ai/README.md` only when stable cockpit rules change.

## Conversational Commands

When the user sends `/start`, `/continue`, or `/close`, treat it as a request
to manage a plan. These are the human-facing commands.

- `/start` never moves or rewrites the human draft in place. It audits the
  draft, then WRITES A NEW FILE in the target backlog folder
  (`mainline`/`annexes`/`fixes`) fully restructured per
  `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`, then routes it with
  `.ai/tools/plan.ps1 start -Path <original draft> -RewrittenPath <new file
  already written in the backlog folder> -Audited`. `plan.ps1` archives the
  untouched original under `0 - HUMAN START HERE/archive/` and registers the
  rewritten file as the workstream's `source_path` (original kept as
  `original_draft_path` for traceability). Do not ask the user to
  pre-structure the human draft unless the intent is impossible to infer.
  `plan.ps1` mechanically rejects `start` if key template sections are absent
  from the rewritten file's text, or if `-RewrittenPath` is not already inside
  the folder matching `-Track` — if it throws, fix the rewritten file (never
  paste the template verbatim) and retry, do not treat the rejection as a
  formatting nuisance to route around.
- `/continue` resumes an existing workstream with `.ai/tools/plan.ps1 continue`.
- `/close` closes and archives an existing workstream with
  `.ai/tools/plan.ps1 close`.

`.ai/tools/plan.ps1` is a mechanical backend. It can refuse unsafe promotion,
but it does not replace the AI audit and structuring step.

If required parameters are missing, inspect `0 - HUMAN START HERE/` and
`.ai/checkpoint.json` before asking the user.
