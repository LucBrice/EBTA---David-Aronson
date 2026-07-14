"""Registry for incremental EBTA signal strategies.

Source: PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md Phase 2.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IncrementalSignalStrategy(Protocol):
    """Stable interface consumed by the Nautilus strategy bridge."""

    def on_bar(self, bar: Any) -> None:
        """Update internal state from one closed bar."""
        ...

    def should_enter(self) -> tuple[bool, Any | None]:
        """Return whether to enter and the side object expected by the caller."""
        ...

    def should_exit(self, bar_count_since_entry: int) -> bool:
        """Return whether an open position should be closed."""
        ...


STRATEGY_REGISTRY: dict[str, type[IncrementalSignalStrategy]] = {}


def register_strategy(payload_code: str, strategy_cls: type[IncrementalSignalStrategy]) -> None:
    if not payload_code:
        raise ValueError("payload_code must not be empty")
    STRATEGY_REGISTRY[payload_code] = strategy_cls


def get_strategy(payload_code: str) -> type[IncrementalSignalStrategy]:
    if payload_code not in STRATEGY_REGISTRY:
        raise KeyError(f"Unknown payload code: {payload_code!r}. Registered: {sorted(STRATEGY_REGISTRY)}")
    return STRATEGY_REGISTRY[payload_code]
