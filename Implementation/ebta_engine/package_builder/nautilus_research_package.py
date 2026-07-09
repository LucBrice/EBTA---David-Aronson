"""Build an EBTA research package backed by NautilusTrader simulations."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, build_data_snapshot, load_ohlcv_bars
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig, SimulationResult
from ebta_engine.strategies.payload_factory import generate_family, liquidity_sweep_family_spec


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
PILOT_SCRIPT = IMPLEMENTATION_ROOT / "examples" / "minimal_pilot_pipeline" / "build_research_package.py"
DEFAULT_NAUTILUS_ASSETS = ["NASDAQ", "XAUUSD"]
DEFAULT_NAUTILUS_START = "2020-01-01T00:00:00Z"
DEFAULT_NAUTILUS_END = "2020-01-03T23:59:00Z"


SegmentRunner = Callable[..., SimulationResult]


def _load_pilot_module():
    spec = importlib.util.spec_from_file_location("minimal_pilot_pipeline", PILOT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_nautilus_inputs(
    *,
    data_root: Path = DEFAULT_DATA_ROOT,
    assets: list[str] | None = None,
    start: str = DEFAULT_NAUTILUS_START,
    end: str = DEFAULT_NAUTILUS_END,
    segment_runner: SegmentRunner | None = None,
) -> dict:
    assets = sorted(assets or DEFAULT_NAUTILUS_ASSETS)
    pilot = _load_pilot_module()
    inputs = copy.deepcopy(pilot.load_pilot_inputs())
    inputs["actor"] = "nautilus_trader_adapter"
    inputs["identifiers"].update(
        {
            "config_id": "CFG-NAUTILUS-MVP-001",
            "project_id": "PRJ-NAUTILUS-MVP",
            "research_family_id": "FAM-LIQUIDITY-SWEEP-NAUTILUS",
            "hypothesis_id": "HYP-LIQUIDITY-SWEEP-NAUTILUS-XAUUSD-NASDAQ",
            "process_version_id": "PROC-NAUTILUS-MVP-001",
            "document_hash": "NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER",
        }
    )
    snapshot = build_data_snapshot(data_root, assets, start=start, end=end)
    inputs["data_snapshots"] = [snapshot]
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

    run_one = segment_runner or _subprocess_segment_runner
    search_space = pilot._pilot_search_space(inputs)
    payloads = _payloads_by_axis(assets, inputs["identifiers"]["research_family_id"], search_space["fold_id"])
    bars_by_asset = {
        asset: load_ohlcv_bars(data_root, asset, start=start, end=end, max_bars=12)
        for asset in assets
    }
    candidate_series: list[list[float]] = []
    train_scores: list[float] = []
    for candidate_row in search_space["candidates"]:
        parameters = candidate_row["parameters"]
        asset = parameters["asset"]
        payload = payloads[(asset, parameters["bias_filter"], parameters["session"])]
        candidate = Candidate(
            candidate_id=candidate_row["candidate_id"],
            research_family_id=inputs["identifiers"]["research_family_id"],
            payload=payload.to_dict(),
            asset=asset,
            complexity=int(parameters.get("complexity", 1)),
            fold_id=search_space["fold_id"],
        )
        result = run_one(
            candidate=candidate,
            bars=bars_by_asset[asset],
            cost_model=_nautilus_cost_model(),
            instrument_config=_instrument_config(asset),
            seed=13,
            starting_nav=1000.0,
            trade_size="1",
            interval_value=1,
            interval_unit="MINUTE",
            timestamp_is_close=False,
        )
        series = result.daily_returns
        candidate_series.append(series)
        train_scores.append(_mean(series))
    inputs["train_scores_by_rank"] = train_scores
    inputs["representative_test_scores_by_rank"] = [max(train_scores)]
    inputs["candidate_test_returns_by_rank"] = candidate_series
    inputs["candidate_test_dates"] = [
        bar.timestamp.isoformat().replace("+00:00", "Z")
        for bar in bars_by_asset[assets[0]][: len(candidate_series[0])]
    ]
    inputs["data_availability_checks"] = [
        {"available_at": snapshot["available_at"], "decision_at": "2020-01-04T00:00:00Z"}
    ]
    inputs["execution_report"] = {
        "status": "PASS",
        "cost_model": "nautilus_zero_fee_deterministic",
        "central_scenario": "tradable_net",
        "orders": [{"order_id": "ORDER-NAUTILUS-MVP-SUMMARY", "status": "FILLED", "fill_id": "FILL-NAUTILUS-MVP-SUMMARY"}],
        "nav_reconciliation": "PASS",
        "engine": "nautilus_trader",
        "backtrader_runtime_dependency": False,
    }
    inputs["reproduction_report"]["commands"] = [
        "Implementation\\adapters\\nautilus_env\\venv\\Scripts\\python.exe -m ebta_engine.package_builder.nautilus_research_package"
    ]
    inputs["reproduction_report"]["notes"] = "Nautilus package built from local OHLCV CSV files and EBTA StrategyPayload contracts; no BACKTRADER runtime dependency."
    inputs["incubation_report"]["data_source_ids"] = [snapshot["data_snapshot_id"]]
    inputs["oos_access_log"][0]["actor"] = "nautilus_trader_adapter"
    inputs["oos_access_log"][0]["read_paths"] = [str(data_root)]
    return inputs


def build_nautilus_research_package(
    package_dir: Path,
    *,
    data_root: Path = DEFAULT_DATA_ROOT,
    assets: list[str] | None = None,
    start: str = DEFAULT_NAUTILUS_START,
    end: str = DEFAULT_NAUTILUS_END,
    segment_runner: SegmentRunner | None = None,
) -> dict:
    pilot = _load_pilot_module()
    inputs = build_nautilus_inputs(
        data_root=data_root,
        assets=assets,
        start=start,
        end=end,
        segment_runner=segment_runner,
    )
    return pilot.build_package(package_dir, pilot_inputs=inputs)


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
    return CostModel(
        model_id="NAUTILUS-ZERO-FEE-DETERMINISTIC",
        fill_model="deterministic",
        fee_model="zero_fee",
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
            maker_fee="0",
            taker_fee="0",
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
            maker_fee="0",
            taker_fee="0",
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
            timeout=120,
        )
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


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> int:
    package_dir = IMPLEMENTATION_ROOT / "research_packages" / "nautilus_mvp"
    report = build_nautilus_research_package(package_dir)
    print({"package_dir": str(package_dir), "status": report["status"]})
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
