"""Run the Phase 2 Nautilus golden case in the dedicated Nautilus venv."""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import AccountType, OmsType, OrderSide
from nautilus_trader.model.identifiers import InstrumentId, Symbol, Venue
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.trading.strategy import Strategy


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
if str(IMPLEMENTATION_ROOT) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from ebta_engine.strategies.contracts import SimulationResult  # noqa: E402
from ebta_engine.tests.fixtures.nautilus_golden_case.expected_result import (  # noqa: E402
    STARTING_NAV,
    QUANTITY,
    expected_result,
    load_bars,
)


class OneTradeConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType
    trade_size: Decimal


class OneTradeStrategy(Strategy):
    def __init__(self, config: OneTradeConfig):
        super().__init__(config)
        self._bar_count = 0

    def on_start(self) -> None:
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar) -> None:
        self._bar_count += 1
        instrument = self.cache.instrument(self.config.instrument_id)
        if self._bar_count == 1:
            order = self.order_factory.market(
                self.config.instrument_id,
                OrderSide.BUY,
                instrument.make_qty(self.config.trade_size),
            )
            self.submit_order(order)
        elif self._bar_count == 3:
            self.close_all_positions(self.config.instrument_id)


def run_golden_case(candidate_id: str = "CAND-GOLDEN") -> SimulationResult:
    bars_fixture = load_bars()
    instrument = _golden_instrument()
    bar_type = BarType.from_str("GOLDEN.SIM-1-DAY-LAST-EXTERNAL")
    bars = BarDataWrangler(bar_type, instrument).process(_bars_dataframe(bars_fixture))
    engine = BacktestEngine(config=BacktestEngineConfig(logging=LoggingConfig(log_level="ERROR")))
    try:
        engine.add_venue(
            venue=Venue("SIM"),
            oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN,
            starting_balances=[Money(STARTING_NAV, USD)],
            base_currency=USD,
            default_leverage=Decimal(1),
        )
        engine.add_instrument(instrument)
        engine.add_data(bars)
        engine.add_strategy(
            OneTradeStrategy(
                OneTradeConfig(
                    instrument_id=instrument.id,
                    bar_type=bar_type,
                    trade_size=Decimal(str(QUANTITY)),
                )
            )
        )
        engine.run()
        return _extract_result(candidate_id, bars_fixture, engine)
    finally:
        engine.dispose()


def assert_matches_expected(actual: SimulationResult, tolerance: float = 1e-9) -> None:
    expected = expected_result(actual.candidate_id)
    if actual.instrument_id != expected.instrument_id:
        raise AssertionError(f"instrument_id mismatch: {actual.instrument_id} != {expected.instrument_id}")
    for field_name in ["timestamps", "nav", "daily_returns", "daily_exposure"]:
        actual_values = getattr(actual, field_name)
        expected_values = getattr(expected, field_name)
        if len(actual_values) != len(expected_values):
            raise AssertionError(f"{field_name} length mismatch")
        for index, (actual_value, expected_value) in enumerate(zip(actual_values, expected_values)):
            if isinstance(expected_value, float):
                if abs(actual_value - expected_value) > tolerance:
                    raise AssertionError(
                        f"{field_name}[{index}] mismatch: {actual_value} != {expected_value}"
                    )
            elif actual_value != expected_value:
                raise AssertionError(f"{field_name}[{index}] mismatch: {actual_value} != {expected_value}")
    if abs(actual.total_costs - expected.total_costs) > tolerance:
        raise AssertionError(f"total_costs mismatch: {actual.total_costs} != {expected.total_costs}")
    if abs(actual.positions[0]["realized_pnl"] - expected.positions[0]["realized_pnl"]) > tolerance:
        raise AssertionError("realized_pnl mismatch")


