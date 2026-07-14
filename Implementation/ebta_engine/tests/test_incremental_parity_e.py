import unittest

from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, load_ohlcv_bars
from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.incremental.payload_e import PayloadEStrategy, frame_from_bars
from ebta_engine.strategies.payloads import payload_by_code
from ebta_engine.strategies.signals.entry_signal import compute_entry_signals


class IncrementalParityETests(unittest.TestCase):
    def test_payload_e_matches_vectorized_oracle_on_available_m1_data(self):
        bars = _load_real_bars_or_skip(self)
        payload = payload_by_code(bars[0].asset, "E").to_dict()
        payload.pop("payload_hash", None)
        strategy = PayloadEStrategy(payload)

        for bar in bars:
            strategy.on_bar(bar)
            strategy.should_enter()

        oracle = compute_entry_signals(frame_from_bars(bars), frame_from_bars(resample_ohlcv(bars, 3)))
        expected = [(ts.to_pydatetime(), "BUY" if value > 0 else "SELL") for ts, value in oracle[oracle != 0].items()]
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
