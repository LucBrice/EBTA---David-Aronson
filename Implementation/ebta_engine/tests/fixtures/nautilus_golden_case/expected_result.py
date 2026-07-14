"""Stdlib-only expected result for the deterministic Nautilus golden case."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ebta_engine.strategies.contracts import CostModel, InstrumentConfig, SimulationResult


FIXTURE_DIR = Path(__file__).resolve().parent
STARTING_NAV = 1000.0
QUANTITY = 1.0


def load_bars() -> list[dict[str, Any]]:
    with (FIXTURE_DIR / "bars.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def deterministic_cost_model() -> CostModel:
    return CostModel(
        model_id="NAUTILUS-GOLDEN-DETERMINISTIC",
        fill_model="guaranteed_bar_open_close",
        fee_model="zero_fee",
        commission_per_lot=0.0,
        slippage_bps=0.0,
        financing_rate_daily=0.0,
        impact_model="none",
        latency_nanos=0,
        prob_fill_on_limit=1.0,
        prob_slippage=0.0,
    )


def deterministic_instrument_config() -> InstrumentConfig:
    return InstrumentConfig(
        instrument_id="GOLDEN.SIM",
        symbol="GOLDEN",
        venue="SIM",
        price_precision=2,
        size_precision=0,
        price_increment="0.01",
        size_increment="1",
        margin_init="0",
        margin_maint="0",
        maker_fee="0",
        taker_fee="0",
    )


def expected_result(candidate_id: str = "CAND-GOLDEN") -> SimulationResult:
    bars = load_bars()

    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=deterministic_instrument_config().instrument_id,
        timestamps=[str(bar["timestamp"]) for bar in bars],
        daily_returns=[0.0 for _ in bars],
        daily_exposure=[0.0 for _ in bars],
        nav=[STARTING_NAV for _ in bars],
        total_costs=0.0,
        orders=[],
        fills=[],
        positions=[],
        metadata={
            "fixture": "nautilus_golden_case",
            "calculation": "r2_recalibrated_no_m1_signal_expected_result",
            "no_m1_signal": True,
        },
    )
