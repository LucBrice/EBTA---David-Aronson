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
- `.agents/` is historical/tooling support only; it is not a project-state authority. It also hosts `.agents/skills/`, a cross-AI catalog of playbooks (SKILL.md files) usable by any AI working on this repo, not only Claude — see Operating Rules.
- `.codex/` is a Codex adapter area only; it is not normative.

## Operating Rules

- Do not create competing sources of truth.
- Do not modify `Protocole/` unless the task explicitly requires protocol work.
- Read `.ai/governance/` before any normative, structural, or implementation-impacting modification.
- Do not modify BACKTRADER before reading its local governance and receiving explicit scope.
- Keep `AGENTS.md` thin. Put AI project state in `.ai/`, not in parallel state folders.
- Human drafts enter through `0 - HUMAN START HERE/` and are never executable by default.
- If active hook or tracking paths change, update `.ai/checkpoint.json` first; update `.ai/README.md` only when stable cockpit rules change.
- Every commit touching this repo (by any AI or human) follows the detailed
  commit-message shape already in this repo's history — see e.g. `94338b6` or
  `184b013` as reference examples, not a one-off style. Minimum shape: a
  `type(scope): summary` title (French scope/summary matching this repo's
  convention), then a body with (1) the why — which audit/plan/finding drove
  the change, not just what changed; (2) numbered root causes/changes if more
  than one distinct thing is fixed; (3) a "Fichiers modifies" section listing
  each changed file with the reason it changed; (4) a "Non touches" section
  naming what was deliberately left alone (e.g. `Protocole/`, `validators/`)
  to prove scope was respected; (5) a "Validation" section with the actual
  commands run and their real result (tests, schema validation, package
  build, pre-commit hook), not generic claims; (6) a `Co-Authored-By` footer
  naming the authoring AI. A short one-line commit message is not acceptable
  for changes under `Implementation/`, `Protocole/`, or `.ai/` — rewrite it
  (amend, since not yet pushed) before moving on if the first draft is too
  thin.
- Consult `.agents/skills/` for specialized playbooks. Each `SKILL.md` documents its own trigger; when a task's shape matches one, read and follow it, regardless of which AI or tool is operating. In particular:
  - After implementing or modifying code under `Implementation/ebta_engine/` (or adjacent adapters/examples), and before declaring the task done, apply `.agents/skills/bug-hunter/SKILL.md` on the touched files. A confirmed real bug it finds must be fixed (or explicitly escalated to the human) before the task counts as complete.
  - Before calling `.ai/tools/plan.ps1 close` (see `/close` below), apply both `.agents/skills/bug-hunter/SKILL.md` (full sweep of the workstream's touched files, not just the last diff) and `.agents/skills/plan-conformance-audit/SKILL.md`. Do not call `plan.ps1 close` if either reports an open confirmed bug or a missing Exit criterion.

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
- After `/start` writes the plan and before `/continue` begins real
  implementation, run an architecture-refinement loop on the plan: invoke
  `code-architecture-evaluator` (`/evaluate`), fix what it flags, re-run
  `/evaluate`, and repeat until no major blind spot remains — cap at 3-4
  passes total; if issues are still surfacing after that, the plan itself
  needs human input, not another automated pass. Once the loop converges,
  commit the current state (the refined plan plus any `/evaluate`-driven
  fixes) as a clean pre-implementation baseline, matching this repo's
  existing commit style (topic-scoped `type(scope): summary` title, a body
  itemizing what changed and why per file/section, a test-suite status
  line, `Co-Authored-By`). This baseline exists so implementation starts
  from a reviewed, revertible point — see e.g. commit `184b013` for the
  expected shape. Only then does `/continue` begin implementation.
- `/continue` resumes an existing workstream with `.ai/tools/plan.ps1 continue`.
- `/close` first applies `.agents/skills/bug-hunter/SKILL.md` on the
  workstream's touched files and `.agents/skills/plan-conformance-audit/SKILL.md`
  against its Exit criteria. Only if bug-hunter reports zero open confirmed
  bugs AND the conformance audit reports no missing criterion does `/close`
  proceed to close and archive the workstream with `.ai/tools/plan.ps1 close`.
  Otherwise report what is open (bugs and/or missing criteria) and do not
  call `plan.ps1 close` until the human decides how to proceed.

`.ai/tools/plan.ps1` is a mechanical backend. It can refuse unsafe promotion,
but it does not replace the AI audit and structuring step.

If required parameters are missing, inspect `0 - HUMAN START HERE/` and
`.ai/checkpoint.json` before asking the user.
