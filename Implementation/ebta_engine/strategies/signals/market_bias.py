"""Vectorized higher-timeframe market bias oracle."""

from __future__ import annotations

import pandas as pd


def compute_market_bias(df: pd.DataFrame, tf_minutes: int) -> pd.Series:
    """Return -1, 0, or 1 bias using only closed previous HTF candles."""
    if tf_minutes <= 0:
        raise ValueError("tf_minutes must be positive")
    missing = {"open", "high", "low", "close"} - set(df.columns)
    if missing:
        raise ValueError(f"OHLC columns missing: {sorted(missing)}")

    high = df["high"]
    low = df["low"]
    open_ = df["open"]
    close = df["close"]
    high_1 = high.shift(1)
    high_2 = high.shift(2)
    low_1 = low.shift(1)
    low_2 = low.shift(2)
    open_2 = open_.shift(2)
    close_1 = close.shift(1)
    close_2 = close.shift(2)
    body_high_2 = pd.concat([open_2, close_2], axis=1).max(axis=1)
    body_low_2 = pd.concat([open_2, close_2], axis=1).min(axis=1)

    engulf = (high_1 > high_2) & (low_1 < low_2)
    engulf_bull = engulf & (close_1 > body_high_2)
    engulf_bear = engulf & (close_1 < body_low_2)
    engulf_neutral = engulf & (close_1 >= body_low_2) & (close_1 <= body_high_2)

    bullish_1 = (high_1 > high_2) & (close_1 > high_2)
    bullish_2 = (low_1 < low_2) & (close_1 > low_2)
    bearish_1 = (low_1 < low_2) & (close_1 < low_2)
    bearish_2 = (high_1 > high_2) & (close_1 < high_2)

    bias = pd.Series(0, index=df.index, dtype="int64")
    bias[engulf_bull | ((bullish_1 | bullish_2) & ~engulf)] = 1
    bias[engulf_bear | ((bearish_1 | bearish_2) & ~engulf)] = -1
    bias[engulf_neutral] = 0
    return bias.fillna(0).astype("int64")


def align_mtf_filter(target: pd.DataFrame, h1: pd.DataFrame, h4: pd.DataFrame, d1: pd.DataFrame) -> pd.Series:
    """Align H1/H4/D1 bias to target bars and authorize agreeing HTF pairs."""
    b_h1 = _aligned_bias(target, h1, 60)
    b_h4 = _aligned_bias(target, h4, 240)
    b_d1 = _aligned_bias(target, d1, 1440)
    auth = pd.Series(0, index=target.index, dtype="int64")
    h1_h4 = (b_h1 == b_h4) & (b_h4 != 0)
    h4_d1 = (b_h4 == b_d1) & (b_d1 != 0)
    auth[h1_h4 | h4_d1] = b_h4[h1_h4 | h4_d1]
    return auth


def _aligned_bias(target: pd.DataFrame, source: pd.DataFrame, tf_minutes: int) -> pd.Series:
    if source is None or source.empty:
        return pd.Series(0, index=target.index, dtype="int64")
    return compute_market_bias(source, tf_minutes).reindex(target.index, method="ffill").fillna(0).astype("int64")
