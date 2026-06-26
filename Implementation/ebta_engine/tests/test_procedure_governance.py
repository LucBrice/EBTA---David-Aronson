import unittest

from ebta_engine.procedures.data_availability import validate_availability
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.procedures.lifecycle import deployment_gate, incubation_gate
from ebta_engine.procedures.oos_access import authorize_oos_access
from ebta_engine.procedures.registry_lineage import review_registry_lineage
from ebta_engine.procedures.robustness import robustness_verdict
from ebta_engine.procedures.sealing import validate_pre_oos_seal
from ebta_engine.procedures.walk_forward import validate_walk_forward_schedule


class GovernanceProcedureTests(unittest.TestCase):
    def test_data_availability_blocks_future_data(self):
        report = validate_availability(
            [{"available_at": "2026-01-02T00:00:00Z", "decision_at": "2026-01-01T00:00:00Z"}]
        )
        self.assertEqual(report["status"], "FAIL")

    def test_walk_forward_rejects_overlapping_oos(self):
        report = validate_walk_forward_schedule(
            [
                {"fold_id": "F1", "train": ["2020-01-01", "2020-12-31"], "test": ["2021-01-01", "2021-06-30"], "oos": ["2021-07-01", "2021-12-31"]},
                {"fold_id": "F2", "train": ["2020-07-01", "2021-06-30"], "test": ["2021-07-01", "2021-12-31"], "oos": ["2021-12-01", "2022-06-30"]},
            ]
        )
        self.assertEqual(report["status"], "FAIL")

    def test_registry_lineage_detects_missing_influential_candidate(self):
        report = review_registry_lineage(["CAND-A"], ["CAND-A", "CAND-B"])
        self.assertEqual(report["missing_influential_candidates"], ["CAND-B"])

    def test_robustness_rejects_oos_consumption(self):
        report = robustness_verdict([{"stress_id": "S1", "uses_observed_oos": True, "blocking": True, "scenario_verdict": "PASS"}])
        self.assertEqual(report["status"], "FAIL")

    def test_oos_access_requires_pre_oos_seal(self):
        denied = authorize_oos_access({"pre_oos_sealed": False})
        self.assertEqual(denied["status"], "DENIED")
        seal = validate_pre_oos_seal("PRE_OOS_SEALED", manifest_hash="HASH", independent_approval=True)
        self.assertEqual(seal["status"], "PASS")

    def test_economic_gate_remains_separate_from_statistical_gate(self):
        report = economic_gate_report(
            {
                "statistical_status": "PASS",
                "return_hurdle_pass": True,
                "drawdown_pass": True,
                "capacity_pass": False,
                "costs_pass": True,
                "execution_pass": True,
            }
        )
        self.assertEqual(report["economic_status"], "REJECTED_ECONOMIC")
        self.assertEqual(report["global_status"], "REJECTED_ECONOMIC")

    def test_lifecycle_requires_validation_ready_before_incubation(self):
        incubation = incubation_gate(
            {
                "statistical_status": "PASS",
                "economic_status": "PASS",
                "robustness_status": "PASS",
                "execution_status": "PASS",
                "package_stage": "PRE_OOS_SEALED",
                "reproduction_status": "PASS",
            }
        )
        self.assertEqual(incubation["status"], "FAIL")
        deployment = deployment_gate(
            {
                "paper_trading_status": "PASS",
                "package_stage": "DEPLOYMENT_CERTIFIED",
                "kill_switch_tested": True,
                "live_approval": True,
            }
        )
        self.assertEqual(deployment["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
