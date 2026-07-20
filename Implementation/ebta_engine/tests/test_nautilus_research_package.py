import csv
import hashlib
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from ebta_engine.package_builder.nautilus_research_package import build_nautilus_research_package
from ebta_engine.procedures._utils import canonical_json
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.procedures.lifecycle import incubation_gate
from ebta_engine.strategies.contracts import SimulationResult
from ebta_engine.validators.gate_validator import gate_report


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

        document_hash = config.pop("document_hash")
        expected_hash = hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest().upper()
        self.assertEqual(document_hash, expected_hash)
        self.assertEqual(len(document_hash), 64)
        self.assertNotIn("PLACEHOLDER", document_hash)


class NautilusStatisticalGateProductionTests(unittest.TestCase):
    """Non-regression proof for PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE."""

    def test_real_wrc_fail_reaches_economic_and_incubation_gates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_statistical_fail_segment_runner,
            )
            config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
            wrc = json.loads((package_dir / "reports" / "wrc.json").read_text(encoding="utf-8"))
            economic = json.loads((package_dir / "reports" / "economic.json").read_text(encoding="utf-8"))
            incubation = json.loads((package_dir / "reports" / "incubation_gate.json").read_text(encoding="utf-8"))
            robustness = json.loads((package_dir / "reports" / "robustness.json").read_text(encoding="utf-8"))
            execution = json.loads((package_dir / "reports" / "execution.json").read_text(encoding="utf-8"))
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))
            oos_access = json.loads((package_dir / "reports" / "oos_access_decision.json").read_text(encoding="utf-8"))
            reproduction = json.loads(
                (package_dir / "reports" / "reproduction_validation.json").read_text(encoding="utf-8")
            )

        # The old R3 defect kept the package PASS despite a real statistical gate failure.
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(wrc["verdict"], "FAIL")
        self.assertEqual(economic["statistical_status"], "FAIL")
        self.assertEqual(economic["economic_status"], "PASS")
        self.assertEqual(economic["global_status"], "FAIL")
        self.assertEqual(incubation["status"], "FAIL")
        self.assertIn("statistical_status", incubation["failures"])
        self.assertEqual(oos_access["status"], "DENIED")
        self.assertIn("wrc_pass", oos_access["missing_requirements"])
        for field in ("oos_access_log", "opening_authorization", "single_oos_execution_log"):
            with self.subTest(field=field):
                self.assertEqual(gates[field], "INCONCLUSIVE")

        old_economic = economic_gate_report(
            {
                "statistical_status": "PASS",
                "return_hurdle_pass": True,
                "drawdown_pass": True,
                "capacity_pass": True,
                "costs_pass": True,
                "execution_pass": True,
                "thresholds": economic["thresholds"],
                "observed_values": economic["observed_values"],
                "capacity_grid": economic["capacity_grid"],
            }
        )
        old_incubation = incubation_gate(
            {
                "statistical_status": "PASS",
                "economic_status": old_economic["economic_status"],
                "robustness_status": robustness["status"],
                "execution_status": execution["status"],
                "package_stage": config["reproducibility_manifest"]["package_stage"],
                "reproduction_status": reproduction["status"],
            }
        )
        self.assertEqual(old_economic["global_status"], "PASS")
        self.assertEqual(old_incubation["status"], "PASS")


class NautilusRobustnessGateProductionTests(unittest.TestCase):
    """Non-regression proof for PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE."""

    def test_real_robustness_fail_reaches_g5_gate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_root = _write_fixture_data(root / "data")
            package_dir = root / "research_package"
            report = build_nautilus_research_package(
                package_dir,
                data_root=data_root,
                assets=["NASDAQ"],
                segment_runner=_robustness_fail_segment_runner,
            )
            gates = json.loads((package_dir / "reports" / "gates.json").read_text(encoding="utf-8"))
            robustness = json.loads((package_dir / "reports" / "robustness.json").read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(robustness["status"], "FAIL")
        self.assertEqual(gates["pre_oos_robustness_verdict"], "FAIL")

        honest_gate_report = gate_report(gates)
        g5 = _gate_by_id(honest_gate_report, "G5")
        self.assertEqual(g5["status"], "INCONCLUSIVE")
        self.assertIn("pre_oos_robustness_verdict", g5["missing"])

        old_hardcoded_gates = dict(gates)
        old_hardcoded_gates["pre_oos_robustness_verdict"] = "PASS"
        old_g5 = _gate_by_id(gate_report(old_hardcoded_gates), "G5")
        self.assertEqual(old_g5["status"], "PASS")
        self.assertEqual(robustness["status"], "FAIL")


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
        self.assertEqual(report["status"], "PASS")
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


def _gate_by_id(report: dict, gate_id: str) -> dict:
    for gate in report["gates"]:
        if gate["gate_id"] == gate_id:
            return gate
    raise AssertionError(f"missing gate {gate_id}")


def _write_asset_csv(folder: Path, filename: str, rows: list[dict]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
