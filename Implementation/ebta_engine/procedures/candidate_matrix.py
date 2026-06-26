"""Candidate matrix construction for complete Test-side families.

Source: SOP 03 section 14; SOP 02 sections 4 and 5; SOP 06 section 17.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations

from typing import Any

from ebta_engine.procedures._utils import stable_id


def build_candidate_matrix(
    candidate_series: dict[str, list[float]],
    *,
    dates: list[str] | None = None,
    influential_candidates: list[str] | None = None,
    fold_id: str = "FOLD-001",
) -> dict[str, Any]:
    if not candidate_series:
        raise ValueError("candidate matrix requires at least one candidate")
    columns = sorted(candidate_series)
    lengths = {len(candidate_series[candidate_id]) for candidate_id in columns}
    if len(lengths) != 1:
        raise ValueError("all candidate series must share the same length")
    row_count = lengths.pop()
    if dates is None:
        dates = [str(index) for index in range(row_count)]
    if len(dates) != row_count:
        raise ValueError("dates length must match candidate series length")

    influential = set(influential_candidates or columns)
    missing = sorted(influential.difference(columns))
    if missing:
        raise ValueError(f"influential candidates missing from matrix: {missing}")

    rows = []
    for row_index, date in enumerate(dates):
        rows.append({"date": date, "values": {candidate_id: candidate_series[candidate_id][row_index] for candidate_id in columns}})

    payload = {
        "artifact_type": "candidate_matrix",
        "fold_id": fold_id,
        "candidate_ids": columns,
        "row_count": row_count,
        "rows": rows,
        "complete_family": True,
    }
    payload["matrix_id"] = stable_id("MATRIX", payload, 16)
    return payload

