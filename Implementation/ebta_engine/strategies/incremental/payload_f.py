"""Incremental payload F strategy with MTF bias filtering."""

from __future__ import annotations

import pandas as pd

from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.incremental.payload_e import PayloadEStrategy, frame_from_bars
from ebta_engine.strategies.registry import register_strategy
from ebta_engine.strategies.signals.market_bias import align_mtf_filter


class PayloadFStrategy(PayloadEStrategy):
    payload_code = "F"

    def _signal(self, frame_m1: pd.DataFrame, frame_m3: pd.DataFrame) -> pd.Series:
        signal = super()._signal(frame_m1, frame_m3)
        return apply_mtf_bias_filter(signal, self._bars_m1, frame_m3)


def apply_mtf_bias_filter(signal: pd.Series, bars_m1: list, frame_m3: pd.DataFrame) -> pd.Series:
    h1 = frame_from_bars(resample_ohlcv(bars_m1, 60))
    h4 = frame_from_bars(resample_ohlcv(bars_m1, 240))
    d1 = frame_from_bars(resample_ohlcv(bars_m1, 1440))
    bias = align_mtf_filter(frame_m3, h1, h4, d1)
    return signal.where(((signal > 0) & (bias > 0)) | ((signal < 0) & (bias < 0)), 0)


register_strategy("F", PayloadFStrategy)
