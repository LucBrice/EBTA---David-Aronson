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
    entry_price = float(bars[0]["close"])
    exit_price = float(bars[-1]["close"])
    timestamps: list[str] = []
    nav: list[float] = []
    daily_returns: list[float] = []
    daily_exposure: list[float] = []
    previous_nav = STARTING_NAV

    for index, bar in enumerate(bars):
        mark_price = float(bar["close"])
        current_nav = STARTING_NAV + (mark_price - entry_price) * QUANTITY
        timestamps.append(str(bar["timestamp"]))
        nav.append(current_nav)
        daily_returns.append((current_nav - previous_nav) / previous_nav)
        daily_exposure.append(0.0 if index == len(bars) - 1 else (mark_price * QUANTITY) / current_nav)
        previous_nav = current_nav

    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=deterministic_instrument_config().instrument_id,
        timestamps=timestamps,
        daily_returns=daily_returns,
        daily_exposure=daily_exposure,
        nav=nav,
        total_costs=0.0,
        orders=[
            {
                "side": "BUY",
                "quantity": QUANTITY,
                "price": entry_price,
                "timestamp": bars[0]["timestamp"],
            },
            {
                "side": "SELL",
                "quantity": QUANTITY,
                "price": exit_price,
                "timestamp": bars[-1]["timestamp"],
            },
        ],
        fills=[
            {
                "side": "BUY",
                "quantity": QUANTITY,
                "price": entry_price,
                "timestamp": bars[0]["timestamp"],
            },
            {
                "side": "SELL",
                "quantity": QUANTITY,
                "price": exit_price,
                "timestamp": bars[-1]["timestamp"],
            },
        ],
        positions=[
            {
                "quantity": QUANTITY,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "realized_pnl": (exit_price - entry_price) * QUANTITY,
            }
        ],
        metadata={
            "fixture": "nautilus_golden_case",
            "calculation": "stdlib_independent_expected_result",
        },
    )
