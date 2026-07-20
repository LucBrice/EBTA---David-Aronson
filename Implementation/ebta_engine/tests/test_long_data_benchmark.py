import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ebta_engine.benchmarks import long_data
from ebta_engine.benchmarks.long_data import (
    _cell_contract_error,
    _process_tree_rss_bytes,
    _run_worker_process,
    _worker_data,
    _worker_main,
    _write_json_atomic,
    run_benchmark,
)


class LongDataBenchmarkTests(unittest.TestCase):
    def test_data_worker_separates_scan_and_load_and_matches_counts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = _write_fixture_data(Path(temp_dir) / "data")
            payload = _worker_data(
                data_root,
                "NASDAQ",
                "2020-01-01T00:00:00Z",
                "2020-01-01T00:02:00Z",
            )

        self.assertTrue(payload["load_matches_scan"])
        self.assertEqual(payload["loaded_bar_count"], 3)
        self.assertEqual(payload["inspection"]["bar_count"], 3)
        self.assertIsNone(_cell_contract_error("data", payload))

    def test_pipeline_contract_rejects_oos_and_wrong_campaign_cardinality(self):
        payload = _valid_pipeline_payload()
        self.assertIsNone(_cell_contract_error("pipeline", payload))

        payload["benchmark_metrics"]["oos_segment_count"] = 1
        self.assertEqual(_cell_contract_error("pipeline", payload), "oos_metrics_not_zero")

        payload = _valid_pipeline_payload()
        payload["benchmark_metrics"]["candidate_count"] = 8
        self.assertEqual(_cell_contract_error("pipeline", payload), "candidate_count_not_16")

    def test_worker_timeout_is_reported_and_process_tree_is_terminated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = Path(temp_dir) / "never.json"
            report = _run_worker_process(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                result_path=result_path,
                timeout_seconds=0.2,
            )

        self.assertEqual(report["status"], "BUDGET_EXCEEDED")
        self.assertEqual(report["reason"], "cell_timeout")

    def test_process_tree_rss_includes_current_process(self):
        self.assertGreater(_process_tree_rss_bytes(os.getpid()), 0)

    def test_atomic_json_writer_leaves_only_complete_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "nested" / "report.json"
            _write_json_atomic(target, {"status": "COMPLETED"})
            payload = json.loads(target.read_text(encoding="utf-8"))
            temporary_files = list(target.parent.glob("*.tmp"))

        self.assertEqual(payload, {"status": "COMPLETED"})
        self.assertEqual(temporary_files, [])

    def test_data_worker_main_serializes_data_invalid_instead_of_crashing(self):
        class Args:
            worker_result: Path
            data_root: Path
            start = "2020-01-01T00:00:00Z"
            end = "2020-01-01T00:01:00Z"
            assets = ["NASDAQ"]
            worker_kind = "data"

        with tempfile.TemporaryDirectory() as temp_dir:
            args = Args()
            args.worker_result = Path(temp_dir) / "result.json"
            args.data_root = Path(temp_dir) / "missing"
            exit_code = _worker_main(args)  # type: ignore[arg-type]
            payload = json.loads(args.worker_result.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["worker_status"], "DATA_INVALID")
        self.assertIn("not found", payload["error"])

    def test_pipeline_is_not_started_when_a_data_prerequisite_fails(self):
        declared_results = [
            {"status": "DATA_INVALID", "reason": "bad csv"},
            {"status": "COMPLETED"},
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.json"
            with (
                patch.object(long_data, "WINDOWS", (("TEST", "2020-01-01T00:00:00Z", "2020-01-02T00:00:00Z"),)),
                patch.object(long_data, "_run_declared_cell", side_effect=declared_results) as run_cell,
            ):
                report = run_benchmark(output, data_root=Path(temp_dir))

        self.assertEqual(run_cell.call_count, 2)
        self.assertEqual(report["pipeline_cells"][0]["status"], "DATA_INVALID")
        self.assertEqual(report["pipeline_cells"][0]["reason"], "data_prerequisite_not_completed")


def _valid_pipeline_payload() -> dict:
    return {
        "build_outcome": {"status": "PRE_OOS_ONLY"},
        "benchmark_metrics": {
            "candidate_count": 16,
            "test_segment_count": 32,
            "fold_schedules_aligned": True,
            "test_bar_evaluation_count": 46_080,
            "unique_test_bar_count": 5_760,
            "oos_segment_count": 0,
            "oos_bar_count": 0,
        },
        "oos_access_log_exists": False,
        "oos_access_log_event_count": 0,
        "package_validation": {"status": "FAIL"},
    }


def _write_fixture_data(data_root: Path) -> Path:
    folder = data_root / "NASDAQ 1m"
    folder.mkdir(parents=True)
    rows = [
        {
            "timestamp": f"2020-01-01T00:0{minute}:00Z",
            "open": "100",
            "high": "102",
            "low": "99",
            "close": "101",
            "volume": "10",
        }
        for minute in range(3)
    ]
    with (folder / "NASDAQ.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)
    return data_root


if __name__ == "__main__":
    unittest.main()
