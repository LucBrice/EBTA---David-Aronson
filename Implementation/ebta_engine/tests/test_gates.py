import unittest

from ebta_engine.validators.gate_validator import validate_gates


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


if __name__ == "__main__":
    unittest.main()
