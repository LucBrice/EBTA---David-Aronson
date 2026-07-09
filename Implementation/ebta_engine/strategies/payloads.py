"""Executable decomposition of reference payloads E to I.

Source: PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF.md Phase 3 and
read-only BACKTRADER audit of strategies/sweep_lq.py.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from typing import Any


PAYLOAD_CODES = ("E", "F", "G", "H", "I")


@dataclass(frozen=True)
class StrategyPayload:
    asset: str
    timeframe: str
    strategy_family: str
    payload_code: str
    direction: str
    entry_level: str
    entry_criterion: str | dict[str, Any]
    bias_filter: str
    time_filter: str
    session: str
    exit_criterion: str | dict[str, Any]
    risk_model: str
    sizing_model: str
    parameters: dict
    payload_version: str = "1.0.0"

    @property
    def payload_hash(self) -> str:
        encoded = json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["payload_hash"] = self.payload_hash
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "StrategyPayload":
        payload = dict(payload)
        supplied_hash = payload.pop("payload_hash", None)
        allowed = {field.name for field in fields(cls)}
        unexpected = sorted(set(payload) - allowed)
        if unexpected:
            raise ValueError(f"unexpected StrategyPayload fields: {unexpected}")
        missing = sorted(name for name in allowed if name not in payload and name != "payload_version")
        if missing:
            raise ValueError(f"missing StrategyPayload fields: {missing}")
        result = cls(**payload)
        if supplied_hash is not None and supplied_hash != result.payload_hash:
            raise ValueError("payload_hash does not match StrategyPayload content")
        return result


def payload_by_code(asset: str, code: str) -> StrategyPayload:
    if code not in PAYLOAD_CODES:
        raise ValueError(f"unknown E-I payload code: {code}")
    has_bias = code in {"F", "G", "H", "I"}
    session = {"G": "asia", "H": "london", "I": "us"}.get(code, "all")
    return StrategyPayload(
        asset=asset,
        timeframe="3min",
        strategy_family="liquidity_sweep_confirmation",
        payload_code=code,
        direction="long_short",
        entry_level="M15 liquidity levels",
    entry_criterion={
        "criterion_type": "entry",
        "rule_id": "m1_liquidity_sweep_engulfing_m3_close_confirmation",
        "parameters": {},
    },
        bias_filter="directional_mtf_bias" if has_bias else "none",
        time_filter="session_window" if session != "all" else "none",
        session=session,
        exit_criterion={
            "criterion_type": "exit",
            "rule_id": "fixed_horizon",
            "parameters": {"horizon_bars": 10, "bar_minutes": 3},
        },
        risk_model="fixed_fractional_native_mvp",
        sizing_model="unit_notional_native_mvp",
        parameters={
            "horizon_bars": 10,
            "expiry_days": 3,
            "lq_tf_minutes": 15,
            "sweep_window_mins": 240,
            "window_back": 10,
            "window_fwd": 10,
            "window_m3": 20,
        },
    )


def build_payload_grid(assets: list[str], payload_codes: tuple[str, ...] = PAYLOAD_CODES) -> list[StrategyPayload]:
    return [payload_by_code(asset, code) for asset in assets for code in payload_codes]