def _golden_instrument() -> CurrencyPair:
    return CurrencyPair(
        instrument_id=InstrumentId.from_str("GOLDEN.SIM"),
        raw_symbol=Symbol("GOLDEN"),
        base_currency=USD,
        quote_currency=USD,
        price_precision=2,
        size_precision=0,
        price_increment=Price.from_str("0.01"),
        size_increment=Quantity.from_int(1),
        ts_event=0,
        ts_init=0,
        margin_init=Decimal("0"),
        margin_maint=Decimal("0"),
        maker_fee=Decimal("0"),
        taker_fee=Decimal("0"),
    )


def _bars_dataframe(bars_fixture: list[dict[str, Any]]) -> pd.DataFrame:
    values = np.array(
        [
            [bar["open"], bar["high"], bar["low"], bar["close"], bar["volume"]]
            for bar in bars_fixture
        ],
        dtype="float64",
    ).copy()
    frame = pd.DataFrame(
        values,
        columns=["open", "high", "low", "close", "volume"],
        index=pd.to_datetime([bar["timestamp"] for bar in bars_fixture], utc=True),
    ).copy(deep=True)
    for column in frame.columns:
        frame[column] = frame[column].astype("float64").copy()
    return frame


def _extract_result(candidate_id: str, bars_fixture: list[dict[str, Any]], engine: BacktestEngine) -> SimulationResult:
    fills = engine.trader.generate_order_fills_report()
    positions = engine.trader.generate_positions_report()
    if len(fills) != 2:
        raise AssertionError(f"expected 2 fills, got {len(fills)}")
    if len(positions) != 1:
        raise AssertionError(f"expected 1 position, got {len(positions)}")

    entry_fill = fills.iloc[0]
    exit_fill = fills.iloc[-1]
    entry_price = float(entry_fill["avg_px"])
    exit_price = float(exit_fill["avg_px"])
    timestamps: list[str] = []
    nav: list[float] = []
    daily_returns: list[float] = []
    daily_exposure: list[float] = []
    previous_nav = STARTING_NAV
    for index, bar in enumerate(bars_fixture):
        mark_price = float(bar["close"])
        current_nav = STARTING_NAV + (mark_price - entry_price) * QUANTITY
        timestamps.append(str(bar["timestamp"]))
        nav.append(current_nav)
        daily_returns.append((current_nav - previous_nav) / previous_nav)
        daily_exposure.append(0.0 if index == len(bars_fixture) - 1 else (mark_price * QUANTITY) / current_nav)
        previous_nav = current_nav

    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id="GOLDEN.SIM",
        timestamps=timestamps,
        daily_returns=daily_returns,
        daily_exposure=daily_exposure,
        nav=nav,
        total_costs=0.0,
        orders=[
            {
                "side": str(entry_fill["side"]),
                "quantity": float(entry_fill["quantity"]),
                "price": entry_price,
                "timestamp": str(entry_fill["ts_init"]),
            },
            {
                "side": str(exit_fill["side"]),
                "quantity": float(exit_fill["quantity"]),
                "price": exit_price,
                "timestamp": str(exit_fill["ts_init"]),
            },
        ],
        fills=[
            {
                "side": str(entry_fill["side"]),
                "quantity": float(entry_fill["filled_qty"]),
                "price": entry_price,
                "timestamp": str(entry_fill["ts_last"]),
            },
            {
                "side": str(exit_fill["side"]),
                "quantity": float(exit_fill["filled_qty"]),
                "price": exit_price,
                "timestamp": str(exit_fill["ts_last"]),
            },
        ],
        positions=[
            {
                "quantity": QUANTITY,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "realized_pnl": float(str(positions.iloc[0]["realized_pnl"]).split()[0]),
            }
        ],
        metadata={
            "fixture": "nautilus_golden_case",
            "source": "nautilus_trader",
            "total_orders": int(engine.get_result().total_orders),
            "total_positions": int(engine.get_result().total_positions),
        },
    )


def main() -> int:
    result = run_golden_case()
    assert_matches_expected(result)
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
