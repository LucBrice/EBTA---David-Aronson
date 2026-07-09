"""NautilusTrader adapter mapping helpers.

Nautilus imports stay lazy so the EBTA package remains importable without the
dedicated Nautilus venv. Real Nautilus object construction is verified through
the Phase 2/3 venv smoke tests.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Sequence

from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig, SimulationResult


SUPPORTED_INSTRUMENT_CLASSES = {
    "CFD",
    "CURRENCY_PAIR",
    "EQUITY",
    "INDEX",
}

SUPPORTED_FILL_MODELS = {
    "deterministic",
    "fill_model",
    "guaranteed_bar_open_close",
}

SUPPORTED_FEE_MODELS = {
    "maker_taker",
    "zero_fee",
    "fixed",
}


def bar_type_string(
    instrument_id: str,
    *,
    interval_value: int = 1,
    interval_unit: str = "MINUTE",
    price_type: str = "LAST",
    source: str = "EXTERNAL",
) -> str:
    if interval_value <= 0:
        raise ValueError("interval_value must be positive")
    return f"{instrument_id}-{interval_value}-{interval_unit.upper()}-{price_type.upper()}-{source.upper()}"


def build_instrument(config: InstrumentConfig) -> Any:
    """Build a Nautilus instrument from a sealed EBTA instrument config."""
    classes = _nautilus_classes()
    instrument_class = config.asset_class.upper()
    if instrument_class not in SUPPORTED_INSTRUMENT_CLASSES:
        raise ValueError(f"unsupported Nautilus instrument class: {config.asset_class}")

    instrument_id = classes["InstrumentId"].from_str(config.instrument_id)
    raw_symbol = classes["Symbol"](config.symbol)
    price_increment = classes["Price"].from_str(config.price_increment)
    size_increment = classes["Quantity"].from_str(config.size_increment)
    margin_init = Decimal(config.margin_init)
    margin_maint = Decimal(config.margin_maint)
    maker_fee = Decimal(config.maker_fee)
    taker_fee = Decimal(config.taker_fee)

    if instrument_class == "CFD":
        quote_currency = _currency(config.quote_currency)
        base_currency = _optional_base_currency(config.base_currency, config.quote_currency)
        underlying = _asset_class(config.metadata.get("underlying_asset_class", _default_underlying(config.symbol)))
        return classes["Cfd"](
            instrument_id=instrument_id,
            raw_symbol=raw_symbol,
            asset_class=underlying,
            quote_currency=quote_currency,
            price_precision=config.price_precision,
            size_precision=config.size_precision,
            price_increment=price_increment,
            size_increment=size_increment,
            ts_event=0,
            ts_init=0,
            base_currency=base_currency,
            margin_init=margin_init,
            margin_maint=margin_maint,
            maker_fee=maker_fee,
            taker_fee=taker_fee,
            info={"ebta_asset_class": config.asset_class, **dict(config.metadata)},
        )

    if instrument_class == "CURRENCY_PAIR":
        return classes["CurrencyPair"](
            instrument_id=instrument_id,
            raw_symbol=raw_symbol,
            base_currency=_currency(config.base_currency),
            quote_currency=_currency(config.quote_currency),
            price_precision=config.price_precision,
            size_precision=config.size_precision,
            price_increment=price_increment,
            size_increment=size_increment,
            ts_event=0,
            ts_init=0,
            margin_init=margin_init,
            margin_maint=margin_maint,
            maker_fee=maker_fee,
            taker_fee=taker_fee,
            info=dict(config.metadata),
        )

    if instrument_class == "EQUITY":
        return classes["Equity"](
            instrument_id=instrument_id,
            raw_symbol=raw_symbol,
            currency=_currency(config.quote_currency),
            price_precision=config.price_precision,
            price_increment=price_increment,
            lot_size=size_increment,
            ts_event=0,
            ts_init=0,
            margin_init=margin_init,
            margin_maint=margin_maint,
            maker_fee=maker_fee,
            taker_fee=taker_fee,
            info=dict(config.metadata),
        )

    return classes["IndexInstrument"](
        instrument_id=instrument_id,
        raw_symbol=raw_symbol,
        currency=_currency(config.quote_currency),
        price_precision=config.price_precision,
        size_precision=config.size_precision,
        price_increment=price_increment,
        size_increment=size_increment,
        ts_event=0,
        ts_init=0,
        info=dict(config.metadata),
    )


def map_cost_model_to_venue(
    engine: Any,
    venue: Any,
    cost_model: CostModel,
    *,
    starting_balances: list[Any],
    seed: int,
    base_currency: str = "USD",
) -> None:
    """Attach a declared EBTA execution model to a Nautilus backtest engine."""
    if cost_model.fill_model.lower() not in SUPPORTED_FILL_MODELS:
        raise ValueError(f"unsupported fill_model: {cost_model.fill_model}")
    if cost_model.fee_model.lower() not in SUPPORTED_FEE_MODELS:
        raise ValueError(f"unsupported fee_model: {cost_model.fee_model}")
    if not starting_balances:
        raise ValueError("starting_balances must not be empty")

    classes = _nautilus_backtest_classes()
    venue_obj = classes["Venue"](venue) if isinstance(venue, str) else venue
    engine.add_venue(
        venue=venue_obj,
        oms_type=classes["OmsType"].HEDGING,
        account_type=classes["AccountType"].MARGIN,
        starting_balances=starting_balances,
        base_currency=_currency(base_currency),
        default_leverage=Decimal(1),
        margin_model=classes["LeveragedMarginModel"](),
        fill_model=classes["FillModel"](
            prob_fill_on_limit=cost_model.prob_fill_on_limit,
            prob_slippage=cost_model.prob_slippage,
            random_seed=seed,
        ),
        fee_model=_fee_model(cost_model, base_currency),
        latency_model=classes["LatencyModel"](base_latency_nanos=cost_model.latency_nanos),
    )


def map_ohlcv_to_bars(
    bars: Sequence[OhlcvBar],
    instrument: Any,
    *,
    interval_value: int = 1,
    interval_unit: str = "MINUTE",
    timestamp_is_close: bool = False,
) -> list[Any]:
    """Map EBTA OHLCV bars to Nautilus bars without exposing segment identity."""
    if not bars:
        raise ValueError("bars must not be empty")
    assets = {bar.asset for bar in bars}
    if len(assets) != 1:
        raise ValueError(f"bars must contain exactly one asset, got {sorted(assets)}")

    pd, np, bar_type_cls, wrangler_cls = _nautilus_data_tools()
    values = np.array(
        [[bar.open, bar.high, bar.low, bar.close, bar.volume] for bar in bars],
        dtype="float64",
    ).copy()
    frame = pd.DataFrame(
        values,
        columns=["open", "high", "low", "close", "volume"],
        index=pd.to_datetime([bar.timestamp for bar in bars], utc=True),
    ).copy(deep=True)
    for column in frame.columns:
        frame[column] = frame[column].astype("float64").copy()

    bar_type = bar_type_cls.from_str(
        bar_type_string(str(instrument.id), interval_value=interval_value, interval_unit=interval_unit)
    )
    ts_init_delta = 0 if timestamp_is_close else _interval_to_nanos(interval_value, interval_unit)
    return list(wrangler_cls(bar_type, instrument).process(frame, ts_init_delta=ts_init_delta))


def run_segment(
    candidate: Candidate,
    bars: Sequence[OhlcvBar],
    cost_model: CostModel,
    instrument_config: InstrumentConfig,
    *,
    seed: int,
    starting_nav: float = 1000.0,
    trade_size: str = "1",
    interval_value: int = 1,
    interval_unit: str = "MINUTE",
    timestamp_is_close: bool = False,
    engine: Any | None = None,
) -> SimulationResult:
    """Run one opaque EBTA segment through Nautilus and return EBTA output."""
    if not bars:
        raise ValueError("bars must not be empty")
    classes = _nautilus_engine_classes()
    instrument = build_instrument(instrument_config)
    nautilus_bars = map_ohlcv_to_bars(
        bars,
        instrument,
        interval_value=interval_value,
        interval_unit=interval_unit,
        timestamp_is_close=timestamp_is_close,
    )
    bar_type = classes["BarType"].from_str(
        bar_type_string(str(instrument.id), interval_value=interval_value, interval_unit=interval_unit)
    )
    eng = engine or classes["BacktestEngine"](
        config=classes["BacktestEngineConfig"](logging=classes["LoggingConfig"](log_level="ERROR"))
    )
    owns_engine = engine is None
    try:
        map_cost_model_to_venue(
            eng,
            instrument_config.venue,
            cost_model,
            starting_balances=[classes["Money"](starting_nav, _currency(instrument_config.quote_currency))],
            seed=seed,
            base_currency=instrument_config.quote_currency,
        )
        eng.add_instrument(instrument)
        eng.add_data(nautilus_bars)
        strategy_config = classes["GenericPayloadStrategyConfig"](
            payload=dict(candidate.payload),
            instrument_id=instrument.id,
            bar_type=bar_type,
            trade_size=Decimal(trade_size),
        )
        eng.add_strategy(classes["GenericPayloadStrategy"](strategy_config))
        eng.run()
        return extract_simulation_result(
            candidate_id=candidate.candidate_id,
            instrument_id=str(instrument.id),
            source_bars=bars,
            engine=eng,
            starting_nav=starting_nav,
            quantity=float(trade_size),
        )
    finally:
        if owns_engine:
            eng.dispose()


def extract_simulation_result(
    *,
    candidate_id: str,
    instrument_id: str,
    source_bars: Sequence[OhlcvBar],
    engine: Any,
    starting_nav: float,
    quantity: float,
) -> SimulationResult:
    fills = engine.trader.generate_order_fills_report()
    positions = engine.trader.generate_positions_report()
    if fills.empty:
        return _flat_simulation_result(candidate_id, instrument_id, source_bars, starting_nav)

    entry_fill = fills.iloc[0]
    exit_fill = fills.iloc[-1]
    entry_price = float(entry_fill["avg_px"])
    exit_price = float(exit_fill["avg_px"])
    timestamps: list[str] = []
    nav: list[float] = []
    daily_returns: list[float] = []
    daily_exposure: list[float] = []
    previous_nav = starting_nav
    for index, bar in enumerate(source_bars):
        mark_price = float(bar.close)
        current_nav = starting_nav + (mark_price - entry_price) * quantity
        timestamps.append(_timestamp_to_z(bar.timestamp))
        nav.append(current_nav)
        daily_returns.append((current_nav - previous_nav) / previous_nav if previous_nav else 0.0)
        daily_exposure.append(0.0 if index == len(source_bars) - 1 else (mark_price * quantity) / current_nav)
        previous_nav = current_nav

    realized_pnl = (exit_price - entry_price) * quantity
    if not positions.empty and "realized_pnl" in positions:
        realized_pnl = float(str(positions.iloc[0]["realized_pnl"]).split()[0])

    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=instrument_id,
        timestamps=timestamps,
        daily_returns=daily_returns,
        daily_exposure=daily_exposure,
        nav=nav,
        total_costs=0.0,
        orders=_fills_to_records(fills, "avg_px", "quantity", "ts_init"),
        fills=_fills_to_records(fills, "avg_px", "filled_qty", "ts_last"),
        positions=[
            {
                "quantity": quantity,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "realized_pnl": realized_pnl,
            }
        ],
        metadata={
            "source": "nautilus_trader",
            "total_orders": int(engine.get_result().total_orders),
            "total_positions": int(engine.get_result().total_positions),
        },
    )


def run_multifold_segments(
    segment_inputs: Sequence[dict[str, Any]],
    *,
    runner: Any | None = None,
) -> list[dict[str, Any]]:
    """Run declared fold/candidate segment inputs without exposing segment labels."""
    if not segment_inputs:
        raise ValueError("segment_inputs must not be empty")
    run_one = runner or run_segment
    outputs: list[dict[str, Any]] = []
    for item in segment_inputs:
        candidate = item["candidate"]
        result = run_one(
            candidate=item["candidate"],
            bars=item["bars"],
            cost_model=item["cost_model"],
            instrument_config=item["instrument_config"],
            seed=item["seed"],
            starting_nav=item.get("starting_nav", 1000.0),
            trade_size=item.get("trade_size", "1"),
            interval_value=item.get("interval_value", 1),
            interval_unit=item.get("interval_unit", "MINUTE"),
            timestamp_is_close=item.get("timestamp_is_close", False),
        )
        outputs.append(
            {
                "fold_id": item.get("fold_id") or candidate.fold_id,
                "candidate_id": candidate.candidate_id,
                "asset": candidate.asset,
                "simulation_result": result,
            }
        )
    return outputs


def _flat_simulation_result(
    candidate_id: str,
    instrument_id: str,
    source_bars: Sequence[OhlcvBar],
    starting_nav: float,
) -> SimulationResult:
    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=instrument_id,
        timestamps=[_timestamp_to_z(bar.timestamp) for bar in source_bars],
        daily_returns=[0.0 for _ in source_bars],
        daily_exposure=[0.0 for _ in source_bars],
        nav=[starting_nav for _ in source_bars],
        total_costs=0.0,
        metadata={"source": "nautilus_trader", "status": "NO_MODEL"},
    )


def _fills_to_records(fills: Any, price_column: str, quantity_column: str, timestamp_column: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _, row in fills.iterrows():
        records.append(
            {
                "side": str(row["side"]),
                "quantity": float(row[quantity_column]),
                "price": float(row[price_column]),
                "timestamp": str(row[timestamp_column]),
            }
        )
    return records


def _timestamp_to_z(value: Any) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _interval_to_nanos(interval_value: int, interval_unit: str) -> int:
    if interval_value <= 0:
        raise ValueError("interval_value must be positive")
    unit = interval_unit.upper()
    factors = {
        "SECOND": 1_000_000_000,
        "MINUTE": 60_000_000_000,
        "HOUR": 3_600_000_000_000,
        "DAY": 86_400_000_000_000,
    }
    if unit not in factors:
        raise ValueError(f"unsupported interval_unit: {interval_unit}")
    return interval_value * factors[unit]


def _default_underlying(symbol: str) -> str:
    upper = symbol.upper()
    if "XAU" in upper or "GOLD" in upper:
        return "COMMODITY"
    if "NAS" in upper or "IDX" in upper or "INDEX" in upper:
        return "INDEX"
    return "ALTERNATIVE"


def _optional_base_currency(base_currency: str, quote_currency: str) -> Any | None:
    if not base_currency or base_currency.upper() == quote_currency.upper():
        return None
    return _currency(base_currency)


def _currency(code: str) -> Any:
    currencies = _nautilus_classes()["currencies"]
    name = code.upper()
    if not hasattr(currencies, name):
        raise ValueError(f"unsupported Nautilus currency code: {code}")
    return getattr(currencies, name)


def _asset_class(name: str) -> Any:
    asset_class = _nautilus_classes()["AssetClass"]
    key = name.upper()
    if not hasattr(asset_class, key):
        raise ValueError(f"unsupported Nautilus asset class: {name}")
    return getattr(asset_class, key)


def _fee_model(cost_model: CostModel, currency_code: str) -> Any:
    classes = _nautilus_backtest_classes()
    fee_model = cost_model.fee_model.lower()
    if fee_model in {"maker_taker", "zero_fee"}:
        if fee_model == "zero_fee" and cost_model.commission_per_lot != 0.0:
            raise ValueError("zero_fee cost model requires commission_per_lot == 0")
        return classes["MakerTakerFeeModel"]()
    if fee_model == "fixed":
        if cost_model.commission_per_lot <= 0.0:
            raise ValueError("fixed fee model requires positive commission_per_lot")
        return classes["FixedFeeModel"](
            classes["Money"](Decimal(str(cost_model.commission_per_lot)), _currency(currency_code))
        )
    raise ValueError(f"unsupported fee_model: {cost_model.fee_model}")


def _nautilus_classes() -> dict[str, Any]:
    from nautilus_trader.model import currencies
    from nautilus_trader.model.enums import AssetClass
    from nautilus_trader.model.identifiers import InstrumentId, Symbol
    from nautilus_trader.model.instruments import Cfd, CurrencyPair, Equity, IndexInstrument
    from nautilus_trader.model.objects import Price, Quantity

    return {
        "AssetClass": AssetClass,
        "Cfd": Cfd,
        "CurrencyPair": CurrencyPair,
        "Equity": Equity,
        "IndexInstrument": IndexInstrument,
        "InstrumentId": InstrumentId,
        "Price": Price,
        "Quantity": Quantity,
        "Symbol": Symbol,
        "currencies": currencies,
    }


def _nautilus_backtest_classes() -> dict[str, Any]:
    from nautilus_trader.accounting.margin_models import LeveragedMarginModel
    from nautilus_trader.backtest.models import FillModel, FixedFeeModel, LatencyModel, MakerTakerFeeModel
    from nautilus_trader.model.enums import AccountType, OmsType
    from nautilus_trader.model.identifiers import Venue
    from nautilus_trader.model.objects import Money

    return {
        "AccountType": AccountType,
        "FillModel": FillModel,
        "FixedFeeModel": FixedFeeModel,
        "LatencyModel": LatencyModel,
        "LeveragedMarginModel": LeveragedMarginModel,
        "MakerTakerFeeModel": MakerTakerFeeModel,
        "Money": Money,
        "OmsType": OmsType,
        "Venue": Venue,
    }


def _nautilus_data_tools() -> tuple[Any, Any, Any, Any]:
    import numpy as np
    import pandas as pd
    from nautilus_trader.model.data import BarType
    from nautilus_trader.persistence.wranglers import BarDataWrangler

    return pd, np, BarType, BarDataWrangler


def _nautilus_engine_classes() -> dict[str, Any]:
    from nautilus_trader.backtest.engine import BacktestEngine
    from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
    from nautilus_trader.model.data import BarType
    from nautilus_trader.model.objects import Money

    from ebta_engine.adapters.nautilus_strategy_bridge import GenericPayloadStrategy, GenericPayloadStrategyConfig

    return {
        "BacktestEngine": BacktestEngine,
        "BacktestEngineConfig": BacktestEngineConfig,
        "BarType": BarType,
        "GenericPayloadStrategy": GenericPayloadStrategy,
        "GenericPayloadStrategyConfig": GenericPayloadStrategyConfig,
        "LoggingConfig": LoggingConfig,
        "Money": Money,
    }
