import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PILOT_SCRIPT = ROOT / "examples" / "minimal_pilot_pipeline" / "build_research_package.py"


class MinimalPilotPipelineTests(unittest.TestCase):
    def test_minimal_pilot_pipeline_builds_valid_package(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "research_package"
            report = module.build_package(package_dir)
            reports_dir = package_dir / "reports"
            self.assertTrue((reports_dir / "search_space.json").exists())
            self.assertTrue((reports_dir / "candidate_matrix.json").exists())
            self.assertTrue((reports_dir / "data_availability.json").exists())
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            wrc = json.loads((reports_dir / "wrc.json").read_text(encoding="utf-8"))
            oos = json.loads((reports_dir / "oos.json").read_text(encoding="utf-8"))
            candidate_matrix = json.loads((reports_dir / "candidate_matrix.json").read_text(encoding="utf-8"))
            manifest = json.loads((package_dir / "manifests" / "reproducibility_manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["manifest_artifact_failures"], [])
        self.assertEqual(report["semantic_errors"], [])
        self.assertEqual(report["gate_report"]["summary"]["inconclusive"], 0)
        self.assertTrue(all(result["status"] == "PASS" for result in report["invariant_results"]))
        self.assertEqual(config["candidate_space"]["candidate_count"], len(candidate_matrix["candidate_ids"]))
        self.assertEqual(wrc["replications"], config["statistical_plan"]["wrc_bootstrap_replications"])
        self.assertEqual(oos["replications"], 5000)
        self.assertTrue(all("artifact_role" in artifact for artifact in manifest["artifacts"]))


if __name__ == "__main__":
    unittest.main()
