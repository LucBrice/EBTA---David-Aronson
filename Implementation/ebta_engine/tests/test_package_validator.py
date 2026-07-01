import json
import tempfile
import unittest
from pathlib import Path
from shutil import copytree

from ebta_engine.manifests.manifest_builder import build_manifest
from ebta_engine.persistence import atomic_write_json
from ebta_engine.validators.package_validator import REQUIRED_PACKAGE_PATHS, validate_package_dir


ROOT = Path(__file__).resolve().parents[1]


class PackageValidatorTests(unittest.TestCase):
    def test_valid_minimal_package_validates_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            manifest = build_manifest(
                package_dir,
                sorted(path for path in REQUIRED_PACKAGE_PATHS if path != "manifests/reproducibility_manifest.json"),
                "VALIDATION_READY",
            )
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)
            report = validate_package_dir(package_dir)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["gate_report"]["summary"]["inconclusive"], 0)
            self.assertTrue(all(result["status"] == "PASS" for result in report["invariant_results"]))

    def test_manifest_mismatch_fails_package(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            manifest = build_manifest(package_dir, ["config.json"], "PRE_OOS_SEALED")
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            config["config_id"] = "MUTATED"
            atomic_write_json(package_dir / "config.json", config)
            report = validate_package_dir(package_dir)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("hash mismatch: config.json", report["manifest_failures"])

    def test_gate_or_invariant_failure_fails_package_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))
            gates.pop("wrc_report")
            atomic_write_json(package_dir / "reports" / "gates.json", gates)
            manifest = build_manifest(
                package_dir,
                sorted(path for path in REQUIRED_PACKAGE_PATHS if path != "manifests/reproducibility_manifest.json"),
                "VALIDATION_READY",
            )
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)
            report = validate_package_dir(package_dir)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(report["gate_failures"])

    def test_missing_required_procedure_artifact_fails_package_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            (package_dir / "reports" / "search_space.json").unlink()
            manifest = build_manifest(
                package_dir,
                sorted(
                    path
                    for path in REQUIRED_PACKAGE_PATHS
                    if path not in {"manifests/reproducibility_manifest.json", "reports/search_space.json"}
                ),
                "VALIDATION_READY",
            )
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)
            report = validate_package_dir(package_dir)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("reports/search_space.json", report["missing_paths"])

    def test_present_g_bias_report_must_pass_when_available(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            manifest = build_manifest(
                package_dir,
                sorted(path for path in REQUIRED_PACKAGE_PATHS if path != "manifests/reproducibility_manifest.json"),
                "VALIDATION_READY",
            )
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)
            atomic_write_json(package_dir / "reports" / "g_bias.json", {"artifact_type": "g_bias_report", "status": "FAIL"})

            report = validate_package_dir(package_dir)

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["bias_gate_failures"], ["G-BIAS FAIL"])

    def test_enforced_g_bias_report_missing_fails_package(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            manifest = build_manifest(
                package_dir,
                sorted(path for path in REQUIRED_PACKAGE_PATHS if path != "manifests/reproducibility_manifest.json"),
                "VALIDATION_READY",
            )
            atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)

            report = validate_package_dir(package_dir, enforce_bias_governance=True)

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["bias_gate_failures"], ["missing optional enforced artifact: reports/g_bias.json"])


if __name__ == "__main__":
    unittest.main()
