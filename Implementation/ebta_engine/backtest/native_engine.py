"""Deterministic native backtest for the EBTA MVP."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.features.causal_signals import build_signal_decisions
from ebta_engine.risk.sizing import unit_notional_size
from ebta_engine.strategies.payloads import StrategyPayload


@dataclass(frozen=True)
class BacktestResult:
    candidate_key: str
    returns: list[float]
    nav: list[float]
    orders: list[dict]
    fills: list[dict]
    positions: list[dict]


def run_native_backtest(payload: StrategyPayload, bars: list[OhlcvBar], *, max_observations: int = 4) -> BacktestResult:
    decisions = build_signal_decisions(payload, bars)
    returns: list[float] = []
    nav = [100_000.0]
    orders: list[dict] = []
    fills: list[dict] = []
    positions: list[dict] = []
    notional = unit_notional_size()
    for index, decision in enumerate(decisions[:max_observations]):
        entry_bar = bars[index + 3]
        exit_bar = bars[index + 4]
        raw_return = math.log(exit_bar.close / entry_bar.close)
        signal_return = decision.signal * raw_return
        cost = 0.00001 if decision.signal else 0.0
        net_return = signal_return - cost
        returns.append(round(net_return, 10))
        nav.append(round(nav[-1] * (1.0 + net_return), 6))
        if decision.signal:
            order_id = f"ORDER-{payload.asset}-{payload.payload_code}-{index + 1:03d}"
            fill_id = f"FILL-{payload.asset}-{payload.payload_code}-{index + 1:03d}"
            orders.append({"order_id": order_id, "status": "FILLED", "signal_id": decision.timestamp})
            fills.append({"fill_id": fill_id, "order_id": order_id, "price": exit_bar.close, "notional": notional})
            positions.append({"timestamp": decision.timestamp, "direction": decision.signal, "notional": notional})
    if not returns:
        raise ValueError("native backtest produced no returns")
    return BacktestResult(
        candidate_key=f"{payload.asset}:{payload.payload_code}",
        returns=returns,
        nav=nav,
        orders=orders,
        fills=fills,
        positions=positions,
    )
