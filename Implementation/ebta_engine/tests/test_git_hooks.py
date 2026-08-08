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
from unittest.mock import MagicMock, patch

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
            mock_run.return_value.stdout = "0"
            result = pre_push_hook.main()
        self.assertEqual(result, 0)
        # main() now also fetches and checks staleness before running the
        # suite (Council of Five decision); the test command must still be
        # among the calls, not necessarily the only one.
        mock_run.assert_any_call(pre_push_hook.TEST_COMMAND)

    def test_failing_suite_blocks_the_push(self):
        with (
            patch("sys.stdin", io.StringIO("")),
            patch.object(pre_push_hook.subprocess, "run") as mock_run,
        ):
            mock_run.return_value.returncode = 1
            result = pre_push_hook.main()
        self.assertEqual(result, 1)


class PrePushReadRefsTests(unittest.TestCase):
    def test_well_formed_lines_are_parsed(self):
        stdin = "refs/heads/main abc123 refs/heads/main def456\n"
        with patch("sys.stdin", io.StringIO(stdin)):
            refs = pre_push_hook.read_pushed_refs()
        self.assertEqual(refs, [("refs/heads/main", "abc123", "refs/heads/main", "def456")])

    def test_malformed_line_is_skipped_not_crashed_on(self):
        stdin = "not enough fields\n"
        with patch("sys.stdin", io.StringIO(stdin)):
            refs = pre_push_hook.read_pushed_refs()
        self.assertEqual(refs, [])


class PrePushNonFastForwardTests(unittest.TestCase):
    """Council of Five decision: block only a genuinely non-fast-forward ref
    update (force push or unfetched divergence); a plain fast-forward push
    or a brand-new branch must never be blocked by this check.
    """

    def _run_with_is_ancestor(self, refs, is_ancestor_result):
        with patch.object(pre_push_hook, "_is_ancestor", return_value=is_ancestor_result) as mock_is_ancestor:
            blocked = pre_push_hook.check_non_fastforward(refs)
        return blocked, mock_is_ancestor

    def test_fast_forward_update_is_not_blocked(self):
        refs = [("refs/heads/main", "local_sha", "refs/heads/main", "remote_sha")]
        blocked, mock_is_ancestor = self._run_with_is_ancestor(refs, is_ancestor_result=True)
        self.assertFalse(blocked)
        mock_is_ancestor.assert_called_once_with("remote_sha", "local_sha")

    def test_non_fast_forward_update_is_blocked(self):
        refs = [("refs/heads/main", "local_sha", "refs/heads/main", "remote_sha")]
        blocked, _ = self._run_with_is_ancestor(refs, is_ancestor_result=False)
        self.assertTrue(blocked)

    def test_new_branch_push_skips_the_check_entirely(self):
        refs = [("refs/heads/feature", "local_sha", "refs/heads/feature", pre_push_hook.ZERO_SHA)]
        with patch.object(pre_push_hook, "_is_ancestor") as mock_is_ancestor:
            blocked = pre_push_hook.check_non_fastforward(refs)
        self.assertFalse(blocked)
        mock_is_ancestor.assert_not_called()

    def test_branch_deletion_skips_the_check_entirely(self):
        refs = [("refs/heads/feature", pre_push_hook.ZERO_SHA, "refs/heads/feature", "remote_sha")]
        with patch.object(pre_push_hook, "_is_ancestor") as mock_is_ancestor:
            blocked = pre_push_hook.check_non_fastforward(refs)
        self.assertFalse(blocked)
        mock_is_ancestor.assert_not_called()


class PrePushStalenessWarningTests(unittest.TestCase):
    """Council of Five decision: staleness relative to origin/main is
    informational only and must never block the push - only a genuine
    non-fast-forward ref update (covered above) does.

    Adversarial-tester finding (retroactive fix workstream, 2026-08-08): a
    failed 'git fetch' or 'git rev-list' must never be silently treated as
    "up to date" - that would turn a verification failure into false
    reassurance (SILENT_FALLBACK). Each of the three possible outcomes
    (up-to-date / behind / could-not-verify) is tested separately below so
    they cannot be confused with one another.
    """

    @staticmethod
    def _completed(returncode, stdout=""):
        result = MagicMock()
        result.returncode = returncode
        result.stdout = stdout
        return result

    def test_behind_origin_main_prints_a_warning_but_returns_nothing_blocking(self):
        with patch.object(pre_push_hook.subprocess, "run") as mock_run:
            mock_run.side_effect = [
                self._completed(0),  # git fetch: succeeds
                self._completed(0, "3"),  # git rev-list: 3 commits behind
            ]
            with patch("builtins.print") as mock_print:
                pre_push_hook.warn_if_behind_origin_main()
        printed = "\n".join(str(call.args[0]) for call in mock_print.call_args_list if call.args)
        self.assertIn("AVERTISSEMENT", printed)
        self.assertIn("3 commit(s)", printed)

    def test_up_to_date_prints_nothing(self):
        with patch.object(pre_push_hook.subprocess, "run") as mock_run:
            mock_run.side_effect = [
                self._completed(0),  # git fetch: succeeds
                self._completed(0, "0"),  # git rev-list: up to date
            ]
            with patch("builtins.print") as mock_print:
                pre_push_hook.warn_if_behind_origin_main()
        mock_print.assert_not_called()

    def test_failed_fetch_is_reported_explicitly_not_treated_as_up_to_date(self):
        with patch.object(pre_push_hook.subprocess, "run") as mock_run:
            mock_run.side_effect = [self._completed(1)]  # git fetch: fails
            with patch("builtins.print") as mock_print:
                pre_push_hook.warn_if_behind_origin_main()
        printed = "\n".join(str(call.args[0]) for call in mock_print.call_args_list if call.args)
        self.assertIn("AVERTISSEMENT", printed)
        self.assertIn("fetch origin", printed)
        # Only the fetch was attempted - rev-list must not run on a failed fetch.
        self.assertEqual(mock_run.call_count, 1)

    def test_failed_rev_list_is_reported_explicitly_not_treated_as_up_to_date(self):
        with patch.object(pre_push_hook.subprocess, "run") as mock_run:
            mock_run.side_effect = [
                self._completed(0),  # git fetch: succeeds
                self._completed(1),  # git rev-list: fails (e.g. unknown ref)
            ]
            with patch("builtins.print") as mock_print:
                pre_push_hook.warn_if_behind_origin_main()
        printed = "\n".join(str(call.args[0]) for call in mock_print.call_args_list if call.args)
        self.assertIn("AVERTISSEMENT", printed)
        self.assertIn("impossible de comparer", printed)


if __name__ == "__main__":
    unittest.main()
