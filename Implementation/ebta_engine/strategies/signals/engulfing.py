"""Vectorized engulfing pattern detection.

Source: read-only BACKTRADER/features/core.py, ported for EBTA parity tests.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def detect_engulfing(df: pd.DataFrame) -> pd.Series:
    """Return True where either a bullish or bearish engulfing pattern closes."""
    components = detect_engulfing_components(df)
    return components["engulf_bull"] | components["engulf_bear"]


def detect_engulfing_components(df: pd.DataFrame) -> dict[str, pd.Series]:
    _require_ohlc(df)
    high = df["high"]
    low = df["low"]
    open_ = df["open"]
    close = df["close"]
    body_high = pd.concat([open_, close], axis=1).max(axis=1)
    body_low = pd.concat([open_, close], axis=1).min(axis=1)

    bull_2 = (low < low.shift(1)) & (close > body_high.shift(1))
    bull_3 = (low.shift(1) < low.shift(2)) & (close.shift(1) <= body_high.shift(2)) & (
        close > body_high.shift(1)
    )
    bear_2 = (high > high.shift(1)) & (close < body_low.shift(1))
    bear_3 = (high.shift(1) > high.shift(2)) & (close.shift(1) >= body_low.shift(2)) & (
        close < body_low.shift(1)
    )

    pivot_bull_2 = pd.concat([low, low.shift(1)], axis=1).min(axis=1)
    pivot_bull_3 = pd.concat([low, low.shift(1), low.shift(2)], axis=1).min(axis=1)
    pivot_bear_2 = pd.concat([high, high.shift(1)], axis=1).max(axis=1)
    pivot_bear_3 = pd.concat([high, high.shift(1), high.shift(2)], axis=1).max(axis=1)

    return {
        "engulf_bull": (bull_2 | bull_3).fillna(False).astype(bool),
        "engulf_bear": (bear_2 | bear_3).fillna(False).astype(bool),
        "pivot_bull": pivot_bull_2.where(bull_2, pivot_bull_3.where(bull_3, np.nan)),
        "pivot_bear": pivot_bear_2.where(bear_2, pivot_bear_3.where(bear_3, np.nan)),
    }


def _require_ohlc(df: pd.DataFrame) -> None:
    missing = {"open", "high", "low", "close"} - set(df.columns)
    if missing:
        raise ValueError(f"OHLC columns missing: {sorted(missing)}")
