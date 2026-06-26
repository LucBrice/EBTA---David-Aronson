"""Evidence checks and reports for gates G0 to G14.

Source: Protocole/PAQUET D'EXECUTION EBTA.md section 2 and section 4.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: str
    missing: list[str]
    present: list[str]


GATE_REQUIREMENTS = {
    "G0": ["config_id", "project_id", "research_family_id", "hypothesis_id", "process_version_id", "template_hash"],
    "G1": ["data_snapshots", "availability_timestamps", "anti_leakage_report"],
    "G2": ["registry_initialized", "candidate_catalog", "local_matrix", "independent_registry_review"],
    "G3": ["selection_rule", "train_only_calibration_log", "selected_candidate_id"],
    "G4": ["wrc_report", "wrc_status", "wrc_family_matrix"],
    "G5": ["robustness_report", "robustness_matrix", "pre_oos_robustness_verdict"],
    "G6": ["execution_report", "cost_model", "capacity_grid", "nav_reconciliation"],
    "G7": ["pre_oos_manifest", "frozen_config", "test_reports", "independent_pre_oos_approval"],
    "G8": ["oos_access_log", "opening_authorization", "single_oos_execution_log"],
    "G9": ["oos_report", "concatenated_oos_series", "oos_bootstrap_report", "power_report"],
    "G10": ["economic_report", "statistical_gate_report", "economic_gate_report"],
    "G11": ["validation_ready_manifest", "reproduction_report", "incubation_approval"],
    "G12": ["incubation_report", "paper_trading_log", "monitoring_plan"],
    "G13": ["deployment_certified_manifest", "live_version_id", "kill_switch", "live_approval"],
    "G14": ["lifecycle_archive", "incident_log", "retention_policy"],
}


def validate_gates(evidence: dict) -> list[GateResult]:
    results: list[GateResult] = []
    for gate_id, requirements in GATE_REQUIREMENTS.items():
        missing = [name for name in requirements if not evidence.get(name)]
        present = [name for name in requirements if evidence.get(name)]
        status = "PASS" if not missing else "INCONCLUSIVE"
        results.append(GateResult(gate_id, status, missing, present))
    return results


def gate_report(evidence: dict) -> dict:
    results = validate_gates(evidence)
    return {
        "summary": {
            "total": len(results),
            "pass": sum(1 for result in results if result.status == "PASS"),
            "inconclusive": sum(1 for result in results if result.status == "INCONCLUSIVE"),
        },
        "gates": [
            {
                "gate_id": result.gate_id,
                "status": result.status,
                "present": result.present,
                "missing": result.missing,
            }
            for result in results
        ],
    }
