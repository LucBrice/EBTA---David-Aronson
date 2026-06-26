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

from ebta_engine.manifests.manifest_builder import build_manifest
from ebta_engine.persistence import append_jsonl, atomic_write_json
from ebta_engine.procedures.candidate_matrix import build_candidate_matrix
from ebta_engine.procedures.complexity_selection import select_complexity
from ebta_engine.procedures.data_availability import validate_availability
from ebta_engine.procedures.detrending import detrend_returns
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.procedures.ml_manifest import build_ml_manifest
from ebta_engine.procedures.oos_confidence_interval import oos_confidence_interval
from ebta_engine.procedures.optimization import optimize_on_train
from ebta_engine.procedures.registry_lineage import review_registry_lineage
from ebta_engine.procedures.robustness import robustness_verdict
from ebta_engine.procedures.search_space import build_search_space_snapshot
from ebta_engine.procedures.walk_forward import validate_walk_forward_schedule
from ebta_engine.procedures.wrc import wrc_test
from ebta_engine.validators.package_validator import validate_package_dir


ARTIFACT_PATHS = [
    "config.json",
    "registry.jsonl",
    "oos_access_log.jsonl",
    "reports/gates.json",
    "reports/invariant_evidence.json",
    "reports/wrc.json",
    "reports/robustness.json",
    "reports/oos.json",
    "reports/economic.json",
    "reports/execution.json",
    "reports/reproduction.json",
    "reports/search_space.json",
    "reports/optimization_log.json",
    "reports/ml_manifest.json",
    "reports/complexity_selection.json",
    "reports/candidate_matrix.json",
    "reports/data_availability.json",
    "reports/fold_schedule.json",
    "reports/registry_review.json",
    "reports/detrending.json",
    "series/oos_primary_returns.json",
]

WRC_REPLICATIONS = 5000
OOS_REPLICATIONS = 5000
WRC_SEED = 13
OOS_SEED = 23


def build_package(package_dir: Path) -> dict:
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    _write_config(package_dir)
    _write_registry(package_dir)
    _write_oos_access_log(package_dir)
    _write_reports(package_dir)
    _write_series(package_dir)
    _write_manifest(package_dir)

    return validate_package_dir(package_dir)


def _write_config(package_dir: Path) -> None:
    atomic_write_json(
        package_dir / "config.json",
        {
            "schema_version": "1.0.0",
            "config_id": "CFG-PILOT-001",
            "project_id": "PRJ-PILOT",
            "research_family_id": "FAM-PILOT",
            "hypothesis_id": "HYP-PILOT-MA",
            "process_version_id": "PROC-PILOT-001",
            "protocol_version": "EBTA-DOC-1.0",
            "data_snapshots": [
                {
                    "data_snapshot_id": "DATA-PILOT-001",
                    "available_at": "2019-12-31T00:00:00Z",
                }
            ],
            "walk_forward_schedule": [
                {
                    "fold_id": "FOLD-001",
                    "train": ["2020-01-01", "2021-12-31"],
                    "test": ["2022-01-01", "2022-12-31"],
                    "oos": ["2023-01-01", "2023-12-31"],
                    "purge_days": 5,
                    "embargo_days": 2,
                    "warmup_days": 20,
                    "policy": "rolling",
                    "information_cutoff": "2022-12-31T23:59:59Z",
                }
            ],
            "candidate_space": {"candidate_count": 4},
            "selection_rule": {"rule": "pre_registered_max_test_after_wrc_pass"},
            "statistical_plan": {
                "wrc_alpha": 0.05,
                "wrc_bootstrap_replications": WRC_REPLICATIONS,
                "wrc_seed": WRC_SEED,
                "wrc_mean_block_length": 2,
                "oos_bootstrap_replications": OOS_REPLICATIONS,
                "oos_seed": OOS_SEED,
                "oos_mean_block_length": 2,
            },
            "execution_model": {"central_scenario": "tradable_net"},
            "robustness_plan": {"required_before_oos": True},
            "oos_opening_gate": {"requires_pre_oos_sealed": True},
            "incubation_plan": {"requires_validation_ready": True},
            "reproducibility_manifest": {"package_stage": "VALIDATION_READY"},
            "document_hash": "PILOT_CONFIG_HASH_PLACEHOLDER",
        },
    )


