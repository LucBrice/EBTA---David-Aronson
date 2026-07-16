"""NautilusTrader adapter mapping helpers.

Nautilus imports stay lazy so the EBTA package remains importable without the
dedicated Nautilus venv. Real Nautilus object construction is verified through
the Phase 2/3 venv smoke tests.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Sequence

from ebta_engine.data.local_ohlcv import OhlcvBar
from ebta_engine.data.resample import resample_ohlcv
from ebta_engine.strategies.incremental.payload_e import _signal_parameters, frame_from_bars
from ebta_engine.strategies.payloads import StrategyPayload
from ebta_engine.strategies.signals.entry_signal import compute_entry_signals
from ebta_engine.strategies.signals.market_bias import align_mtf_filter
from ebta_engine.strategies.signals.sessions import filter_session
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
    warmup_bars: Sequence[OhlcvBar] | None = None,
    engine: Any | None = None,
) -> SimulationResult:
    """Run one opaque EBTA segment through Nautilus and return EBTA output."""
    if not bars:
        raise ValueError("bars must not be empty")
    classes = _nautilus_engine_classes()
    instrument = build_instrument(instrument_config)
    active_bars = list(warmup_bars or []) + list(bars)
    warmup_bar_count = len(warmup_bars or [])
    mapped_series = _map_multitimeframe_bars(
        active_bars,
        instrument,
        source_interval_value=interval_value,
        source_interval_unit=interval_unit,
        timestamp_is_close=timestamp_is_close,
    )
    bar_types = [bar_type_string(str(instrument.id), interval_value=value, interval_unit=unit) for value, unit, _ in mapped_series]
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
        for _, _, nautilus_bars in mapped_series:
            eng.add_data(nautilus_bars)
        strategy_config = classes["GenericPayloadStrategyConfig"](
            payload=dict(candidate.payload),
            instrument_id=instrument.id,
            bar_types=bar_types,
            trade_size=Decimal(trade_size),
            warmup_bar_count=warmup_bar_count,
            precomputed_decisions=_precomputed_decisions(
                candidate.payload,
                active_bars,
                warmup_bar_count=warmup_bar_count,
            ),
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
    strategy = _strategy_from_engine(engine)
    nav_series = _extract_nav_series(strategy)
    if _is_flat(engine.portfolio) and _report_empty(fills) and not nav_series:
        return _flat_simulation_result(candidate_id, instrument_id, source_bars, starting_nav)

    if nav_series:
        timestamps = [item[0] for item in nav_series]
        nav = [item[1] for item in nav_series]
        daily_exposure = [(item[2] / item[1]) if item[1] else 0.0 for item in nav_series]
    else:
        timestamps = [_timestamp_to_z(bar.timestamp) for bar in source_bars]
        nav = [starting_nav for _ in source_bars]
        daily_exposure = [0.0 for _ in source_bars]

    daily_returns = _returns_from_nav(nav)

    return SimulationResult(
        candidate_id=candidate_id,
        instrument_id=instrument_id,
        timestamps=timestamps,
        daily_returns=daily_returns,
        daily_exposure=daily_exposure,
        nav=nav,
        total_costs=_extract_costs(fills),
        orders=_fills_to_records(fills, "avg_px", "quantity", "ts_init"),
        fills=_fills_to_records(fills, "avg_px", "filled_qty", "ts_last"),
        positions=_extract_positions(positions),
        metadata={
            "source": "nautilus_trader",
            "total_orders": int(engine.get_result().total_orders),
            "total_positions": int(engine.get_result().total_positions),
            **dict(getattr(strategy, "_metadata", {})),
        },
    )


def run_multifold_segments(
    segment_inputs: Sequence[dict[str, Any]],
    *,
    runner: Any | None = None,
    max_workers: int = 1,
) -> list[dict[str, Any]]:
    """Run declared fold/candidate segment inputs without exposing segment labels."""
    if not segment_inputs:
        raise ValueError("segment_inputs must not be empty")
    if max_workers <= 0:
        raise ValueError("max_workers must be positive")
    run_one = runner or run_segment
    if max_workers == 1:
        return [_run_segment_input(item, run_one) for item in segment_inputs]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(lambda item: _run_segment_input(item, run_one), segment_inputs))


def _run_segment_input(item: dict[str, Any], run_one: Any) -> dict[str, Any]:
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
        warmup_bars=item.get("warmup_bars"),
    )
    return {
        "fold_id": item.get("fold_id") or candidate.fold_id,
        "candidate_id": candidate.candidate_id,
        "asset": candidate.asset,
        "simulation_result": result,
    }


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
        total_costs = 0.0,
        metadata={"source": "nautilus_trader", "status": "NO_MODEL"},
    )


def _extract_nav_series(strategy: Any) -> list[tuple[str, float, float]]:
    snapshots = list(getattr(strategy, "_nav_snapshots", []) or [])
    series: list[tuple[str, float, float]] = []
    for ts_event_nanos, equity, net_exposure in snapshots:
        timestamp = _nanos_to_z(int(ts_event_nanos))
        series.append((timestamp, float(equity), float(net_exposure)))
    return series


def _extract_costs(fills_report: Any) -> float:
    if _report_empty(fills_report) or "commission" not in fills_report:
        return 0.0
    return sum(_money_float(value) for value in fills_report["commission"])


def _extract_positions(positions_report: Any) -> list[dict[str, Any]]:
    if _report_empty(positions_report):
        return []
    records: list[dict[str, Any]] = []
    for _, row in positions_report.iterrows():
        records.append(
            {
                "quantity": _row_float(row, "quantity", "signed_qty", "size", default=0.0),
                "entry_price": _row_float(row, "avg_px_open", "entry_price", "avg_px", default=0.0),
                "exit_price": _row_float(row, "avg_px_close", "exit_price", default=0.0),
                "realized_pnl": _row_float(row, "realized_pnl", "realized_return", default=0.0),
            }
        )
    return records


def _first_strategy(strategies: Any) -> Any:
    if callable(strategies):
        strategies = strategies()
    return strategies[0] if strategies else None


def _strategy_from_engine(engine: Any) -> Any:
    trader = getattr(engine, "trader", None)
    strategy = _first_strategy(getattr(trader, "strategies", None))
    if strategy is not None:
        return strategy
    return _first_strategy(getattr(engine, "strategies", None))


def _returns_from_nav(nav: list[float]) -> list[float]:
    returns: list[float] = []
    previous: float | None = None
    for value in nav:
        if previous is None:
            returns.append(0.0)
        else:
            returns.append((value - previous) / previous if previous else 0.0)
        previous = value
    return returns


def _is_flat(portfolio: Any) -> bool:
    value = getattr(portfolio, "is_flat", False)
    try:
        return bool(value()) if callable(value) else bool(value)
    except Exception:
        return False


def _report_empty(report: Any) -> bool:
    return report is None or bool(getattr(report, "empty", False))


def _row_float(row: Any, *names: str, default: float) -> float:
    for name in names:
        if name not in row:
            continue
        value = row[name]
        if _is_missing_report_value(value):
            continue
        return _money_float(value)
    return default


def _is_missing_report_value(value: Any) -> bool:
    if value is None:
        return True
    try:
        if value != value:
            return True
    except Exception:
        pass
    text = str(value).strip().lower()
    return text in {"", "none", "nan", "nat", "<na>"}


def _money_float(value: Any) -> float:
    try:
        if isinstance(value, dict) and len(value) == 1:
            value = next(iter(value.values()))
        return float(value)
    except Exception:
        return float(str(value).split()[0])


def _map_multitimeframe_bars(
    bars: Sequence[OhlcvBar],
    instrument: Any,
    *,
    source_interval_value: int,
    source_interval_unit: str,
    timestamp_is_close: bool,
) -> list[tuple[int, str, list[Any]]]:
    unit = source_interval_unit.upper()
    if source_interval_value == 1 and unit == "MINUTE":
        series: list[tuple[int, str, list[OhlcvBar]]] = [
            (1, "MINUTE", list(bars)),
            (3, "MINUTE", resample_ohlcv(list(bars), 3)),
            (15, "MINUTE", resample_ohlcv(list(bars), 15)),
            (1, "HOUR", resample_ohlcv(list(bars), 60)),
            (4, "HOUR", resample_ohlcv(list(bars), 240)),
            (1, "DAY", resample_ohlcv(list(bars), 1440)),
        ]
    else:
        series = [(source_interval_value, unit, list(bars))]
    mapped: list[tuple[int, str, list[Any]]] = []
    for value, unit, source in series:
        source_timestamp_is_close = timestamp_is_close if value == 1 and unit == "MINUTE" else True
        mapped.append(
            (
                value,
                unit,
                map_ohlcv_to_bars(
                    source,
                    instrument,
                    interval_value=value,
                    interval_unit=unit,
                    timestamp_is_close=source_timestamp_is_close,
                ),
            )
        )
    return mapped


def _precomputed_decisions(
    payload_dict: dict[str, Any],
    bars: Sequence[OhlcvBar],
    *,
    warmup_bar_count: int,
) -> list[tuple[int, str]]:
    if not bars:
        return []
    payload = StrategyPayload.from_dict(dict(payload_dict))
    code = _strategy_code(payload)
    bars_m1 = list(bars)
    frame_m1 = frame_from_bars(bars_m1)
    frame_m3 = frame_from_bars(resample_ohlcv(bars_m1, 3))
    if frame_m3.empty:
        return []
    signal = compute_entry_signals(frame_m1, frame_m3, **_signal_parameters(dict(payload_dict)))
    if code == "F" or (code in {"G", "H", "I"} and payload.bias_filter == "directional_mtf_bias"):
        bias = align_mtf_filter(
            frame_m3,
            frame_from_bars(resample_ohlcv(bars_m1, 60)),
            frame_from_bars(resample_ohlcv(bars_m1, 240)),
            frame_from_bars(resample_ohlcv(bars_m1, 1440)),
        )
        signal = signal.where(((signal > 0) & (bias > 0)) | ((signal < 0) & (bias < 0)), 0)
    if code in {"G", "H", "I"}:
        signal = signal.where(filter_session(frame_m3, _session_for_code(code)), 0)

    warmup_cutoff = _warmup_cutoff(bars_m1, warmup_bar_count)
    decisions: list[tuple[int, str]] = []
    for timestamp, value in signal[signal != 0].items():
        decision_time = _as_utc_datetime(timestamp)
        if warmup_cutoff is not None and decision_time <= warmup_cutoff:
            continue
        decisions.append((_datetime_to_nanos(decision_time), "BUY" if int(value) > 0 else "SELL"))
    return decisions


def _strategy_code(payload: StrategyPayload) -> str:
    if payload.payload_code in {"E", "F", "G", "H", "I"}:
        return payload.payload_code
    session = payload.session.lower()
    if session == "asia":
        return "G"
    if session == "london":
        return "H"
    if session == "us":
        return "I"
    if payload.bias_filter != "none":
        return "F"
    return "E"


def _session_for_code(code: str) -> str:
    return {"G": "asia", "H": "london", "I": "us"}[code]


def _warmup_cutoff(bars: Sequence[OhlcvBar], warmup_bar_count: int) -> datetime | None:
    if warmup_bar_count <= 0:
        return None
    return bars[min(warmup_bar_count, len(bars)) - 1].timestamp.astimezone(timezone.utc)


def _as_utc_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        timestamp = value
    else:
        timestamp = value.to_pydatetime()
    if timestamp.tzinfo is None:
        raise ValueError(f"timestamp is not timezone-aware: {timestamp!r}")
    return timestamp.astimezone(timezone.utc)


def _datetime_to_nanos(value: datetime) -> int:
    return int(value.timestamp() * 1_000_000_000)


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


def _nanos_to_z(value: int) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(value / 1_000_000_000, timezone.utc).isoformat().replace("+00:00", "Z")


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
