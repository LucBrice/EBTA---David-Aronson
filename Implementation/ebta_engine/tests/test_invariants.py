import unittest
import json
from pathlib import Path

from ebta_engine.validators.invariant_validator import validate_invariants


ROOT = Path(__file__).resolve().parents[1]


class InvariantTests(unittest.TestCase):
    def test_minimal_package_passes_executable_invariants(self):
        package = json.loads(
            (ROOT / "fixtures" / "valid_minimal" / "reports" / "invariant_evidence.json").read_text(encoding="utf-8")
        )
        results = {result.invariant_id: result for result in validate_invariants(package)}
        for invariant_id in [f"INV-{index:03d}" for index in range(1, 17)]:
            self.assertEqual(results[invariant_id].status, "PASS")

    def test_overlap_fails_inv_001(self):
        results = validate_invariants(
            {
                "oos_segments": [
                    {"id": "A", "start": "2023-01-01", "end": "2023-06-30"},
                    {"id": "B", "start": "2023-06-01", "end": "2023-12-31"},
                ]
            }
        )
        self.assertEqual({r.invariant_id: r.status for r in results}["INV-001"], "FAIL")

    def test_wrc_non_pass_fails_inv_003(self):
        results = validate_invariants({"oos_openings": [{"wrc_local_status": "FAIL"}]})
        self.assertEqual({r.invariant_id: r.status for r in results}["INV-003"], "FAIL")

    def test_each_invalid_invariant_fixture_fails_its_target(self):
        cases = json.loads(
            (ROOT / "fixtures" / "invalid_invariants" / "all_invalid_cases.json").read_text(encoding="utf-8")
        )
        for invariant_id, package in cases.items():
            with self.subTest(invariant_id=invariant_id):
                results = {result.invariant_id: result.status for result in validate_invariants(package)}
                self.assertEqual(results[invariant_id], "FAIL")


if __name__ == "__main__":
    unittest.main()
