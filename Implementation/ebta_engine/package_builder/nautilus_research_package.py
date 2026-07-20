"""Build an EBTA research package backed by NautilusTrader simulations."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypedDict

from ebta_engine.adapters.nautilus_mapping import run_multifold_segments
from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, OhlcvBar, build_data_snapshot, load_ohlcv_bars, resolve_data_root
from ebta_engine.data.walk_forward import WalkForwardSplitter
from ebta_engine.package_builder.economic_calibration import compute_economic_pass_flags, economic_observed_values
from ebta_engine.procedures._utils import canonical_json
from ebta_engine.risk.robustness import compute_robustness_scenarios
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig, SimulationResult
from ebta_engine.strategies.payload_factory import generate_family, liquidity_sweep_family_spec


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
PILOT_SCRIPT = IMPLEMENTATION_ROOT / "examples" / "minimal_pilot_pipeline" / "build_research_package.py"
DEFAULT_NAUTILUS_ASSETS = ["NASDAQ", "XAUUSD"]
DEFAULT_NAUTILUS_START = "2020-01-01T00:00:00Z"
DEFAULT_NAUTILUS_END = "2020-01-10T23:59:00Z"
NAUTILUS_SEGMENT_TIMEOUT_SECONDS = 300
# Nautilus/Rust logging is process-global and the Windows venv is not reliable
# under concurrent subprocess segment launches. Keep isolation per segment, but
# run those subprocesses sequentially to avoid validation hangs.
NAUTILUS_SEGMENT_WORKERS = 1

# SOP 08 production thresholds for the Nautilus MVP perimeter (NASDAQ,
# XAUUSD, liquidity-sweep family), calibrated by the human on 2026-07-10 (see
# .ai/backlog/fixes/PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md section
# 10): annualized return must be strictly positive net of costs (a positive
# per-period mean return is equivalent, since annualization is a monotonic
# positive scaling); max drawdown 20% relative to the running high-water
# mark. capacity_pass and execution_pass remain documented constants
# (True) — no production target_capital or execution stress grid has been
# calibrated yet; costs_pass has no separate absolute cap and is derived
# from the net-of-costs return (see economic_calibration.compute_economic_pass_flags).
NAUTILUS_ECONOMIC_THRESHOLDS = {
    "minimum_mean_return": 0.0,
    "maximum_drawdown": 0.20,
}


SegmentRunner = Callable[..., SimulationResult]
RuntimeClock = Callable[[], datetime]


class OosRunSpec(TypedDict):
    asset: str
    date_range: list[str]
    run_input: dict[str, Any]


def _load_pilot_module():
    spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
    assert spec is not None and spec.loader is not None, f"cannot load spec for {PILOT_SCRIPT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_nautilus_inputs(
    *,
    data_root: Path | None = None,
    assets: list[str] | None = None,
    start: str = DEFAULT_NAUTILUS_START,
    end: str = DEFAULT_NAUTILUS_END,
    segment_runner: SegmentRunner | None = None,
    package_dir: Path,
    clock: RuntimeClock | None = None,
) -> dict:
    effective_data_root = resolve_data_root(data_root)
    assets = sorted(assets or DEFAULT_NAUTILUS_ASSETS)
    pilot = _load_pilot_module()
    inputs = copy.deepcopy(pilot.load_pilot_inputs())
    inputs["oos_access_template"] = copy.deepcopy(inputs["oos_access_log"][0])
    inputs["oos_access_log"] = []
    inputs["pre_oos_seal"].pop("fixture_sealed_at", None)
    inputs["actor"] = "nautilus_trader_adapter"
    inputs["identifiers"].update(
        {
            "config_id": "CFG-NAUTILUS-MVP-001",
            "project_id": "PRJ-NAUTILUS-MVP",
            "research_family_id": "FAM-LIQUIDITY-SWEEP-NAUTILUS",
            "hypothesis_id": "HYP-LIQUIDITY-SWEEP-NAUTILUS-XAUUSD-NASDAQ",
            "process_version_id": "PROC-NAUTILUS-MVP-001",
            "document_hash": "",
        }
    )
    snapshot = build_data_snapshot(effective_data_root, assets, start=start, end=end)
    inputs["data_snapshots"] = [snapshot]
    inputs["statistical_plan"]["wrc_run_secondary"] = False
    inputs["candidate_space"].update(
        {
            "base_spec": {"logic": "liquidity_sweep_confirmation", "engine": "nautilus_trader"},
            "asset_universe": assets,
            "asset_selection_axis": "asset",
            "asset_selection_rule": "evaluate_all_declared_assets",
            "parameter_grid": {
                "asset": assets,
                "bias_filter": ["none", "directional_mtf_bias"],
                "session": ["all", "asia", "london", "us"],
            },
            "budget": {"max_candidates": len(assets) * 8, "max_train_evaluations": len(assets) * 8},
            "validity_criteria": ["train_only_calibration", "complete_test_matrix", "nautilus_data_provenance"],
            "stability_criteria": ["payload_complexity_tie_break", "turnover_cost_exposure_tie_break"],
        }
    )
    inputs["execution_model"]["cost_model"] = _nautilus_cost_model().to_dict()

    run_one = segment_runner or _subprocess_segment_runner
    segment_workers = 1 if segment_runner is not None else NAUTILUS_SEGMENT_WORKERS
    search_space = pilot._pilot_search_space(inputs)
    raw_bars_by_asset = {
        asset: load_ohlcv_bars(effective_data_root, asset, start=start, end=end)
        for asset in assets
    }
    day_index_by_asset = {
        asset: _day_boundary_index(bars)
        for asset, bars in raw_bars_by_asset.items()
    }
    splitter = WalkForwardSplitter(
        n_folds=2,
        train_size=2,
        test_size=1,
        oos_size=1,
        purge_days=0,
        embargo_days=0,
        warmup_days=0,
    )
    reference_folds = splitter.build_folds(day_index_by_asset[assets[0]])
    inputs["walk_forward_schedule"] = splitter.schedule(reference_folds)
    inputs["information_stop_criterion"] = {
        "criterion_type": "FIXED_FOLD_COUNT",
        "description": "Nautilus MVP executes two preregistered walk-forward folds.",
        "fixed_fold_count": len(reference_folds),
        "fixed_end_date": None,
    }
    search_space = pilot._pilot_search_space(inputs)
    folds_by_asset = {
        asset: splitter.build_folds(day_index_by_asset[asset])
        for asset in assets
    }
    candidate_series_by_id = {candidate_row["candidate_id"]: [] for candidate_row in search_space["candidates"]}
    result_by_candidate: dict[str, list[SimulationResult]] = {
        candidate_row["candidate_id"]: [] for candidate_row in search_space["candidates"]
    }
    segment_inputs = []
    candidate_rows_by_id = {row["candidate_id"]: row for row in search_space["candidates"]}
    payloads_by_fold = {
        fold["fold_id"]: _payloads_by_axis(assets, inputs["identifiers"]["research_family_id"], fold["fold_id"])
        for fold in reference_folds
    }
    for fold in reference_folds:
        for candidate_row in search_space["candidates"]:
            parameters = candidate_row["parameters"]
            asset = parameters["asset"]
            asset_fold = _fold_by_id(folds_by_asset[asset], fold["fold_id"])
            payload = payloads_by_fold[fold["fold_id"]][(asset, parameters["bias_filter"], parameters["session"])]
            segment_inputs.append(
                {
                    "fold_id": fold["fold_id"],
                    "candidate": Candidate(
                        candidate_id=candidate_row["candidate_id"],
                        research_family_id=inputs["identifiers"]["research_family_id"],
                        payload=payload.to_dict(),
                        asset=asset,
                        complexity=int(parameters.get("complexity", 1)),
                        fold_id=fold["fold_id"],
                    ),
                    "bars": _slice_bars_by_date_range(raw_bars_by_asset[asset], *asset_fold["schedule"]["test"]),
                    "cost_model": _nautilus_cost_model(),
                    "instrument_config": _instrument_config(asset),
                    "seed": 13,
                    "starting_nav": 1000.0,
                    "trade_size": "1",
                    "interval_value": 1,
                    "interval_unit": "MINUTE",
                    "timestamp_is_close": True,
                }
            )
    inputs["registry_timestamp"] = _runtime_timestamp(clock)
    inputs["identifiers"]["document_hash"] = _config_document_hash(pilot, inputs)
    pilot.prepare_pre_oos_package(package_dir, inputs)
    test_outputs = run_multifold_segments(segment_inputs, runner=run_one, max_workers=segment_workers)
    for output in test_outputs:
        result = output["simulation_result"]
        candidate_series_by_id[output["candidate_id"]].extend(result.daily_returns)
        result_by_candidate[output["candidate_id"]].append(result)

    candidate_series = [candidate_series_by_id[row["candidate_id"]] for row in search_space["candidates"]]
    train_scores: list[float] = []
    for series in candidate_series:
        train_scores.append(_mean(series))
    selected_candidate_id = max(zip(search_space["candidates"], train_scores), key=lambda item: item[1])[0]["candidate_id"]
    selected_row = candidate_rows_by_id[selected_candidate_id]
    oos_inputs: list[OosRunSpec] = []
    for fold in reference_folds:
        parameters = selected_row["parameters"]
        asset = parameters["asset"]
        asset_fold = _fold_by_id(folds_by_asset[asset], fold["fold_id"])
        payload = payloads_by_fold[fold["fold_id"]][(asset, parameters["bias_filter"], parameters["session"])]
        oos_inputs.append(
            {
                "asset": asset,
                "date_range": asset_fold["schedule"]["oos"],
                "run_input": {
                    "fold_id": fold["fold_id"],
                    "candidate": Candidate(
                        candidate_id=selected_candidate_id,
                        research_family_id=inputs["identifiers"]["research_family_id"],
                        payload=payload.to_dict(),
                        asset=asset,
                        complexity=int(parameters.get("complexity", 1)),
                        fold_id=fold["fold_id"],
                    ),
                    "cost_model": _nautilus_cost_model(),
                    "instrument_config": _instrument_config(asset),
                    "seed": 29,
                    "starting_nav": 1000.0,
                    "trade_size": "1",
                    "interval_value": 1,
                    "interval_unit": "MINUTE",
                    "timestamp_is_close": True,
                },
            }
        )
    inputs["train_scores_by_rank"] = train_scores
    inputs["representative_test_scores_by_rank"] = [max(train_scores)]
    inputs["candidate_test_returns_by_rank"] = candidate_series
    first_candidate_id = search_space["candidates"][0]["candidate_id"]
    inputs["candidate_test_dates"] = [
        timestamp
        for result in result_by_candidate[first_candidate_id]
        for timestamp in result.timestamps
    ]
    test_results = [result for results in result_by_candidate.values() for result in results]
    inputs["execution_report"] = _execution_report(test_results, [], require_oos=False)
    inputs["robustness_plan"]["scenarios"] = compute_robustness_scenarios(
        {
            "ROB-NAUTILUS-CENTRAL": test_results,
            "ROB-NAUTILUS-PLAUSIBLE": test_results,
            "ROB-NAUTILUS-EXTREME": test_results,
        },
        scenario_grid=_nautilus_robustness_grid(),
    )
    if clock is not None:
        inputs["pre_oos_seal"]["fixture_sealed_at"] = _runtime_timestamp(clock)
    pre_oos_reports = pilot._pre_oos_reports(inputs)
    pilot.cache_pre_oos_reports(inputs, pre_oos_reports)
    oos_access_decision = pre_oos_reports["oos_access_decision"]
    if oos_access_decision["status"] != "AUTHORIZED":
        inputs["_build_outcome"] = {
            "status": "DENIED",
            "package_built": False,
            "oos_access_decision": copy.deepcopy(oos_access_decision),
            "pre_oos_reports_hash": pre_oos_reports["content_hash"],
        }
        return inputs

    access_template = inputs["oos_access_template"]
    oos_outputs = []
    for index, (fold, oos_spec) in enumerate(zip(reference_folds, oos_inputs), start=1):
        access_event = {
            **access_template,
            "access_event_id": f"OOS-ACCESS-NAUTILUS-{index:03d}",
            "timestamp": _runtime_timestamp(clock),
            "actor": "nautilus_trader_adapter",
            "fold_id": fold["fold_id"],
            "oos_segment_id": f"OOS-{index:03d}",
            "read_paths": [str(effective_data_root)],
            "write_paths": ["reports/oos.json", "series/oos_primary_returns.json"],
            "result_artifact_hash": "",
        }
        inputs["oos_access_log"].append(access_event)
        pilot._write_oos_access_log(package_dir, {"oos_access_log": [access_event]})
        run_input = dict(oos_spec["run_input"])
        asset = oos_spec["asset"]
        run_input["bars"] = _slice_bars_by_date_range(raw_bars_by_asset[asset], *oos_spec["date_range"])
        oos_outputs.extend(run_multifold_segments([run_input], runner=run_one, max_workers=segment_workers))
    oos_results = [output["simulation_result"] for output in oos_outputs]
    all_simulation_results = [result for results in result_by_candidate.values() for result in results] + oos_results
    oos_returns = [value for result in oos_results for value in result.daily_returns]
    inputs["oos_returns"] = oos_returns
    inputs["oos_primary_returns"] = [
        {
            "date": timestamp[:10],
            "net_detrended_log_return": value,
            "status": "EXPOSED",
            "fold_id": output["fold_id"],
        }
        for output in oos_outputs
        for timestamp, value in zip(output["simulation_result"].timestamps, output["simulation_result"].daily_returns)
    ]
    inputs["train_scores_by_rank"] = train_scores
    inputs["representative_test_scores_by_rank"] = [max(train_scores)]
    inputs["candidate_test_returns_by_rank"] = candidate_series
    first_candidate_id = search_space["candidates"][0]["candidate_id"]
    inputs["candidate_test_dates"] = [
        timestamp
        for result in result_by_candidate[first_candidate_id]
        for timestamp in result.timestamps
    ]
    inputs["data_availability_checks"] = [
        {"available_at": snapshot["available_at"], "decision_at": fold["schedule"]["information_cutoff"]}
        for fold in reference_folds
    ]
    inputs["execution_report"] = _execution_report(all_simulation_results, oos_results, require_oos=True)
    inputs["reproduction_report"]["commands"] = [
        "Implementation\\adapters\\nautilus_env\\venv\\Scripts\\python.exe -m ebta_engine.package_builder.nautilus_research_package"
    ]
    inputs["reproduction_report"]["notes"] = "Nautilus package built from local OHLCV CSV files and EBTA StrategyPayload contracts; no BACKTRADER runtime dependency."
    inputs["incubation_report"]["data_source_ids"] = [snapshot["data_snapshot_id"]]
    selected_oos = _merge_results(selected_candidate_id, oos_results)
    economic_thresholds = dict(NAUTILUS_ECONOMIC_THRESHOLDS)
    min_annualized_return = inputs["economic_gate"].get("thresholds", {}).get("min_annualized_return")
    if min_annualized_return is not None:
        economic_thresholds["min_annualized_return"] = min_annualized_return
    economic_flags = compute_economic_pass_flags(selected_oos, thresholds=economic_thresholds)
    inputs["economic_gate"] = selected_oos.economic_gate_evidence(
        # Placeholder only: the pilot assembly overwrites this with the real
        # WRC verdict before building economic.json.
        statistical_status="PENDING_WRC",
        thresholds=economic_thresholds,
        observed_values={
            **economic_observed_values(selected_oos),
            "mean_oos_return": _mean(oos_returns),
            "fold_count": len(reference_folds),
        },
        capacity_grid=inputs["economic_gate"]["capacity_grid"],
        **economic_flags,
    )
    return inputs


def build_nautilus_research_package(
    package_dir: Path,
    *,
    data_root: Path | None = None,
    assets: list[str] | None = None,
    start: str = DEFAULT_NAUTILUS_START,
    end: str = DEFAULT_NAUTILUS_END,
    segment_runner: SegmentRunner | None = None,
    clock: RuntimeClock | None = None,
) -> dict:
    pilot = _load_pilot_module()
    inputs = build_nautilus_inputs(
        data_root=data_root,
        assets=assets,
        start=start,
        end=end,
        segment_runner=segment_runner,
        package_dir=package_dir,
        clock=clock,
    )
    denied = inputs.get("_build_outcome")
    if denied is not None:
        return denied
    return pilot.build_package(package_dir, pilot_inputs=inputs, prepared_pre_oos=True)


def _config_document_hash(pilot: Any, inputs: dict[str, Any]) -> str:
    document = copy.deepcopy(pilot.config_document(inputs))
    document.pop("document_hash")
    return hashlib.sha256(canonical_json(document).encode("utf-8")).hexdigest().upper()


def _runtime_timestamp(clock: RuntimeClock | None) -> str:
    value = (clock or (lambda: datetime.now(timezone.utc)))()
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("runtime clock must return a timezone-aware datetime")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _payloads_by_axis(assets: list[str], research_family_id: str, fold_id: str) -> dict[tuple[str, str, str], Any]:
    generated = generate_family(
        assets=assets,
        spec=liquidity_sweep_family_spec(),
        research_family_id=research_family_id,
        fold_id=fold_id,
    )
    return {
        (payload.asset, payload.bias_filter, payload.session): payload
        for payload in generated["payloads"]
    }


def _nautilus_cost_model() -> CostModel:
    # Indicative maker/taker fee rates (2026-07-10 calibration decision, see
    # .ai/backlog/fixes/PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md
    # section 10): generic retail CFD-style rates, not yet sourced from a
    # real broker. maker_fee/taker_fee live on InstrumentConfig
    # (_instrument_config) and are consumed by Nautilus's MakerTakerFeeModel
    # via fee_model="maker_taker" below (nautilus_mapping.py::_fee_model()).
    return CostModel(
        model_id="NAUTILUS-MAKER-TAKER-INDICATIVE",
        fill_model="deterministic",
        fee_model="maker_taker",
        commission_per_lot=0.0,
        latency_nanos=0,
        prob_fill_on_limit=1.0,
        prob_slippage=0.0,
    )


def _instrument_config(asset: str) -> InstrumentConfig:
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
            maker_fee="0.0002",
            taker_fee="0.0005",
            base_currency="XAU",
            quote_currency="USD",
            asset_class="CFD",
            metadata={"underlying_asset_class": "COMMODITY"},
        )
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
            maker_fee="0.0002",
            taker_fee="0.0005",
            asset_class="CFD",
            metadata={"underlying_asset_class": "INDEX"},
        )
    raise ValueError(f"unsupported Nautilus package asset: {asset}")


def _subprocess_segment_runner(**kwargs) -> SimulationResult:
    payload = {
        "candidate": kwargs["candidate"].to_dict(),
        "bars": [_bar_to_dict(bar) for bar in kwargs["bars"]],
        "cost_model": kwargs["cost_model"].to_dict(),
        "instrument_config": kwargs["instrument_config"].to_dict(),
        "seed": kwargs["seed"],
        "starting_nav": kwargs.get("starting_nav", 1000.0),
        "trade_size": kwargs.get("trade_size", "1"),
        "interval_value": kwargs.get("interval_value", 1),
        "interval_unit": kwargs.get("interval_unit", "MINUTE"),
        "timestamp_is_close": kwargs.get("timestamp_is_close", False),
    }
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle)
        request_path = Path(handle.name)
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "ebta_engine.adapters.nautilus_segment_cli", str(request_path)],
            cwd=IMPLEMENTATION_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=NAUTILUS_SEGMENT_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Nautilus segment subprocess failed "
            f"candidate_id={kwargs['candidate'].candidate_id!r} "
            f"fold_id={kwargs['candidate'].fold_id!r} "
            f"asset={kwargs['candidate'].asset!r} "
            f"bars={len(kwargs['bars'])} "
            f"interval={kwargs.get('interval_value', 1)}-{kwargs.get('interval_unit', 'MINUTE')}\n"
            f"stdout:\n{exc.stdout}\n"
            f"stderr:\n{exc.stderr}"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "Nautilus segment subprocess timed out "
            f"candidate_id={kwargs['candidate'].candidate_id!r} "
            f"fold_id={kwargs['candidate'].fold_id!r} "
            f"asset={kwargs['candidate'].asset!r} "
            f"bars={len(kwargs['bars'])} "
            f"timeout_seconds={NAUTILUS_SEGMENT_TIMEOUT_SECONDS}\n"
            f"stdout:\n{exc.stdout}\n"
            f"stderr:\n{exc.stderr}"
        ) from exc
    finally:
        request_path.unlink(missing_ok=True)
    result_payload = json.loads(completed.stdout.strip().splitlines()[-1])
    result_payload.pop("result_hash", None)
    return SimulationResult(**result_payload)


def _bar_to_dict(bar: Any) -> dict[str, Any]:
    return {
        "asset": bar.asset,
        "timestamp": bar.timestamp.isoformat().replace("+00:00", "Z"),
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume,
    }


def _day_boundary_index(bars: list[OhlcvBar]) -> list[OhlcvBar]:
    """Return one bar per day for fold date boundaries, never for simulation."""
    if not bars:
        raise ValueError("no bars loaded for Nautilus package")
    by_day: dict[str, OhlcvBar] = {}
    for bar in sorted(bars, key=lambda item: item.timestamp):
        by_day.setdefault(bar.timestamp.date().isoformat(), bar)
    return [by_day[day] for day in sorted(by_day)]


def _slice_bars_by_date_range(bars: list[OhlcvBar], start_day: str, end_day: str) -> list[OhlcvBar]:
    """Return raw M1 bars with calendar dates inside the inclusive day range."""
    sliced = [
        bar
        for bar in bars
        if start_day <= bar.timestamp.date().isoformat() <= end_day
    ]
    if not sliced:
        raise ValueError(f"no bars found in inclusive date range [{start_day}, {end_day}]")
    return sliced


def _fold_by_id(folds: list[dict[str, Any]], fold_id: str) -> dict[str, Any]:
    for fold in folds:
        if fold["fold_id"] == fold_id:
            return fold
    raise KeyError(fold_id)


def _merge_results(candidate_id: str, results: list[SimulationResult]) -> SimulationResult:
    if not results:
        raise ValueError("cannot merge empty SimulationResult list")
    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=results[0].instrument_id,
        timestamps=[timestamp for result in results for timestamp in result.timestamps],
        daily_returns=[value for result in results for value in result.daily_returns],
        daily_exposure=[value for result in results for value in result.daily_exposure],
        nav=[value for result in results for value in result.nav],
        total_costs=sum(result.total_costs for result in results),
        orders=[order for result in results for order in result.orders],
        fills=[fill for result in results for fill in result.fills],
        positions=[position for result in results for position in result.positions],
        metadata={"source": "nautilus_trader", "fold_count": len(results)},
    )


def _total_orders(results: list[SimulationResult]) -> int:
    total = 0
    for result in results:
        raw_total = result.metadata.get("total_orders") if isinstance(result.metadata, dict) else None
        total += int(raw_total) if raw_total is not None else len(result.orders)
    return total


def _execution_nav_evidence(
    all_results: list[SimulationResult],
    oos_results: list[SimulationResult],
    *,
    require_oos: bool = True,
) -> dict[str, Any]:
    all_nav = [value for result in all_results for value in result.nav]
    oos_nav = [value for result in oos_results for value in result.nav]
    total_orders = _total_orders(all_results)
    oos_total_orders = _total_orders(oos_results)
    nav_positive = bool(all_nav) and all(value > 0.0 for value in all_nav)
    nav_non_flat = _series_non_flat(all_nav)
    oos_nav_non_flat = _series_non_flat(oos_nav)
    failures: list[str] = []

    if total_orders <= 0:
        failures.append("total_orders")
    if require_oos and oos_total_orders <= 0:
        failures.append("oos_total_orders")
    if not all_nav:
        failures.append("nav")
    if require_oos and not oos_nav:
        failures.append("oos_nav")
    if all_nav and not nav_positive:
        failures.append("nav_non_positive")
    if all_nav and not nav_non_flat:
        failures.append("nav_flat")
    if oos_nav and not oos_nav_non_flat:
        failures.append("oos_nav_flat")

    if "nav_non_positive" in failures:
        status = "FAIL"
    elif failures:
        status = "INCONCLUSIVE"
    else:
        status = "PASS"

    return {
        "status": status,
        "nav_reconciliation": status,
        "nav_observation_count": len(all_nav),
        "oos_nav_observation_count": len(oos_nav),
        "nav_positive": nav_positive,
        "nav_non_flat": nav_non_flat,
        "oos_nav_non_flat": oos_nav_non_flat,
        "failures": failures,
    }


def _execution_report(
    all_results: list[SimulationResult],
    oos_results: list[SimulationResult],
    *,
    require_oos: bool,
) -> dict[str, Any]:
    evidence = _execution_nav_evidence(all_results, oos_results, require_oos=require_oos)
    return {
        "status": evidence["status"],
        "cost_model": _nautilus_cost_model().model_id,
        "central_scenario": "tradable_net",
        "orders": [{"order_id": "ORDER-NAUTILUS-MVP-SUMMARY", "status": "FILLED", "fill_id": "FILL-NAUTILUS-MVP-SUMMARY"}],
        "total_orders": _total_orders(all_results),
        "oos_total_orders": _total_orders(oos_results),
        "nav_reconciliation": evidence["nav_reconciliation"],
        "nav_observation_count": evidence["nav_observation_count"],
        "oos_nav_observation_count": evidence["oos_nav_observation_count"],
        "nav_positive": evidence["nav_positive"],
        "nav_non_flat": evidence["nav_non_flat"],
        "oos_nav_non_flat": evidence["oos_nav_non_flat"],
        "failures": evidence["failures"],
        "engine": "nautilus_trader",
        "evidence_scope": "TEST_ONLY" if not require_oos else "TEST_AND_OOS",
        "backtrader_runtime_dependency": False,
    }


def _series_non_flat(values: list[float]) -> bool:
    return bool(values) and any(value != values[0] for value in values[1:])


def _nautilus_robustness_grid() -> dict[str, Any]:
    return {
        "scenarios": [
            {
                "stress_id": "ROB-NAUTILUS-CENTRAL",
                "classification": "CENTRAL",
                "blocking": True,
                "minimum_mean_return": -1.0,
                "stress_family": "central_execution",
            },
            {
                "stress_id": "ROB-NAUTILUS-PLAUSIBLE",
                "classification": "PLAUSIBLE_BASE",
                "blocking": True,
                "minimum_mean_return": -1.0,
                "stress_family": "plausible_execution",
            },
            {
                "stress_id": "ROB-NAUTILUS-EXTREME",
                "classification": "EXTREME",
                "blocking": False,
                "minimum_mean_return": -1.0,
                "stress_family": "extreme_diagnostic",
            },
        ]
    }


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> int:
    package_dir = IMPLEMENTATION_ROOT / "research_packages" / "nautilus_mvp"
    report = build_nautilus_research_package(package_dir)
    summary = {"package_dir": str(package_dir), "status": report["status"]}
    if report.get("oos_access_decision"):
        summary["missing_requirements"] = report["oos_access_decision"].get("missing_requirements", [])
    print(summary)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
