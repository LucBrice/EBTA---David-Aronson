"""DST-aware session filters for signal oracles."""

from __future__ import annotations

from typing import TypedDict

import pandas as pd


class _SessionWindow(TypedDict):
    tz: str
    open: float
    close: float


_SESSION_CONFIG: dict[str, _SessionWindow] = {
    "asia": {"tz": "Asia/Tokyo", "open": 9.0, "close": 18.0},
    "london": {"tz": "Europe/London", "open": 8.0, "close": 17.0},
    "us": {"tz": "America/New_York", "open": 9.5, "close": 16.0},
}


def filter_session(df: pd.DataFrame, session: str, tz: str | None = None) -> pd.Series:
    """Return a boolean mask selecting bars inside a named local session."""
    if session == "all":
        return pd.Series(True, index=df.index)
    if session not in _SESSION_CONFIG:
        raise ValueError(f"unknown session: {session!r}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("df must be indexed by a DatetimeIndex")
    index = df.index
    if index.tz is None:
        index = index.tz_localize(tz or "UTC")
    else:
        index = index.tz_convert(tz or "UTC")
    config = _SESSION_CONFIG[session]
    local = index.tz_convert(config["tz"])
    local_hour = local.hour + local.minute / 60.0
    return pd.Series((local_hour >= config["open"]) & (local_hour < config["close"]), index=df.index)
