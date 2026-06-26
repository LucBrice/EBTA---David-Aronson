"""Build and verify EBTA reproducibility manifests."""

from __future__ import annotations

import json
from pathlib import Path

from ebta_engine.constants import PROTOCOL_VERSION, SCHEMA_VERSION
from ebta_engine.manifests.hash_utils import sha256_file


def build_manifest(package_dir: Path, artifact_paths: list[str], package_stage: str) -> dict:
    config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
    artifacts = [
        {
            "path": path,
            "sha256": sha256_file(package_dir / path),
            **_artifact_metadata(path, package_stage),
        }
        for path in sorted(artifact_paths)
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": config["project_id"],
        "hypothesis_id": config["hypothesis_id"],
        "research_family_id": config["research_family_id"],
        "protocol_version": PROTOCOL_VERSION,
        "package_stage": package_stage,
        "configuration": {
            "config_id": config["config_id"],
            "config_path": "config.json",
            "config_hash": sha256_file(package_dir / "config.json"),
        },
        "data_snapshots": config.get("data_snapshots", []),
        "code_environment": {
            "runtime": "EBTA-ENGINE-0.1.0",
            "language": "python-standard-library-first",
        },
        "random_seeds": _collect_random_seeds(config),
        "walk_forward_schedule": config.get("walk_forward_schedule", []),
        "candidate_registry": {
            "registry_path": "registry.jsonl",
            "research_family_id": config["research_family_id"],
        },
        "test_matrices": ["reports/candidate_matrix.json"],
        "oos_matrices": ["series/oos_primary_returns.json"],
        "gate_reports": ["reports/gates.json"],
        "execution_logs": ["reports/execution.json"],
        "oos_access_logs": ["oos_access_log.jsonl"],
        "artifacts": artifacts,
        "reviewers": ["independent_reviewer"],
        "approvals": ["runtime_fixture_approval"],
    }


def verify_manifest(package_dir: Path, manifest: dict) -> list[str]:
    failures: list[str] = []
    for artifact in manifest.get("artifacts", []):
        path = package_dir / artifact["path"]
        if not path.exists():
            failures.append(f"missing artifact: {artifact['path']}")
            continue
        actual = sha256_file(path)
        if actual != artifact["sha256"]:
            failures.append(f"hash mismatch: {artifact['path']}")
    return failures


def _artifact_metadata(path: str, package_stage: str) -> dict[str, str]:
    if path == "config.json":
        role = "configuration"
        artifact_type = "preregistered_config"
        source = "Protocole/PAQUET D'EXECUTION EBTA.md section 3.1"
    elif path == "registry.jsonl":
        role = "registry"
        artifact_type = "experiment_registry"
        source = "Protocole/PAQUET D'EXECUTION EBTA.md section 3.2; SOP 03"
    elif path == "oos_access_log.jsonl":
        role = "oos_access_log"
        artifact_type = "oos_access_log"
        source = "Protocole/PAQUET D'EXECUTION EBTA.md section 3.3; SOP 10"
    elif path.startswith("reports/"):
        role = "report"
        artifact_type = Path(path).stem
        source = "Protocole/PAQUET D'EXECUTION EBTA.md sections 2, 4, and 6"
    elif path.startswith("series/"):
        role = "series"
        artifact_type = Path(path).stem
        source = "SOP 01; SOP 08; Protocole/PAQUET D'EXECUTION EBTA.md section 5"
    else:
        role = "artifact"
        artifact_type = Path(path).stem
        source = "Protocole/PAQUET D'EXECUTION EBTA.md section 5"
    return {
        "artifact_role": role,
        "artifact_type": artifact_type,
        "source_normative": source,
        "produced_by": "ebta_engine",
        "package_stage": package_stage,
    }


def _collect_random_seeds(config: dict) -> dict:
    plan = config.get("statistical_plan", {})
    return {
        key: value
        for key, value in plan.items()
        if "seed" in key or key.endswith("_replications") or key.endswith("_block_length")
    }
