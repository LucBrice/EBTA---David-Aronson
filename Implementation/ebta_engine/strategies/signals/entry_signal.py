"""Vectorized liquidity-sweep entry signal oracle."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ebta_engine.strategies.signals.engulfing import detect_engulfing_components
from ebta_engine.strategies.signals.liquidity import compute_liquidity_pools, latest_levels


def compute_entry_signals(
    bars_m1: pd.DataFrame,
    bars_m3: pd.DataFrame,
    pools_m15: pd.Series | None = None,
    *,
    expiry_days: int = 3,
    sweep_window_mins: int = 240,
    window_back: int = 10,
    window_fwd: int = 10,
    window_m3: int = 20,
) -> pd.Series:
    """Return +1 BUY, -1 SELL, or 0 on M3 confirmation bars."""
    components = detect_engulfing_components(bars_m1)
    if pools_m15 is None:
        pools_m15 = compute_liquidity_pools(bars_m1, expiry_days=expiry_days, tf_minutes=1)
    bull_levels = latest_levels(pools_m15, "bull").reindex(bars_m1.index, method="ffill")
    bear_levels = latest_levels(pools_m15, "bear").reindex(bars_m1.index, method="ffill")

    signal_bull = _directional_signal(
        bars_m1,
        bars_m3,
        levels=bull_levels,
        engulf_mask=components["engulf_bear"],
        pivots=components["pivot_bear"],
        side=1,
        sweep_window_mins=sweep_window_mins,
        window_back=window_back,
        window_fwd=window_fwd,
        window_m3=window_m3,
    )
    signal_bear = _directional_signal(
        bars_m1,
        bars_m3,
        levels=bear_levels,
        engulf_mask=components["engulf_bull"],
        pivots=components["pivot_bull"],
        side=-1,
        sweep_window_mins=sweep_window_mins,
        window_back=window_back,
        window_fwd=window_fwd,
        window_m3=window_m3,
    )
    conflict = (signal_bull != 0) & (signal_bear != 0)
    if conflict.any():
        raise ValueError(f"Signal BUY+SELL simultane detecte a {conflict[conflict].index.tolist()[:5]}")
    return (signal_bull + signal_bear).astype("int64")


def _directional_signal(
    bars_m1: pd.DataFrame,
    bars_m3: pd.DataFrame,
    *,
    levels: pd.Series,
    engulf_mask: pd.Series,
    pivots: pd.Series,
    side: int,
    sweep_window_mins: int,
    window_back: int,
    window_fwd: int,
    window_m3: int,
) -> pd.Series:
    output = pd.Series(0, index=bars_m3.index, dtype="int64")
    highs = bars_m1["high"].to_numpy()
    lows = bars_m1["low"].to_numpy()
    level_values = levels.to_numpy()
    m1_index = bars_m1.index
    m3_index = bars_m3.index
    m3_close = bars_m3["close"].to_numpy()
    sweep_window = pd.Timedelta(minutes=sweep_window_mins)

    for sweep_index in _sweep_indices(highs, lows, level_values, side):
        engulf = _nearest_engulf(sweep_index, engulf_mask.to_numpy(), pivots.to_numpy(), window_back, window_fwd)
        if engulf is None:
            continue
        pivot, birth_index = engulf
        if m1_index[birth_index] - m1_index[sweep_index] > sweep_window:
            continue
        m3_start = max(0, m3_index.searchsorted(m1_index[birth_index], side="right") - 1)
        m3_end = min(len(m3_index), m3_start + window_m3)
        closes = m3_close[m3_start:m3_end]
        hits = np.where(closes > pivot)[0] if side == 1 else np.where(closes < pivot)[0]
        if len(hits) == 0:
            continue
        confirm_index = m3_start + int(hits[0])
        if confirm_index + 1 < len(output):
            output.iloc[confirm_index + 1] = side
    return output


def _sweep_indices(highs: np.ndarray, lows: np.ndarray, levels: np.ndarray, side: int) -> list[int]:
    indices: list[int] = []
    active = False
    previous_level = np.nan
    best_extreme = np.inf if side == 1 else -np.inf
    for index, level in enumerate(levels):
        if np.isnan(level):
            active = False
            previous_level = np.nan
            continue
        touched = lows[index] <= level if side == 1 else highs[index] >= level
        level_changed = np.isnan(previous_level) or level != previous_level
        extended = (lows[index] < best_extreme) if side == 1 else (highs[index] > best_extreme)
        if touched and (not active or level_changed or extended):
            indices.append(index)
            active = True
            best_extreme = lows[index] if side == 1 else highs[index]
        elif not touched:
            active = False
            best_extreme = np.inf if side == 1 else -np.inf
        previous_level = level
    return indices


def _nearest_engulf(
    sweep_index: int,
    engulf_mask: np.ndarray,
    pivots: np.ndarray,
    window_back: int,
    window_fwd: int,
) -> tuple[float, int] | None:
    start = max(0, sweep_index - window_back)
    end = min(len(engulf_mask) - 1, sweep_index + window_fwd)
    best_index: int | None = None
    best_distance = window_back + window_fwd + 1
    for index in range(start, end + 1):
        if bool(engulf_mask[index]):
            distance = abs(index - sweep_index)
            if distance < best_distance or (distance == best_distance and index < sweep_index):
                best_distance = distance
                best_index = index
    if best_index is None:
        return None
    return float(pivots[best_index]), best_index
