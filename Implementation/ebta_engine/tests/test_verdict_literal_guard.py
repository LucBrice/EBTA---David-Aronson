import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ebta_engine.validators.verdict_literal_guard import audit_allowlist, load_allowlist, scan_repository, scan_source


ROOT = Path(__file__).resolve().parents[3]
ALLOWLIST_PATH = Path(__file__).resolve().parent / "verdict_literal_allowlist.json"


def _allowlist_for(candidates, *, category="derived_calculation"):
    return {
        "schema_version": "1.0.0",
        "expected_count": len(candidates),
        "entries": [
            {
                "fingerprint": candidate.fingerprint,
                "category": category,
                "justification": "controlled unit-test case",
                "decision_source": "PLAN_GARDE_LITTERAUX_VERDICT",
            }
            for candidate in candidates
        ],
    }


class VerdictLiteralGuardTests(unittest.TestCase):
    def test_repository_inventory_matches_annotated_allowlist(self):
        candidates = scan_repository(ROOT)
        report = audit_allowlist(candidates, load_allowlist(ALLOWLIST_PATH))

        self.assertEqual(len(candidates), 32)
        self.assertEqual(report["status"], "PASS", report)

    def test_unapproved_positive_literal_in_persisted_gate_sink_fails(self):
        candidates = scan_source(
            'atomic_write_json(path, {"economic_report": "PASS"})\n',
            relative_path="Implementation/examples/hostile.py",
        )
        report = audit_allowlist(
            candidates,
            {"schema_version": "1.0.0", "expected_count": 0, "entries": []},
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["unapproved"][0]["sink"], "dict:economic_report")
        self.assertTrue(report["count_mismatch"])

    def test_derived_calculation_and_expected_contract_can_be_reviewed(self):
        scenarios = (
            ('status = "PASS" if not failures else "FAIL"\n', "derived_calculation"),
            ('required = {"statistical_status": "PASS"}\n', "expected_contract"),
        )
        for source, category in scenarios:
            with self.subTest(category=category):
                candidates = scan_source(source, relative_path="Implementation/ebta_engine/example.py")
                report = audit_allowlist(candidates, _allowlist_for(candidates, category=category))
                self.assertEqual(report["status"], "PASS", report)

    def test_technical_attestation_outside_exact_sink_registry_is_ignored(self):
        candidates = scan_source(
            'payload = {"package_validator_status_is_not_rewritten": True}\n',
            relative_path="Implementation/ebta_engine/benchmark.py",
        )
        self.assertEqual(candidates, [])

    def test_stale_entry_and_invalid_annotation_fail(self):
        candidates = scan_source('status = "PASS"\n', relative_path="Implementation/ebta_engine/example.py")
        allowlist = _allowlist_for(candidates)
        allowlist["entries"][0]["fingerprint"] = "stale-fingerprint"
        allowlist["entries"][0]["category"] = "comfort_exception"

        report = audit_allowlist(candidates, allowlist)

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["stale"], ["stale-fingerprint"])
        self.assertEqual(len(report["unapproved"]), 1)
        self.assertTrue(any("category is invalid" in error for error in report["format_errors"]))

    def test_fingerprint_is_line_independent_but_diagnostic_line_is_current(self):
        first = scan_source('status = "PASS"\n', relative_path="Implementation/ebta_engine/example.py")
        moved = scan_source('\n\nstatus = "PASS"\n', relative_path="Implementation/ebta_engine/example.py")

        self.assertEqual(first[0].fingerprint, moved[0].fingerprint)
        self.assertEqual(first[0].line, 1)
        self.assertEqual(moved[0].line, 3)

    def test_syntax_error_is_not_silently_ignored(self):
        with self.assertRaises(SyntaxError):
            scan_source('status = "PASS" if\n', relative_path="Implementation/ebta_engine/broken.py")

    def test_repository_scan_does_not_follow_external_symlink(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            source_root = repo_root / "Implementation" / "ebta_engine"
            source_root.mkdir(parents=True)
            link = source_root / "linked.py"
            link.write_text('status = "PASS"\n', encoding="utf-8")

            original_is_symlink = Path.is_symlink

            def simulated_is_symlink(path):
                return path == link or original_is_symlink(path)

            with patch.object(Path, "is_symlink", simulated_is_symlink):
                self.assertEqual(scan_repository(repo_root), [])


if __name__ == "__main__":
    unittest.main()
