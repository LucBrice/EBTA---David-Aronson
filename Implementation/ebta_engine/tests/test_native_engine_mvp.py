import csv
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ebta_engine.backtest.native_engine import run_native_backtest
from ebta_engine.data.local_ohlcv import load_ohlcv_bars
from ebta_engine.package_builder.native_research_package import build_native_inputs, build_native_research_package
from ebta_engine.schema_validation import validate
from ebta_engine.strategies.payloads import PAYLOAD_CODES, build_payload_grid, payload_by_code
from ebta_engine.validators.artifact_validators import load_schema


class NativeEngineMvpTests(unittest.TestCase):
    def test_payload_grid_covers_assets_x_e_to_i(self):
        payloads = build_payload_grid(["NASDAQ", "XAUUSD"])
        pairs = {(payload.asset, payload.payload_code) for payload in payloads}
        self.assertEqual(len(payloads), 10)
        self.assertEqual(pairs, {(asset, code) for asset in ["NASDAQ", "XAUUSD"] for code in PAYLOAD_CODES})
        self.assertEqual(payload_by_code("NASDAQ", "G").session, "asia")
        self.assertEqual(payload_by_code("XAUUSD", "F").bias_filter, "directional_mtf_bias")

    def test_strategy_payload_schema_accepts_native_payload(self):
        schema = load_schema("strategy_payload.schema.json")
        errors = validate(payload_by_code("NASDAQ", "I").to_dict(), schema)
        self.assertEqual(errors, [])

    def test_local_loader_requires_utc_and_filters_window(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = _write_fixture_data(Path(temp_dir), close_offset=0.0)
            bars = load_ohlcv_bars(
                data_root,
                "XAUUSD",
                start="2020-01-01T00:02:00Z",
                end="2020-01-01T00:05:00Z",
            )
        self.assertEqual(len(bars), 4)
        self.assertEqual(bars[0].timestamp.tzinfo, timezone.utc)
        self.assertEqual(bars[0].timestamp.isoformat(), "2020-01-01T00:02:00+00:00")

    def test_native_backtest_is_price_dependent_not_stubbed(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left_root = _write_fixture_data(Path(left_dir), close_offset=0.0)
            right_root = _write_fixture_data(Path(right_dir), close_offset=10.0)
            payload = payload_by_code("NASDAQ", "E")
            left_bars = load_ohlcv_bars(left_root, "NASDAQ", start="2020-01-01T00:00:00Z", end="2020-01-01T00:09:00Z")
            right_bars = load_ohlcv_bars(right_root, "NASDAQ", start="2020-01-01T00:00:00Z", end="2020-01-01T00:09:00Z")
            left_result = run_native_backtest(payload, left_bars)
            right_result = run_native_backtest(payload, right_bars)
        self.assertNotEqual(left_result.returns, right_result.returns)
        self.assertTrue(left_result.orders)

    def test_native_inputs_generate_complete_xauusd_nasdaq_payload_matrix(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = _write_fixture_data(Path(temp_dir), close_offset=0.0)
            inputs = build_native_inputs(data_root=data_root)
        self.assertEqual(inputs["candidate_space"]["asset_universe"], ["NASDAQ", "XAUUSD"])
        self.assertEqual(inputs["candidate_space"]["parameter_grid"]["payload_code"], list(PAYLOAD_CODES))
        self.assertEqual(len(inputs["candidate_test_returns_by_rank"]), 10)
        self.assertTrue(inputs["data_snapshots"][0]["checksum"])

    def test_native_research_package_validates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data", close_offset=0.0)
            package_dir = root / "research_package"
            report = build_native_research_package(package_dir, data_root=data_root)
            candidate_matrix = json.loads((package_dir / "reports" / "candidate_matrix.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(candidate_matrix["candidate_ids"]), 10)
        self.assertEqual(set(candidate_matrix["candidate_assets"].values()), {"NASDAQ", "XAUUSD"})


def _write_fixture_data(data_root: Path, *, close_offset: float) -> Path:
    rows = []
    start = datetime(2020, 1, 1, tzinfo=timezone.utc)
    for index in range(12):
        timestamp = start + timedelta(minutes=index)
        close = 100.0 + close_offset + index * (1.0 if index % 2 == 0 else 0.3)
        rows.append(
            {
                "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "open": close - 0.1,
                "high": close + 0.2,
                "low": close - 0.2,
                "close": close,
                "volume": 1.0 + index,
            }
        )
    _write_asset_csv(data_root / "NASDAQ 1m", "USATECH.IDXUSD-m1-bid-2020-01-01-2020-01-31.csv", rows)
    _write_asset_csv(data_root / "XAUUSD 1m", "XAUUSD-m1-bid-2020-01-01-2020-01-31.csv", rows)
    return data_root


def _write_asset_csv(folder: Path, filename: str, rows: list[dict]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
