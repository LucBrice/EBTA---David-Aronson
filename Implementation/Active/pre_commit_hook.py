#!/usr/bin/env python
"""Pre-commit hook: detect stale .ai/checkpoint.json and invalid cockpit
JSON schemas before committing.

Install as .git/hooks/pre-commit (see Implementation/Active/INSTALL_GIT_HOOK.md).
"""
import json
import subprocess
import sys
from pathlib import Path

CHECKPOINT = Path(".ai/checkpoint.json")
RELAY_FILES = [
    ".ai/README.md",
    ".ai/checkpoint.json",
    ".ai/checkpoint.schema.json",
]
RELAY_PREFIXES = [
    ".ai/backlog/",
    ".ai/tools/",
]

# Files with a companion JSON Schema that must validate before commit.
# Independent of RELAY_FILES/RELAY_PREFIXES above (Implementation/Active/tracking.json
# is not an AI-cockpit relay file, but it is schema-constrained project state -
# see CLAUDE.md's "Validate the JSON project-state files" section).
SCHEMA_CHECKED_FILES = {
    ".ai/checkpoint.json": ".ai/checkpoint.schema.json",
    "Implementation/Active/tracking.json": "Implementation/Active/tracking.schema.json",
}


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return set(result.stdout.splitlines())


def get_last_commit_date():
    """Return the last commit's author date, truncated to yyyy-MM-dd.

    checkpoint.json's updated_at field is date-only (see
    .ai/tools/plan.ps1::Write-Checkpoint, which always writes
    "yyyy-MM-dd"). Comparing it against a full ISO-8601 timestamp
    (previous behavior, %aI) meant a date-only string is always treated
    as "earlier" than any same-day timestamp in plain string comparison,
    permanently blocking every commit after the first one made on a given
    day. Truncating both sides to date granularity fixes that false
    positive while still catching a genuinely stale (older-day) checkpoint.
    """
    result = subprocess.run(
        ["git", "log", "--format=%ad", "--date=short", "-n", "1"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def is_ai_cockpit_file(path):
    return path in RELAY_FILES or any(path.startswith(prefix) for prefix in RELAY_PREFIXES)


def check_staleness(staged):
    """Block a commit that touches the AI cockpit while checkpoint.updated_at
    is stale (unchanged since a prior day's commit). Returns 0 (pass) or 1
    (block); prints its own diagnostics either way, matching this hook's
    pre-existing behavior.
    """
    if not any(is_ai_cockpit_file(f) for f in staged):
        return 0

    if not CHECKPOINT.exists():
        print("[EBTA pre-commit] WARNING: .ai/checkpoint.json not found. Skipping stale check.")
        return 0

    try:
        checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        print(f"[EBTA pre-commit] ERROR: .ai/checkpoint.json is not valid JSON: {e}")
        return 1

    updated_at = checkpoint.get("updated_at", "")
    last_commit_date = get_last_commit_date()

    if last_commit_date and updated_at and updated_at < last_commit_date:
        print()
        print("=" * 72)
        print("[EBTA pre-commit] BLOCKED: checkpoint.json is stale.")
        print(f"  checkpoint.updated_at : {updated_at}")
        print(f"  last commit date       : {last_commit_date}")
        print()
        print("  Action requise: mettre a jour .ai/checkpoint.json avant")
        print("  de committer les fichiers du cockpit IA actif.")
        print("  Voir AGENTS.md et .ai/README.md.")
        print("=" * 72)
        print()
        return 1

    print(f"[EBTA pre-commit] checkpoint.json is current ({updated_at}). OK.")
    return 0


def _resolve_schema_validator():
    """Return (validate_fn, is_full_coverage).

    validate_fn(instance, schema) -> list[str] of human-readable error
    messages (empty list means valid).

    jsonschema (external) is authoritative when importable - it is the same
    library CLAUDE.md's documented manual validation commands use, and it
    supports every keyword these two schemas use (pattern, format,
    uniqueItems, maxItems, among others).

    If jsonschema is not installed, this falls back to the repo's own
    ebta_engine.schema_validation - a stdlib-only subset validator built for
    the runtime's own schemas (type, required, properties, items, enum,
    additionalProperties, minItems only; see that module's docstring). This
    fallback does NOT check pattern/format/uniqueItems/maxItems, so it can
    miss a real violation. The caller must print an explicit downgrade
    notice whenever this fallback is used - silently claiming the same
    coverage as jsonschema would recreate exactly the kind of false
    assurance this hook exists to prevent (see PLAN_ADVERSARIAL_TESTER_GOUVERNANCE_OUTILLE
    for the sibling finding on incident_logger.py's silent fallback).
    Pyrefly/jsonschema for CI is explicitly authorized by the human decision
    logged in EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md section 10 for the
    CI runner only, not as a hard local dependency - so this hook must keep
    working, at reduced strength, on a machine that never installed it.
    """
    try:
        import jsonschema
    except ImportError:
        def _validate_partial(instance, schema):
            sys.path.insert(0, "Implementation")
            from ebta_engine.schema_validation import validate as _validate

            errors = _validate(instance, schema)
            return [f"{error.path}: {error.message}" for error in errors]

        return _validate_partial, False

    def _validate_full(instance, schema):
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator = validator_cls(schema)
        messages = []
        for error in sorted(validator.iter_errors(instance), key=str):
            location = "/".join(str(part) for part in error.absolute_path) or "$"
            messages.append(f"{location}: {error.message}")
        return messages

    return _validate_full, True


def check_schemas(staged):
    """Block a commit that stages checkpoint.json or tracking.json with
    content that fails their JSON Schema. Returns 0 (pass) or 1 (block).
    """
    touched = [path for path in SCHEMA_CHECKED_FILES if path in staged]
    if not touched:
        return 0

    validate_fn, is_full_coverage = _resolve_schema_validator()
    if not is_full_coverage:
        print(
            "[EBTA pre-commit] WARNING: jsonschema is not installed - falling back "
            "to the internal partial validator (pattern/format/uniqueItems/maxItems "
            "are NOT checked by this fallback). Install jsonschema for full coverage."
        )

    blocked = False
    for data_path in touched:
        schema_path = Path(SCHEMA_CHECKED_FILES[data_path])
        try:
            instance = json.loads(Path(data_path).read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as e:
            print(f"[EBTA pre-commit] ERROR: {data_path} is not valid JSON: {e}")
            blocked = True
            continue
        except FileNotFoundError:
            print(f"[EBTA pre-commit] WARNING: {data_path} is staged but not found on disk. Skipping schema check.")
            continue

        if not schema_path.exists():
            print(f"[EBTA pre-commit] ERROR: schema file not found for {data_path}: {schema_path}")
            blocked = True
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))

        errors = validate_fn(instance, schema)
        if errors:
            print()
            print("=" * 72)
            print(f"[EBTA pre-commit] BLOCKED: {data_path} fails schema validation ({schema_path}).")
            for message in errors:
                print(f"  - {message}")
            print("=" * 72)
            print()
            blocked = True
        else:
            print(f"[EBTA pre-commit] {data_path} matches {schema_path}. OK.")

    return 1 if blocked else 0


def main():
    staged = get_staged_files()
    staleness_result = check_staleness(staged)
    schema_result = check_schemas(staged)
    return 1 if (staleness_result or schema_result) else 0


if __name__ == "__main__":
    sys.exit(main())
