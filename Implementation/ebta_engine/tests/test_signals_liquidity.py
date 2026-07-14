import unittest

import pandas as pd

from ebta_engine.strategies.signals.liquidity import compute_liquidity_pools, latest_levels


class LiquiditySignalTests(unittest.TestCase):
    def test_pool_birth_is_available_on_next_bar_open(self):
        frame = pd.DataFrame(
            {
                "open": [10.0, 9.5, 12.0],
                "high": [11.0, 10.5, 13.0],
                "low": [9.0, 8.5, 11.0],
                "close": [9.5, 11.5, 12.5],
            },
            index=pd.date_range("2026-01-01", periods=3, freq="15min", tz="UTC"),
        )

        pools = compute_liquidity_pools(frame, expiry_days=1, tf_minutes=15)

        self.assertEqual(pools.iloc[1], [])
        self.assertEqual(pools.iloc[2][0]["side"], "bull")
        self.assertEqual(latest_levels(pools, "bull").iloc[2], 8.5)


if __name__ == "__main__":
    unittest.main()
