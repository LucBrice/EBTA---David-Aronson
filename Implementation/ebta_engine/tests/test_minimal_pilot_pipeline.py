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
                    "economic.json",
                    "execution.json",
                    "robustness.json",
                    "optimization_log.json",
                    "ml_manifest.json",
                    "complexity_selection.json",
                    "registry_review.json",
                ]
            }
            manifest = json.loads((package_dir / "manifests" / "reproducibility_manifest.json").read_text(encoding="utf-8"))
            direct_validation = module.validate_package_dir(package_dir)
            registered_candidates = module._registered_candidates_from_registry(package_dir)

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
        expected_g6_gate_values = {
            "execution_report": procedure_reports["execution.json"]["status"],
            "cost_model": "PASS",
            "capacity_grid": "PASS",
            "nav_reconciliation": procedure_reports["execution.json"]["nav_reconciliation"],
        }
        self.assertNotEqual(procedure_reports["economic.json"]["economic_status"], "")
        for field, expected_status in expected_g6_gate_values.items():
            with self.subTest(field=field):
                self.assertEqual(gates[field], expected_status)
        expected_lot_d_gate_values = {
            "registry_initialized": module._g2_registry_initialized_gate(
                procedure_reports["registry_review.json"],
                registered_candidates,
            ),
            "candidate_catalog": module._g2_candidate_catalog_gate(search_space),
            "local_matrix": module._g2_local_matrix_gate(candidate_matrix, procedure_reports["registry_review.json"]),
            "selection_rule": module._g3_selection_rule_gate(procedure_reports["complexity_selection.json"]),
            "train_only_calibration_log": module._g3_train_calibration_gate(
                procedure_reports["optimization_log.json"],
                procedure_reports["ml_manifest.json"],
            ),
            "wrc_report": module._g4_wrc_report_gate(wrc),
            "wrc_family_matrix": module._g4_wrc_family_matrix_gate(wrc, candidate_matrix),
            "robustness_report": module._g5_robustness_report_gate(procedure_reports["robustness.json"]),
            "robustness_matrix": module._g5_robustness_matrix_gate(procedure_reports["robustness.json"]),
            "test_reports": module._test_reports_gate(
                {
                    "candidate_matrix": candidate_matrix,
                    "wrc": wrc,
                    "robustness": procedure_reports["robustness.json"],
                    "economic": procedure_reports["economic.json"],
                }
            ),
            "economic_report": module._gate_verdict(procedure_reports["economic.json"]["economic_status"]),
            "statistical_gate_report": module._gate_verdict(procedure_reports["economic.json"]["statistical_status"]),
            "economic_gate_report": module._gate_verdict(procedure_reports["economic.json"]["global_status"]),
        }
        for field, expected_status in expected_lot_d_gate_values.items():
            with self.subTest(field=field):
                self.assertEqual(gates[field], expected_status)
                self.assertIsInstance(gates[field], str)
                self.assertNotEqual(gates[field], True)
        manifest_paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertEqual(manifest_paths, set(package_shape["artifact_paths"]))
        self.assertTrue(all("artifact_role" in artifact for artifact in manifest["artifacts"]))
        for name, procedure_report in procedure_reports.items():
            if name == "economic.json":
                continue
            if "status" not in procedure_report:
                continue
            self.assertIn(procedure_report["status"], {"PASS", "AUTHORIZED"})
        self.assertEqual(procedure_reports["oos_access_decision.json"]["status"], "AUTHORIZED")

    def test_lot_d_registry_review_detects_registry_missing_matrix_candidate(self):
        spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
        assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "research_package"
            package_dir.mkdir()
            registry_event = {
                "event_type": "REGISTER_CANDIDATE",
                "candidate_id": "CAND-A",
            }
            (package_dir / "registry.jsonl").write_text(json.dumps(registry_event) + "\n", encoding="utf-8")
            registered_candidates = module._registered_candidates_from_registry(package_dir)

        registry_review = module.review_registry_lineage(registered_candidates, ["CAND-A", "CAND-B"])

        self.assertEqual(registered_candidates, ["CAND-A"])
        self.assertEqual(registry_review["status"], "FAIL")
        self.assertEqual(registry_review["missing_influential_candidates"], ["CAND-B"])
        self.assertEqual(module._g2_registry_initialized_gate(registry_review, registered_candidates), "FAIL")

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
