import unittest
from typing import cast

import pandas as pd

from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, load_ohlcv_bars
from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.incremental.payload_e import frame_from_bars
from ebta_engine.strategies.incremental.payload_f import PayloadFStrategy
from ebta_engine.strategies.payloads import payload_by_code
from ebta_engine.strategies.signals.entry_signal import compute_entry_signals
from ebta_engine.strategies.signals.market_bias import align_mtf_filter


class IncrementalParityFTests(unittest.TestCase):
    def test_payload_f_matches_bias_filtered_oracle_on_available_m1_data(self):
        bars = _load_real_bars_or_skip(self)
        payload = payload_by_code(bars[0].asset, "F").to_dict()
        payload.pop("payload_hash", None)
        strategy = PayloadFStrategy(payload)

        for bar in bars:
            strategy.on_bar(bar)
            strategy.should_enter()

        m1 = frame_from_bars(bars)
        m3 = frame_from_bars(resample_ohlcv(bars, 3))
        signal = compute_entry_signals(m1, m3)
        bias = align_mtf_filter(
            m3,
            frame_from_bars(resample_ohlcv(bars, 60)),
            frame_from_bars(resample_ohlcv(bars, 240)),
            frame_from_bars(resample_ohlcv(bars, 1440)),
        )
        oracle = signal.where(((signal > 0) & (bias > 0)) | ((signal < 0) & (bias < 0)), 0)
        expected = [
            (cast(pd.Timestamp, ts).to_pydatetime(), "BUY" if value > 0 else "SELL")
            for ts, value in oracle[oracle != 0].items()
        ]
        actual = [(decision.timestamp, decision.side) for decision in strategy.decisions]
        self.assertEqual(actual, expected)


def _load_real_bars_or_skip(testcase: unittest.TestCase):
    try:
        bars = load_ohlcv_bars(DEFAULT_DATA_ROOT, "XAUUSD", max_bars=180)
    except (FileNotFoundError, ValueError) as exc:
        testcase.skipTest(f"M1 data not found at DEFAULT_DATA_ROOT - skip parity test: {exc}")
    if len(bars) < 120:
        testcase.skipTest("M1 data not found at DEFAULT_DATA_ROOT - skip parity test: insufficient bars")
    return bars


if __name__ == "__main__":
    unittest.main()
