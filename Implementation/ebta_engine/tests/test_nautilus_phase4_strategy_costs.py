import json
import subprocess
import textwrap
import unittest
from pathlib import Path

from ebta_engine.adapters.nautilus_mapping import SUPPORTED_FEE_MODELS, SUPPORTED_FILL_MODELS


class NautilusPhase4StrategyCostsTests(unittest.TestCase):
    def test_mapping_module_exposes_declared_cost_model_sets_without_nautilus_import(self):
        self.assertIn("deterministic", SUPPORTED_FILL_MODELS)
        self.assertIn("zero_fee", SUPPORTED_FEE_MODELS)

    def test_dedicated_venv_maps_cost_model_and_uses_single_strategy_class(self):
        implementation_root = Path(__file__).resolve().parents[2]
        python_exe = implementation_root / "adapters" / "nautilus_env" / "venv" / "Scripts" / "python.exe"
        if not python_exe.exists():
            self.skipTest(f"Nautilus venv missing: {python_exe}")
        script = textwrap.dedent(
            """
            import json
            from decimal import Decimal

            from nautilus_trader.model.currencies import USD
            from nautilus_trader.model.identifiers import InstrumentId
            from nautilus_trader.model.objects import Money

            from ebta_engine.adapters.nautilus_mapping import map_cost_model_to_venue
            from ebta_engine.adapters.nautilus_strategy_bridge import GenericPayloadStrategy, GenericPayloadStrategyConfig
            from ebta_engine.strategies.contracts import CostModel
            from ebta_engine.strategies.payloads import payload_by_code

            class FakeEngine:
                def __init__(self):
                    self.kwargs = None

                def add_venue(self, **kwargs):
                    self.kwargs = kwargs

            engine = FakeEngine()
            cost_model = CostModel(
                model_id="CM-P4",
                fill_model="deterministic",
                fee_model="zero_fee",
                commission_per_lot=0.0,
                latency_nanos=123,
                prob_fill_on_limit=1.0,
                prob_slippage=0.0,
            )
            map_cost_model_to_venue(
                engine,
                "SIM",
                cost_model,
                starting_balances=[Money(1000, USD)],
                seed=17,
            )
            config_a = GenericPayloadStrategyConfig(
                payload=payload_by_code("NASDAQ", "E").to_dict(),
                instrument_id=InstrumentId.from_str("NASDAQ.SIM"),
                bar_types=["NASDAQ.SIM-1-MINUTE-LAST-EXTERNAL", "NASDAQ.SIM-3-MINUTE-LAST-EXTERNAL"],
                trade_size=Decimal("1"),
            )
            config_b = GenericPayloadStrategyConfig(
                payload=payload_by_code("XAUUSD", "G").to_dict(),
                instrument_id=InstrumentId.from_str("XAUUSD.SIM"),
                bar_types=["XAUUSD.SIM-1-MINUTE-LAST-EXTERNAL", "XAUUSD.SIM-3-MINUTE-LAST-EXTERNAL"],
                trade_size=Decimal("1"),
            )
            strategy_a = GenericPayloadStrategy(config_a)
            strategy_b = GenericPayloadStrategy(config_b)
            print(json.dumps({
                "venue": str(engine.kwargs["venue"]),
                "oms_type": engine.kwargs["oms_type"].name,
                "account_type": engine.kwargs["account_type"].name,
                "fill_model": type(engine.kwargs["fill_model"]).__name__,
                "fee_model": type(engine.kwargs["fee_model"]).__name__,
                "latency_model": type(engine.kwargs["latency_model"]).__name__,
                "margin_model": type(engine.kwargs["margin_model"]).__name__,
                "latency_nanos": engine.kwargs["latency_model"].base_latency_nanos,
                "strategy_class_a": type(strategy_a).__name__,
                "strategy_class_b": type(strategy_b).__name__,
                "payload_a": strategy_a.payload_code,
                "payload_b": strategy_b.payload_code,
                "session_b": strategy_b.session,
                "bar_types_count": len(strategy_a.config.bar_types),
                "has_nav_snapshots": hasattr(strategy_a, "_nav_snapshots"),
            }, sort_keys=True))
            """
        )
        completed = subprocess.run(
            [str(python_exe), "-c", script],
            cwd=implementation_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        actual = json.loads(completed.stdout.strip().splitlines()[-1])
        self.assertEqual(actual["venue"], "SIM")
        self.assertEqual(actual["oms_type"], "HEDGING")
        self.assertEqual(actual["account_type"], "MARGIN")
        self.assertEqual(actual["fill_model"], "FillModel")
        self.assertEqual(actual["fee_model"], "MakerTakerFeeModel")
        self.assertEqual(actual["latency_model"], "LatencyModel")
        self.assertEqual(actual["margin_model"], "LeveragedMarginModel")
        self.assertEqual(actual["latency_nanos"], 123)
        self.assertEqual(actual["strategy_class_a"], "GenericPayloadStrategy")
        self.assertEqual(actual["strategy_class_b"], "GenericPayloadStrategy")
        self.assertNotEqual(actual["payload_a"], actual["payload_b"])
        self.assertEqual(actual["session_b"], "asia")
        self.assertEqual(actual["bar_types_count"], 2)
        self.assertTrue(actual["has_nav_snapshots"])


if __name__ == "__main__":
    unittest.main()
