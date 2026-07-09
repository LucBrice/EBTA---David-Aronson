"""Generic Nautilus strategy bridge for EBTA strategy payloads."""

from __future__ import annotations

from decimal import Decimal

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.trading.strategy import Strategy

from ebta_engine.strategies.payloads import StrategyPayload


class GenericPayloadStrategyConfig(StrategyConfig, frozen=True):
    payload: dict
    instrument_id: InstrumentId
    bar_type: BarType
    trade_size: Decimal


class GenericPayloadStrategy(Strategy):
    """Single Nautilus Strategy class parameterized only by StrategyConfig."""

    def __init__(self, config: GenericPayloadStrategyConfig) -> None:
        super().__init__(config)
        self._payload = StrategyPayload.from_dict(config.payload)
        self._bar_count = 0
        self._entry_bar: int | None = None
        self._entry_rule_id = _rule_id(self._payload.entry_criterion)
        self._exit_horizon_bars = _horizon_bars(self._payload.exit_criterion)

    @property
    def payload_code(self) -> str:
        return self._payload.payload_code

    @property
    def session(self) -> str:
        return self._payload.session

    def on_start(self) -> None:
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar) -> None:
        self._bar_count += 1
        instrument = self.cache.instrument(self.config.instrument_id)
        if self._entry_bar is None and self._entry_rule_id:
            order = self.order_factory.market(
                self.config.instrument_id,
                OrderSide.BUY,
                instrument.make_qty(self.config.trade_size),
            )
            self.submit_order(order)
            self._entry_bar = self._bar_count
            return
        if self._entry_bar is not None and self._bar_count - self._entry_bar >= self._exit_horizon_bars:
            self.close_all_positions(self.config.instrument_id)


def _rule_id(criterion: str | dict) -> str:
    if isinstance(criterion, dict):
        return str(criterion.get("rule_id", ""))
    return criterion


def _horizon_bars(criterion: str | dict) -> int:
    if isinstance(criterion, dict):
        parameters = criterion.get("parameters", {})
        value = int(parameters.get("horizon_bars", 1))
    else:
        value = 1
    return max(1, value)
