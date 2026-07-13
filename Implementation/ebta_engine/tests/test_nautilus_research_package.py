import csv
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ebta_engine.package_builder.nautilus_research_package import build_nautilus_research_package
from ebta_engine.strategies.contracts import SimulationResult


class NautilusEconomicGateProductionTests(unittest.TestCase):
    """Non-regression proof for PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.

    Proves, on the real production path (not the isolated experiment
    module), that a known-losing candidate is rejected by the economic
    gate — the exact failure the hardcoded True booleans could never
    produce.
    """

    def test_known_loser_is_rejected_by_real_economic_gate_in_production(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_losing_segment_runner,
            )
            economic = json.loads((package_dir / "reports" / "economic.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(economic["economic_status"], "REJECTED_ECONOMIC")
        self.assertIn("return_hurdle_pass", economic["failures"])
        self.assertIn("costs_pass", economic["failures"])


class NautilusResearchPackageTests(unittest.TestCase):
    def test_nautilus_package_builder_validates_with_injected_segment_runner(self):
        calls = []

        def runner(**kwargs):
            calls.append(kwargs)
            return _fake_segment_runner(**kwargs)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=runner,
            )
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            search_space = json.loads((package_dir / "reports" / "search_space.json").read_text(encoding="utf-8"))
            execution = json.loads((package_dir / "reports" / "execution.json").read_text(encoding="utf-8"))
            fold_schedule = json.loads((package_dir / "reports" / "fold_schedule.json").read_text(encoding="utf-8"))
            oos_series = json.loads((package_dir / "series" / "oos_primary_returns.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(config["walk_forward_schedule"]), 2)
        self.assertEqual(fold_schedule["fold_count"], 2)
        self.assertEqual(config["candidate_space"]["asset_universe"], ["NASDAQ"])
        self.assertEqual(search_space["candidate_count"], 8)
        self.assertEqual(search_space["asset_candidate_count"], {"NASDAQ": 8})
        self.assertEqual(execution["engine"], "nautilus_trader")
        self.assertEqual(len(oos_series["observations"]), 2)
        self.assertGreater(len(calls), 8)
        for call in calls:
            self.assertNotIn("segment", call)
            self.assertNotIn("segment_label", call)
            self.assertNotIn("oos", call)


def _losing_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    starting_nav = kwargs.get("starting_nav", 1000.0)
    returns = [-0.01 for _ in bars]
    nav = []
    current_nav = starting_nav
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
        metadata={"source": "fake_nautilus_losing_test_runner"},
    )


def _fake_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    return SimulationResult(
        candidate_id=kwargs["candidate"].candidate_id,
        instrument_id=kwargs["instrument_config"].instrument_id,
        timestamps=[bar.timestamp.isoformat().replace("+00:00", "Z") for bar in bars],
        daily_returns=[0.001 for _ in bars],
        daily_exposure=[0.1 for _ in bars],
        nav=[1000.0 + index for index, _ in enumerate(bars)],
        total_costs=0.0,
        metadata={"source": "fake_nautilus_test_runner"},
    )


def _write_fixture_data(data_root: Path) -> Path:
    rows = []
    start = datetime(2020, 1, 1, tzinfo=timezone.utc)
    for index in range(5):
        timestamp = start + timedelta(days=index)
        close = 100.0 + index * 0.5
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
    return data_root


def _write_asset_csv(folder: Path, filename: str, rows: list[dict]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
