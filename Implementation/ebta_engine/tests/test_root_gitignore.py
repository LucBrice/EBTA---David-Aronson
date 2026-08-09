from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ROOT_GITIGNORE = REPO_ROOT / ".gitignore"

EXPECTED_RULES = (
    "__pycache__/",
    "*.py[cod]",
    ".venv/",
    "venv/",
    ".pytest_cache/",
    ".pyrefly/",
    ".ruff_cache/",
    ".env",
    ".env.*",
    "!.env.example",
    ".claude/settings.local.json",
    ".DS_Store",
    "Thumbs.db",
    "*.log",
    "*.tmp",
)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", *args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def policy_rules(text: str) -> tuple[str, ...]:
    return tuple(
        line
        for raw_line in text.splitlines()
        if (line := raw_line.strip()) and not line.startswith("#")
    )


def policy_contract_errors(text: str) -> list[str]:
    rules = policy_rules(text)
    return [] if rules == EXPECTED_RULES else ["root gitignore policy differs"]


class RootGitignoreTests(unittest.TestCase):
    def test_root_policy_is_exact_and_reviewable(self):
        text = ROOT_GITIGNORE.read_text(encoding="utf-8")
        self.assertEqual(policy_contract_errors(text), [])

    def test_hostile_policy_mutations_are_rejected(self):
        text = ROOT_GITIGNORE.read_text(encoding="utf-8")
        mutations = (
            text.replace(".env\n", ""),
            text.replace("!.env.example", ""),
            text.replace("*.tmp", ".vscode/"),
            text + "\n*.md\n",
        )
        for mutated_text in mutations:
            with self.subTest(mutated_text=mutated_text):
                self.assertTrue(policy_contract_errors(mutated_text))


    def test_local_artifacts_are_ignored_by_root_policy(self):
        cases = {
            ".env": ".env",
            ".env.local": ".env.*",
            ".claude/settings.local.json": ".claude/settings.local.json",
            ".venv/pyvenv.cfg": ".venv/",
            "scratch/venv/pyvenv.cfg": "venv/",
            "scratch/__pycache__/module.cpython-313.pyc": "__pycache__/",
            ".pytest_cache/state": ".pytest_cache/",
            ".pyrefly/state": ".pyrefly/",
            ".ruff_cache/state": ".ruff_cache/",
            "debug.log": "*.log",
            "scratch.tmp": "*.tmp",
        }
        for path, pattern in cases.items():
            with self.subTest(path=path):
                result = git("check-ignore", "--no-index", "--verbose", "--", path)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f":{pattern}\t", result.stdout)
                self.assertIn(".gitignore:", result.stdout)

    def test_sources_and_examples_remain_visible(self):
        paths = (
            ".env.example",
            ".vscode/settings.json",
            "0 - HUMAN START HERE/example.md",
            "Implementation/ebta_engine/example.py",
            "Protocole/example.md",
        )
        for path in paths:
            with self.subTest(path=path):
                result = git("check-ignore", "--no-index", "--quiet", "--", path)
                self.assertEqual(result.returncode, 1, result.stderr)

    def test_no_tracked_file_is_ignored(self):
        result = git("ls-files", "-ci", "--exclude-standard")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
