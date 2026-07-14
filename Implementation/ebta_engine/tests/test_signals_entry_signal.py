import unittest

import pandas as pd

from ebta_engine.strategies.signals.entry_signal import compute_entry_signals


class EntrySignalTests(unittest.TestCase):
    def test_computes_buy_signal_after_sweep_engulf_confirmation(self):
        m1 = pd.DataFrame(
            {
                "open": [10.0, 9.5, 10.0, 12.0, 12.2, 12.4, 12.6],
                "high": [11.0, 10.5, 11.0, 12.5, 12.7, 12.9, 13.0],
                "low": [9.0, 9.2, 8.5, 11.5, 12.0, 12.1, 12.2],
                "close": [10.0, 10.0, 9.0, 12.2, 12.4, 12.6, 12.8],
            },
            index=pd.date_range("2026-01-01", periods=7, freq="min", tz="UTC"),
        )
        m3 = pd.DataFrame(
            {
                "open": [10.0, 12.0, 12.5, 13.0],
                "high": [12.0, 13.0, 13.5, 14.0],
                "low": [9.0, 11.0, 12.0, 12.5],
                "close": [10.0, 12.6, 13.0, 13.5],
            },
            index=pd.date_range("2026-01-01", periods=4, freq="3min", tz="UTC"),
        )
        pools = pd.Series(
            [
                [],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
                [{"side": "bull", "price": 9.0, "expires_at": 100}],
            ],
            index=m1.index,
        )

        signal = compute_entry_signals(m1, m3, pools, window_back=2, window_fwd=2, window_m3=3)

        self.assertIn(1, set(signal.tolist()))


if __name__ == "__main__":
    unittest.main()
