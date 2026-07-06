"""Executable decomposition of reference payloads E to I.

Source: PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF.md Phase 3 and
read-only BACKTRADER audit of strategies/sweep_lq.py.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


PAYLOAD_CODES = ("E", "F", "G", "H", "I")


@dataclass(frozen=True)
class StrategyPayload:
    asset: str
    timeframe: str
    strategy_family: str
    payload_code: str
    direction: str
    entry_level: str
    entry_criterion: str
    bias_filter: str
    time_filter: str
    session: str
    exit_criterion: str
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
        entry_criterion="M1 liquidity sweep plus engulfing with strict M3 close confirmation",
        bias_filter="directional_mtf_bias" if has_bias else "none",
        time_filter="session_window" if session != "all" else "none",
        session=session,
        exit_criterion="fixed_horizon_10x3min_bars",
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
