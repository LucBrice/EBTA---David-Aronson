"""Deterministic schema migrations for EBTA runtime artifacts.

Source: PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md Phase 1.
Type: CONTRACT_ENCODING.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


CURRENT_CONFIG_SCHEMA_VERSION = "1.1.0"
CURRENT_STRATEGY_PAYLOAD_SCHEMA_VERSION = "1.1.0"


def migrate_config_1_0_to_1_1(config: dict[str, Any]) -> dict[str, Any]:
    if config.get("schema_version") != "1.0.0":
        raise ValueError("migrate_config_1_0_to_1_1 expects schema_version 1.0.0")
    migrated = deepcopy(config)
    migrated["schema_version"] = CURRENT_CONFIG_SCHEMA_VERSION

    execution_model = migrated.setdefault("execution_model", {})
    execution_model.setdefault(
        "cost_model",
        {
            "model_id": execution_model.get("central_scenario", "tradable_net"),
            "fill_model": "declared_default",
            "fee_model": "declared_default",
            "commission_per_lot": 0.0,
            "slippage_bps": 0.0,
            "financing_rate_daily": 0.0,
            "impact_model": "none",
            "latency_nanos": 0,
            "prob_fill_on_limit": 1.0,
            "prob_slippage": 0.0,
        },
    )
    execution_model.setdefault(
        "instrument_config",
        {
            "instrument_id": "DECLARED-INSTRUMENT",
            "symbol": "DECLARED",
            "venue": "SIM",
            "price_precision": 2,
            "size_precision": 2,
            "price_increment": "0.01",
            "size_increment": "0.01",
            "margin_init": "0",
            "margin_maint": "0",
            "maker_fee": "0",
            "taker_fee": "0",
        },
    )

    candidate_space = migrated.setdefault("candidate_space", {})
    candidate_space.setdefault("complexity_definition", {"source": "legacy_complexity_field"})
    candidate_space.setdefault("complexity_levels", [0])
    return migrated


def migrate_strategy_payload_1_0_to_1_1(payload: dict[str, Any]) -> dict[str, Any]:
    migrated = deepcopy(payload)
    migrated["payload_version"] = CURRENT_STRATEGY_PAYLOAD_SCHEMA_VERSION
    migrated["entry_criterion"] = _criterion_to_object(migrated.get("entry_criterion"), "entry")
    migrated["exit_criterion"] = _criterion_to_object(migrated.get("exit_criterion"), "exit")
    migrated.pop("payload_hash", None)
    return migrated


def _criterion_to_object(value: Any, criterion_type: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return deepcopy(value)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{criterion_type}_criterion must be a non-empty string or object")
    return {
        "criterion_type": criterion_type,
        "rule_id": value,
        "parameters": {},
    }
