import json
import subprocess
import textwrap
import unittest
from pathlib import Path

from ebta_engine.adapters.nautilus_mapping import run_multifold_segments
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig, SimulationResult


class NautilusPhase5RunSegmentTests(unittest.TestCase):
    def test_multifold_orchestration_returns_procedure_consumable_results_without_segment_leakage(self):
        candidate = Candidate(
            candidate_id="CAND-FAKE",
            research_family_id="FAM",
            payload={"payload": "fake"},
            asset="XAUUSD",
            complexity=1,
            fold_id="FOLD-001",
            metadata={"segment": "TRAIN"},
        )
        result = SimulationResult(
            candidate_id="CAND-FAKE",
            instrument_id="XAUUSD.SIM",
            timestamps=["2026-01-01T00:00:00Z"],
            daily_returns=[0.01],
            daily_exposure=[0.5],
            nav=[1010.0],
            total_costs=0.0,
        )

        def fake_runner(**kwargs):
            self.assertNotIn("segment", kwargs)
            return result

        outputs = run_multifold_segments(
            [
                {
                    "fold_id": "FOLD-001",
                    "candidate": candidate,
                    "bars": [],
                    "cost_model": CostModel("CM", "deterministic", "zero_fee"),
                    "instrument_config": InstrumentConfig(
                        instrument_id="XAUUSD.SIM",
                        symbol="XAUUSD",
                        venue="SIM",
                        price_precision=2,
                        size_precision=2,
                        price_increment="0.01",
                        size_increment="0.01",
                        margin_init="0",
                        margin_maint="0",
                        maker_fee="0",
                        taker_fee="0",
                    ),
                    "seed": 1,
                }
            ],
            runner=fake_runner,
        )
        self.assertEqual(outputs[0]["fold_id"], "FOLD-001")
        self.assertIs(outputs[0]["simulation_result"], result)
        detrending = result.detrending_inputs(market_returns=[0.0], cash_returns=[0.0])
        self.assertEqual(detrending["strat_net_returns"], [0.01])
        economic = result.economic_gate_evidence(
            statistical_status="PASS",
            thresholds={},
            observed_values={},
            capacity_grid=[],
            return_hurdle_pass=True,
            drawdown_pass=True,
            capacity_pass=True,
            costs_pass=True,
            execution_pass=True,
        )
        self.assertEqual(economic["simulation_result_hash"], result.result_hash)

    def test_dedicated_venv_run_segment_matches_golden_case(self):
        script = textwrap.dedent(
            """
            import json
            from datetime import datetime, timezone

            from ebta_engine.adapters.nautilus_mapping import run_segment
            from ebta_engine.data.local_ohlcv import OhlcvBar
            from ebta_engine.strategies.contracts import Candidate
            from ebta_engine.strategies.payloads import payload_by_code
            from ebta_engine.tests.fixtures.nautilus_golden_case.expected_result import (
                deterministic_cost_model,
                deterministic_instrument_config,
                expected_result,
                load_bars,
            )

            bars = [
                OhlcvBar(
                    "GOLDEN",
                    datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone(timezone.utc),
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row["volume"],
                )
                for row in load_bars()
            ]
            payload = payload_by_code("GOLDEN", "E").to_dict()
            payload["exit_criterion"]["parameters"]["horizon_bars"] = 2
            payload.pop("payload_hash", None)
            candidate = Candidate(
                candidate_id="CAND-GOLDEN",
                research_family_id="FAM-GOLDEN",
                payload=payload,
                asset="GOLDEN",
                complexity=1,
                metadata={"segment": "OOS_SHOULD_NOT_ENTER_NAUTILUS"},
            )
            actual = run_segment(
                candidate,
                bars,
                deterministic_cost_model(),
                deterministic_instrument_config(),
                seed=17,
                starting_nav=1000.0,
                trade_size="1",
                interval_value=1,
                interval_unit="DAY",
                timestamp_is_close=True,
            )
            expected = expected_result().to_dict()
            print(json.dumps({
                "actual": actual.to_dict(),
                "expected": expected,
            }, sort_keys=True))
            """
        )
        payload = self._run_venv_json(script)
        actual = payload["actual"]
        expected = payload["expected"]
        self.assertEqual(actual["instrument_id"], expected["instrument_id"])
        self.assertEqual(actual["timestamps"], expected["timestamps"])
        for field_name in ["nav", "daily_returns", "daily_exposure"]:
            self.assertEqual(len(actual[field_name]), len(expected[field_name]))
            for actual_value, expected_value in zip(actual[field_name], expected[field_name]):
                self.assertAlmostEqual(actual_value, expected_value, places=9)
        self.assertEqual(actual["total_costs"], 0.0)
        self.assertEqual(actual["positions"], [])
        self.assertTrue(actual["metadata"]["no_m1_signal"])
        self.assertNotIn("segment", actual["metadata"])

    def test_dedicated_venv_run_segment_handles_no_model_without_trades(self):
        script = textwrap.dedent(
            """
            import json
            from datetime import datetime, timezone

            from ebta_engine.adapters.nautilus_mapping import run_segment
            from ebta_engine.data.local_ohlcv import OhlcvBar
            from ebta_engine.strategies.contracts import Candidate
            from ebta_engine.strategies.payloads import payload_by_code
            from ebta_engine.tests.fixtures.nautilus_golden_case.expected_result import (
                deterministic_cost_model,
                deterministic_instrument_config,
                load_bars,
            )

            bars = [
                OhlcvBar(
                    "GOLDEN",
                    datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone(timezone.utc),
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row["volume"],
                )
                for row in load_bars()
            ]
            no_model_payload = payload_by_code("GOLDEN", "E").to_dict()
            no_model_payload["entry_criterion"]["rule_id"] = ""
            no_model_payload.pop("payload_hash", None)
            no_model = run_segment(
                Candidate(
                    candidate_id="CAND-NOMODEL",
                    research_family_id="FAM-GOLDEN",
                    payload=no_model_payload,
                    asset="GOLDEN",
                    complexity=1,
                ),
                bars,
                deterministic_cost_model(),
                deterministic_instrument_config(),
                seed=17,
                starting_nav=1000.0,
                trade_size="1",
                interval_value=1,
                interval_unit="DAY",
                timestamp_is_close=True,
            )
            print(json.dumps({
                "no_model": no_model.to_dict(),
            }, sort_keys=True))
            """
        )
        payload = self._run_venv_json(script)
        no_model = payload["no_model"]
        self.assertTrue(no_model["metadata"]["no_m1_signal"])
        self.assertEqual(no_model["nav"], [1000.0, 1000.0, 1000.0])
        self.assertEqual(no_model["daily_exposure"], [0.0, 0.0, 0.0])

    def _run_venv_json(self, script: str) -> dict:
        implementation_root = Path(__file__).resolve().parents[2]
        python_exe = implementation_root / "adapters" / "nautilus_env" / "venv" / "Scripts" / "python.exe"
        if not python_exe.exists():
            self.skipTest(f"Nautilus venv missing: {python_exe}")
        completed = subprocess.run(
            [str(python_exe), "-c", script],
            cwd=implementation_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return json.loads(completed.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    unittest.main()
