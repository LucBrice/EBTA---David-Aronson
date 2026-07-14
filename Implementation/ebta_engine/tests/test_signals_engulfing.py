import unittest

import pandas as pd

from ebta_engine.strategies.signals.engulfing import detect_engulfing, detect_engulfing_components


class EngulfingSignalTests(unittest.TestCase):
    def test_detects_bullish_and_bearish_patterns(self):
        frame = pd.DataFrame(
            {
                "open": [10.0, 9.5, 12.0],
                "high": [11.0, 10.5, 13.0],
                "low": [9.0, 8.5, 11.0],
                "close": [9.5, 11.5, 8.0],
            },
            index=pd.date_range("2026-01-01", periods=3, freq="min", tz="UTC"),
        )

        components = detect_engulfing_components(frame)

        self.assertTrue(bool(components["engulf_bull"].iloc[1]))
        self.assertTrue(bool(components["engulf_bear"].iloc[2]))
        self.assertTrue(bool(detect_engulfing(frame).iloc[1]))
        self.assertEqual(components["pivot_bull"].iloc[1], 8.5)
        self.assertEqual(components["pivot_bear"].iloc[2], 13.0)


if __name__ == "__main__":
    unittest.main()
