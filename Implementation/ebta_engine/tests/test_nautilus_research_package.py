import csv
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ebta_engine.package_builder.nautilus_research_package import build_nautilus_research_package
from ebta_engine.strategies.contracts import SimulationResult


class NautilusResearchPackageTests(unittest.TestCase):
    def test_nautilus_package_builder_validates_with_injected_segment_runner(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_fake_segment_runner,
            )
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            search_space = json.loads((package_dir / "reports" / "search_space.json").read_text(encoding="utf-8"))
            execution = json.loads((package_dir / "reports" / "execution.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(config["candidate_space"]["asset_universe"], ["NASDAQ"])
        self.assertEqual(search_space["candidate_count"], 8)
        self.assertEqual(search_space["asset_candidate_count"], {"NASDAQ": 8})
        self.assertEqual(execution["engine"], "nautilus_trader")


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
    for index in range(12):
        timestamp = start + timedelta(minutes=index)
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