def _write_registry(package_dir: Path) -> None:
    for index, candidate in enumerate(_pilot_search_space()["candidates"], start=1):
        append_jsonl(
            package_dir / "registry.jsonl",
            {
                "schema_version": "1.0.0",
                "event_id": f"EVT-PILOT-{index:03d}",
                "timestamp": "2026-01-01T00:00:00Z",
                "actor": "minimal_pilot_pipeline",
                "event_type": "REGISTER_CANDIDATE",
                "project_id": "PRJ-PILOT",
                "research_family_id": "FAM-PILOT",
                "candidate_id": candidate["candidate_id"],
                "run_id": f"RUN-PILOT-{index:03d}",
                "fold_id": "FOLD-001",
                "data_snapshot_id": "DATA-PILOT-001",
                "input_hashes": [],
                "output_hashes": [],
                "decision_status": "PASS",
                "evidence_path": "reports/candidate_matrix.json",
                "parent_event_id": "",
                "chain_hash": f"CHAIN-PILOT-{index:03d}",
            },
        )


def _write_oos_access_log(package_dir: Path) -> None:
    append_jsonl(
        package_dir / "oos_access_log.jsonl",
        {
            "schema_version": "1.0.0",
            "access_event_id": "OOS-ACCESS-PILOT-001",
            "timestamp": "2026-01-02T00:00:00Z",
            "actor": "minimal_pilot_pipeline",
            "fold_id": "FOLD-001",
            "oos_segment_id": "OOS-001",
            "pre_oos_package_hash": "PREOOS-HASH-PILOT",
            "opening_authorization_id": "AUTH-PILOT-001",
            "access_reason": "authorized_oos_execution",
            "command_or_process_id": "CMD-PILOT-001",
            "read_paths": ["series/oos_input.csv"],
            "write_paths": ["reports/oos.json"],
            "result_artifact_hash": "RESULT-HASH-PILOT",
            "incident_flag": False,
            "reviewer": "independent_reviewer",
        },
    )


def _write_reports(package_dir: Path) -> None:
    procedure_reports = _procedure_reports()
    candidate_ids = procedure_reports["candidate_matrix"]["candidate_ids"]
    gates = {
        "config_id": "CFG-PILOT-001",
        "project_id": "PRJ-PILOT",
        "research_family_id": "FAM-PILOT",
        "hypothesis_id": "HYP-PILOT-MA",
        "process_version_id": "PROC-PILOT-001",
        "template_hash": "TEMPLATE-HASH-PILOT",
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
        "execution.json": {"status": "PASS", "cost_model": "pilot_costs"},
        "reproduction.json": {"status": "PASS", "reproduced_by": "minimal_pilot_pipeline"},
        "search_space.json": procedure_reports["search_space"],
        "optimization_log.json": procedure_reports["optimization_log"],
        "ml_manifest.json": procedure_reports["ml_manifest"],
        "complexity_selection.json": procedure_reports["complexity_selection"],
        "candidate_matrix.json": procedure_reports["candidate_matrix"],
        "data_availability.json": procedure_reports["data_availability"],
        "fold_schedule.json": procedure_reports["fold_schedule"],
        "registry_review.json": procedure_reports["registry_review"],
        "detrending.json": procedure_reports["detrending"],
    }
    for filename, payload in static_reports.items():
        atomic_write_json(package_dir / "reports" / filename, payload)


