import json
import subprocess
import unittest
from pathlib import Path

from ebta_engine.tests.fixtures.nautilus_golden_case.expected_result import (
    deterministic_cost_model,
    deterministic_instrument_config,
    expected_result,
    load_bars,
)


class NautilusPhase2GoldenCaseTests(unittest.TestCase):
    def test_expected_result_is_stdlib_deterministic_and_pinned(self):
        bars = load_bars()
        result = expected_result()
        self.assertEqual(len(bars), 3)
        self.assertEqual(result.instrument_id, "GOLDEN.SIM")
        self.assertEqual(result.nav, [1000.0, 1001.0, 1002.0])
        self.assertEqual(result.total_costs, 0.0)
        self.assertAlmostEqual(result.daily_returns[0], 0.0, places=12)
        self.assertAlmostEqual(result.daily_returns[1], 1.0 / 1000.0, places=12)
        self.assertAlmostEqual(result.daily_returns[2], 1.0 / 1001.0, places=12)
        self.assertEqual(result.positions[0]["realized_pnl"], 2.0)

    def test_golden_case_execution_contract_is_degenerate_and_manual(self):
        cost_model = deterministic_cost_model()
        instrument = deterministic_instrument_config()
        self.assertEqual(cost_model.prob_fill_on_limit, 1.0)
        self.assertEqual(cost_model.prob_slippage, 0.0)
        self.assertEqual(cost_model.latency_nanos, 0)
        self.assertEqual(cost_model.commission_per_lot, 0.0)
        self.assertEqual(instrument.price_increment, "0.01")
        self.assertEqual(instrument.size_increment, "1")

    def test_dedicated_venv_runs_nautilus_golden_case_against_expected_result(self):
        implementation_root = Path(__file__).resolve().parents[2]
        python_exe = implementation_root / "adapters" / "nautilus_env" / "venv" / "Scripts" / "python.exe"
        runner = implementation_root / "adapters" / "nautilus_env" / "run_golden_case.py"
        if not python_exe.exists():
            self.skipTest(f"Nautilus venv missing: {python_exe}")
        completed = subprocess.run(
            [str(python_exe), str(runner)],
            cwd=implementation_root.parent,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        actual = json.loads(completed.stdout.strip().splitlines()[-1])
        expected = expected_result().to_dict()
        self.assertEqual(actual["instrument_id"], expected["instrument_id"])
        self.assertEqual(actual["timestamps"], expected["timestamps"])
        for field_name in ["nav", "daily_returns", "daily_exposure"]:
            self.assertEqual(len(actual[field_name]), len(expected[field_name]))
            for actual_value, expected_value in zip(actual[field_name], expected[field_name]):
                self.assertAlmostEqual(actual_value, expected_value, places=9)
        self.assertEqual(actual["total_costs"], expected["total_costs"])
        self.assertEqual(actual["positions"][0]["realized_pnl"], expected["positions"][0]["realized_pnl"])
        self.assertEqual(actual["metadata"]["total_orders"], 2)
        self.assertEqual(actual["metadata"]["total_positions"], 1)


if __name__ == "__main__":
    unittest.main()
