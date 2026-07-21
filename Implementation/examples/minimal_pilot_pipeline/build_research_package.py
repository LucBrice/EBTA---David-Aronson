"""Build a minimal EBTA research_package from deterministic pilot artifacts.

Source: Protocole/PAQUET D'EXECUTION EBTA.md sections 2, 3, 5, and 6.
Type: IMPLEMENTATION_DETAIL / TEST_FIXTURE.

This pilot intentionally stays local to Implementation/. It does not read or
write BACKTRADER and does not create methodological rules.
"""

from __future__ import annotations

import copy
import json
import math
import shutil
import sys
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
if str(IMPLEMENTATION_ROOT) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from ebta_engine.governance import evaluate_bias_gate
from ebta_engine.governance.human_evidence import evidence_gate, normalize_pre_oos_human_evidence
from ebta_engine.manifests.manifest_builder import build_manifest
from ebta_engine.persistence import append_jsonl, atomic_write_json
from ebta_engine.procedures.candidate_matrix import build_candidate_matrix
from ebta_engine.procedures.complexity_selection import select_complexity
from ebta_engine.procedures.data_availability import validate_availability
from ebta_engine.procedures.detrending import detrend_returns
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.procedures.incubation_report import validate_incubation_report, validate_live_deployment_report
from ebta_engine.procedures.lifecycle import deployment_gate, incubation_gate
from ebta_engine.procedures.ml_manifest import build_ml_manifest
from ebta_engine.procedures.monitoring import validate_consultation_log, validate_monitoring_plan
from ebta_engine.procedures.oos_access import authorize_oos_access
from ebta_engine.procedures.oos_confidence_interval import oos_confidence_interval
from ebta_engine.procedures.optimization import optimize_on_train
from ebta_engine.procedures.registry_lineage import review_registry_lineage
from ebta_engine.procedures.reproduction_report import validate_reproduction_report
from ebta_engine.procedures.robustness import robustness_verdict
from ebta_engine.procedures.sealing import validate_pre_oos_seal
from ebta_engine.procedures.search_space import build_search_space_snapshot
from ebta_engine.procedures.walk_forward import validate_walk_forward_schedule
from ebta_engine.procedures.wrc import wrc_test
from ebta_engine.validators.package_validator import validate_package_dir


PILOT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUTS_PATH = PILOT_ROOT / "inputs" / "pilot_inputs.json"
DEFAULT_PACKAGE_SHAPE_PATH = PILOT_ROOT / "inputs" / "package_shape.json"


