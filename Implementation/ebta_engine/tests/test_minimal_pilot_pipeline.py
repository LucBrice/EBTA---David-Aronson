import importlib.util
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PILOT_SCRIPT = ROOT / "examples" / "minimal_pilot_pipeline" / "build_research_package.py"


class MinimalPilotPipelineTests(unittest.TestCase):
    def test_g9_gate_value_only_passes_pass(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(module._g9_gate_value("PASS"), "PASS")
        for verdict in ("FAIL", "INCONCLUSIVE", "NOT_VALIDATED", "UNKNOWN"):
            with self.subTest(verdict=verdict):
                self.assertEqual(module._g9_gate_value(verdict), "INCONCLUSIVE")

    def test_minimal_pilot_pipeline_builds_valid_package(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            pilot_inputs = module.load_pilot_inputs()
            package_shape = module.load_package_shape()
            package_dir = Path(temp_dir) / "research_package"
            report = module.build_package(package_dir)
            reports_dir = package_dir / "reports"
            self.assertTrue((reports_dir / "search_space.json").exists())
            self.assertTrue((reports_dir / "candidate_matrix.json").exists())
            self.assertTrue((reports_dir / "data_availability.json").exists())
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            wrc = json.loads((reports_dir / "wrc.json").read_text(encoding="utf-8"))
            oos = json.loads((reports_dir / "oos.json").read_text(encoding="utf-8"))
            gates = json.loads((reports_dir / "gates.json").read_text(encoding="utf-8"))
            search_space = json.loads((reports_dir / "search_space.json").read_text(encoding="utf-8"))
            candidate_matrix = json.loads((reports_dir / "candidate_matrix.json").read_text(encoding="utf-8"))
            procedure_reports = {
                name: json.loads((reports_dir / name).read_text(encoding="utf-8"))
                for name in [
                    "data_availability.json",
                    "sealing.json",
                    "oos_access_decision.json",
                    "monitoring_plan.json",
                    "monitoring_consultation_log.json",
                    "incubation_report.json",
                    "incubation_gate.json",
                    "live_deployment.json",
                    "deployment_gate.json",
                    "reproduction_validation.json",
                ]
            }
            manifest = json.loads((package_dir / "manifests" / "reproducibility_manifest.json").read_text(encoding="utf-8"))
            direct_validation = module.validate_package_dir(package_dir)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(direct_validation["status"], "PASS")
        self.assertEqual(report["manifest_artifact_failures"], [])
        self.assertEqual(report["semantic_errors"], [])
        self.assertEqual(report["gate_report"]["summary"]["inconclusive"], 0)
        self.assertTrue(all(result["status"] == "PASS" for result in report["invariant_results"]))
        self.assertEqual(config["config_id"], pilot_inputs["identifiers"]["config_id"])
        self.assertEqual(config["project_id"], pilot_inputs["identifiers"]["project_id"])
        self.assertEqual(config["walk_forward_schedule"], pilot_inputs["walk_forward_schedule"])
        self.assertEqual(config["candidate_space"]["candidate_count"], len(candidate_matrix["candidate_ids"]))
        self.assertEqual(config["candidate_space"]["asset_universe"], ["EURUSD", "XAUUSD"])
        self.assertEqual(config["candidate_space"]["asset_selection_axis"], "asset")
        self.assertEqual(search_space["asset_candidate_count"], {"EURUSD": 4, "XAUUSD": 4})
        self.assertEqual(set(candidate_matrix["candidate_assets"].values()), {"EURUSD", "XAUUSD"})
        self.assertEqual(wrc["replications"], config["statistical_plan"]["wrc_bootstrap_replications"])
        self.assertEqual(oos["replications"], pilot_inputs["statistical_plan"]["oos_bootstrap_replications"])
        expected_g9_gate_value = module._g9_gate_value(oos["statistical_gate"])
        for field in ("oos_report", "concatenated_oos_series", "oos_bootstrap_report"):
            self.assertEqual(gates[field], expected_g9_gate_value)
        self.assertEqual(gates["power_report"], module._g9_gate_value(oos["power_check"]["status"]))
        expected_lot_c_gate_values = {
            "data_snapshots": procedure_reports["data_availability.json"]["status"],
            "availability_timestamps": procedure_reports["data_availability.json"]["status"],
            "anti_leakage_report": procedure_reports["data_availability.json"]["status"],
            "pre_oos_manifest": procedure_reports["sealing.json"]["status"],
            "frozen_config": procedure_reports["sealing.json"]["status"],
            "validation_ready_manifest": procedure_reports["reproduction_validation.json"]["status"],
            "reproduction_report": procedure_reports["reproduction_validation.json"]["status"],
            "incubation_approval": procedure_reports["reproduction_validation.json"]["status"],
            "incubation_report": procedure_reports["incubation_report.json"]["status"],
            "paper_trading_log": procedure_reports["monitoring_consultation_log.json"]["status"],
            "monitoring_plan": procedure_reports["monitoring_plan.json"]["status"],
            "deployment_certified_manifest": procedure_reports["deployment_gate.json"]["status"],
        }
        for field, expected_status in expected_lot_c_gate_values.items():
            with self.subTest(field=field):
                self.assertEqual(gates[field], expected_status)
        manifest_paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertEqual(manifest_paths, set(package_shape["artifact_paths"]))
        self.assertTrue(all("artifact_role" in artifact for artifact in manifest["artifacts"]))
        for procedure_report in procedure_reports.values():
            self.assertIn(procedure_report["status"], {"PASS", "AUTHORIZED"})
        self.assertEqual(procedure_reports["oos_access_decision.json"]["status"], "AUTHORIZED")

    def test_minimal_pilot_contract_requires_package_shape(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                module.build_package(Path(temp_dir) / "research_package", package_shape={"artifact_paths": []})

    def test_minimal_pilot_fails_on_preregistered_oos_replication_drift(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        pilot_inputs = deepcopy(module.load_pilot_inputs())
        pilot_inputs["statistical_plan"]["oos_bootstrap_replications"] = 4999

        with tempfile.TemporaryDirectory() as temp_dir:
            report = module.build_package(Path(temp_dir) / "research_package", pilot_inputs=pilot_inputs)

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("OOS bootstrap replications must be preregistered as 5000 under DN-022", report["semantic_errors"])

    def test_minimal_pilot_fails_when_wrc_omits_evaluated_asset(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "research_package"
            module.build_package(package_dir)
            evidence_path = package_dir / "reports" / "invariant_evidence.json"
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["wrc_matrix_candidates"] = [
                candidate_id
                for candidate_id in evidence["wrc_matrix_candidates"]
                if evidence["candidate_assets"][candidate_id] != "XAUUSD"
            ]
            module.atomic_write_json(evidence_path, evidence)
            report = module.validate_package_dir(package_dir)

        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(failure.startswith("INV-017 FAIL") for failure in report["invariant_failures"]))


if __name__ == "__main__":
    unittest.main()
