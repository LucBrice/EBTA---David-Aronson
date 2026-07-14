import unittest

import pandas as pd

from ebta_engine.strategies.signals.sessions import filter_session


class SessionSignalTests(unittest.TestCase):
    def test_filters_london_with_dst_aware_conversion(self):
        frame = pd.DataFrame(index=pd.DatetimeIndex(["2026-07-13T07:30:00Z", "2026-07-13T17:30:00Z"]))

        mask = filter_session(frame, "london")

        self.assertEqual(mask.tolist(), [True, False])

    def test_all_session_keeps_every_bar(self):
        frame = pd.DataFrame(index=pd.date_range("2026-01-01", periods=2, freq="h", tz="UTC"))

        self.assertEqual(filter_session(frame, "all").tolist(), [True, True])


if __name__ == "__main__":
    unittest.main()