def load_pilot_inputs(path: Path = DEFAULT_INPUTS_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_package_shape(path: Path = DEFAULT_PACKAGE_SHAPE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_package(
    package_dir: Path,
    *,
    pilot_inputs: dict | None = None,
    package_shape: dict | None = None,
    prepared_pre_oos: bool = False,
    allow_test_fixture_human_evidence: bool = False,
) -> dict:
    pilot_inputs = pilot_inputs or load_pilot_inputs()
    package_shape = package_shape or load_package_shape()
    _validate_pilot_contract(pilot_inputs, package_shape)
    prepare_human_evidence(
        pilot_inputs,
        allow_test_fixture=allow_test_fixture_human_evidence,
    )

    if prepared_pre_oos:
        _validate_prepared_pre_oos_package(package_dir, pilot_inputs)
    else:
        prepare_pre_oos_package(package_dir, pilot_inputs)
    _write_reports(package_dir, pilot_inputs, package_shape)
    if not prepared_pre_oos:
        _write_oos_access_log(package_dir, pilot_inputs)
    _write_series(package_dir, pilot_inputs)
    _write_manifest(package_dir, package_shape)

    return validate_package_dir(package_dir)


def prepare_pre_oos_package(package_dir: Path, pilot_inputs: dict) -> None:
    """Create the durable config and append-only registry before Test execution."""

    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    _write_config(package_dir, pilot_inputs)
    _write_registry(package_dir, pilot_inputs)


def prepare_human_evidence(pilot_inputs: dict, *, allow_test_fixture: bool = False) -> dict:
    normalized = normalize_pre_oos_human_evidence(
        pilot_inputs.get("pre_oos_human_evidence"),
        expected_subjects={
            "registry_review": pilot_inputs["identifiers"]["research_family_id"],
            "pre_oos_approval": pilot_inputs["pre_oos_seal"]["manifest_hash"],
        },
        allow_test_fixture=allow_test_fixture,
    )
    pilot_inputs["_normalized_pre_oos_human_evidence"] = normalized
    return normalized


def _validate_prepared_pre_oos_package(package_dir: Path, pilot_inputs: dict) -> None:
    expected_files = {"config.json", "registry.jsonl", "oos_access_log.jsonl"}
    actual_files = {
        path.relative_to(package_dir).as_posix()
        for path in package_dir.rglob("*")
        if path.is_file()
    } if package_dir.exists() else set()
    if actual_files != expected_files:
        raise ValueError(
            "prepared authorized package must contain exactly config.json, registry.jsonl and oos_access_log.jsonl; "
            f"got {sorted(actual_files)}"
        )
    actual_config = json.loads((package_dir / "config.json").read_text(encoding="utf-8"))
    if actual_config != config_document(pilot_inputs):
        raise ValueError("prepared pre-OOS config does not match current pilot inputs")
    registry_events = [
        json.loads(line)
        for line in (package_dir / "registry.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_count = len(pilot_inputs["walk_forward_schedule"]) * len(_pilot_search_space(pilot_inputs)["candidates"])
    if len(registry_events) != expected_count:
        raise ValueError(f"prepared pre-OOS registry event count mismatch: expected {expected_count}, got {len(registry_events)}")
    if any(event.get("timestamp") != pilot_inputs["registry_timestamp"] for event in registry_events):
        raise ValueError("prepared pre-OOS registry timestamp does not match current pilot inputs")
    access_events = [
        json.loads(line)
        for line in (package_dir / "oos_access_log.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if access_events != pilot_inputs["oos_access_log"]:
        raise ValueError("prepared OOS access log does not match current pilot inputs")


def _validate_pilot_contract(pilot_inputs: dict, package_shape: dict) -> None:
    required_input_keys = {
        "identifiers",
        "data_snapshots",
        "walk_forward_schedule",
        "candidate_space",
        "selection_rule",
        "statistical_plan",
        "execution_model",
        "robustness_plan",
        "oos_opening_gate",
        "incubation_plan",
        "reproducibility_manifest",
        "g_bias_reviewer_report",
    }
    missing_inputs = sorted(required_input_keys - pilot_inputs.keys())
    if missing_inputs:
        raise ValueError(f"pilot input contract missing keys: {missing_inputs}")
    if not package_shape.get("artifact_paths"):
        raise ValueError("package shape must define artifact_paths")


def config_document(pilot_inputs: dict) -> dict:
    """Return the exact configuration document written into the package."""

    identifiers = pilot_inputs["identifiers"]
    search_space = _pilot_search_space(pilot_inputs)
    candidate_space = pilot_inputs["candidate_space"]
    candidate_count = len(search_space["candidates"])
    return {
        "schema_version": "1.1.0",
        "config_id": identifiers["config_id"],
        "project_id": identifiers["project_id"],
        "research_family_id": identifiers["research_family_id"],
        "hypothesis_id": identifiers["hypothesis_id"],
        "process_version_id": identifiers["process_version_id"],
        "protocol_version": identifiers["protocol_version"],
        "data_snapshots": pilot_inputs["data_snapshots"],
        "walk_forward_schedule": pilot_inputs["walk_forward_schedule"],
        "candidate_space": {
            "candidate_count": candidate_count,
            "asset_universe": candidate_space.get("asset_universe", []),
            "asset_selection_axis": candidate_space.get("asset_selection_axis"),
            "asset_selection_rule": candidate_space.get("asset_selection_rule"),
            "asset_candidate_count": search_space.get("asset_candidate_count"),
            "complexity_definition": candidate_space.get("complexity_definition", {"source": "parameter_grid"}),
            "complexity_levels": candidate_space.get(
                "complexity_levels",
                sorted({candidate.get("complexity", 0) for candidate in search_space["candidates"]}),
            ),
        },
        "selection_rule": pilot_inputs["selection_rule"],
        "statistical_plan": pilot_inputs["statistical_plan"],
        "execution_model": pilot_inputs["execution_model"],
        "robustness_plan": {"required_before_oos": pilot_inputs["robustness_plan"]["required_before_oos"]},
        "oos_opening_gate": pilot_inputs["oos_opening_gate"],
        "incubation_plan": pilot_inputs["incubation_plan"],
        "reproducibility_manifest": pilot_inputs["reproducibility_manifest"],
        "pre_oos_human_evidence": _human_evidence(pilot_inputs),
        "document_hash": identifiers["document_hash"],
    }


def _write_config(package_dir: Path, pilot_inputs: dict) -> None:
    atomic_write_json(package_dir / "config.json", config_document(pilot_inputs))


def _write_registry(package_dir: Path, pilot_inputs: dict) -> None:
    identifiers = pilot_inputs["identifiers"]
    actor = pilot_inputs.get("actor", "minimal_pilot_pipeline")
    event_index = 1
    for fold in pilot_inputs["walk_forward_schedule"]:
        for candidate in _pilot_search_space(pilot_inputs)["candidates"]:
            append_jsonl(
                package_dir / "registry.jsonl",
                {
                    "schema_version": "1.0.0",
                    "event_id": f"EVT-PILOT-{event_index:03d}",
                    "timestamp": pilot_inputs["registry_timestamp"],
                    "actor": actor,
                    "event_type": "REGISTER_CANDIDATE",
                    "project_id": identifiers["project_id"],
                    "research_family_id": identifiers["research_family_id"],
                    "candidate_id": candidate["candidate_id"],
                    "run_id": f"RUN-PILOT-{event_index:03d}",
                    "fold_id": fold["fold_id"],
                    "data_snapshot_id": pilot_inputs["data_snapshots"][0]["data_snapshot_id"],
                    "input_hashes": [
                        f"config_hash:{identifiers['document_hash']}",
                        f"data_hash:{pilot_inputs['data_snapshots'][0]['data_snapshot_id']}",
                    ],
                    "output_hashes": [
                        f"code_hash:{pilot_inputs['reproduction_report']['environment']['code_commit_hash']}",
                    ],
                    "decision_status": "PASS",
                    "evidence_path": "reports/candidate_matrix.json",
                    "parent_event_id": "",
                    "chain_hash": f"CHAIN-PILOT-{event_index:03d}",
                },
            )
            event_index += 1


def _write_oos_access_log(package_dir: Path, pilot_inputs: dict) -> None:
    for event in pilot_inputs["oos_access_log"]:
        append_jsonl(package_dir / "oos_access_log.jsonl", event)


def _g9_gate_value(statistical_gate: str) -> str:
    if statistical_gate == "PASS":
        return "PASS"
    return "INCONCLUSIVE"


def _gate_verdict(value: object) -> str:
    if value == "PASS":
        return "PASS"
    if value == "FAIL":
        return "FAIL"
    return "INCONCLUSIVE"


def _g8_oos_access_gate(oos_access_decision: dict) -> str:
    if oos_access_decision.get("status") == "AUTHORIZED":
        return "PASS"
    if oos_access_decision.get("status") == "DENIED":
        return "INCONCLUSIVE"
    return "INCONCLUSIVE"


def _g6_cost_model_gate(pilot_inputs: dict, execution_report: dict) -> str:
    declared_cost_model = pilot_inputs.get("execution_model", {}).get("cost_model")
    declared_model_id = (
        declared_cost_model.get("model_id")
        if isinstance(declared_cost_model, dict)
        else declared_cost_model
    )
    reported_model_id = execution_report.get("cost_model")
    if not declared_model_id or not reported_model_id:
        return "INCONCLUSIVE"
    if reported_model_id != declared_model_id:
        return "FAIL"
    return "PASS"


def _g6_capacity_grid_gate(economic_report: dict) -> str:
    failures = set(economic_report.get("failures", []))
    capacity_grid = economic_report.get("capacity_grid", [])
    if "capacity_pass" in failures:
        return "FAIL"
    if "capacity_grid" in failures or not capacity_grid:
        return "INCONCLUSIVE"
    return "PASS"


def _read_jsonl_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def _registered_candidates_from_registry(package_dir: Path) -> list[str]:
    events = _read_jsonl_events(package_dir / "registry.jsonl")
    return sorted(
        {
            event["candidate_id"]
            for event in events
            if event.get("event_type") == "REGISTER_CANDIDATE" and event.get("candidate_id")
        }
    )


def _registry_lineage_events(package_dir: Path) -> list[dict]:
    events = _read_jsonl_events(package_dir / "registry.jsonl")
    return [event for event in events if event.get("parent_candidate_ids")]


def _presence_gate(report: dict, required_keys: list[str]) -> str:
    if not report:
        return "INCONCLUSIVE"
    return "PASS" if all(report.get(key) not in (None, "", [], {}) for key in required_keys) else "INCONCLUSIVE"


def _g2_registry_initialized_gate(registry_review: dict, registered_candidates: list[str]) -> str:
    if not registered_candidates:
        return "INCONCLUSIVE"
    return _gate_verdict(registry_review.get("status"))


def _g2_candidate_catalog_gate(search_space: dict) -> str:
    return _presence_gate(search_space, ["candidates", "candidate_count", "canonical_hash"])


def _g2_local_matrix_gate(candidate_matrix: dict, registry_review: dict) -> str:
    if registry_review.get("status") == "FAIL":
        return "FAIL"
    if candidate_matrix.get("complete_family") is not True:
        return "INCONCLUSIVE"
    return _presence_gate(candidate_matrix, ["candidate_ids", "rows", "matrix_id"])


def _g3_selection_rule_gate(complexity_selection: dict) -> str:
    if complexity_selection.get("status") != "PASS":
        return "INCONCLUSIVE"
    return _presence_gate(complexity_selection, ["selection_rule", "selected_candidate_id"])


def _g3_train_calibration_gate(optimization_log: dict, ml_manifest: dict) -> str:
    if optimization_log.get("source_segment") != "Train_k" or ml_manifest.get("train_segment") != "Train_k":
        return "FAIL"
    evaluations = optimization_log.get("evaluations", [])
    if not evaluations:
        return "INCONCLUSIVE"
    if any(entry.get("status") != "EVALUATED" for entry in evaluations):
        return "INCONCLUSIVE"
    return _presence_gate(ml_manifest, ["manifest_id", "selection_rule", "transformations"])


def _g4_wrc_report_gate(wrc_report: dict) -> str:
    return _presence_gate(wrc_report, ["candidate_ids", "verdict", "wrc_pvalue", "family_catalogue_hash"])


def _g4_wrc_family_matrix_gate(wrc_report: dict, candidate_matrix: dict) -> str:
    wrc_candidates = sorted(wrc_report.get("candidate_ids", []))
    matrix_candidates = sorted(candidate_matrix.get("candidate_ids", []))
    if not wrc_candidates or not matrix_candidates:
        return "INCONCLUSIVE"
    return "PASS" if wrc_candidates == matrix_candidates else "FAIL"


def _g5_robustness_report_gate(robustness_report: dict) -> str:
    return _presence_gate(robustness_report, ["artifact_type", "status", "classification_counts"])


def _g5_robustness_matrix_gate(robustness_report: dict) -> str:
    counts = robustness_report.get("classification_counts", {})
    expected_classes = {"CENTRAL", "PLAUSIBLE_BASE", "EXTREME"}
    if not counts:
        return "INCONCLUSIVE"
    return "PASS" if expected_classes.issubset(counts) else "INCONCLUSIVE"


def _test_reports_gate(procedure_reports: dict) -> str:
    required_reports = {
        "candidate_matrix": ["candidate_ids", "rows", "matrix_id"],
        "wrc": ["candidate_ids", "verdict", "wrc_pvalue"],
        "robustness": ["artifact_type", "status"],
        "economic": ["artifact_type", "statistical_status", "economic_status", "global_status"],
    }
    for report_name, keys in required_reports.items():
        if _presence_gate(procedure_reports.get(report_name, {}), keys) != "PASS":
            return "INCONCLUSIVE"
    return "PASS"


def _min_annualized_return_threshold(economic_gate: dict, *, sessions_per_year: int = 252) -> float:
    thresholds = economic_gate.get("thresholds", {})
    if "min_annualized_return" in thresholds:
        return float(thresholds["min_annualized_return"])
    if "minimum_mean_return" in thresholds:
        return math.expm1(sessions_per_year * float(thresholds["minimum_mean_return"]))
    raise KeyError("economic_gate.thresholds must define min_annualized_return or minimum_mean_return")


def _pre_oos_sealing_report(pilot_inputs: dict) -> dict:
    seal_inputs = dict(pilot_inputs["pre_oos_seal"])
    seal_inputs["independent_approval"] = evidence_gate(
        _human_evidence(pilot_inputs),
        "pre_oos_approval",
    ) == "PASS"
    fixture_sealed_at = seal_inputs.pop("fixture_sealed_at", None)
    clock = None
    if fixture_sealed_at is not None:
        fixture_time = datetime.fromisoformat(fixture_sealed_at.replace("Z", "+00:00"))
        if fixture_time.tzinfo is None or fixture_time.utcoffset() is None:
            raise ValueError("pre_oos_seal.fixture_sealed_at must be timezone-aware")
        clock = lambda: fixture_time
    return validate_pre_oos_seal(**seal_inputs, clock=clock)


def _oos_openings_from_wrc(schedule: list[dict], local_wrc_reports: list[dict]) -> list[dict]:
    status_by_fold = {
        report["fold_id"]: report.get("verdict", "INCONCLUSIVE")
        for report in local_wrc_reports
    }
    return [
        {
            "fold_id": fold["fold_id"],
            "wrc_local_status": status_by_fold.get(fold["fold_id"], "INCONCLUSIVE"),
        }
        for fold in schedule
    ]


def _identifier_evidence_gate(value: object) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else "INCONCLUSIVE"


def _boolean_evidence_gate(value: object) -> str:
    if value is True:
        return "PASS"
    if value is False:
        return "FAIL"
    return "INCONCLUSIVE"


def _artifact_evidence_gate(package_dir: Path, package_shape: dict, evidence_name: str) -> str:
    mapping = package_shape.get("gate_evidence_paths", {})
    relative_path = mapping.get(evidence_name) if isinstance(mapping, dict) else None
    if not isinstance(relative_path, str) or not relative_path.strip():
        return "INCONCLUSIVE"
    if relative_path not in package_shape.get("artifact_paths", []):
        return "INCONCLUSIVE"
    candidate = Path(relative_path)
    if candidate.is_absolute():
        return "FAIL"
    package_root = package_dir.resolve()
    resolved = (package_dir / candidate).resolve()
    try:
        resolved.relative_to(package_root)
    except ValueError:
        return "FAIL"
    return "PASS" if resolved.is_file() else "INCONCLUSIVE"


def _write_reports(package_dir: Path, pilot_inputs: dict, package_shape: dict) -> None:
    identifiers = pilot_inputs["identifiers"]
    procedure_reports = _procedure_reports(pilot_inputs, package_dir=package_dir)
    candidate_ids = procedure_reports["candidate_matrix"]["candidate_ids"]
    oos_gate_value = _g9_gate_value(procedure_reports["oos"]["statistical_gate"])
    power_gate_value = _g9_gate_value(procedure_reports["oos"]["power_check"]["status"])
    data_availability_status = procedure_reports["data_availability"]["status"]
    sealing_status = procedure_reports["sealing"]["status"]
    reproduction_status = procedure_reports["reproduction_validation"]["status"]
    monitoring_plan_status = procedure_reports["monitoring_plan"]["status"]
    monitoring_consultation_status = procedure_reports["monitoring_consultation_log"]["status"]
    incubation_report_status = procedure_reports["incubation_report"]["status"]
    deployment_gate_status = procedure_reports["deployment_gate"]["status"]
    execution_status = _gate_verdict(procedure_reports["execution"].get("status"))
    nav_reconciliation_status = _gate_verdict(procedure_reports["execution"].get("nav_reconciliation"))
    cost_model_status = _g6_cost_model_gate(pilot_inputs, procedure_reports["execution"])
    capacity_grid_status = _g6_capacity_grid_gate(procedure_reports["economic"])
    registry_review = procedure_reports["registry_review"]
    registered_candidates = procedure_reports["registered_candidates"]
    search_space = procedure_reports["search_space"]
    candidate_matrix = procedure_reports["candidate_matrix"]
    wrc = procedure_reports["wrc"]
    local_wrc_reports = procedure_reports["wrc_local_reports"]
    robustness = procedure_reports["robustness"]
    economic = procedure_reports["economic"]
    oos_access_gate = _g8_oos_access_gate(procedure_reports["oos_access_decision"])
    gates = {
        "config_id": identifiers["config_id"],
        "project_id": identifiers["project_id"],
        "research_family_id": identifiers["research_family_id"],
        "hypothesis_id": identifiers["hypothesis_id"],
        "process_version_id": identifiers["process_version_id"],
        "template_hash": identifiers["template_hash"],
        "data_snapshots": data_availability_status,
        "availability_timestamps": data_availability_status,
        "anti_leakage_report": data_availability_status,
        "registry_initialized": _g2_registry_initialized_gate(registry_review, registered_candidates),
        "candidate_catalog": _g2_candidate_catalog_gate(search_space),
        "local_matrix": _g2_local_matrix_gate(candidate_matrix, registry_review),
        "independent_registry_review": evidence_gate(_human_evidence(pilot_inputs), "registry_review"),
        "selection_rule": _g3_selection_rule_gate(procedure_reports["complexity_selection"]),
        "train_only_calibration_log": _g3_train_calibration_gate(
            procedure_reports["optimization_log"],
            procedure_reports["ml_manifest"],
        ),
        "selected_candidate_id": procedure_reports["complexity_selection"]["selected_candidate_id"],
        "wrc_report": _g4_wrc_report_gate(wrc),
        "wrc_status": wrc["verdict"],
        "wrc_family_matrix": _g4_wrc_family_matrix_gate(wrc, candidate_matrix),
        "robustness_report": _g5_robustness_report_gate(robustness),
        "robustness_matrix": _g5_robustness_matrix_gate(robustness),
        "pre_oos_robustness_verdict": robustness["status"],
        "execution_report": execution_status,
        "cost_model": cost_model_status,
        "capacity_grid": capacity_grid_status,
        "nav_reconciliation": nav_reconciliation_status,
        "pre_oos_manifest": sealing_status,
        "frozen_config": sealing_status,
        "test_reports": _test_reports_gate(procedure_reports),
        "independent_pre_oos_approval": evidence_gate(_human_evidence(pilot_inputs), "pre_oos_approval"),
        "oos_access_log": oos_access_gate,
        "opening_authorization": oos_access_gate,
        "single_oos_execution_log": oos_access_gate,
        "oos_report": oos_gate_value,
        "concatenated_oos_series": oos_gate_value,
        "oos_bootstrap_report": oos_gate_value,
        "power_report": power_gate_value,
        "economic_report": _gate_verdict(economic.get("economic_status")),
        "statistical_gate_report": _gate_verdict(economic.get("statistical_status")),
        "economic_gate_report": _gate_verdict(economic.get("global_status")),
        "validation_ready_manifest": reproduction_status,
        "reproduction_report": reproduction_status,
        "incubation_approval": reproduction_status,
        "incubation_report": incubation_report_status,
        "paper_trading_log": monitoring_consultation_status,
        "monitoring_plan": monitoring_plan_status,
        "deployment_certified_manifest": deployment_gate_status,
        "live_version_id": _identifier_evidence_gate(pilot_inputs["live_deployment_report"].get("live_version_id")),
        "kill_switch": _boolean_evidence_gate(pilot_inputs["live_deployment_report"].get("kill_switch_tested")),
        "live_approval": True,
        "lifecycle_archive": _artifact_evidence_gate(package_dir, package_shape, "lifecycle_archive"),
        "incident_log": _artifact_evidence_gate(package_dir, package_shape, "incident_log"),
        "retention_policy": _artifact_evidence_gate(package_dir, package_shape, "retention_policy"),
    }
    invariant_evidence = {
        "oos_segments": [
            {"id": f"OOS-{index:03d}", "start": fold["oos"][0], "end": fold["oos"][1]}
            for index, fold in enumerate(pilot_inputs["walk_forward_schedule"], start=1)
        ],
        "pre_oos_sealed_at": procedure_reports["sealing"].get("sealed_at"),
        "oos_access_log": [
            {"timestamp": event["timestamp"], "fold_id": event["fold_id"]}
            for event in pilot_inputs["oos_access_log"]
        ],
        "oos_openings": _oos_openings_from_wrc(
            pilot_inputs["walk_forward_schedule"],
            local_wrc_reports,
        ),
        "influential_candidates": candidate_ids,
        "registered_candidates": candidate_ids,
        "applicable_candidates": candidate_ids,
        "wrc_matrix_candidates": procedure_reports["wrc"]["candidate_ids"],
        "asset_selection_axis": procedure_reports["search_space"].get("asset_selection_axis"),
        "asset_universe": procedure_reports["search_space"].get("asset_universe"),
        "candidate_assets": procedure_reports["search_space"].get("candidate_asset_map"),
        "transformation_fits": [
            dict(transformation)
            for transformation in procedure_reports["ml_manifest"]["transformations"]
        ],
        "decision_events": [
            {
                "decision_at": event["decision_at"],
                "data_available_at": event["available_at"],
            }
            for event in pilot_inputs["data_availability_checks"]
        ],
        "expected_oos_days": [row["date"] for row in pilot_inputs["oos_primary_returns"]],
        "oos_series_days": [
            {"date": row["date"], "status": row.get("status", "EXPOSED")}
            for row in pilot_inputs["oos_primary_returns"]
        ],
        "bootstrap_sources": {"oos": "OOS_STATIONARY_BLOCK", "wrc_test": "WRC_JOINT_ZERO_CENTERED"},
        "gate_reports": {
            "statistical": "PASS",
            "economic": "PASS",
            "final": "PASS",
            "final_components": ["statistical", "economic"],
        },
        "robustness_checks": [{"name": "stress_pre_oos", "uses_observed_oos": False}],
        "same_oos_reruns": [{"rerun_id": "RERUN-TECH-001", "post_mortem_id": "PM-001"}],
        "influential_modifications": [
            {"modification_id": "MOD-001", "creates_new_candidate_or_version": True}
        ],
        "package_stages": [
            "PRE_OOS_SEALED",
            "VALIDATION_READY",
            "INCUBATION_STARTED",
            "DEPLOYMENT_CERTIFIED",
            "LIVE_LIMITED_STARTED",
        ],
        "manifest_hash_failures": [],
    }
    static_reports = {
        "gates.json": gates,
        "invariant_evidence.json": invariant_evidence,
        "wrc.json": _compact_wrc_report_with_locals(
            procedure_reports["wrc"],
            local_wrc_reports,
        ),
        "robustness.json": procedure_reports["robustness"],
        "oos.json": _compact_oos_report(procedure_reports["oos"]),
        "economic.json": procedure_reports["economic"],
        "execution.json": procedure_reports["execution"],
        "reproduction.json": pilot_inputs["reproduction_report"],
        "reproduction_validation.json": procedure_reports["reproduction_validation"],
        "sealing.json": procedure_reports["sealing"],
        "oos_access_decision.json": procedure_reports["oos_access_decision"],
        "monitoring_plan.json": procedure_reports["monitoring_plan"],
        "monitoring_consultation_log.json": procedure_reports["monitoring_consultation_log"],
        "incubation_report.json": procedure_reports["incubation_report"],
        "incubation_gate.json": procedure_reports["incubation_gate"],
        "live_deployment.json": procedure_reports["live_deployment"],
        "deployment_gate.json": procedure_reports["deployment_gate"],
        "search_space.json": procedure_reports["search_space"],
        "optimization_log.json": procedure_reports["optimization_log"],
        "ml_manifest.json": procedure_reports["ml_manifest"],
        "complexity_selection.json": procedure_reports["complexity_selection"],
        "candidate_matrix.json": procedure_reports["candidate_matrix"],
        "data_availability.json": procedure_reports["data_availability"],
        "fold_schedule.json": procedure_reports["fold_schedule"],
        "registry_review.json": procedure_reports["registry_review"],
        "detrending.json": procedure_reports["detrending"],
        "g_bias.json": procedure_reports["g_bias"],
    }
    for filename, payload in static_reports.items():
        atomic_write_json(package_dir / "reports" / filename, payload)


def _pre_oos_reports(pilot_inputs: dict) -> dict:
    search_space = _pilot_search_space(pilot_inputs)
    candidate_ids = [candidate["candidate_id"] for candidate in search_space["candidates"]]
    statistical_plan = pilot_inputs["statistical_plan"]
    train_scores = _scores_by_rank(candidate_ids, pilot_inputs["train_scores_by_rank"])
    optimization_log = optimize_on_train(search_space, train_scores)
    representatives = optimization_log["representatives"]
    test_scores = _scores_by_rank(
        [representative["candidate_id"] for representative in representatives],
        pilot_inputs["representative_test_scores_by_rank"],
    )
    complexity_selection = select_complexity(representatives, test_scores)
    candidate_returns = _scores_by_rank(candidate_ids, pilot_inputs["candidate_test_returns_by_rank"])
    candidate_matrix = build_candidate_matrix(
        candidate_returns,
        dates=pilot_inputs["candidate_test_dates"],
        influential_candidates=candidate_ids,
        asset_universe=search_space.get("asset_universe"),
        candidate_assets=search_space.get("candidate_asset_map"),
        fold_id=_fold_scope_id(pilot_inputs["walk_forward_schedule"]),
    )
    wrc = wrc_test(
        candidate_returns,
        replications=statistical_plan["wrc_bootstrap_replications"],
        mean_block_length=statistical_plan["wrc_mean_block_length"],
        seed=statistical_plan["wrc_seed"],
        alpha=statistical_plan["wrc_alpha"],
        run_secondary=statistical_plan.get("wrc_run_secondary", True),
    )
    local_wrc_reports = _local_wrc_reports(
        candidate_returns,
        dates=pilot_inputs["candidate_test_dates"],
        schedule=pilot_inputs["walk_forward_schedule"],
        statistical_plan=statistical_plan,
    )
    robustness = robustness_verdict(pilot_inputs["robustness_plan"]["scenarios"])
    sealing = _pre_oos_sealing_report(pilot_inputs)
    g_bias = _g_bias_report(pilot_inputs, search_space, candidate_matrix, robustness)
    access_request = _oos_access_request(pilot_inputs, wrc, robustness, sealing, g_bias)
    if sealing.get("sealed_at"):
        access_request["timestamp"] = sealing["sealed_at"]
    oos_access_decision = authorize_oos_access(access_request)
    reports: dict[str, Any] = {
        "search_space": search_space,
        "optimization_log": optimization_log,
        "complexity_selection": complexity_selection,
        "candidate_matrix": candidate_matrix,
        "wrc": wrc,
        "wrc_local_reports": local_wrc_reports,
        "robustness": robustness,
        "sealing": sealing,
        "g_bias": g_bias,
        "oos_access_decision": oos_access_decision,
    }
    reports["content_hash"] = _stable_payload_hash(reports)
    return reports


def cache_pre_oos_reports(pilot_inputs: dict, reports: dict) -> None:
    cached = copy.deepcopy(reports)
    expected_hash = cached.pop("content_hash", None)
    actual_hash = _stable_payload_hash(cached)
    if expected_hash != actual_hash:
        raise ValueError("pre-OOS report content hash mismatch")
    cached["content_hash"] = expected_hash
    pilot_inputs["_pre_oos_reports"] = cached


def _resolved_pre_oos_reports(pilot_inputs: dict) -> dict:
    cached = pilot_inputs.get("_pre_oos_reports")
    if cached is None:
        return _pre_oos_reports(pilot_inputs)
    reports = copy.deepcopy(cached)
    expected_hash = reports.pop("content_hash", None)
    if expected_hash != _stable_payload_hash(reports):
        raise ValueError("cached pre-OOS reports were mutated after authorization")
    reports["content_hash"] = expected_hash
    return reports


def _procedure_reports(pilot_inputs: dict, *, package_dir: Path | None = None) -> dict:
    pre_oos = _resolved_pre_oos_reports(pilot_inputs)
    search_space = pre_oos["search_space"]
    candidate_matrix = pre_oos["candidate_matrix"]
    wrc = pre_oos["wrc"]
    local_wrc_reports = pre_oos["wrc_local_reports"]
    robustness = pre_oos["robustness"]
    sealing = pre_oos["sealing"]
    g_bias = pre_oos["g_bias"]
    oos_access_decision = pre_oos["oos_access_decision"]
    statistical_plan = pilot_inputs["statistical_plan"]
    registered_candidates = _registered_candidates_from_registry(package_dir) if package_dir is not None else []
    lineage_events = _registry_lineage_events(package_dir) if package_dir is not None else []
    ml_inputs = pilot_inputs["ml_manifest"]
    ml_manifest = build_ml_manifest(
        ml_inputs["ml_id"],
        train_segment=ml_inputs["train_segment"],
        features=ml_inputs["features"],
        transformations=ml_inputs["transformations"],
        hyperparameters=ml_inputs["hyperparameters"],
        seeds=ml_inputs["seeds"],
        complexity_levels=ml_inputs["complexity_levels"],
        selection_rule=ml_inputs["selection_rule"],
    )
    detrending_inputs = pilot_inputs["detrending"]
    detrending = detrend_returns(
        detrending_inputs["portfolio_returns"],
        detrending_inputs["benchmark_returns"],
        detrending_inputs["cash_returns"],
        detrending_inputs["betas"],
        segment_id=detrending_inputs["segment_id"],
    )
    oos = oos_confidence_interval(
        pilot_inputs["oos_returns"],
        replications=statistical_plan["oos_bootstrap_replications"],
        mean_block_length=statistical_plan["oos_mean_block_length"],
        seed=statistical_plan["oos_seed"],
        pre_oos_development_returns=pilot_inputs["pre_oos_development_returns"],
        min_annualized_return=_min_annualized_return_threshold(pilot_inputs["economic_gate"]),
    )
    economic_gate_evidence = {
        **pilot_inputs["economic_gate"],
        "statistical_status": wrc["verdict"],
    }
    economic = economic_gate_report(economic_gate_evidence)
    monitoring_plan = validate_monitoring_plan(pilot_inputs["incubation_plan"]["monitoring"])
    monitoring_consultation_log = validate_consultation_log(
        pilot_inputs["monitoring_consultations"],
        max_consultations=pilot_inputs["incubation_plan"]["monitoring"].get("max_consultations"),
        alpha_spending_function=pilot_inputs["incubation_plan"]["monitoring"].get("alpha_spending_function"),
    )
    incubation_report = validate_incubation_report(pilot_inputs["incubation_report"])
    live_deployment = validate_live_deployment_report(pilot_inputs["live_deployment_report"])
    reproduction_validation = validate_reproduction_report(
        pilot_inputs["reproduction_report"],
        original_manifest={"artefact_hashes": pilot_inputs["reproduction_report"]["reproduced_artefact_hashes"]},
    )
    incubation_gate_report = incubation_gate(
        {
            "statistical_status": wrc["verdict"],
            "economic_status": economic["economic_status"],
            "robustness_status": robustness["status"],
            "execution_status": pilot_inputs["execution_report"]["status"],
            "package_stage": pilot_inputs["reproducibility_manifest"]["package_stage"],
            "reproduction_status": reproduction_validation["status"],
        }
    )
    deployment_gate_report = deployment_gate(
        {
            "paper_trading_status": incubation_report["status"],
            "package_stage": pilot_inputs["live_deployment_report"]["package_stage"],
            "kill_switch_tested": pilot_inputs["live_deployment_report"]["kill_switch_tested"],
            "live_approval": True,
        }
    )
    return {
        "search_space": search_space,
        "optimization_log": pre_oos["optimization_log"],
        "ml_manifest": ml_manifest,
        "complexity_selection": pre_oos["complexity_selection"],
        "candidate_matrix": candidate_matrix,
        "wrc": wrc,
        "wrc_local_reports": local_wrc_reports,
        "oos": oos,
        "economic": economic,
        "robustness": robustness,
        "g_bias": g_bias,
        "execution": pilot_inputs["execution_report"],
        "reproduction_validation": reproduction_validation,
        "sealing": sealing,
        "oos_access_decision": oos_access_decision,
        "monitoring_plan": monitoring_plan,
        "monitoring_consultation_log": monitoring_consultation_log,
        "incubation_report": incubation_report,
        "incubation_gate": incubation_gate_report,
        "live_deployment": live_deployment,
        "deployment_gate": deployment_gate_report,
        "detrending": detrending,
        "data_availability": validate_availability(pilot_inputs["data_availability_checks"]),
        "fold_schedule": validate_walk_forward_schedule(
            pilot_inputs["walk_forward_schedule"],
            information_stop_criterion=pilot_inputs["information_stop_criterion"],
        ),
        "registered_candidates": registered_candidates,
        "registry_review": review_registry_lineage(
            registered_candidates,
            candidate_matrix["candidate_ids"],
            lineage_events=lineage_events,
        ),
    }


def _oos_access_request(pilot_inputs: dict, wrc: dict, robustness: dict, sealing: dict, g_bias: dict) -> dict:
    template = pilot_inputs.get("oos_access_template")
    if template is None:
        access_log = pilot_inputs.get("oos_access_log", [])
        if not access_log:
            raise ValueError("pilot inputs require oos_access_template before authorization")
        template = access_log[0]
    return {
        **template,
        "pre_oos_sealed": sealing["status"] == "PASS",
        "wrc_pass": wrc.get("verdict") == "PASS",
        "robustness_pass": robustness["status"] == "PASS",
        "execution_pass": pilot_inputs["execution_report"]["status"] == "PASS",
        "independent_approval": evidence_gate(
            _human_evidence(pilot_inputs),
            "pre_oos_approval",
        ) == "PASS",
        "bias_gate_pass": g_bias["status"] == "PASS",
    }


def _g_bias_report(pilot_inputs: dict, search_space: dict, candidate_matrix: dict, robustness: dict) -> dict:
    candidate_ids = [candidate["candidate_id"] for candidate in search_space["candidates"]]
    decision_lock = _decision_lock_payload(pilot_inputs)
    return evaluate_bias_gate(
        candidate_registry=_registry_events(pilot_inputs, candidate_ids),
        statistical_family_matrix=candidate_matrix,
        preregistration_manifest=decision_lock,
        executed_configuration=decision_lock,
        robustness_plan=pilot_inputs["robustness_plan"],
        robustness_matrix=robustness,
        oos_access_log=pilot_inputs["oos_access_log"],
        incident_log=pilot_inputs.get("bias_incidents", []),
        reviewer_report=pilot_inputs["g_bias_reviewer_report"],
    )


def _decision_lock_payload(pilot_inputs: dict) -> dict:
    return {
        "primary_metric": pilot_inputs["candidate_space"]["selection_metric"],
        "secondary_metrics": pilot_inputs["candidate_space"].get("stability_criteria", []),
        "economic_hurdle": pilot_inputs["economic_gate"]["thresholds"],
        "benchmark": pilot_inputs["detrending"].get("benchmark_id", "cash_plus_benchmark_returns"),
        "cost_model": pilot_inputs["candidate_space"]["cost_model"],
        "slippage_model": pilot_inputs["execution_model"].get("slippage_model", "pilot_fixed_spread"),
        "execution_assumptions": pilot_inputs["execution_model"],
    }


def _human_evidence(pilot_inputs: dict) -> dict:
    normalized = pilot_inputs.get("_normalized_pre_oos_human_evidence")
    if not isinstance(normalized, dict):
        normalized = prepare_human_evidence(pilot_inputs)
    return normalized


def _registry_events(pilot_inputs: dict, candidate_ids: list[str]) -> list[dict[str, object]]:
    identifiers = pilot_inputs["identifiers"]
    return [
        {
            "run_id": f"RUN-PILOT-{fold_index:03d}-{index:03d}",
            "candidate_id": candidate_id,
            "config_hash": identifiers["document_hash"],
            "code_hash": pilot_inputs["reproduction_report"]["environment"]["code_commit_hash"],
            "data_hash": pilot_inputs["data_snapshots"][0]["data_snapshot_id"],
            "decision_status": "PASS",
        }
        for fold_index, _fold in enumerate(pilot_inputs["walk_forward_schedule"], start=1)
        for index, candidate_id in enumerate(candidate_ids, start=1)
    ]


def _pilot_search_space(pilot_inputs: dict) -> dict:
    identifiers = pilot_inputs["identifiers"]
    candidate_space = pilot_inputs["candidate_space"]
    statistical_plan = pilot_inputs["statistical_plan"]
    return build_search_space_snapshot(
        identifiers["research_family_id"],
        _fold_scope_id(pilot_inputs["walk_forward_schedule"]),
        candidate_space["parameter_grid"],
        base_spec=candidate_space["base_spec"],
        universe_snapshot_id=pilot_inputs["data_snapshots"][0]["data_snapshot_id"],
        universe_snapshot_hash=f"{pilot_inputs['data_snapshots'][0]['data_snapshot_id']}-HASH",
        budget=candidate_space["budget"],
        stop_rule=candidate_space["stop_rule"],
        seeds=[statistical_plan["wrc_seed"], statistical_plan["oos_seed"]],
        selection_metric=candidate_space["selection_metric"],
        cost_model=candidate_space["cost_model"],
        asset_universe=candidate_space.get("asset_universe"),
        asset_selection_axis=candidate_space.get("asset_selection_axis"),
        asset_selection_rule=candidate_space.get("asset_selection_rule"),
        validity_criteria=candidate_space["validity_criteria"],
        stability_criteria=candidate_space["stability_criteria"],
        transfer_rule=candidate_space["transfer_rule"],
    )


def _fold_scope_id(schedule: list[dict]) -> str:
    if len(schedule) == 1:
        return schedule[0]["fold_id"]
    return "WF-" + "-".join(fold["fold_id"] for fold in schedule)


def _local_wrc_reports(
    candidate_returns: dict[str, list[float]],
    *,
    dates: list[str],
    schedule: list[dict],
    statistical_plan: dict,
) -> list[dict]:
    reports = []
    for fold in schedule:
        test_start, test_end = fold["test"]
        indices = [
            index
            for index, timestamp in enumerate(dates)
            if test_start <= timestamp[:10] <= test_end
        ]
        if not indices:
            reports.append(
                {
                    "artifact_type": "wrc_report",
                    "fold_id": fold["fold_id"],
                    "verdict": "INCONCLUSIVE",
                    "reason": "no candidate Test observations for fold",
                }
            )
            continue

        fold_returns = {
            candidate_id: [values[index] for index in indices]
            for candidate_id, values in candidate_returns.items()
        }
        report = wrc_test(
            fold_returns,
            replications=statistical_plan["wrc_bootstrap_replications"],
            mean_block_length=statistical_plan["wrc_mean_block_length"],
            seed=statistical_plan["wrc_seed"],
            alpha=statistical_plan["wrc_alpha"],
            run_secondary=False,
        )
        report["fold_id"] = fold["fold_id"]
        reports.append(report)
    return reports


def _scores_by_rank(keys: list[str], values: list) -> dict:
    if len(values) < len(keys):
        raise ValueError(f"not enough pilot values for keys: expected {len(keys)}, got {len(values)}")
    return {key: values[index] for index, key in enumerate(keys)}


def _compact_wrc_report(report: dict) -> dict:
    compact = dict(report)
    distribution = compact.pop("bootstrap_distribution", [])
    compact["bootstrap_distribution_count"] = len(distribution)
    compact["bootstrap_distribution_hash"] = _stable_payload_hash(distribution)
    return compact


def _compact_wrc_report_with_locals(report: dict, local_reports: list[dict]) -> dict:
    compact = _compact_wrc_report(report)
    compact["local_reports"] = [_compact_wrc_report(local_report) for local_report in local_reports]
    return compact


def _compact_oos_report(report: dict) -> dict:
    compact = dict(report)
    bootstrap_means = compact.pop("bootstrap_means", [])
    compact["bootstrap_mean_count"] = len(bootstrap_means)
    compact["bootstrap_means_hash"] = _stable_payload_hash(bootstrap_means)
    return compact


def _stable_payload_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def _write_series(package_dir: Path, pilot_inputs: dict) -> None:
    atomic_write_json(
        package_dir / "series" / "oos_primary_returns.json",
        {"observations": pilot_inputs["oos_primary_returns"]},
    )


def _write_manifest(package_dir: Path, package_shape: dict) -> None:
    manifest = build_manifest(package_dir, package_shape["artifact_paths"], package_shape["package_stage"])
    atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)


def main() -> int:
    package_dir = PILOT_ROOT / "research_package"
    report = build_package(package_dir)
    print(json.dumps({"package_dir": str(package_dir), "status": report["status"]}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
