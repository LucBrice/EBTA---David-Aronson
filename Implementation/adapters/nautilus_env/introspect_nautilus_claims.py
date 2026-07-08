"""Targeted empirical checks for EBTA's NautilusTrader implementation plan."""

from __future__ import annotations

from decimal import Decimal
import importlib
import inspect
import sys
import textwrap


SYMBOLS = [
    "nautilus_trader.backtest.engine.BacktestEngine",
    "nautilus_trader.backtest.engine.BacktestEngine.add_venue",
    "nautilus_trader.backtest.engine.BacktestEngine.run",
    "nautilus_trader.backtest.engine.BacktestEngine.reset",
    "nautilus_trader.backtest.engine.BacktestEngine.get_result",
    "nautilus_trader.backtest.engine.BacktestEngine.add_data",
    "nautilus_trader.backtest.engine.BacktestEngine.add_instrument",
    "nautilus_trader.backtest.engine.BacktestEngine.add_strategy",
    "nautilus_trader.backtest.engine.BacktestEngine.clear_data",
    "nautilus_trader.backtest.engine.BacktestEngine.clear_strategies",
    "nautilus_trader.backtest.engine.BacktestEngine.sort_data",
    "nautilus_trader.backtest.engine.BacktestEngine.end",
    "nautilus_trader.config.BacktestEngineConfig",
    "nautilus_trader.config.BacktestRunConfig",
    "nautilus_trader.config.StrategyConfig",
    "nautilus_trader.trading.strategy.Strategy",
    "nautilus_trader.trading.strategy.Strategy.register_indicator_for_bars",
    "nautilus_trader.persistence.wranglers.BarDataWrangler",
    "nautilus_trader.persistence.wranglers.BarDataWrangler.process",
    "nautilus_trader.persistence.catalog.ParquetDataCatalog",
    "nautilus_trader.model.data.Bar",
    "nautilus_trader.model.data.BarType",
    "nautilus_trader.model.data.BarType.from_str",
    "nautilus_trader.model.objects.Price",
    "nautilus_trader.model.objects.Price.from_str",
    "nautilus_trader.model.objects.Price.from_raw",
    "nautilus_trader.model.objects.Quantity",
    "nautilus_trader.model.instruments.CurrencyPair",
    "nautilus_trader.model.instruments.Equity",
    "nautilus_trader.model.instruments.FuturesContract",
    "nautilus_trader.common.factories.OrderFactory",
    "nautilus_trader.common.factories.OrderFactory.bracket",
    "nautilus_trader.common.factories.OrderFactory.trailing_stop_market",
    "nautilus_trader.model.enums.OmsType",
    "nautilus_trader.model.enums.AccountType",
    "nautilus_trader.backtest.models.FillModel",
    "nautilus_trader.backtest.models.BestPriceFillModel",
    "nautilus_trader.backtest.models.ThreeTierFillModel",
    "nautilus_trader.backtest.models.SizeAwareFillModel",
    "nautilus_trader.backtest.models.TwoTierFillModel",
    "nautilus_trader.backtest.models.VolumeSensitiveFillModel",
    "nautilus_trader.backtest.models.MarketHoursFillModel",
    "nautilus_trader.backtest.models.OneTickSlippageFillModel",
    "nautilus_trader.backtest.models.CompetitionAwareFillModel",
    "nautilus_trader.backtest.models.LimitOrderPartialFillModel",
    "nautilus_trader.backtest.models.ProbabilisticFillModel",
    "nautilus_trader.backtest.models.MakerTakerFeeModel",
    "nautilus_trader.backtest.models.FixedFeeModel",
    "nautilus_trader.backtest.models.PerContractFeeModel",
    "nautilus_trader.backtest.models.LatencyModel",
    "nautilus_trader.backtest.models.MarginModel",
    "nautilus_trader.backtest.models.StandardMarginModel",
    "nautilus_trader.backtest.models.LeveragedMarginModel",
    "nautilus_trader.cache.cache.Cache",
    "nautilus_trader.cache.cache.Cache.positions_closed",
    "nautilus_trader.backtest.results.BacktestResult",
    "nautilus_trader.backtest.node.BacktestNode",
]


