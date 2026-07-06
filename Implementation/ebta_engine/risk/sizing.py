"""Sizing policy for the deterministic native MVP."""

from __future__ import annotations


def unit_notional_size(*, capital: float = 100_000.0, risk_fraction: float = 0.001) -> float:
    if capital <= 0:
        raise ValueError("capital must be positive")
    if not 0 < risk_fraction <= 1:
        raise ValueError("risk_fraction must be in (0, 1]")
    return capital * risk_fraction
