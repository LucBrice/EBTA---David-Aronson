import unittest

from ebta_engine.validators.gate_validator import GATE_REQUIREMENTS, validate_gates


class GateTests(unittest.TestCase):
    def test_gate_report_marks_missing_evidence(self):
        evidence = {
            "config_id": "CFG",
            "project_id": "PRJ",
            "research_family_id": "FAM",
            "hypothesis_id": "HYP",
            "process_version_id": "PROC",
            "template_hash": "HASH",
        }
        results = {result.gate_id: result for result in validate_gates(evidence)}
        self.assertEqual(results["G0"].status, "PASS")
        self.assertEqual(results["G1"].status, "INCONCLUSIVE")
        self.assertEqual(results["G1"].missing, ["data_snapshots", "availability_timestamps", "anti_leakage_report"])

    def test_gate_report_rejects_non_pass_wrc_verdict(self):
        evidence = _complete_evidence()
        evidence["wrc_status"] = "FAIL"

        results = {result.gate_id: result for result in validate_gates(evidence)}

        self.assertNotEqual(results["G4"].status, "PASS")
        self.assertIn("wrc_status", results["G4"].missing)

    def test_gate_report_rejects_non_pass_robustness_verdict(self):
        evidence = _complete_evidence()
        evidence["pre_oos_robustness_verdict"] = "FAIL"

        results = {result.gate_id: result for result in validate_gates(evidence)}

        self.assertNotEqual(results["G5"].status, "PASS")
        self.assertIn("pre_oos_robustness_verdict", results["G5"].missing)

    def test_gate_report_rejects_non_pass_oos_gate(self):
        for verdict in ("FAIL", "INCONCLUSIVE"):
            with self.subTest(verdict=verdict):
                evidence = _complete_evidence()
                evidence["oos_report"] = verdict

                results = {result.gate_id: result for result in validate_gates(evidence)}

                self.assertNotEqual(results["G9"].status, "PASS")
                self.assertIn("oos_report", results["G9"].missing)

    def test_gate_report_would_accept_raw_not_validated_oos_gate(self):
        evidence = _complete_evidence()
        evidence["oos_report"] = "NOT_VALIDATED"

        results = {result.gate_id: result for result in validate_gates(evidence)}

        self.assertEqual(results["G9"].status, "PASS")
        self.assertIn("oos_report", results["G9"].present)


def _complete_evidence() -> dict[str, object]:
    evidence: dict[str, object] = {name: True for requirements in GATE_REQUIREMENTS.values() for name in requirements}
    evidence["wrc_status"] = "PASS"
    evidence["pre_oos_robustness_verdict"] = "PASS"
    return evidence


if __name__ == "__main__":
    unittest.main()
