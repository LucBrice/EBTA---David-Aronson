"""Tests for the versioned git hook sources under Implementation/Active/.

Implementation/Active/ is not a Python package (it hosts the source of
truth for hooks installed at .git/hooks/, per
Implementation/Active/INSTALL_GIT_HOOK.md), so the modules are loaded here
via importlib.util rather than a normal package import.
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ACTIVE_DIR = Path(__file__).resolve().parents[2] / "Active"


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ACTIVE_DIR / filename)
    assert spec is not None, f"Could not build a module spec for {filename}"
    assert spec.loader is not None, f"Module spec for {filename} has no loader"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pre_commit_hook = _load_module("ebta_pre_commit_hook_under_test", "pre_commit_hook.py")
pre_push_hook = _load_module("ebta_pre_push_hook_under_test", "pre_push_hook.py")


class PreCommitStalenessTests(unittest.TestCase):
    def test_non_cockpit_file_skips_the_check_entirely(self):
        result = pre_commit_hook.check_staleness({"Implementation/ebta_engine/foo.py"})
        self.assertEqual(result, 0)

    def test_cockpit_file_staged_with_stale_checkpoint_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_path = Path(temp_dir) / "checkpoint.json"
            checkpoint_path.write_text(json.dumps({"updated_at": "2020-01-01"}), encoding="utf-8")
            with (
                patch.object(pre_commit_hook, "CHECKPOINT", checkpoint_path),
                patch.object(pre_commit_hook, "get_last_commit_date", return_value="2026-08-07"),
            ):
                result = pre_commit_hook.check_staleness({".ai/checkpoint.json"})
        self.assertEqual(result, 1)

    def test_cockpit_file_staged_with_current_checkpoint_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_path = Path(temp_dir) / "checkpoint.json"
            checkpoint_path.write_text(json.dumps({"updated_at": "2026-08-07"}), encoding="utf-8")
            with (
                patch.object(pre_commit_hook, "CHECKPOINT", checkpoint_path),
                patch.object(pre_commit_hook, "get_last_commit_date", return_value="2026-08-07"),
            ):
                result = pre_commit_hook.check_staleness({".ai/tools/plan.ps1"})
        self.assertEqual(result, 0)

    def test_malformed_checkpoint_json_is_blocked_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_path = Path(temp_dir) / "checkpoint.json"
            checkpoint_path.write_text("{not valid json", encoding="utf-8")
            with patch.object(pre_commit_hook, "CHECKPOINT", checkpoint_path):
                result = pre_commit_hook.check_staleness({".ai/checkpoint.json"})
        self.assertEqual(result, 1)


class PreCommitSchemaTests(unittest.TestCase):
    """Adversarial regression for Lot 2: a checkpoint.json/tracking.json
    that violates its own schema must block the commit, not pass silently.
    """

    def _schema_checked_paths(self, temp_dir: str):
        checkpoint_data = Path(temp_dir) / "checkpoint.json"
        checkpoint_schema = Path(temp_dir) / "checkpoint.schema.json"
        tracking_data = Path(temp_dir) / "tracking.json"
        tracking_schema = Path(temp_dir) / "tracking.schema.json"
        return {
            str(checkpoint_data): str(checkpoint_schema),
            str(tracking_data): str(tracking_schema),
        }

    def test_no_schema_checked_file_staged_is_a_noop(self):
        result = pre_commit_hook.check_schemas({"Implementation/ebta_engine/foo.py"})
        self.assertEqual(result, 0)

    def test_invalid_checkpoint_json_content_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mapping = self._schema_checked_paths(temp_dir)
            checkpoint_data_path, checkpoint_schema_path = next(iter(mapping.items()))
            Path(checkpoint_schema_path).write_text(
                json.dumps({"type": "object", "required": ["schema_version"], "properties": {"schema_version": {"type": "string"}}}),
                encoding="utf-8",
            )
            # Hostile: required field entirely absent.
            Path(checkpoint_data_path).write_text(json.dumps({"not_the_right_field": True}), encoding="utf-8")

            with patch.object(pre_commit_hook, "SCHEMA_CHECKED_FILES", mapping):
                result = pre_commit_hook.check_schemas({checkpoint_data_path})
        self.assertEqual(result, 1)

    def test_valid_checkpoint_json_content_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mapping = self._schema_checked_paths(temp_dir)
            checkpoint_data_path, checkpoint_schema_path = next(iter(mapping.items()))
            Path(checkpoint_schema_path).write_text(
                json.dumps({"type": "object", "required": ["schema_version"], "properties": {"schema_version": {"type": "string"}}}),
                encoding="utf-8",
            )
            Path(checkpoint_data_path).write_text(json.dumps({"schema_version": "1.3.0"}), encoding="utf-8")

            with patch.object(pre_commit_hook, "SCHEMA_CHECKED_FILES", mapping):
                result = pre_commit_hook.check_schemas({checkpoint_data_path})
        self.assertEqual(result, 0)

    def test_pattern_keyword_violation_is_caught_when_jsonschema_available(self):
        # This is the adversarial case that motivated keeping jsonschema as
        # the authoritative validator: the internal fallback validator
        # (ebta_engine.schema_validation) does not implement "pattern" at
        # all (see that module's docstring) and would silently accept this.
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            self.skipTest("jsonschema not installed in this environment; fallback-only coverage cannot be distinguished here.")

        with tempfile.TemporaryDirectory() as temp_dir:
            mapping = self._schema_checked_paths(temp_dir)
            data_path, schema_path = next(iter(mapping.items()))
            Path(schema_path).write_text(
                json.dumps(
                    {
                        "type": "object",
                        "required": ["schema_version"],
                        "properties": {"schema_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"}},
                    }
                ),
                encoding="utf-8",
            )
            # Hostile: schema_version present (satisfies the fallback
            # validator's weaker "required"/"type" checks) but does not
            # match the required semver pattern.
            Path(data_path).write_text(json.dumps({"schema_version": "not-a-semver"}), encoding="utf-8")

            with patch.object(pre_commit_hook, "SCHEMA_CHECKED_FILES", mapping):
                result = pre_commit_hook.check_schemas({data_path})
        self.assertEqual(result, 1)

    def test_fallback_validator_still_catches_basic_violations_without_jsonschema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mapping = self._schema_checked_paths(temp_dir)
            data_path, schema_path = next(iter(mapping.items()))
            Path(schema_path).write_text(
                json.dumps({"type": "object", "required": ["schema_version"], "properties": {"schema_version": {"type": "string"}}}),
                encoding="utf-8",
            )
            Path(data_path).write_text(json.dumps({}), encoding="utf-8")

            def _raise_import_error(name, *args, **kwargs):
                if name == "jsonschema":
                    raise ImportError("simulated: jsonschema not installed")
                return real_import(name, *args, **kwargs)

            real_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __builtins__.__import__
            with (
                patch.object(pre_commit_hook, "SCHEMA_CHECKED_FILES", mapping),
                patch("builtins.__import__", side_effect=_raise_import_error),
            ):
                result = pre_commit_hook.check_schemas({data_path})
        self.assertEqual(result, 1)


class PrePushHookTests(unittest.TestCase):
    def test_passing_suite_allows_the_push(self):
        with (
            patch("sys.stdin", io.StringIO("")),
            patch.object(pre_push_hook.subprocess, "run") as mock_run,
        ):
            mock_run.return_value.returncode = 0
            result = pre_push_hook.main()
        self.assertEqual(result, 0)
        mock_run.assert_called_once_with(pre_push_hook.TEST_COMMAND)

    def test_failing_suite_blocks_the_push(self):
        with (
            patch("sys.stdin", io.StringIO("")),
            patch.object(pre_push_hook.subprocess, "run") as mock_run,
        ):
            mock_run.return_value.returncode = 1
            result = pre_push_hook.main()
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
