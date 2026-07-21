import csv
import hashlib
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from ebta_engine.package_builder.nautilus_research_package import build_nautilus_inputs, build_nautilus_research_package
from ebta_engine.procedures._utils import canonical_json
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
        # The old R3 defect kept the package PASS despite a real economic gate failure.
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(economic["economic_status"], "REJECTED_ECONOMIC")
        self.assertIn("return_hurdle_pass", economic["failures"])
        self.assertIn("costs_pass", economic["failures"])


class NautilusReproducibilityProductionTests(unittest.TestCase):
    def test_environment_data_root_and_real_config_document_hash_reach_package(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            with patch.dict(os.environ, {"EBTA_DATA_ROOT": str(data_root)}):
                build_nautilus_research_package(
                    package_dir,
                    assets=["NASDAQ"],
                    segment_runner=_fake_segment_runner,
                )
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            registry_event = json.loads((package_dir / "registry.jsonl").read_text(encoding="utf-8").splitlines()[0])
            access_event = json.loads((package_dir / "oos_access_log.jsonl").read_text(encoding="utf-8").splitlines()[0])

        document_hash = config.pop("document_hash")
        expected_hash = hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest().upper()
        self.assertEqual(document_hash, expected_hash)
        self.assertEqual(len(document_hash), 64)
        self.assertNotIn("PLACEHOLDER", document_hash)
        for event in (registry_event, access_event):
            timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            self.assertEqual(timestamp.utcoffset(), timedelta(0))


class NautilusStatisticalGateProductionTests(unittest.TestCase):
    """Non-regression proof for PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE."""

    def test_real_wrc_fail_reaches_economic_and_incubation_gates(self):
        calls = []

        def runner(**kwargs):
            calls.append(kwargs["seed"])
            return _statistical_fail_segment_runner(**kwargs)

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
            files = {path.relative_to(package_dir).as_posix() for path in package_dir.rglob("*") if path.is_file()}

        self.assertEqual(config["config_id"], "CFG-NAUTILUS-MVP-001")
        self.assertEqual(report["status"], "DENIED")
        self.assertFalse(report["package_built"])
        self.assertIn("wrc_pass", report["oos_access_decision"]["missing_requirements"])
        self.assertNotIn(29, calls)
        self.assertEqual(files, {"config.json", "registry.jsonl"})


class NautilusRobustnessGateProductionTests(unittest.TestCase):
    """Non-regression proof for PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE."""

    def test_real_robustness_fail_reaches_g5_gate(self):
        calls = []

        def runner(**kwargs):
            calls.append(kwargs["seed"])
            return _robustness_fail_segment_runner(**kwargs)

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

        self.assertEqual(report["status"], "DENIED")
        self.assertIn("robustness_pass", report["oos_access_decision"]["missing_requirements"])
        self.assertNotIn(29, calls)
        self.assertFalse((package_dir / "oos_access_log.jsonl").exists())

    def test_r5_r6_cost_scenarios_execute_distinct_models_and_can_reject(self):
        observed_spreads = []

        def runner(**kwargs):
            spread = kwargs["cost_model"].spread_points
            observed_spreads.append(spread)
            bars = kwargs["bars"]
            daily_return = 0.002 - spread / 1000.0
            return SimulationResult(
                candidate_id=kwargs["candidate"].candidate_id,
                instrument_id=kwargs["instrument_config"].instrument_id,
                timestamps=[bar.timestamp.isoformat().replace("+00:00", "Z") for bar in bars],
                daily_returns=[daily_return for _ in bars],
                daily_exposure=[0.1 for _ in bars],
                nav=[1000.0 * (1.0 + daily_return) ** (index + 1) for index, _ in enumerate(bars)],
                total_costs=spread * 2.0,
                metadata={"source": "cost_sensitive_test_runner", "total_orders": 2},
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inputs = build_nautilus_inputs(
                data_root=_write_fixture_data(root / "data"),
                assets=["NASDAQ"],
                package_dir=root / "research_package",
                segment_runner=runner,
                execution_scope="PRE_OOS_BENCHMARK",
            )

        scenarios = {row["classification"]: row for row in inputs["robustness_plan"]["scenarios"]}
        self.assertEqual(sorted(set(observed_spreads)), [1.502, 3.515, 3.558])
        self.assertEqual(scenarios["CENTRAL"]["scenario_verdict"], "PASS")
        self.assertEqual(scenarios["PLAUSIBLE_BASE"]["scenario_verdict"], "REJECTED_ECONOMIC")
        self.assertEqual(scenarios["EXTREME"]["scenario_verdict"], "REJECTED_ECONOMIC")
        self.assertGreater(scenarios["CENTRAL"]["mean_return"], scenarios["EXTREME"]["mean_return"])


class NautilusChronologyProductionTests(unittest.TestCase):
    def test_pre_oos_benchmark_scope_stops_even_when_gates_authorize(self):
        calls = []

        def runner(**kwargs):
            calls.append(kwargs["seed"])
            return _fake_segment_runner(**kwargs)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            inputs = build_nautilus_inputs(
                package_dir=package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=runner,
                execution_scope="PRE_OOS_BENCHMARK",
            )
            oos_access_log_exists = (package_dir / "oos_access_log.jsonl").exists()

        self.assertEqual(inputs["_build_outcome"]["status"], "PRE_OOS_ONLY")
        self.assertEqual(inputs["_build_outcome"]["oos_access_decision"]["status"], "AUTHORIZED")
        self.assertNotIn(29, calls)
        self.assertFalse(oos_access_log_exists)
        metrics = inputs["_benchmark_metrics"]
        self.assertEqual(metrics["candidate_count"], 8)
        self.assertEqual(metrics["test_segment_count"], 16)
        self.assertEqual(metrics["test_bar_evaluation_count"], 48)
        self.assertEqual(metrics["unique_test_bar_count"], 6)
        self.assertTrue(metrics["fold_schedules_aligned"])

    def test_unknown_execution_scope_is_rejected_before_data_access(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "unsupported execution_scope"):
                build_nautilus_inputs(
                    package_dir=Path(temp_dir) / "research_package",
                    data_root=Path(temp_dir) / "missing-data",
                    execution_scope="OOS_BENCHMARK",  # type: ignore[arg-type]
                )

    def test_registry_and_access_are_persisted_before_their_respective_runs(self):
        instants = iter(
            [
                datetime(2026, 7, 20, 10, 0, tzinfo=timezone.utc),
                datetime(2026, 7, 20, 10, 1, tzinfo=timezone.utc),
                datetime(2026, 7, 20, 10, 2, tzinfo=timezone.utc),
                datetime(2026, 7, 20, 10, 3, tzinfo=timezone.utc),
            ]
        )
        observed_files = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"

            def runner(**kwargs):
                files = {path.name for path in package_dir.iterdir() if path.is_file()}
                observed_files.append((kwargs["seed"], files))
                self.assertIn("registry.jsonl", files)
                if kwargs["seed"] == 29:
                    self.assertIn("oos_access_log.jsonl", files)
                else:
                    self.assertNotIn("oos_access_log.jsonl", files)
                return _fake_segment_runner(**kwargs)

            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=runner,
                clock=lambda: next(instants),
            )
            registry = [json.loads(line) for line in (package_dir / "registry.jsonl").read_text(encoding="utf-8").splitlines()]
            access = [json.loads(line) for line in (package_dir / "oos_access_log.jsonl").read_text(encoding="utf-8").splitlines()]
            sealing = json.loads((package_dir / "reports" / "sealing.json").read_text(encoding="utf-8"))
            decision = json.loads((package_dir / "reports" / "oos_access_decision.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["gate_failures"], ["G14 INCONCLUSIVE: missing ['lifecycle_archive', 'incident_log', 'retention_policy']"])
        self.assertTrue(all(event["timestamp"] == "2026-07-20T10:00:00Z" for event in registry))
        self.assertEqual(sealing["sealed_at"], "2026-07-20T10:01:00Z")
        self.assertEqual(decision["log_entry"]["timestamp"], "2026-07-20T10:01:00Z")
        self.assertEqual([event["timestamp"] for event in access], ["2026-07-20T10:02:00Z", "2026-07-20T10:03:00Z"])
        self.assertTrue(any(seed == 29 for seed, _files in observed_files))

    def test_naive_runtime_clock_is_rejected_before_test_execution(self):
        calls = []
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            with self.assertRaisesRegex(ValueError, "timezone-aware"):
                build_nautilus_research_package(
                    root / "research_package",
                    data_root=data_root,
                    assets=["NASDAQ"],
                    segment_runner=lambda **kwargs: calls.append(kwargs) or _fake_segment_runner(**kwargs),
                    clock=lambda: datetime(2026, 7, 20, 10, 0),
                )
        self.assertEqual(calls, [])


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
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))
            fold_schedule = json.loads((package_dir / "reports" / "fold_schedule.json").read_text(encoding="utf-8"))
            oos_series = json.loads((package_dir / "series" / "oos_primary_returns.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["gate_failures"], ["G14 INCONCLUSIVE: missing ['lifecycle_archive', 'incident_log', 'retention_policy']"])
        self.assertEqual(len(config["walk_forward_schedule"]), 2)
        self.assertEqual(fold_schedule["fold_count"], 2)
        self.assertEqual(config["candidate_space"]["asset_universe"], ["NASDAQ"])
        self.assertEqual(search_space["candidate_count"], 8)
        self.assertEqual(search_space["asset_candidate_count"], {"NASDAQ": 8})
        self.assertEqual(execution["engine"], "nautilus_trader")
        self.assertEqual(execution["status"], "PASS")
        self.assertEqual(execution["nav_reconciliation"], "PASS")
        self.assertGreater(execution["total_orders"], 0)
        self.assertGreater(execution["oos_total_orders"], 0)
        for field in ("execution_report", "cost_model", "capacity_grid", "nav_reconciliation"):
            with self.subTest(field=field):
                self.assertEqual(gates[field], "PASS")
        self.assertEqual(len(oos_series["observations"]), 6)
        self.assertGreater(len(calls), 8)
        for call in calls:
            self.assertNotIn("segment", call)
            self.assertNotIn("segment_label", call)
            self.assertNotIn("oos", call)
            self.assertEqual(call["interval_value"], 1)
            self.assertEqual(call["interval_unit"], "MINUTE")
            self.assertEqual(len(call["bars"]), 3)

    def test_oos_without_orders_and_flat_nav_cannot_pass_g6(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_flat_oos_zero_order_segment_runner,
            )
            execution = json.loads((package_dir / "reports" / "execution.json").read_text(encoding="utf-8"))
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(execution["status"], "INCONCLUSIVE")
        self.assertEqual(execution["nav_reconciliation"], "INCONCLUSIVE")
        self.assertEqual(execution["oos_total_orders"], 0)
        self.assertIn("oos_total_orders", execution["failures"])
        self.assertIn("oos_nav_flat", execution["failures"])
        self.assertEqual(gates["execution_report"], "INCONCLUSIVE")
        self.assertEqual(gates["nav_reconciliation"], "INCONCLUSIVE")

    def test_non_positive_nav_fails_execution_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_non_positive_nav_segment_runner,
            )
            execution = json.loads((package_dir / "reports" / "execution.json").read_text(encoding="utf-8"))
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(execution["status"], "FAIL")
        self.assertEqual(execution["nav_reconciliation"], "FAIL")
        self.assertIn("nav_non_positive", execution["failures"])
        self.assertEqual(gates["execution_report"], "FAIL")
        self.assertEqual(gates["nav_reconciliation"], "FAIL")


def _losing_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    starting_nav = kwargs.get("starting_nav", 1000.0)
    returns = [(-0.01 if kwargs["seed"] == 29 else 0.001) for _ in bars]
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
        metadata={"source": "fake_nautilus_losing_test_runner", "total_orders": 2},
    )


def _statistical_fail_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    starting_nav = kwargs.get("starting_nav", 1000.0)
    if kwargs["seed"] == 13:
        returns = [0.0 for _ in bars]
    else:
        returns = [0.01 for _ in bars]
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
        metadata={"source": "fake_nautilus_statistical_fail_runner", "total_orders": 2},
    )


