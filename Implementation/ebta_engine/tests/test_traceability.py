import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TraceabilityTests(unittest.TestCase):
    def test_runtime_artifacts_are_referenced(self):
        matrix = (ROOT / "TRACEABILITY_MATRIX.md").read_text(encoding="utf-8")
        required = [
            "schemas/config.schema.json",
            "schemas/experiment_registry_event.schema.json",
            "schemas/oos_access_event.schema.json",
            "schemas/reproducibility_manifest.schema.json",
            "validators/invariant_validator.py",
            "adapters/backtrader_mapping.py",
        ]
        for artifact in required:
            self.assertIn(artifact, matrix)


if __name__ == "__main__":
    unittest.main()
