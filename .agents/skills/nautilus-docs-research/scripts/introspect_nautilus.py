"""Empirically inspect NautilusTrader symbols in the currently active Python environment.

This script never guesses: if nautilus_trader is not importable, or a symbol
does not resolve, it says so explicitly and exits non-zero rather than
fabricating a signature. This mirrors the "Fondations empiriques verifiees"
methodology already used in this repo's Nautilus implementation plan.

Usage:
    python introspect_nautilus.py <dotted.path.to.Symbol> [<dotted.path.to.Symbol2> ...]

Examples:
    python introspect_nautilus.py nautilus_trader.backtest.engine.BacktestEngine
    python introspect_nautilus.py nautilus_trader.model.enums.OmsType
    python introspect_nautilus.py nautilus_trader.trading.strategy.Strategy
    python introspect_nautilus.py nautilus_trader.accounting.margin_models.LeveragedMarginModel
"""

from __future__ import annotations

import importlib
import inspect
import sys


def resolve(dotted_path: str):
    """Resolve a dotted path by trying progressively shorter module prefixes.

    NautilusTrader mixes Rust/Cython extension modules with Python re-exports,
    so the importable module boundary is not always obvious from the dotted
    path alone. Trying the longest prefix first and shortening on failure
    finds the right split without guessing it.
    """
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
    raise ImportError(f"could not resolve any importable prefix of {dotted_path!r} ({last_error})")


def describe(dotted_path: str) -> bool:
    """Print what is actually true about a symbol. Returns False if not found."""
    print(f"=== {dotted_path} ===")
    try:
        obj = resolve(dotted_path)
    except (ImportError, AttributeError) as exc:
        print(f"NOT FOUND: {exc}")
        print("Do not assume this symbol exists under a different name without re-checking.")
        print()
        return False

    if inspect.isclass(obj) or inspect.isfunction(obj) or inspect.ismethod(obj):
        kind = "class" if inspect.isclass(obj) else "function/method"
        print(f"kind: {kind}")
        try:
            print(f"signature: {inspect.signature(obj)}")
        except (TypeError, ValueError) as exc:
            print(f"signature unavailable: {exc}")
        if inspect.isclass(obj):
            print("public members:")
            for name, member in inspect.getmembers(obj):
                if name.startswith("_"):
                    continue
                member_kind = "method" if inspect.isfunction(member) or inspect.ismethod(member) else "attr"
                print(f"  - {name} ({member_kind})")
    else:
        print(f"type: {type(obj)!r}")
        print(f"repr: {obj!r}")
    print()
    return True


def main(argv: list[str]) -> int:
    try:
        import nautilus_trader
    except ImportError:
        print("nautilus_trader is NOT installed in this Python environment.")
        print(f"(interpreter: {sys.executable})")
        print("Report this explicitly to the user/AI relying on this check.")
        print("Do not answer API questions from memory or documentation alone")
        print("when empirical verification was expected and unavailable.")
        return 1

    print(f"nautilus_trader version: {getattr(nautilus_trader, '__version__', 'unknown')}")
    print(f"python executable: {sys.executable}")
    print()

    if not argv:
        print("No symbols given. Pass one or more dotted paths to inspect, e.g.:")
        print("  python introspect_nautilus.py nautilus_trader.backtest.engine.BacktestEngine")
        return 0

    all_found = True
    for dotted_path in argv:
        if not describe(dotted_path):
            all_found = False
    return 0 if all_found else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
