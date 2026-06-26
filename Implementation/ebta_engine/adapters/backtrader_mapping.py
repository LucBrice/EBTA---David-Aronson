"""BACKTRADER adapter boundary definitions.

This local adapter maps an external payload into EBTA artifact names. It does not
read or modify the BACKTRADER repository.
"""

from __future__ import annotations

REQUIRED_EXTERNAL_KEYS = {
    "config",
    "registry_events",
    "oos_access_events",
    "orders",
    "fills",
    "positions",
    "nav",
    "gate_reports",
}

EBTA_ARTIFACT_MAP = {
    "config": "config.json",
    "registry_events": "registry.jsonl",
    "oos_access_events": "oos_access_log.jsonl",
    "gate_reports": "reports/gates.json",
}

PROCEDURE_INPUT_MAP = {
    "config": ["search_space", "walk_forward", "sealing"],
    "registry_events": ["registry_lineage", "candidate_matrix"],
    "orders": ["returns", "economic_gate"],
    "fills": ["returns", "economic_gate"],
    "positions": ["returns", "detrending", "economic_gate"],
    "nav": ["returns", "oos_confidence_interval", "economic_gate"],
    "gate_reports": ["sealing", "oos_access", "lifecycle"],
    "oos_access_events": ["oos_access"],
}

CONTRACT_ERRORS = {
    "missing_external_key": "External engine did not provide a required EBTA input.",
    "winner_only_matrix": "External engine provided only the selected winner instead of the full Test family.",
    "oos_selection_input": "External engine supplied OOS data to a selection or tie-break procedure.",
    "wrc_reused_for_oos_ci": "External engine attempted to reuse WRC Test bootstrap evidence for OOS estimation.",
}


def validate_external_payload(payload: dict) -> list[str]:
    return sorted(REQUIRED_EXTERNAL_KEYS - set(payload))


def map_payload_to_ebta_artifacts(payload: dict) -> dict:
    missing = validate_external_payload(payload)
    if missing:
        raise ValueError(f"missing external keys: {missing}")
    return {
        "config.json": payload["config"],
        "registry.jsonl": payload["registry_events"],
        "oos_access_log.jsonl": payload["oos_access_events"],
        "reports/execution.json": {
            "orders": payload["orders"],
            "fills": payload["fills"],
            "positions": payload["positions"],
            "nav": payload["nav"],
        },
        "reports/gates.json": payload["gate_reports"],
    }


def procedure_input_requirements() -> dict:
    return {
        "required_external_keys": sorted(REQUIRED_EXTERNAL_KEYS),
        "procedure_input_map": PROCEDURE_INPUT_MAP,
        "contract_errors": CONTRACT_ERRORS,
    }
