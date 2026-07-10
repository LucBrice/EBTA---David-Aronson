"""Controlled gate discrimination experiment for the Nautilus MVP.

This module is intentionally outside the production package-builder path. It
feeds existing EBTA gates with honest synthetic evidence and never changes the
procedures, adapters, validators, manifests, or protocol documents.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
if str(IMPLEMENTATION_ROOT) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from ebta_engine.adapters.nautilus_mapping import run_multifold_segments
from ebta_engine.data.local_ohlcv import OhlcvBar, load_ohlcv_bars
from ebta_engine.data.walk_forward import WalkForwardSplitter
from ebta_engine.package_builder.nautilus_research_package import _subprocess_segment_runner
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.procedures.robustness import pre_oos_robustness_verdict
from ebta_engine.risk.robustness import compute_robustness_scenarios
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig
from ebta_engine.strategies.contracts import SimulationResult
from ebta_engine.strategies.payloads import payload_by_code


FIXTURE_ROOT = IMPLEMENTATION_ROOT / "ebta_engine" / "tests" / "fixtures" / "gate_discrimination"
TRAIN_SIZE = 5
TEST_SIZE = 5
OOS_SIZE = 5
N_FOLDS = 2
HORIZON_BARS = 3
ECONOMIC_THRESHOLDS = {
    "minimum_mean_return": 0.0001,
    "maximum_total_costs": 0.0,
    "maximum_drawdown": 0.02,
}
CAPACITY_GRID = [{"capital": 1000.0, "status": "PASS", "reason": "synthetic MVP capacity not stressed"}]
DEFAULT_REPORT_PATH = Path(__file__).with_name("gate_discrimination_report.json")


REQUIRED_ECONOMIC_THRESHOLDS = (
    "minimum_mean_return",
    "maximum_total_costs",
    "maximum_drawdown",
)


def compute_economic_pass_flags(
    result: SimulationResult,
    *,
    thresholds: dict[str, float],
) -> dict[str, bool]:
    """Compute the five booleans consumed by economic_gate_report()."""
    missing = [key for key in REQUIRED_ECONOMIC_THRESHOLDS if key not in thresholds]
    if missing:
        raise ValueError(f"missing economic thresholds: {missing}")
    mean_return = _mean(result.daily_returns)
    max_drawdown = _max_drawdown(result.nav)
    return {
        "return_hurdle_pass": mean_return >= float(thresholds["minimum_mean_return"]),
        "drawdown_pass": max_drawdown <= float(thresholds["maximum_drawdown"]),
        "capacity_pass": True,
        "costs_pass": result.total_costs <= float(thresholds["maximum_total_costs"]),
        "execution_pass": True,
    }


def economic_observed_values(result: SimulationResult) -> dict[str, float]:
    """Return the scalar observations used to justify economic pass flags."""
    return {
        "mean_return": _mean(result.daily_returns),
        "total_costs": result.total_costs,
        "max_drawdown": _max_drawdown(result.nav),
    }


def run_controlled_gate_experiment(
    *,
    data_root: Path = FIXTURE_ROOT,
    segment_runner: Any | None = None,
) -> dict[str, Any]:
    """Run the controlled winner/loser experiment through EBTA gate helpers."""
    run_one = segment_runner or _subprocess_segment_runner
    candidates = [
        ("CONTROLLED-WINNER-NASDAQ", "NASDAQ"),
        ("CONTROLLED-LOSER-XAUUSD", "XAUUSD"),
    ]
    candidate_reports = []
    for candidate_id, asset in candidates:
        candidate_reports.append(
            _evaluate_candidate(
                candidate_id=candidate_id,
                asset=asset,
                data_root=data_root,
                segment_runner=run_one,
            )
        )
    by_id = {item["candidate_id"]: item for item in candidate_reports}
    winner = by_id["CONTROLLED-WINNER-NASDAQ"]
    loser = by_id["CONTROLLED-LOSER-XAUUSD"]
    status = "PASS" if (
        winner["economic_status"] == "PASS"
        and winner["robustness_status"] == "PASS"
        and (
            loser["economic_status"] == "REJECTED_ECONOMIC"
            or loser["robustness_status"] == "FAIL"
        )
    ) else "FAIL"
    return {
        "status": status,
        "thresholds": dict(ECONOMIC_THRESHOLDS),
        "candidate_reports": candidate_reports,
    }


def write_report(report: dict[str, Any], path: Path = DEFAULT_REPORT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _evaluate_candidate(
    *,
    candidate_id: str,
    asset: str,
    data_root: Path,
    segment_runner: Any | None,
) -> dict[str, Any]:
    bars = load_ohlcv_bars(data_root, asset)
    splitter = WalkForwardSplitter(
        n_folds=N_FOLDS,
        train_size=TRAIN_SIZE,
        test_size=TEST_SIZE,
        oos_size=OOS_SIZE,
        purge_days=0,
        embargo_days=0,
        warmup_days=0,
    )
    folds = splitter.build_folds(bars)
    candidate = _candidate(candidate_id, asset)
    common = {
        "candidate": candidate,
        "cost_model": _cost_model(),
        "instrument_config": _instrument_config(asset),
        "seed": 41,
        "starting_nav": 1000.0,
        "trade_size": "1",
        "interval_value": 1,
        "interval_unit": "DAY",
        "timestamp_is_close": True,
    }
    test_inputs = [{**common, "fold_id": fold["fold_id"], "bars": fold["test_bars"]} for fold in folds]
    oos_inputs = [{**common, "fold_id": fold["fold_id"], "bars": fold["oos_bars"]} for fold in folds]
    test_outputs = run_multifold_segments(test_inputs, runner=segment_runner)
    oos_outputs = run_multifold_segments(oos_inputs, runner=segment_runner)
    test_results = [output["simulation_result"] for output in test_outputs]
    oos_result = _merge_results(candidate_id, [output["simulation_result"] for output in oos_outputs])
    robustness_scenarios = compute_robustness_scenarios(
        {
            "CONTROLLED-CENTRAL": test_results,
            "CONTROLLED-PLAUSIBLE": test_results,
        },
        scenario_grid=_robustness_grid(),
    )
    robustness_report = pre_oos_robustness_verdict(
        robustness_scenarios,
        preregistered_catalogue=["CONTROLLED-CENTRAL", "CONTROLLED-PLAUSIBLE"],
    )
    economic_report = _economic_report(oos_result)
    return {
        "candidate_id": candidate_id,
        "asset": asset,
        "test_mean_return": _mean([value for result in test_results for value in result.daily_returns]),
        "oos_mean_return": _mean(oos_result.daily_returns),
        "economic_status": economic_report["global_status"],
        "economic_failures": economic_report["failures"],
        "robustness_status": robustness_report["status"],
        "robustness_scenarios": robustness_scenarios,
    }


def _economic_report(result: SimulationResult) -> dict[str, Any]:
    flags = compute_economic_pass_flags(result, thresholds=ECONOMIC_THRESHOLDS)
    evidence = result.economic_gate_evidence(
        statistical_status="PASS",
        thresholds=ECONOMIC_THRESHOLDS,
        observed_values=economic_observed_values(result),
        capacity_grid=CAPACITY_GRID,
        **flags,
    )
    return economic_gate_report(evidence)


def _candidate(candidate_id: str, asset: str) -> Candidate:
    payload = payload_by_code(asset, "E").to_dict()
    payload["exit_criterion"]["parameters"]["horizon_bars"] = HORIZON_BARS
    payload.pop("payload_hash", None)
    return Candidate(
        candidate_id=candidate_id,
        research_family_id="FAM-CONTROLLED-GATE-DISCRIMINATION",
        payload=payload,
        asset=asset,
        complexity=1,
    )


def _cost_model() -> CostModel:
    return CostModel(
        model_id="CONTROLLED-ZERO-FEE-DETERMINISTIC",
        fill_model="deterministic",
        fee_model="zero_fee",
        commission_per_lot=0.0,
        latency_nanos=0,
        prob_fill_on_limit=1.0,
        prob_slippage=0.0,
    )


def _instrument_config(asset: str) -> InstrumentConfig:
    if asset == "NASDAQ":
        return InstrumentConfig(
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
    if asset == "XAUUSD":
        return InstrumentConfig(
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
    raise ValueError(f"unsupported controlled experiment asset: {asset}")


def _robustness_grid() -> dict[str, Any]:
    return {
        "scenarios": [
            {
                "stress_id": "CONTROLLED-CENTRAL",
                "classification": "CENTRAL",
                "blocking": True,
                "minimum_mean_return": 0.0001,
                "stress_family": "controlled_central",
            },
            {
                "stress_id": "CONTROLLED-PLAUSIBLE",
                "classification": "PLAUSIBLE_BASE",
                "blocking": True,
                "minimum_mean_return": 0.0001,
                "stress_family": "controlled_plausible",
            },
        ]
    }


def _merge_results(candidate_id: str, results: list[SimulationResult]) -> SimulationResult:
    if not results:
        raise ValueError("cannot merge empty SimulationResult list")
    returns = [value for result in results for value in result.daily_returns]
    nav = []
    current_nav = 1000.0
    for value in returns:
        current_nav *= 1.0 + value
        nav.append(current_nav)
    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=results[0].instrument_id,
        timestamps=[timestamp for result in results for timestamp in result.timestamps],
        daily_returns=returns,
        daily_exposure=[value for result in results for value in result.daily_exposure],
        nav=nav,
        total_costs=sum(result.total_costs for result in results),
        orders=[order for result in results for order in result.orders],
        fills=[fill for result in results for fill in result.fills],
        positions=[position for result in results for position in result.positions],
        metadata={"source": "controlled_gate_discrimination", "fold_count": len(results)},
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _max_drawdown(nav: list[float]) -> float:
    if not nav:
        raise ValueError("nav must not be empty")
    peak = nav[0]
    max_drawdown = 0.0
    for value in nav:
        if value <= 0:
            return float("inf")
        if value > peak:
            peak = value
        max_drawdown = max(max_drawdown, (peak - value) / peak)
    return max_drawdown


def main() -> int:
    report = run_controlled_gate_experiment()
    report_path = write_report(report)
    print(json.dumps({**report, "report_path": str(report_path)}, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
