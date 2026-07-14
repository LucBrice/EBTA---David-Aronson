"""Generic Nautilus strategy bridge for EBTA strategy payloads."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.trading.strategy import Strategy

from ebta_engine.strategies import incremental  # noqa: F401 - imports register strategies
from ebta_engine.strategies.payloads import StrategyPayload
from ebta_engine.strategies.registry import get_strategy


class GenericPayloadStrategyConfig(StrategyConfig, frozen=True):
    payload: dict
    instrument_id: InstrumentId
    bar_types: list[str]
    trade_size: Decimal
    warmup_bar_count: int = 0


class GenericPayloadStrategy(Strategy):
    """Single Nautilus Strategy class parameterized only by StrategyConfig."""

    def __init__(self, config: GenericPayloadStrategyConfig) -> None:
        super().__init__(config)
        self._payload = StrategyPayload.from_dict(config.payload)
        strategy_cls = get_strategy(_registry_code(self._payload))
        self._signal_strategy = strategy_cls(dict(config.payload), warmup_bar_count=config.warmup_bar_count)
        self._m1_bar_count = 0
        self._seen_bar_count = 0
        self._entry_bar: int | None = None
        self._exit_horizon_bars = _horizon_bars(self._payload.exit_criterion)
        self._venue = config.instrument_id.venue
        self._nav_snapshots: list[tuple[int, float, float]] = []
        self._metadata: dict[str, Any] = {}
        self._warned_no_m1 = False

    @property
    def payload_code(self) -> str:
        return self._payload.payload_code

    @property
    def session(self) -> str:
        return self._payload.session

    def on_start(self) -> None:
        for bar_type in self.config.bar_types:
            self.subscribe_bars(BarType.from_str(bar_type))

    def on_bar(self, bar: Bar) -> None:
        self._seen_bar_count += 1
        is_m1 = _is_m1_bar(bar)
        if is_m1:
            self._m1_bar_count += 1
            self._record_nav_snapshot(bar)
        elif self._seen_bar_count > self.config.warmup_bar_count and not self._warned_no_m1:
            logging.warning("[EBTA] No M1 bar received after warm-up — strategy is in NO_SIGNAL mode")
            self._metadata["no_m1_signal"] = True
            self._warned_no_m1 = True

        self._signal_strategy.on_bar(bar)
        instrument = self.cache.instrument(self.config.instrument_id)
        should_enter, side = self._signal_strategy.should_enter()
        if self._entry_bar is None and should_enter:
            order = self.order_factory.market(
                self.config.instrument_id,
                _to_order_side(side),
                instrument.make_qty(self.config.trade_size),
            )
            self.submit_order(order)
            self._entry_bar = self._m1_bar_count
            return
        if self._entry_bar is not None and self._signal_strategy.should_exit(self._m1_bar_count - self._entry_bar):
            self.close_all_positions(self.config.instrument_id)

    def _record_nav_snapshot(self, bar: Bar) -> None:
        equity = _call_float(self.portfolio, "equity", self._venue)
        exposure = _call_float(self.portfolio, "net_exposure", self.config.instrument_id)
        self._nav_snapshots.append((int(bar.ts_event), equity, exposure))


def _horizon_bars(criterion: str | dict) -> int:
    if isinstance(criterion, dict):
        parameters = criterion.get("parameters", {})
        value = int(parameters.get("horizon_bars", 1))
    else:
        value = 1
    return max(1, value)


def _registry_code(payload: StrategyPayload) -> str:
    if payload.payload_code in {"E", "F", "G", "H", "I"}:
        return payload.payload_code
    session = payload.session.lower()
    if session == "asia":
        return "G"
    if session == "london":
        return "H"
    if session == "us":
        return "I"
    if payload.bias_filter != "none":
        return "F"
    return "E"


def _is_m1_bar(bar: Bar) -> bool:
    return "-1-MINUTE-" in str(bar.bar_type)


def _to_order_side(side: Any) -> OrderSide:
    buy = getattr(OrderSide, "BUY")
    sell = getattr(OrderSide, "SELL")
    if side == buy or str(side).upper() == "BUY":
        return buy
    if side == sell or str(side).upper() == "SELL":
        return sell
    raise ValueError(f"unsupported order side: {side!r}")


def _call_float(obj: Any, name: str, argument: Any) -> float:
    value = getattr(obj, name, None)
    try:
        result = value(argument) if callable(value) else value
    except Exception:
        return 0.0
    try:
        return float(str(result).split()[0])
    except Exception:
        return 0.0
