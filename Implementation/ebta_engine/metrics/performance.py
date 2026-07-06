"""Performance metrics used by the native MVP."""

from __future__ import annotations


def mean_return(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot compute mean_return on an empty series")
    return sum(values) / len(values)
