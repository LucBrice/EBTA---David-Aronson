import importlib.util
import unittest
from pathlib import Path

from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.strategies.contracts import SimulationResult


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_PATH = IMPLEMENTATION_ROOT / "examples" / "controlled_experiments" / "gate_discrimination_experiment.py"


def _load_experiment_module():
    spec = importlib.util.spec_from_file_location("gate_discrimination_experiment", EXPERIMENT_PATH)
    assert spec is not None and spec.loader is not None, f"cannot load spec for {EXPERIMENT_PATH}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GateDiscriminationEconomicFlagTests(unittest.TestCase):
    def setUp(self):
        self.experiment = _load_experiment_module()
        self.thresholds = {
            "minimum_mean_return": 0.001,
            "maximum_total_costs": 0.0,
            "maximum_drawdown": 0.02,
        }

    def test_compute_economic_pass_flags_accepts_known_winner(self):
        result = _simulation_result([0.002, 0.002, 0.002], [1000.0, 1002.0, 1004.0])
        flags = self.experiment.compute_economic_pass_flags(result, thresholds=self.thresholds)
        self.assertEqual(
            flags,
            {
                "return_hurdle_pass": True,
                "drawdown_pass": True,
                "capacity_pass": True,
                "costs_pass": True,
                "execution_pass": True,
            },
        )

    def test_compute_economic_pass_flags_rejects_known_loser(self):
        result = _simulation_result([-0.002, -0.002, -0.002], [1000.0, 998.0, 996.0])
        flags = self.experiment.compute_economic_pass_flags(result, thresholds=self.thresholds)
        self.assertFalse(flags["return_hurdle_pass"])
        self.assertTrue(flags["drawdown_pass"])

    def test_compute_economic_pass_flags_rejects_missing_thresholds(self):
        result = _simulation_result([0.002], [1000.0])
        with self.assertRaises(ValueError):
            self.experiment.compute_economic_pass_flags(result, thresholds={"minimum_mean_return": 0.001})

    def test_gate_discrimination_fixture_files_are_directional(self):
        fixture_root = Path(__file__).resolve().parent / "fixtures" / "gate_discrimination"
        rising = (fixture_root / "NASDAQ 1m" / "NASDAQ-gate-discrimination-rising.csv").read_text(encoding="utf-8")
        falling = (fixture_root / "XAUUSD 1m" / "XAUUSD-gate-discrimination-falling.csv").read_text(encoding="utf-8")
        self.assertIn("109.9399", rising)
        self.assertIn("90.9156", falling)
        self.assertEqual(len(rising.strip().splitlines()), 21)
        self.assertEqual(len(falling.strip().splitlines()), 21)

    def test_deterministic_fake_runner_discriminates_winner_and_loser(self):
        report = self.experiment.run_controlled_gate_experiment(segment_runner=_fake_segment_runner)
        by_id = {item["candidate_id"]: item for item in report["candidate_reports"]}
        winner = by_id["CONTROLLED-WINNER-NASDAQ"]
        loser = by_id["CONTROLLED-LOSER-XAUUSD"]
        self.assertEqual(report["status"], "PASS")
        self.assertGreater(winner["oos_mean_return"], 0.0)
        self.assertLess(loser["oos_mean_return"], 0.0)
        self.assertEqual(winner["economic_status"], "PASS")
        self.assertEqual(winner["robustness_status"], "PASS")
        self.assertEqual(loser["economic_status"], "REJECTED_ECONOMIC")
        self.assertEqual(loser["robustness_status"], "FAIL")

    def test_hardcoded_true_flags_would_let_same_loser_pass(self):
        loser = _simulation_result([-0.002, -0.002, -0.002], [1000.0, 998.0, 996.0])
        observed = self.experiment.economic_observed_values(loser)
        flags = self.experiment.compute_economic_pass_flags(loser, thresholds=self.thresholds)
        honest = economic_gate_report(
            loser.economic_gate_evidence(
                statistical_status="PASS",
                thresholds=self.thresholds,
                observed_values=observed,
                capacity_grid=[{"capital": 1000.0}],
                **flags,
            )
        )
        hardcoded_true = economic_gate_report(
            loser.economic_gate_evidence(
                statistical_status="PASS",
                thresholds=self.thresholds,
                observed_values=observed,
                capacity_grid=[{"capital": 1000.0}],
                return_hurdle_pass=True,
                drawdown_pass=True,
                capacity_pass=True,
                costs_pass=True,
                execution_pass=True,
            )
        )
        self.assertEqual(honest["global_status"], "REJECTED_ECONOMIC")
        self.assertEqual(hardcoded_true["global_status"], "PASS")


def _simulation_result(returns, nav, *, costs=0.0):
    return SimulationResult(
        candidate_id="CANDIDATE",
        instrument_id="TEST.SIM",
        timestamps=[f"2020-01-{index + 1:02d}T00:00:00Z" for index in range(len(returns))],
        daily_returns=list(returns),
        daily_exposure=[0.1 for _ in returns],
        nav=list(nav),
        total_costs=costs,
    )


def _fake_segment_runner(**kwargs):
    bars = kwargs["bars"]
    sign = 1.0 if kwargs["candidate"].asset == "NASDAQ" else -1.0
    returns = [sign * 0.002 for _ in bars]
    nav = []
    current_nav = kwargs.get("starting_nav", 1000.0)
    for value in returns:
        current_nav *= 1.0 + value
        nav.append(current_nav)
    return SimulationResult(
        candidate_id=kwargs["candidate"].candidate_id,
        instrument_id=kwargs["instrument_config"].instrument_id,
        timestamps=[bar.timestamp.isoformat().replace("+00:00", "Z") for bar in bars],
        daily_returns=returns,
        daily_exposure=[0.1 for _ in bars],
        nav=nav,
        total_costs=0.0,
        metadata={"source": "fake_controlled_gate_runner"},
    )


if __name__ == "__main__":
    unittest.main()
