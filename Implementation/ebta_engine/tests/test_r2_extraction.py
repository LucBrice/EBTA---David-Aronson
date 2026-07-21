import unittest
from datetime import datetime, timezone

import pandas as pd

from ebta_engine.adapters.nautilus_mapping import extract_simulation_result
from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.strategies.contracts import CostModel


class R2ExtractionTests(unittest.TestCase):
    def test_nav_stays_flat_after_exit_when_strategy_snapshots_are_flat(self):
        engine = _Engine(
            strategy=_Strategy(
                [
                    (_nanos("2026-01-01T00:00:00Z"), 1000.0, 100.0),
                    (_nanos("2026-01-01T00:01:00Z"), 1002.0, 100.0),
                    (_nanos("2026-01-01T00:02:00Z"), 1002.0, 0.0),
                ]
            ),
            fills=_fills(commission=[0.0, 0.0]),
            positions=_positions(realized_pnl=2.0),
            is_flat=True,
        )

        result = extract_simulation_result(
            candidate_id="CAND",
            instrument_id="XAUUSD.SIM",
            source_bars=_bars(),
            engine=engine,
            starting_nav=1000.0,
            quantity=1.0,
        )

        self.assertEqual(result.nav, [1000.0, 1002.0, 1002.0])
        self.assertEqual(result.daily_exposure[-1], 0.0)
        self.assertEqual(result.positions[0]["realized_pnl"], 2.0)

    def test_total_costs_are_summed_from_fill_commissions(self):
        engine = _Engine(
            strategy=_Strategy([(_nanos("2026-01-01T00:00:00Z"), 1000.0, 0.0)]),
            fills=_fills(commission=["1.25 USD", "0.75 USD"]),
            positions=_positions(realized_pnl=0.0),
            is_flat=True,
        )

        result = extract_simulation_result(
            candidate_id="CAND",
            instrument_id="XAUUSD.SIM",
            source_bars=_bars(),
            engine=engine,
            starting_nav=1000.0,
            quantity=1.0,
        )

        self.assertEqual(result.total_costs, 2.0)

    def test_open_position_missing_close_price_uses_default_exit_price(self):
        positions = _positions(realized_pnl=0.0)
        positions.loc[0, "avg_px_close"] = None
        engine = _Engine(
            strategy=_Strategy([(_nanos("2026-01-01T00:00:00Z"), 1000.0, 100.0)]),
            fills=_fills(commission=[0.0, 0.0]),
            positions=positions,
            is_flat=False,
        )

        result = extract_simulation_result(
            candidate_id="CAND",
            instrument_id="XAUUSD.SIM",
            source_bars=_bars(),
            engine=engine,
            starting_nav=1000.0,
            quantity=1.0,
        )

        self.assertEqual(result.positions[0]["exit_price"], 0.0)

    def test_execution_overlay_debits_each_fill_once_and_recomputes_returns(self):
        engine = _Engine(
            strategy=_Strategy(
                [
                    (_nanos("2026-01-01T00:00:00Z"), 1000.0, 100.0),
                    (_nanos("2026-01-01T00:01:00Z"), 1001.0, 100.0),
                    (_nanos("2026-01-01T00:02:00Z"), 1002.0, 0.0),
                ]
            ),
            fills=_fills(commission=[0.0, 0.0]),
            positions=_positions(realized_pnl=2.0),
            is_flat=True,
        )
        cost_model = CostModel(
            "CALIBRATED",
            "fill_model",
            "maker_taker",
            spread_points=2.0,
            point_value=1.0,
            metadata={"classification": "BROKER_PROXY"},
        )

        result = extract_simulation_result(
            candidate_id="CAND",
            instrument_id="XAUUSD.SIM",
            source_bars=_bars(),
            engine=engine,
            starting_nav=1000.0,
            quantity=1.0,
            cost_model=cost_model,
        )

        self.assertEqual(result.nav, [999.0, 1000.0, 1000.0])
        self.assertEqual(result.total_costs, 2.0)
        self.assertAlmostEqual(result.daily_returns[1], 1.0 / 999.0)
        self.assertEqual(result.metadata["execution_costs"]["spread_cost"], 2.0)
        self.assertEqual(len(result.metadata["execution_costs"]["ledger"]), 2)

    def test_fill_after_final_snapshot_is_rejected(self):
        fills = _fills(commission=[0.0, 0.0])
        fills.loc[1, "ts_last"] = "2026-01-01T00:03:00Z"
        engine = _Engine(
            strategy=_Strategy([(_nanos("2026-01-01T00:00:00Z"), 1000.0, 0.0)]),
            fills=fills,
            positions=_positions(realized_pnl=0.0),
            is_flat=True,
        )
        with self.assertRaisesRegex(ValueError, "later than the final NAV snapshot"):
            extract_simulation_result(
                candidate_id="CAND",
                instrument_id="XAUUSD.SIM",
                source_bars=_bars(),
                engine=engine,
                starting_nav=1000.0,
                quantity=1.0,
                cost_model=CostModel("CALIBRATED", "fill_model", "maker_taker", spread_points=1.0),
            )

    def test_no_model_requires_flat_portfolio_empty_fills_and_no_nav_snapshots(self):
        engine = _Engine(
            strategy=_Strategy([]),
            fills=pd.DataFrame(),
            positions=pd.DataFrame(),
            is_flat=True,
        )

        result = extract_simulation_result(
            candidate_id="CAND",
            instrument_id="XAUUSD.SIM",
            source_bars=_bars(),
            engine=engine,
            starting_nav=1000.0,
            quantity=1.0,
        )

        self.assertEqual(result.metadata["status"], "NO_MODEL")
        self.assertEqual(result.nav, [1000.0, 1000.0, 1000.0])


class _Strategy:
    def __init__(self, snapshots):
        self._nav_snapshots = snapshots
        self._metadata = {}


class _Trader:
    def __init__(self, strategy, fills, positions):
        self.strategies = [strategy]
        self._fills = fills
        self._positions = positions

    def generate_order_fills_report(self):
        return self._fills

    def generate_positions_report(self):
        return self._positions


class _Portfolio:
    def __init__(self, is_flat):
        self.is_flat = is_flat


class _Result:
    total_orders = 2
    total_positions = 1


class _Engine:
    def __init__(self, strategy, fills, positions, is_flat):
        self.trader = _Trader(strategy, fills, positions)
        self.portfolio = _Portfolio(is_flat)

    def get_result(self):
        return _Result()


def _bars():
    return [
        OhlcvBar("XAUUSD", datetime(2026, 1, 1, 0, index, tzinfo=timezone.utc), 100, 101, 99, 100, 1)
        for index in range(3)
    ]


def _fills(commission):
    return pd.DataFrame(
        {
            "side": ["BUY", "SELL"],
            "quantity": [1.0, 1.0],
            "filled_qty": [1.0, 1.0],
            "avg_px": [100.0, 102.0],
            "ts_init": ["2026-01-01T00:00:00Z", "2026-01-01T00:02:00Z"],
            "ts_last": ["2026-01-01T00:00:00Z", "2026-01-01T00:02:00Z"],
            "commission": commission,
        }
    )


def _positions(realized_pnl):
    return pd.DataFrame(
        {
            "quantity": [1.0],
            "avg_px_open": [100.0],
            "avg_px_close": [102.0],
            "realized_pnl": [realized_pnl],
        }
    )


def _nanos(timestamp):
    return int(pd.Timestamp(timestamp).timestamp() * 1_000_000_000)


if __name__ == "__main__":
    unittest.main()
