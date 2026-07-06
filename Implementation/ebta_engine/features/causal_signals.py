"""Small causal signal generator for the native EBTA MVP."""

from __future__ import annotations

from dataclasses import dataclass

from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.strategies.payloads import StrategyPayload


@dataclass(frozen=True)
class SignalDecision:
    timestamp: str
    signal: int
    close: float
    reason: str


def build_signal_decisions(payload: StrategyPayload, bars: list[OhlcvBar], *, warmup_bars: int = 3) -> list[SignalDecision]:
    if len(bars) <= warmup_bars + 1:
        raise ValueError("not enough bars to build causal signal decisions")
    decisions: list[SignalDecision] = []
    session_stride = {"all": 1, "asia": 2, "london": 3, "us": 4}[payload.session]
    for index in range(warmup_bars, len(bars) - 1):
        history = bars[index - warmup_bars:index]
        current = bars[index]
        moving_average = sum(bar.close for bar in history) / warmup_bars
        raw_signal = 1 if current.close >= moving_average else -1
        if payload.bias_filter != "none" and history[-1].close < history[0].close:
            raw_signal *= -1
        if index % session_stride != 0:
            raw_signal = 0
        decisions.append(
            SignalDecision(
                timestamp=current.timestamp.isoformat().replace("+00:00", "Z"),
                signal=raw_signal,
                close=current.close,
                reason="causal_ma_bias_session_filter",
            )
        )
    return decisions
