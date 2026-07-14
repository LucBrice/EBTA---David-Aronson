"""Incremental payload E liquidity-sweep strategy."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.registry import register_strategy
from ebta_engine.strategies.signals.entry_signal import compute_entry_signals


@dataclass(frozen=True)
class IncrementalDecision:
    timestamp: datetime
    side: str


class PayloadEStrategy:
    """Bar-by-bar state machine for payload E.

    The implementation updates from the prefix observed so far only. The
    vectorized oracle is used on that prefix as a mechanical parity reference,
    never as a production precomputed decision series.
    """

    payload_code = "E"

    def __init__(self, payload: dict[str, Any] | None = None, *, warmup_bar_count: int = 0) -> None:
        self.payload = payload or {}
        self.warmup_bar_count = warmup_bar_count
        self._bar_count = 0
        self._bars_m1: list[OhlcvBar] = []
        self._pending_side: str | None = None
        self._emitted_signal_times: set[datetime] = set()
        self.decisions: list[IncrementalDecision] = []

    def on_bar(self, bar: Any) -> None:
        timeframe = timeframe_from_bar(bar)
        if timeframe != "M1":
            return
        self._bar_count += 1
        self._bars_m1.append(ohlcv_from_bar(bar))
        if self._bar_count <= self.warmup_bar_count:
            return
        self._update_pending_signal()

    def should_enter(self) -> tuple[bool, str | None]:
        if self._pending_side is None:
            return False, None
        side = self._pending_side
        self._pending_side = None
        return True, side

    def should_exit(self, bar_count_since_entry: int) -> bool:
        return bar_count_since_entry >= _horizon_bars(self.payload)

    def _update_pending_signal(self) -> None:
        if len(self._bars_m1) < 3:
            return
        frame_m1 = frame_from_bars(self._bars_m1)
        bars_m3 = resample_ohlcv(self._bars_m1, 3)
        if len(bars_m3) < 2:
            return
        frame_m3 = frame_from_bars(bars_m3)
        signal = self._signal(frame_m1, frame_m3)
        non_zero = signal[signal != 0]
        if non_zero.empty:
            return
        timestamp = _to_datetime(non_zero.index[-1])
        if timestamp in self._emitted_signal_times:
            return
        side = "BUY" if int(non_zero.iloc[-1]) > 0 else "SELL"
        self._emitted_signal_times.add(timestamp)
        self.decisions.append(IncrementalDecision(timestamp=timestamp, side=side))
        self._pending_side = side

    def _signal(self, frame_m1: pd.DataFrame, frame_m3: pd.DataFrame) -> pd.Series:
        return compute_entry_signals(frame_m1, frame_m3, **_signal_parameters(self.payload))


def frame_from_bars(bars: list[OhlcvBar]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [bar.open for bar in bars],
            "high": [bar.high for bar in bars],
            "low": [bar.low for bar in bars],
            "close": [bar.close for bar in bars],
            "volume": [bar.volume for bar in bars],
        },
        index=pd.DatetimeIndex([bar.timestamp for bar in bars]).tz_convert("UTC"),
    )


def ohlcv_from_bar(bar: Any) -> OhlcvBar:
    if isinstance(bar, OhlcvBar):
        return bar
    timestamp = getattr(bar, "timestamp", None)
    if timestamp is None and hasattr(bar, "ts_event"):
        timestamp = datetime.fromtimestamp(int(bar.ts_event) / 1_000_000_000, timezone.utc)
    if timestamp is None:
        raise ValueError("bar must expose timestamp or ts_event")
    return OhlcvBar(
        asset=str(getattr(bar, "asset", "NAUTILUS")),
        timestamp=_to_datetime(timestamp),
        open=_bar_float(bar.open),
        high=_bar_float(bar.high),
        low=_bar_float(bar.low),
        close=_bar_float(bar.close),
        volume=_bar_float(getattr(bar, "volume", 0.0)),
    )


def timeframe_from_bar(bar: Any) -> str:
    explicit = getattr(bar, "timeframe", None)
    if explicit:
        return str(explicit).upper()
    bar_type = str(getattr(bar, "bar_type", ""))
    if "-3-MINUTE-" in bar_type:
        return "M3"
    if "-15-MINUTE-" in bar_type:
        return "M15"
    if "-1-HOUR-" in bar_type:
        return "H1"
    if "-4-HOUR-" in bar_type:
        return "H4"
    if "-1-DAY-" in bar_type:
        return "D1"
    return "M1"


def _signal_parameters(payload: dict[str, Any]) -> dict[str, Any]:
    parameters = dict(payload.get("parameters", {}))
    return {
        "expiry_days": int(parameters.get("expiry_days", 3)),
        "sweep_window_mins": int(parameters.get("sweep_window_mins", 240)),
        "window_back": int(parameters.get("window_back", 10)),
        "window_fwd": int(parameters.get("window_fwd", 10)),
        "window_m3": int(parameters.get("window_m3", 20)),
    }


def _horizon_bars(payload: dict[str, Any]) -> int:
    exit_criterion = payload.get("exit_criterion", {})
    if isinstance(exit_criterion, dict):
        return max(1, int(exit_criterion.get("parameters", {}).get("horizon_bars", 1)))
    return max(1, int(payload.get("parameters", {}).get("horizon_bars", 1)))


def _bar_float(value: Any) -> float:
    return float(str(value))


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime().astimezone(timezone.utc)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError(f"timestamp is not timezone-aware: {value!r}")
        return value.astimezone(timezone.utc)
    return pd.Timestamp(value).to_pydatetime().astimezone(timezone.utc)


register_strategy("E", PayloadEStrategy)

