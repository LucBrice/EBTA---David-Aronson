"""Build a minimal EBTA research_package from deterministic pilot artifacts.

Source: Protocole/PAQUET D'EXECUTION EBTA.md sections 2, 3, 5, and 6.
Type: IMPLEMENTATION_DETAIL / TEST_FIXTURE.

This pilot intentionally stays local to Implementation/. It does not read or
write BACKTRADER and does not create methodological rules.
"""

from __future__ import annotations

import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
if str(IMPLEMENTATION_ROOT) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from ebta_engine.governance import evaluate_bias_gate
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
) -> dict:
    pilot_inputs = pilot_inputs or load_pilot_inputs()
    package_shape = package_shape or load_package_shape()
    _validate_pilot_contract(pilot_inputs, package_shape)

    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    _write_config(package_dir, pilot_inputs)
    _write_registry(package_dir, pilot_inputs)
    _write_reports(package_dir, pilot_inputs)
    _write_oos_access_log(package_dir, pilot_inputs)
    _write_series(package_dir, pilot_inputs)
    _write_manifest(package_dir, package_shape)

    return validate_package_dir(package_dir)


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


def _write_config(package_dir: Path, pilot_inputs: dict) -> None:
    identifiers = pilot_inputs["identifiers"]
    search_space = _pilot_search_space(pilot_inputs)
    candidate_space = pilot_inputs["candidate_space"]
    candidate_count = len(search_space["candidates"])
    atomic_write_json(
        package_dir / "config.json",
        {
            "schema_version": "1.0.0",
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
            },
            "selection_rule": pilot_inputs["selection_rule"],
            "statistical_plan": pilot_inputs["statistical_plan"],
            "execution_model": pilot_inputs["execution_model"],
            "robustness_plan": {"required_before_oos": pilot_inputs["robustness_plan"]["required_before_oos"]},
            "oos_opening_gate": pilot_inputs["oos_opening_gate"],
            "incubation_plan": pilot_inputs["incubation_plan"],
            "reproducibility_manifest": pilot_inputs["reproducibility_manifest"],
            "document_hash": identifiers["document_hash"],
        },
    )


def _write_registry(package_dir: Path, pilot_inputs: dict) -> None:
    identifiers = pilot_inputs["identifiers"]
    actor = pilot_inputs.get("actor", "minimal_pilot_pipeline")
    for index, candidate in enumerate(_pilot_search_space(pilot_inputs)["candidates"], start=1):
        append_jsonl(
            package_dir / "registry.jsonl",
            {
                "schema_version": "1.0.0",
                "event_id": f"EVT-PILOT-{index:03d}",
                "timestamp": "2026-01-01T00:00:00Z",
                "actor": actor,
                "event_type": "REGISTER_CANDIDATE",
                "project_id": identifiers["project_id"],
                "research_family_id": identifiers["research_family_id"],
                "candidate_id": candidate["candidate_id"],
                "run_id": f"RUN-PILOT-{index:03d}",
                "fold_id": pilot_inputs["walk_forward_schedule"][0]["fold_id"],
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
                "chain_hash": f"CHAIN-PILOT-{index:03d}",
            },
        )


def _write_oos_access_log(package_dir: Path, pilot_inputs: dict) -> None:
    for event in pilot_inputs["oos_access_log"]:
        append_jsonl(package_dir / "oos_access_log.jsonl", event)


