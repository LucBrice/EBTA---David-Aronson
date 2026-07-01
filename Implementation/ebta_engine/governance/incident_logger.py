"""Append-only G-BIAS incident logger.

Source: SOP 13; Protocole/TEMPLATE - Incident de biais EBTA.md.
Type: CONTRACT_ENCODING.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ebta_engine.schema_validation import ValidationError, validate


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INCIDENT_LOG = IMPLEMENTATION_ROOT / "logs" / "INCIDENT_BIAS.jsonl"
SCHEMA_PATH = Path(__file__).with_name("incident_schema.json")
INCIDENT_SCHEMA_VERSION = "1.0.0"
BLOCKING_SEVERITIES = {"LEVEL_2", "LEVEL_3", "LEVEL_4", "LEVEL_5"}
OPEN_STATUSES = {"OPEN", "FAIL", "INCONCLUSIVE", "BURNED"}


def append_incident(
    incident: dict[str, Any],
    log_path: Path | str | None = None,
) -> dict[str, Any]:
    """Validate and append one incident as a JSONL row.

    The function only appends. It never rewrites, truncates, sorts, or removes
    existing incidents.
    """
    normalized = _normalize_incident(incident)
    errors = validate_incident(normalized)
    if errors:
        details = "; ".join(f"{error.path}: {error.message}" for error in errors)
        raise ValueError(f"Invalid G-BIAS incident: {details}")

    target = Path(log_path) if log_path is not None else DEFAULT_INCIDENT_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(normalized, sort_keys=True, separators=(",", ":")) + "\n")
    return normalized


def load_incidents(
    log_path: Path | str | None = None,
    **filters: str,
) -> list[dict[str, Any]]:
    """Load incidents from JSONL, optionally filtering by exact field values."""
    target = Path(log_path) if log_path is not None else DEFAULT_INCIDENT_LOG
    if not target.exists():
        return []

    incidents: list[dict[str, Any]] = []
    with target.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            incident = json.loads(line)
            errors = validate_incident(incident)
            if errors:
                details = "; ".join(f"{error.path}: {error.message}" for error in errors)
                raise ValueError(f"Invalid incident at line {line_number}: {details}")
            if _matches_filters(incident, filters):
                incidents.append(incident)
    return incidents


def load_open_incidents(
    log_path: Path | str | None = None,
    min_blocking_severity: bool = False,
    **filters: str,
) -> list[dict[str, Any]]:
    """Load incidents whose status can block G-BIAS."""
    incidents = load_incidents(log_path, **filters)
    open_incidents = [incident for incident in incidents if incident["status"] in OPEN_STATUSES]
    if min_blocking_severity:
        return [incident for incident in open_incidents if incident["severity"] in BLOCKING_SEVERITIES]
    return open_incidents


def validate_incident(incident: dict[str, Any]) -> list[ValidationError]:
    """Validate an incident against the EBTA G-BIAS incident schema."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return validate(incident, schema)


def _normalize_incident(incident: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(incident)
    normalized.setdefault("schema_version", INCIDENT_SCHEMA_VERSION)
    normalized.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    return normalized


def _matches_filters(incident: dict[str, Any], filters: dict[str, str]) -> bool:
    return all(incident.get(field) == expected for field, expected in filters.items())