def _robustness_fail_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    starting_nav = kwargs.get("starting_nav", 1000.0)
    returns = [-1.5 for _ in bars]
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
        metadata={"source": "fake_nautilus_robustness_fail_runner", "total_orders": 2},
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
        metadata={"source": "fake_nautilus_test_runner", "total_orders": 2},
    )


def _flat_oos_zero_order_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    is_oos = kwargs["seed"] == 29
    return SimulationResult(
        candidate_id=kwargs["candidate"].candidate_id,
        instrument_id=kwargs["instrument_config"].instrument_id,
        timestamps=[bar.timestamp.isoformat().replace("+00:00", "Z") for bar in bars],
        daily_returns=[0.0 if is_oos else 0.001 for _ in bars],
        daily_exposure=[0.1 for _ in bars],
        nav=[1000.0 if is_oos else 1000.0 + index for index, _ in enumerate(bars)],
        total_costs=0.0,
        metadata={"source": "fake_nautilus_flat_oos_zero_order_runner", "total_orders": 0 if is_oos else 2},
    )


def _non_positive_nav_segment_runner(**kwargs) -> SimulationResult:
    bars = kwargs["bars"]
    nav = [-100.0 if kwargs["seed"] == 29 else 1000.0 + index for index, _ in enumerate(bars)]
    return SimulationResult(
        candidate_id=kwargs["candidate"].candidate_id,
        instrument_id=kwargs["instrument_config"].instrument_id,
        timestamps=[bar.timestamp.isoformat().replace("+00:00", "Z") for bar in bars],
        daily_returns=[-1.1 if kwargs["seed"] == 29 else 0.001 for _ in bars],
        daily_exposure=[0.1 for _ in bars],
        nav=nav,
        total_costs=0.0,
        metadata={"source": "fake_nautilus_non_positive_nav_runner", "total_orders": 2},
    )


def _write_fixture_data(data_root: Path) -> Path:
    rows = []
    start = datetime(2020, 1, 1, tzinfo=timezone.utc)
    for index in range(5):
        for minute_offset in range(3):
            timestamp = start + timedelta(days=index, minutes=minute_offset)
            close = 100.0 + index * 0.5 + minute_offset * 0.01
            rows.append(
                {
                    "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                    "open": close - 0.1,
                    "high": close + 0.2,
                    "low": close - 0.2,
                    "close": close,
                    "volume": 1.0 + index + minute_offset,
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
