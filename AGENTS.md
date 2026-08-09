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
8. `.ai/workflows/README.md`, then the applicable `WORKFLOW.md`, before workflow-specific action.

## Responsibility Map

- `Protocole/` is the normative EBTA authority.
- `Implementation/` is the executable translation of `Protocole/`.
- `.ai/` is the single AI cockpit: macro relay, checkpoint, backlog, archive.
- `.ai/governance/` contains AI modification governance; it is procedural, not scientific authority.
- `.ai/workflows/` contains workflow-specific procedures; it is neither scientific authority nor project-state storage.
- `.ai/architecture/` records adoption of external architecture practices; it is neither scientific authority nor a project-state cockpit.
- `0 - HUMAN START HERE/` is the human intake area for raw drafts.
- `Implementation/Active/` contains the micro runtime cockpit: active hook and tracking state.
- `.agents/` is historical/tooling support only; it is not a project-state authority. It also hosts `.agents/skills/`, a cross-AI catalog of playbooks (SKILL.md files) usable by any AI working on this repo, not only Claude — see Operating Rules.
- `.codex/` is a Codex adapter area only; it is not normative.

## Operating Rules

- Before starting substantive work, verify this checkout is not behind `origin/main` (`git fetch` then compare `HEAD` to `origin/main`). This applies to every AI working in this repo, not only Claude Code: a checkout is a per-clone/per-worktree state that no tool's own hooks can sync on your behalf when a push happened elsewhere. `Implementation/Active/pre_push_hook.py` mechanically blocks the destructive case (pushing a rewritten/diverged history) and warns on plain staleness at push time; this rule covers the earlier moment of starting work from a stale base, which no git hook can catch on its own.
- Do not create competing sources of truth.
- Do not modify `Protocole/` unless the task explicitly requires protocol work.
- Read `.ai/governance/` before any normative, structural, or implementation-impacting modification.
- Keep `AGENTS.md` thin. Put AI project state in `.ai/`, not in parallel state folders.
- Human drafts enter through `0 - HUMAN START HERE/` and are never executable by default.
- If active hook or tracking paths change, update `.ai/checkpoint.json` first; update `.ai/README.md` only when stable cockpit rules change.
- Follow the commit contract in `.ai/workflows/common/WORKFLOW.md`.
- Use `POLICIES.md` only as an authorization index; its cited owner files prevail.
- Consult `.agents/skills/` and follow each matching `SKILL.md` trigger.

## Conversational Commands

Treat `/start`, `/continue`, and `/close` as plan-management commands.
Follow `.ai/workflows/common/WORKFLOW.md`, then the specialized workflow
selected by `.ai/workflows/README.md`. The common workflow owns the detailed
evaluation loops, promotion/continuation/closure mechanics, validation,
commit contract, multi-lot gate, and clarification policy.

Treat `/learn-session` as a retrospective command. Invoke
`.agents/skills/capture-coding-session-learnings/SKILL.md`; analysis and
proposal are allowed by the command, while persistence, commit, push, and
external publication each require their own explicit authorization.
After every terminal `/close`, invoke the same retrospective automatically at
the point defined by `.ai/workflows/common/WORKFLOW.md`; this trigger grants no
additional write, commit, push, or publication authority.