def resolve(dotted_path: str):
    parts = dotted_path.split(".")
    last_error: Exception | None = None
    for split_at in range(len(parts), 0, -1):
        module_name = ".".join(parts[:split_at])
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            last_error = exc
            continue
        obj = module
        for attr in parts[split_at:]:
            obj = getattr(obj, attr)
        return obj
    raise ImportError(f"could not resolve {dotted_path!r}: {last_error}")


def describe(dotted_path: str) -> None:
    print(f"## {dotted_path}")
    try:
        obj = resolve(dotted_path)
    except Exception as exc:
        print(f"NOT FOUND: {exc}\n")
        return

    print(f"type: {type(obj)!r}")
    print(f"module: {getattr(obj, '__module__', None)}")
    print(f"name: {getattr(obj, '__qualname__', getattr(obj, '__name__', None))}")
    try:
        print(f"signature: {inspect.signature(obj)}")
    except Exception as exc:
        print(f"signature: unavailable ({type(exc).__name__}: {exc})")
    text_sig = getattr(obj, "__text_signature__", None)
    if text_sig:
        print(f"text_signature: {text_sig}")
    doc = inspect.getdoc(obj)
    if doc:
        print("doc:")
        print(textwrap.indent("\n".join(doc.splitlines()[:24]), "  "))
    if inspect.isclass(obj):
        members = [name for name in dir(obj) if not name.startswith("_")]
        print("members:")
        print("  " + ", ".join(members[:80]))
    print()


def construction_checks() -> None:
    print("# Construction checks")
    import nautilus_trader
    from nautilus_trader.backtest.engine import BacktestEngine
    from nautilus_trader.backtest.models import (
        FillModel,
        LatencyModel,
        LeveragedMarginModel,
        MakerTakerFeeModel,
    )
    from nautilus_trader.model.enums import AccountType, OmsType
    from nautilus_trader.model.objects import Price

    print(f"version: {nautilus_trader.__version__}")
    print(f"python: {sys.executable}")
    engine = BacktestEngine()
    print(f"BacktestEngine(): OK -> {engine!r}")
    print(f"BacktestEngine.cache: {type(engine.cache)!r}")
    engine.dispose()
    print("BacktestEngine.dispose(): OK")

    fill = FillModel(prob_fill_on_limit=0.5, prob_slippage=0.25, random_seed=42)
    print(
        "FillModel kwargs: OK -> "
        f"prob_fill_on_limit={fill.prob_fill_on_limit}, prob_slippage={fill.prob_slippage}"
    )
    latency = LatencyModel(base_latency_nanos=1_000_000)
    print(f"LatencyModel(base_latency_nanos=...): OK -> {latency.base_latency_nanos}")
    print(f"MakerTakerFeeModel(): OK -> {MakerTakerFeeModel()!r}")
    print(f"LeveragedMarginModel(): OK -> {LeveragedMarginModel()!r}")
    print(f"OmsType.HEDGING: {OmsType.HEDGING!r}")
    print(f"AccountType.MARGIN: {AccountType.MARGIN!r}")

    for value in ["3000", "20000", "9200000000", "17014118346046"]:
        try:
            price = Price.from_str(value)
            print(f"Price.from_str({value!r}): OK raw={price.raw} precision={price.precision}")
        except Exception as exc:
            print(f"Price.from_str({value!r}): FAIL {type(exc).__name__}: {exc}")

    for raw in [9_223_372_036_000_000_000, 9_223_372_037_000_000_000]:
        try:
            price = Price.from_raw(raw, 0)
            print(f"Price.from_raw({raw}, 0): OK value={price}")
        except Exception as exc:
            print(f"Price.from_raw({raw}, 0): FAIL {type(exc).__name__}: {exc}")


def main() -> int:
    construction_checks()
    print()
    print("# Symbol checks")
    for symbol in SYMBOLS:
        describe(symbol)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
