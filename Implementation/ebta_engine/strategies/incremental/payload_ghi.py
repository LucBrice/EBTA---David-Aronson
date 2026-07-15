"""Incremental payload G/H/I strategies with session filtering."""

from __future__ import annotations

import pandas as pd

from ebta_engine.strategies.incremental.payload_e import PayloadEStrategy
from ebta_engine.strategies.incremental.payload_f import apply_mtf_bias_filter
from ebta_engine.strategies.registry import register_strategy
from ebta_engine.strategies.signals.sessions import filter_session


class _SessionStrategy(PayloadEStrategy):
    session = "all"

    def _signal(self, frame_m1: pd.DataFrame, frame_m3: pd.DataFrame) -> pd.Series:
        signal = super()._signal(frame_m1, frame_m3)
        if self.payload.get("bias_filter") == "directional_mtf_bias":
            signal = apply_mtf_bias_filter(signal, self._bars_m1, frame_m3)
        mask = filter_session(frame_m3, self.session)
        return signal.where(mask, 0)


class PayloadGStrategy(_SessionStrategy):
    payload_code = "G"
    session = "asia"


class PayloadHStrategy(_SessionStrategy):
    payload_code = "H"
    session = "london"


class PayloadIStrategy(_SessionStrategy):
    payload_code = "I"
    session = "us"


register_strategy("G", PayloadGStrategy)
register_strategy("H", PayloadHStrategy)
register_strategy("I", PayloadIStrategy)
