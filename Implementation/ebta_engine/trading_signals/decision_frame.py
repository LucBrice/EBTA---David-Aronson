"""Serialize native signal decisions into an auditable frame."""

from __future__ import annotations

from ebta_engine.features.causal_signals import SignalDecision
from ebta_engine.strategies.payloads import StrategyPayload


def signal_decision_frame(payload: StrategyPayload, decisions: list[SignalDecision]) -> dict:
    return {
        "artifact_type": "signal_decision_frame",
        "asset": payload.asset,
        "payload_code": payload.payload_code,
        "payload_hash": payload.payload_hash,
        "row_count": len(decisions),
        "rows": [decision.__dict__ for decision in decisions],
    }
