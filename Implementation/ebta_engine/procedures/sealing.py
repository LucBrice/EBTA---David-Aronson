"""Pre-OOS package sealing checks.

Source: SOP 10 sections 5 and 6; SOP 12 section 3; DN-038.
Type: IMPLEMENTATION_DETAIL.
"""

from __future__ import annotations


def validate_pre_oos_seal(package_stage: str, *, manifest_hash: str, independent_approval: bool) -> dict:
    violations = []
    if package_stage != "PRE_OOS_SEALED":
        violations.append("package_not_pre_oos_sealed")
    if not manifest_hash:
        violations.append("missing_manifest_hash")
    if not independent_approval:
        violations.append("missing_independent_approval")
    return {
        "artifact_type": "sealing_report",
        "status": "PASS" if not violations else "FAIL",
        "violations": violations,
    }

