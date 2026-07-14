"""Stacked liquidity pool oracle."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from ebta_engine.strategies.signals.engulfing import detect_engulfing_components


def compute_liquidity_pools(df: pd.DataFrame, expiry_days: int, tf_minutes: int = 15) -> pd.Series:
    """Return active liquidity pools known at each bar open.

    Pool entries are dictionaries with ``side`` ("bull" or "bear"), ``price``,
    and ``expires_at`` integer bar index.
    """
    if expiry_days <= 0:
        raise ValueError("expiry_days must be positive")
    if tf_minutes <= 0:
        raise ValueError("tf_minutes must be positive")
    components = detect_engulfing_components(df)
    expiry_bars = int((expiry_days * 24 * 60) / tf_minutes)
    bull_sources = components["pivot_bull"]
    bear_sources = components["pivot_bear"]
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()

    pool: list[dict] = []
    history: list[list[dict]] = []
    for index in range(len(df)):
        history.append([dict(item) for item in pool])
        pool = [
            item
            for item in pool
            if index <= item["expires_at"]
            and ((item["side"] == "bull" and low[index] > item["price"]) or (item["side"] == "bear" and high[index] < item["price"]))
        ]
        bull_price = bull_sources.iloc[index]
        if not math.isnan(float(bull_price)):
            pool.append({"side": "bull", "price": float(bull_price), "expires_at": index + expiry_bars})
        bear_price = bear_sources.iloc[index]
        if not math.isnan(float(bear_price)):
            pool.append({"side": "bear", "price": float(bear_price), "expires_at": index + expiry_bars})

    return pd.Series(history, index=df.index, dtype=object)


def latest_levels(pools: pd.Series, side: str) -> pd.Series:
    """Extract the most conservative active level for one side."""
    if side not in {"bull", "bear"}:
        raise ValueError("side must be 'bull' or 'bear'")

    def _level(items: list[dict]) -> float:
        prices = [float(item["price"]) for item in items if item.get("side") == side]
        if not prices:
            return np.nan
        return max(prices) if side == "bull" else min(prices)

    return pools.map(_level)
