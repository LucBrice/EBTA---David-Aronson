import unittest
from dataclasses import dataclass
from datetime import datetime, timezone

from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, OhlcvBar, load_ohlcv_bars
from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.incremental.payload_e import PayloadEStrategy, frame_from_bars
from ebta_engine.strategies.incremental.payload_ghi import PayloadGStrategy, PayloadHStrategy, PayloadIStrategy
from ebta_engine.strategies.payloads import payload_by_code
from ebta_engine.strategies.signals.entry_signal import compute_entry_signals
from ebta_engine.strategies.signals.sessions import filter_session


class IncrementalParityGHITests(unittest.TestCase):
    def test_payloads_ghi_match_session_filtered_oracle_on_available_m1_data(self):
        bars = _load_real_bars_or_skip(self)
        for code, cls, session in [
            ("G", PayloadGStrategy, "asia"),
            ("H", PayloadHStrategy, "london"),
            ("I", PayloadIStrategy, "us"),
        ]:
            with self.subTest(code=code):
                payload = payload_by_code(bars[0].asset, code).to_dict()
                payload.pop("payload_hash", None)
                strategy = cls(payload)
                for bar in bars:
                    strategy.on_bar(bar)
                    strategy.should_enter()
                m3 = frame_from_bars(resample_ohlcv(bars, 3))
                signal = compute_entry_signals(frame_from_bars(bars), m3)
                oracle = signal.where(filter_session(m3, session), 0)
                expected = [(ts.to_pydatetime(), "BUY" if value > 0 else "SELL") for ts, value in oracle[oracle != 0].items()]
                actual = [(decision.timestamp, decision.side) for decision in strategy.decisions]
                self.assertEqual(actual, expected)

    def test_short_direction_is_emitted_when_oracle_signal_is_sell(self):
        strategy = PayloadEStrategy(_payload("E"))
        for bar in _synthetic_sell_bars():
            strategy.on_bar(bar)
            entered, side = strategy.should_enter()
            if entered:
                self.assertEqual(side, "SELL")
                return
        self.fail("expected a SELL signal")

    def test_warmup_preserves_state_without_emitting_orders(self):
        warm = PayloadEStrategy(_payload("E"), warmup_bar_count=2)
        cold = PayloadEStrategy(_payload("E"), warmup_bar_count=0)
        bars = _synthetic_buy_bars()
        warm_entries = []
        cold_entries = []
        for bar in bars:
            warm.on_bar(bar)
            cold.on_bar(bar)
            warm_entries.append(warm.should_enter())
            cold_entries.append(cold.should_enter())
        self.assertFalse(any(entered for entered, _ in warm_entries[:2]))
        self.assertEqual([item for item in warm_entries if item[0]], [item for item in cold_entries if item[0]])

    def test_segment_label_does_not_change_result(self):
        train = PayloadEStrategy(_payload("E"))
        oos = PayloadEStrategy(_payload("E"))
        for bar in _synthetic_buy_bars():
            train.on_bar(_SegmentBar(bar, "TRAIN"))
            train.should_enter()
            oos.on_bar(_SegmentBar(bar, "OOS"))
            oos.should_enter()
        self.assertEqual(train.decisions, oos.decisions)


@dataclass(frozen=True)
class _SegmentBar:
    source: OhlcvBar
    segment: str
    timeframe: str = "M1"

    @property
    def asset(self):
        return self.source.asset

    @property
    def timestamp(self):
        return self.source.timestamp

    @property
    def open(self):
        return self.source.open

    @property
    def high(self):
        return self.source.high

    @property
    def low(self):
        return self.source.low

    @property
    def close(self):
        return self.source.close

    @property
    def volume(self):
        return self.source.volume


def _load_real_bars_or_skip(testcase: unittest.TestCase):
    try:
        bars = load_ohlcv_bars(DEFAULT_DATA_ROOT, "XAUUSD", max_bars=180)
    except (FileNotFoundError, ValueError) as exc:
        testcase.skipTest(f"M1 data not found at DEFAULT_DATA_ROOT - skip parity test: {exc}")
    if len(bars) < 120:
        testcase.skipTest("M1 data not found at DEFAULT_DATA_ROOT - skip parity test: insufficient bars")
    return bars


def _payload(code: str) -> dict:
    payload = payload_by_code("XAUUSD", code).to_dict()
    payload.pop("payload_hash", None)
    payload["parameters"].update({"window_back": 2, "window_fwd": 2, "window_m3": 3})
    return payload


def _synthetic_buy_bars():
    prices = [
        (10.0, 11.0, 9.0, 10.0),
        (9.5, 10.5, 9.2, 10.0),
        (10.0, 11.0, 8.5, 9.0),
        (12.0, 12.5, 11.5, 12.2),
        (12.2, 12.7, 12.0, 12.4),
        (12.4, 12.9, 12.1, 12.6),
        (12.6, 13.0, 12.2, 12.8),
    ]
    return _bars(prices)


def _synthetic_sell_bars():
    prices = [
        (10.0, 11.0, 9.0, 10.0),
        (10.0, 12.0, 9.5, 8.5),
        (8.5, 12.5, 8.0, 10.5),
        (7.8, 8.0, 7.2, 7.5),
        (7.5, 7.8, 7.0, 7.4),
        (7.4, 7.7, 7.0, 7.3),
        (7.3, 7.6, 7.0, 7.2),
    ]
    return _bars(prices)


def _bars(prices):
    return [
        OhlcvBar("XAUUSD", datetime(2026, 1, 1, 0, index, tzinfo=timezone.utc), open_, high, low, close, 1.0)
        for index, (open_, high, low, close) in enumerate(prices)
    ]


if __name__ == "__main__":
    unittest.main()
