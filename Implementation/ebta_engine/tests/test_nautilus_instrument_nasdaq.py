import json
import subprocess
import textwrap
import unittest
from pathlib import Path

from ebta_engine.adapters.nautilus_mapping import bar_type_string


class NautilusInstrumentNasdaqTests(unittest.TestCase):
    def test_module_imports_without_nautilus_installed_in_system_python(self):
        self.assertEqual(
            bar_type_string("NASDAQ.SIM", interval_value=1),
            "NASDAQ.SIM-1-MINUTE-LAST-EXTERNAL",
        )

    def test_dedicated_venv_builds_nasdaq_xauusd_instruments_and_bars(self):
        implementation_root = Path(__file__).resolve().parents[2]
        python_exe = implementation_root / "adapters" / "nautilus_env" / "venv" / "Scripts" / "python.exe"
        if not python_exe.exists():
            self.skipTest(f"Nautilus venv missing: {python_exe}")
        script = textwrap.dedent(
            """
            import json
            from datetime import datetime, timezone

            from ebta_engine.adapters.nautilus_mapping import build_instrument, map_ohlcv_to_bars
            from ebta_engine.data.local_ohlcv import OhlcvBar
            from ebta_engine.strategies.contracts import InstrumentConfig

            nasdaq = InstrumentConfig(
                instrument_id="NASDAQ.SIM",
                symbol="NASDAQ",
                venue="SIM",
                price_precision=2,
                size_precision=0,
                price_increment="0.01",
                size_increment="1",
                margin_init="0",
                margin_maint="0",
                maker_fee="0",
                taker_fee="0",
                asset_class="CFD",
                metadata={"underlying_asset_class": "INDEX"},
            )
            xauusd = InstrumentConfig(
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
                base_currency="XAU",
                quote_currency="USD",
                asset_class="CFD",
                metadata={"underlying_asset_class": "COMMODITY"},
            )
            nasdaq_instrument = build_instrument(nasdaq)
            xauusd_instrument = build_instrument(xauusd)
            bars = [
                OhlcvBar("NASDAQ", datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc), 100.0, 101.0, 99.0, 100.5, 10.0),
                OhlcvBar("NASDAQ", datetime(2020, 1, 1, 0, 1, tzinfo=timezone.utc), 100.5, 102.0, 100.0, 101.5, 11.0),
            ]
            mapped = map_ohlcv_to_bars(bars, nasdaq_instrument, interval_value=1, interval_unit="MINUTE")
            print(json.dumps({
                "nasdaq_type": type(nasdaq_instrument).__name__,
                "nasdaq_id": str(nasdaq_instrument.id),
                "nasdaq_price_increment": str(nasdaq_instrument.price_increment),
                "nasdaq_size_increment": str(nasdaq_instrument.size_increment),
                "xauusd_type": type(xauusd_instrument).__name__,
                "xauusd_id": str(xauusd_instrument.id),
                "xauusd_price_increment": str(xauusd_instrument.price_increment),
                "xauusd_size_increment": str(xauusd_instrument.size_increment),
                "bar_count": len(mapped),
                "bar_type": str(mapped[0].bar_type),
                "first_ts_event": mapped[0].ts_event,
                "first_ts_init": mapped[0].ts_init,
                "first_open": str(mapped[0].open),
                "first_close": str(mapped[0].close),
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
        self.assertEqual(actual["nasdaq_type"], "Cfd")
        self.assertEqual(actual["nasdaq_id"], "NASDAQ.SIM")
        self.assertEqual(actual["nasdaq_price_increment"], "0.01")
        self.assertEqual(actual["nasdaq_size_increment"], "1")
        self.assertEqual(actual["xauusd_type"], "Cfd")
        self.assertEqual(actual["xauusd_id"], "XAUUSD.SIM")
        self.assertEqual(actual["xauusd_price_increment"], "0.01")
        self.assertEqual(actual["xauusd_size_increment"], "0.01")
        self.assertEqual(actual["bar_count"], 2)
        self.assertEqual(actual["bar_type"], "NASDAQ.SIM-1-MINUTE-LAST-EXTERNAL")
        self.assertEqual(actual["first_ts_init"] - actual["first_ts_event"], 60_000_000_000)
        self.assertEqual(actual["first_open"], "100.00")
        self.assertEqual(actual["first_close"], "100.50")


if __name__ == "__main__":
    unittest.main()
