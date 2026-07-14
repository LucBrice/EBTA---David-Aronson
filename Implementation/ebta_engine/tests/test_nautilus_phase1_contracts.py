import unittest

from ebta_engine.procedures.detrending import detrend_returns
from ebta_engine.procedures.economic_gate import economic_gate_report
from ebta_engine.migrations.schema_migrations import migrate_config_1_0_to_1_1, migrate_strategy_payload_1_0_to_1_1
from ebta_engine.schema_validation import validate
from ebta_engine.strategies.contracts import Candidate, CostModel, InstrumentConfig, SegmentSimulator, SimulationResult
from ebta_engine.strategies.payload_factory import (
    StrategyFamilySpec,
    StructuralAxis,
    generate_family,
    liquidity_sweep_family_spec,
)
from ebta_engine.strategies.payloads import payload_by_code
from ebta_engine.validators.artifact_validators import load_schema


class NautilusPhase1ContractTests(unittest.TestCase):
    def test_strategy_payload_from_dict_round_trip(self):
        payload = payload_by_code("NASDAQ", "G")
        restored = type(payload).from_dict(payload.to_dict())
        self.assertEqual(restored, payload)
        tampered = payload.to_dict()
        tampered["session"] = "us"
        with self.assertRaises(ValueError):
            type(payload).from_dict(tampered)

    def test_contracts_are_stdlib_serializable_and_validated(self):
        candidate = Candidate(
            candidate_id="CAND-001",
            research_family_id="FAM-001",
            payload=payload_by_code("XAUUSD", "E").to_dict(),
            asset="XAUUSD",
            complexity=0,
        )
        cost_model = CostModel(model_id="COST-001", fill_model="deterministic", fee_model="fixed")
        instrument = InstrumentConfig(
            instrument_id="XAUUSD.SIM",
            symbol="XAUUSD",
            venue="SIM",
            price_precision=2,
            size_precision=2,
            price_increment="0.01",
            size_increment="0.01",
            margin_init="0.05",
            margin_maint="0.05",
            maker_fee="0",
            taker_fee="0",
        )
        self.assertTrue(candidate.canonical_hash)
        self.assertEqual(cost_model.to_dict()["prob_fill_on_limit"], 1.0)
        self.assertEqual(instrument.to_dict()["venue"], "SIM")

    def test_simulation_result_feeds_existing_procedures_without_signature_changes(self):
        result = SimulationResult(
            candidate_id="CAND-001",
            instrument_id="XAUUSD.SIM",
            timestamps=["2026-01-01", "2026-01-02"],
            daily_returns=[0.01, -0.002],
            daily_exposure=[1.0, 0.5],
            nav=[100.0, 100.8],
            total_costs=0.2,
        )
        detrended = detrend_returns(
            **result.detrending_inputs(market_returns=[0.003, 0.001], cash_returns=[0.0, 0.0]),
            segment_id="Test_k",
        )
        self.assertEqual(len(detrended["detrended_returns"]), 2)

        report = economic_gate_report(
            result.economic_gate_evidence(
                statistical_status="PASS",
                thresholds={"min_return": 0.0},
                observed_values={"mean_return": 0.004},
                capacity_grid=[{"capital": 100000, "status": "PASS"}],
                return_hurdle_pass=True,
                drawdown_pass=True,
                capacity_pass=True,
                costs_pass=True,
                execution_pass=True,
            )
        )
        self.assertEqual(report["global_status"], "PASS")

    def test_config_migration_adds_explicit_execution_and_complexity_contracts(self):
        legacy = {
            "schema_version": "1.0.0",
            "config_id": "CFG-001",
            "project_id": "PRJ-001",
            "research_family_id": "FAM-001",
            "hypothesis_id": "HYP-001",
            "process_version_id": "PROC-001",
            "protocol_version": "EBTA-DOC-1.1",
            "data_snapshots": [{"data_snapshot_id": "DATA-001", "available_at": "2026-01-01T00:00:00Z"}],
            "walk_forward_schedule": [
                {
                    "fold_id": "FOLD-001",
                    "train": ["2020-01-01", "2020-12-31"],
                    "test": ["2021-01-01", "2021-12-31"],
                    "oos": ["2022-01-01", "2022-12-31"],
                    "purge_days": 0,
                    "embargo_days": 0,
                    "warmup_days": 1,
                    "policy": "rolling",
                    "information_cutoff": "2021-12-31T23:59:59Z",
                }
            ],
            "candidate_space": {"candidate_count": 1},
            "selection_rule": {"rule": "max_test"},
            "statistical_plan": {
                "wrc_alpha": 0.05,
                "wrc_bootstrap_replications": 1,
                "wrc_seed": 1,
                "wrc_mean_block_length": 1,
                "oos_bootstrap_replications": 1,
                "oos_seed": 1,
                "oos_mean_block_length": 1,
            },
            "execution_model": {"central_scenario": "tradable_net"},
            "robustness_plan": {"required_before_oos": True},
            "oos_opening_gate": {"requires_pre_oos_sealed": True},
            "incubation_plan": {"requires_validation_ready": True},
            "reproducibility_manifest": {"package_stage": "PRE_OOS_SEALED"},
            "document_hash": "HASH",
        }
        migrated = migrate_config_1_0_to_1_1(legacy)
        self.assertEqual(migrated["schema_version"], "1.1.0")
        self.assertIn("cost_model", migrated["execution_model"])
        self.assertIn("instrument_config", migrated["execution_model"])
        self.assertIn("complexity_levels", migrated["candidate_space"])
        self.assertEqual(validate(migrated, load_schema("config.schema.json")), [])

    def test_strategy_payload_migration_structures_entry_and_exit_criteria(self):
        legacy = payload_by_code("NASDAQ", "E").to_dict()
        legacy["payload_version"] = "1.0.0"
        legacy["entry_criterion"] = "legacy_entry"
        legacy["exit_criterion"] = "legacy_exit"
        migrated = migrate_strategy_payload_1_0_to_1_1(legacy)
        restored = type(payload_by_code("NASDAQ", "E")).from_dict(migrated)
        errors = validate(restored.to_dict(), load_schema("strategy_payload.schema.json"))
        self.assertEqual(errors, [])
        entry_criterion = restored.entry_criterion
        self.assertIsInstance(entry_criterion, dict)
        assert isinstance(entry_criterion, dict)
        self.assertEqual(entry_criterion["rule_id"], "legacy_entry")

    def test_payload_factory_generates_full_independent_bias_session_asset_grid(self):
        generated = generate_family(
            assets=["NASDAQ", "XAUUSD"],
            spec=liquidity_sweep_family_spec(),
            research_family_id="FAM-LS",
            fold_id="FOLD-001",
        )
        payloads = generated["payloads"]
        self.assertEqual(len(payloads), 16)
        complexity_counts = {level: 0 for level in [0, 1, 2]}
        for payload in payloads:
            complexity_counts[payload.parameters["complexity"]] += 1
        self.assertEqual(complexity_counts, {0: 2, 1: 8, 2: 6})
        self.assertEqual(generated["search_space"]["asset_candidate_count"], {"NASDAQ": 8, "XAUUSD": 8})

    def test_payload_factory_reduces_dependent_axis_to_default_when_requirement_fails(self):
        spec = StrategyFamilySpec(
            strategy_family="nested_fixture",
            timeframe="1min",
            direction="long_short",
            entry_level="fixture",
            entry_criterion={"criterion_type": "entry", "rule_id": "fixture_entry", "parameters": {}},
            exit_criterion={"criterion_type": "exit", "rule_id": "fixture_exit", "parameters": {}},
            risk_model="fixture",
            sizing_model="fixture",
            parameters={},
            axes=(
                StructuralAxis(
                    name="bias_filter",
                    values=("none", "directional_mtf_bias"),
                    default="none",
                    complexity_by_value={"none": 0, "directional_mtf_bias": 1},
                ),
                StructuralAxis(
                    name="session",
                    values=("all", "asia", "london", "us"),
                    default="all",
                    complexity_by_value={"all": 0, "asia": 1, "london": 1, "us": 1},
                    requires={"bias_filter": ("directional_mtf_bias",)},
                ),
            ),
            payload_code_prefix="FIX",
        )
        generated = generate_family(
            assets=["XAUUSD"],
            spec=spec,
            research_family_id="FAM-FIX",
            fold_id="FOLD-001",
        )
        self.assertEqual(len(generated["payloads"]), 5)

    def test_segment_simulator_fake_produces_consumable_result_without_segment_metadata(self):
        class FakeSegmentSimulator:
            def run(self, candidate: Candidate) -> SimulationResult:
                return SimulationResult(
                    candidate_id=candidate.candidate_id,
                    instrument_id=f"{candidate.asset}.SIM",
                    timestamps=["2026-01-01", "2026-01-02", "2026-01-03"],
                    daily_returns=[0.002, 0.001, -0.0005],
                    daily_exposure=[1.0, 1.0, 0.0],
                    nav=[100.0, 100.2, 100.3],
                    total_costs=0.05,
                    metadata={"source": "fake_segment_simulator"},
                )

        candidate = Candidate(
            candidate_id="CAND-FAKE",
            research_family_id="FAM-FAKE",
            payload=payload_by_code("NASDAQ", "E").to_dict(),
            asset="NASDAQ",
            complexity=0,
        )
        simulator: SegmentSimulator = FakeSegmentSimulator()
        self.assertIsInstance(simulator, SegmentSimulator)
        result = simulator.run(candidate)
        self.assertEqual(result.metadata, {"source": "fake_segment_simulator"})

        detrended = detrend_returns(
            **result.detrending_inputs(
                market_returns=[0.001, 0.001, 0.001],
                cash_returns=[0.0, 0.0, 0.0],
            ),
            segment_id="opaque_segment",
        )
        self.assertEqual(len(detrended["detrended_returns"]), 3)
        report = economic_gate_report(
            result.economic_gate_evidence(
                statistical_status="PASS",
                thresholds={"min_return": 0.0},
                observed_values={"mean_return": 0.00083},
                capacity_grid=[{"capital": 100000, "status": "PASS"}],
                return_hurdle_pass=True,
                drawdown_pass=True,
                capacity_pass=True,
                costs_pass=True,
                execution_pass=True,
            )
        )
        self.assertEqual(report["global_status"], "PASS")


if __name__ == "__main__":
    unittest.main()
