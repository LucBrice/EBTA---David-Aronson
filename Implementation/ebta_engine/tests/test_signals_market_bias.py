import unittest

import pandas as pd

from ebta_engine.strategies.signals.market_bias import align_mtf_filter, compute_market_bias


class MarketBiasSignalTests(unittest.TestCase):
    def test_uses_previous_closed_bars_for_bias(self):
        frame = pd.DataFrame(
            {
                "open": [10.0, 10.0, 10.5],
                "high": [11.0, 12.0, 13.0],
                "low": [9.0, 9.5, 10.0],
                "close": [10.0, 12.5, 12.0],
            },
            index=pd.date_range("2026-01-01", periods=3, freq="h", tz="UTC"),
        )

        bias = compute_market_bias(frame, 60)

        self.assertEqual(int(bias.iloc[0]), 0)
        self.assertEqual(int(bias.iloc[2]), 1)

    def test_authorizes_when_higher_timeframes_agree(self):
        target = pd.DataFrame(index=pd.date_range("2026-01-01", periods=3, freq="min", tz="UTC"))
        htf = pd.DataFrame(
            {"open": [10, 10, 11], "high": [11, 12, 13], "low": [9, 9, 10], "close": [10, 13, 12]},
            index=pd.date_range("2026-01-01", periods=3, freq="h", tz="UTC"),
        )

        auth = align_mtf_filter(target, htf, htf, htf)

        self.assertEqual(len(auth), len(target))


if __name__ == "__main__":
    unittest.main()