def _procedure_reports() -> dict:
    search_space = _pilot_search_space()
    candidate_ids = [candidate["candidate_id"] for candidate in search_space["candidates"]]
    train_scores = {candidate_id: index / 100 for index, candidate_id in enumerate(candidate_ids, start=1)}
    optimization_log = optimize_on_train(search_space, train_scores)
    representatives = optimization_log["representatives"]
    test_scores = {representative["candidate_id"]: index / 100 for index, representative in enumerate(representatives, start=1)}
    complexity_selection = select_complexity(representatives, test_scores)
    candidate_matrix = build_candidate_matrix(
        {
            candidate_ids[0]: [0.03, 0.02, 0.04, 0.03],
            candidate_ids[1]: [0.02, 0.01, 0.01, 0.02],
            candidate_ids[2]: [-0.01, 0.00, -0.02, 0.01],
            candidate_ids[3]: [0.00, -0.01, 0.00, -0.02],
        },
        dates=["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"],
        influential_candidates=candidate_ids,
        fold_id="FOLD-001",
    )
    ml_manifest = build_ml_manifest(
        "ML-PILOT-001",
        train_segment="Train_k",
        features=["ret_1", "vol_5"],
        transformations=[{"name": "standardize", "fit_segment": "Train_k"}],
        hyperparameters={"depth": 1},
        seeds=[7],
        complexity_levels=[1, 2],
        selection_rule="max_test_score",
    )
    detrending = detrend_returns([0.01, 0.02, 0.015], [0.005, 0.006, 0.004], [0.001, 0.001, 0.001], [1.0, 1.0, 0.5], segment_id="OOS_GLOBAL")
    wrc = wrc_test(
        {
            candidate_ids[0]: [0.03, 0.02, 0.04, 0.03],
            candidate_ids[1]: [0.02, 0.01, 0.01, 0.02],
            candidate_ids[2]: [-0.01, 0.00, -0.02, 0.01],
            candidate_ids[3]: [0.00, -0.01, 0.00, -0.02],
        },
        replications=WRC_REPLICATIONS,
        mean_block_length=2,
        seed=WRC_SEED,
        alpha=0.05,
    )
    oos = oos_confidence_interval([0.01, 0.02, 0.015, 0.012], replications=OOS_REPLICATIONS, mean_block_length=2, seed=OOS_SEED)
    economic = economic_gate_report(
        {
            "statistical_status": "PASS",
            "return_hurdle_pass": True,
            "drawdown_pass": True,
            "capacity_pass": True,
            "costs_pass": True,
            "execution_pass": True,
            "thresholds": {"min_annualized_return": 0.10, "max_drawdown": 0.20, "target_capital": 1000000},
            "observed_values": {"annualized_return": 0.18, "max_drawdown": 0.08, "validated_capital": 1500000},
            "capacity_grid": [{"capital": 1000000, "status": "PASS"}],
        }
    )
    robustness = robustness_verdict(
        [{"stress_id": "ROB-PILOT-001", "uses_observed_oos": False, "blocking": True, "scenario_verdict": "PASS"}]
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
        "detrending": detrending,
        "data_availability": validate_availability(
            [{"available_at": "2019-12-31T00:00:00Z", "decision_at": "2020-01-01T00:00:00Z"}]
        ),
        "fold_schedule": validate_walk_forward_schedule(
            [
                {
                    "fold_id": "FOLD-001",
                    "train": ["2020-01-01", "2021-12-31"],
                    "test": ["2022-01-01", "2022-12-31"],
                    "oos": ["2023-01-01", "2023-12-31"],
                    "purge_days": 5,
                    "embargo_days": 2,
                    "warmup_days": 20,
                    "policy": "rolling",
                    "information_cutoff": "2022-12-31T23:59:59Z",
                }
            ]
        ),
        "registry_review": review_registry_lineage(candidate_ids, candidate_ids),
    }


def _pilot_search_space() -> dict:
    return build_search_space_snapshot(
        "FAM-PILOT",
        "FOLD-001",
        {"complexity": [1, 2], "lookback": [5, 10]},
        base_spec={"logic": "moving_average"},
        universe_snapshot_id="DATA-PILOT-001",
        universe_snapshot_hash="DATA-PILOT-001-HASH",
        budget={"max_candidates": 4, "max_train_evaluations": 4},
        stop_rule="evaluate_preregistered_grid_once",
        seeds=[WRC_SEED, OOS_SEED],
        selection_metric="mean_net_detrended_log_return",
        cost_model="tradable_net",
        validity_criteria=["train_only_calibration", "complete_test_matrix"],
        stability_criteria=["lower_complexity_tie_break", "turnover_cost_exposure_tie_break"],
        transfer_rule="mechanical_train_to_test_then_selected_candidate_to_oos",
    )


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


def _write_series(package_dir: Path) -> None:
    atomic_write_json(
        package_dir / "series" / "oos_primary_returns.json",
        {
            "observations": [
                {"date": "2023-01-02", "net_detrended_log_return": 0.001, "status": "EXPOSED"},
                {"date": "2023-01-03", "net_detrended_log_return": 0.0, "status": "NO_MODEL"},
            ]
        },
    )


def _write_manifest(package_dir: Path) -> None:
    manifest = build_manifest(package_dir, ARTIFACT_PATHS, "VALIDATION_READY")
    atomic_write_json(package_dir / "manifests" / "reproducibility_manifest.json", manifest)


def main() -> int:
    package_dir = Path(__file__).resolve().parent / "research_package"
    report = build_package(package_dir)
    print(json.dumps({"package_dir": str(package_dir), "status": report["status"]}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
