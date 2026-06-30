"""Small JSON-schema subset validator for EBTA runtime schemas.

Supported keywords are intentionally limited to the schemas in this package:
type, required, properties, items, enum, additionalProperties, minItems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    path: str
    message: str


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[ValidationError]:
    errors: list[ValidationError] = []
    expected_type = schema.get("type")
    if expected_type and not _matches_type(instance, expected_type):
        return [ValidationError(path, f"expected {expected_type}")]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(ValidationError(path, f"expected one of {schema['enum']}"))

    if _schema_includes_type(expected_type, "object"):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(ValidationError(f"{path}.{key}", "missing required property"))
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(ValidationError(f"{path}.{key}", "unexpected property"))

    if _schema_includes_type(expected_type, "array"):
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(ValidationError(path, f"expected at least {min_items} items"))
        item_schema = schema.get("items")
        if item_schema:
            for index, value in enumerate(instance):
                errors.extend(validate(value, item_schema, f"{path}[{index}]"))

    return errors


def _schema_includes_type(expected_type: str | list[str] | None, json_type: str) -> bool:
    if expected_type is None:
        return False
    if isinstance(expected_type, list):
        return json_type in expected_type
    return expected_type == json_type


def _matches_type(instance: Any, expected_type: str | list[str]) -> bool:
    if isinstance(expected_type, list):
        return any(_matches_type(instance, item) for item in expected_type)
    if expected_type == "null":
        return instance is None
    if expected_type == "object":
        return isinstance(instance, dict)
    if expected_type == "array":
        return isinstance(instance, list)
    if expected_type == "string":
        return isinstance(instance, str)
    if expected_type == "boolean":
        return isinstance(instance, bool)
    if expected_type == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected_type == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    return False
