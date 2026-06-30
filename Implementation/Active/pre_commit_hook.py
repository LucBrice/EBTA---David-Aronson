#!/usr/bin/env python3
"""Pre-commit hook: detect stale .ai/checkpoint.json before committing.

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


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return set(result.stdout.splitlines())


def get_last_commit_timestamp():
    result = subprocess.run(
        ["git", "log", "--format=%aI", "-n", "1"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def is_ai_cockpit_file(path):
    return path in RELAY_FILES or any(path.startswith(prefix) for prefix in RELAY_PREFIXES)


def main():
    staged = get_staged_files()

    # Only run check if any active AI cockpit file is being committed.
    if not any(is_ai_cockpit_file(f) for f in staged):
        return 0

    if not CHECKPOINT.exists():
        print("[EBTA pre-commit] WARNING: .ai/checkpoint.json not found. Skipping stale check.")
        return 0

    try:
        checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[EBTA pre-commit] ERROR: .ai/checkpoint.json is not valid JSON: {e}")
        return 1

    updated_at = checkpoint.get("updated_at", "")
    last_commit = get_last_commit_timestamp()

    if last_commit and updated_at and updated_at <= last_commit:
        print()
        print("=" * 72)
        print("[EBTA pre-commit] BLOCKED: checkpoint.json is stale.")
        print(f"  checkpoint.updated_at : {updated_at}")
        print(f"  last commit timestamp  : {last_commit}")
        print()
        print("  Action requise: mettre a jour .ai/checkpoint.json avant")
        print("  de committer les fichiers du cockpit IA actif.")
        print("  Voir AGENTS.md et .ai/README.md.")
        print("=" * 72)
        print()
        return 1

    print(f"[EBTA pre-commit] checkpoint.json is current ({updated_at}). OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
