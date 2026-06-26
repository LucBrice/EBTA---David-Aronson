"""Search-space snapshot construction.

Source: SOP 06 sections 5 and 23; SOP 03 sections 6 and 8.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

from itertools import product
from typing import Any

from ebta_engine.procedures._utils import canonical_json, stable_id


def expand_parameter_grid(parameters: dict[str, list[Any]]) -> list[dict[str, Any]]:
    if not parameters:
        raise ValueError("parameter grid must not be empty")
    keys = sorted(parameters)
    for key in keys:
        if not parameters[key]:
            raise ValueError(f"parameter grid level is empty: {key}")
    return [dict(zip(keys, values)) for values in product(*(parameters[key] for key in keys))]


def canonical_candidate_id(specification: dict[str, Any]) -> str:
    return stable_id("CAND", specification)


def build_search_space_snapshot(
    research_family_id: str,
    fold_id: str,
    parameters: dict[str, list[Any]],
    *,
    base_spec: dict[str, Any] | None = None,
    complexity_key: str = "complexity",
    search_type: str = "parametric",
    no_model_policy: str = "NO_MODEL",
    universe_snapshot_id: str | None = None,
    universe_snapshot_hash: str | None = None,
    budget: dict[str, Any] | None = None,
    stop_rule: str | None = None,
    seeds: list[int] | None = None,
    selection_metric: str | None = None,
    cost_model: str | None = None,
    validity_criteria: list[str] | None = None,
    stability_criteria: list[str] | None = None,
    transfer_rule: str | None = None,
) -> dict[str, Any]:
    base = dict(base_spec or {})
    candidates = []
    for values in expand_parameter_grid(parameters):
        canonical_spec = {**base, "parameters": values}
        candidate = {
            "candidate_id": canonical_candidate_id(canonical_spec),
            "research_family_id": research_family_id,
            "fold_id": fold_id,
            "canonical_spec": canonical_spec,
            "parameters": values,
            "complexity": values.get(complexity_key, 0),
        }
        candidates.append(candidate)
    candidates.sort(key=lambda item: item["candidate_id"])
    preregistration = {
        "universe_snapshot_id": universe_snapshot_id,
        "universe_snapshot_hash": universe_snapshot_hash,
        "budget": budget,
        "stop_rule": stop_rule,
        "seeds": seeds,
        "selection_metric": selection_metric,
        "cost_model": cost_model,
        "validity_criteria": validity_criteria,
        "stability_criteria": stability_criteria,
        "transfer_rule": transfer_rule,
    }
    missing_fields = [key for key, value in preregistration.items() if value in (None, [], {})]
    return {
        "artifact_type": "search_space",
        "research_family_id": research_family_id,
        "fold_id": fold_id,
        "search_type": search_type,
        "candidate_count": len(candidates),
        "canonical_hash": stable_id("SPACE", [candidate["canonical_spec"] for candidate in candidates], 16),
        "no_model_policy": no_model_policy,
        "candidates": candidates,
        "canonical_json": canonical_json([candidate["canonical_spec"] for candidate in candidates]),
        "pre_registration": {**preregistration, "missing_fields": missing_fields},
    }