def _write_reports(package_dir: Path, pilot_inputs: dict) -> None:
    identifiers = pilot_inputs["identifiers"]
    procedure_reports = _procedure_reports(pilot_inputs)
    candidate_ids = procedure_reports["candidate_matrix"]["candidate_ids"]
    gates = {
        "config_id": identifiers["config_id"],
        "project_id": identifiers["project_id"],
        "research_family_id": identifiers["research_family_id"],
        "hypothesis_id": identifiers["hypothesis_id"],
        "process_version_id": identifiers["process_version_id"],
        "template_hash": identifiers["template_hash"],
        "data_snapshots": True,
        "availability_timestamps": True,
        "anti_leakage_report": True,
        "registry_initialized": True,
        "candidate_catalog": True,
        "local_matrix": True,
        "independent_registry_review": True,
        "selection_rule": True,
        "train_only_calibration_log": True,
        "selected_candidate_id": procedure_reports["complexity_selection"]["selected_candidate_id"],
        "wrc_report": True,
        "wrc_status": procedure_reports["wrc"]["verdict"],
        "wrc_family_matrix": True,
        "robustness_report": True,
        "robustness_matrix": True,
        "pre_oos_robustness_verdict": "PASS",
        "execution_report": True,
        "cost_model": True,
        "capacity_grid": True,
        "nav_reconciliation": True,
        "pre_oos_manifest": True,
        "frozen_config": True,
        "test_reports": True,
        "independent_pre_oos_approval": True,
        "oos_access_log": True,
        "opening_authorization": True,
        "single_oos_execution_log": True,
        "oos_report": True,
        "concatenated_oos_series": True,
        "oos_bootstrap_report": True,
        "power_report": True,
        "economic_report": True,
        "statistical_gate_report": True,
        "economic_gate_report": True,
        "validation_ready_manifest": True,
        "reproduction_report": True,
        "incubation_approval": True,
        "incubation_report": True,
        "paper_trading_log": True,
        "monitoring_plan": True,
        "deployment_certified_manifest": True,
        "live_version_id": "LIVE-PILOT-001",
        "kill_switch": True,
        "live_approval": True,
        "lifecycle_archive": True,
        "incident_log": True,
        "retention_policy": True,
    }
    invariant_evidence = {
        "oos_segments": [
            {"id": "OOS-001", "start": "2023-01-01", "end": "2023-12-31"},
            {"id": "OOS-002", "start": "2024-01-01", "end": "2024-12-31"},
        ],
        "pre_oos_sealed_at": "2023-01-01T00:00:00Z",
        "oos_access_log": [{"timestamp": "2023-01-02T00:00:00Z", "fold_id": "FOLD-001"}],
        "oos_openings": [{"fold_id": "FOLD-001", "wrc_local_status": "PASS"}],
        "influential_candidates": candidate_ids,
        "registered_candidates": candidate_ids,
        "applicable_candidates": candidate_ids,
        "wrc_matrix_candidates": procedure_reports["wrc"]["candidate_ids"],
        "asset_selection_axis": procedure_reports["search_space"].get("asset_selection_axis"),
        "asset_universe": procedure_reports["search_space"].get("asset_universe"),
        "candidate_assets": procedure_reports["search_space"].get("candidate_asset_map"),
        "transformation_fits": [{"name": "scaler", "fit_segment": "Train_k"}],
        "decision_events": [
            {"decision_at": "2023-01-02T00:00:00Z", "data_available_at": "2023-01-01T00:00:00Z"}
        ],
        "expected_oos_days": ["2023-01-02", "2023-01-03"],
        "oos_series_days": [
            {"date": "2023-01-02", "status": "EXPOSED"},
            {"date": "2023-01-03", "status": "NO_MODEL"},
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
        "wrc.json": _compact_wrc_report(procedure_reports["wrc"]),
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


def _procedure_reports(pilot_inputs: dict) -> dict:
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
        fold_id=pilot_inputs["walk_forward_schedule"][0]["fold_id"],
    )
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
    wrc = wrc_test(
        candidate_returns,
        replications=statistical_plan["wrc_bootstrap_replications"],
        mean_block_length=statistical_plan["wrc_mean_block_length"],
        seed=statistical_plan["wrc_seed"],
        alpha=statistical_plan["wrc_alpha"],
    )
    oos = oos_confidence_interval(
        pilot_inputs["oos_returns"],
        replications=statistical_plan["oos_bootstrap_replications"],
        mean_block_length=statistical_plan["oos_mean_block_length"],
        seed=statistical_plan["oos_seed"],
    )
    economic = economic_gate_report(pilot_inputs["economic_gate"])
    robustness = robustness_verdict(pilot_inputs["robustness_plan"]["scenarios"])
    sealing = validate_pre_oos_seal(**pilot_inputs["pre_oos_seal"])
    g_bias = _g_bias_report(pilot_inputs, search_space, candidate_matrix, robustness)
    oos_access_decision = authorize_oos_access(_oos_access_request(pilot_inputs, robustness, sealing, g_bias))
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
            "statistical_status": "PASS",
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
        "optimization_log": optimization_log,
        "ml_manifest": ml_manifest,
        "complexity_selection": complexity_selection,
        "candidate_matrix": candidate_matrix,
        "wrc": wrc,
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
        "registry_review": review_registry_lineage(candidate_ids, candidate_ids),
    }


def _oos_access_request(pilot_inputs: dict, robustness: dict, sealing: dict, g_bias: dict) -> dict:
    event = pilot_inputs["oos_access_log"][0]
    return {
        **event,
        "pre_oos_sealed": sealing["status"] == "PASS",
        "wrc_pass": True,
        "robustness_pass": robustness["status"] == "PASS",
        "execution_pass": pilot_inputs["execution_report"]["status"] == "PASS",
        "independent_approval": pilot_inputs["pre_oos_seal"]["independent_approval"],
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


def _registry_events(pilot_inputs: dict, candidate_ids: list[str]) -> list[dict[str, object]]:
    identifiers = pilot_inputs["identifiers"]
    return [
        {
            "run_id": f"RUN-PILOT-{index:03d}",
            "candidate_id": candidate_id,
            "config_hash": identifiers["document_hash"],
            "code_hash": pilot_inputs["reproduction_report"]["environment"]["code_commit_hash"],
            "data_hash": pilot_inputs["data_snapshots"][0]["data_snapshot_id"],
            "decision_status": "PASS",
        }
        for index, candidate_id in enumerate(candidate_ids, start=1)
    ]


def _pilot_search_space(pilot_inputs: dict) -> dict:
    identifiers = pilot_inputs["identifiers"]
    candidate_space = pilot_inputs["candidate_space"]
    statistical_plan = pilot_inputs["statistical_plan"]
    return build_search_space_snapshot(
        identifiers["research_family_id"],
        pilot_inputs["walk_forward_schedule"][0]["fold_id"],
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
