import unittest
from pathlib import Path

from ebta_engine.adapters.backtrader_mapping import (
    map_payload_to_ebta_artifacts,
    procedure_input_requirements,
    validate_external_payload,
)


ROOT = Path(__file__).resolve().parents[2]


class BacktraderAdapterBoundaryTests(unittest.TestCase):
    def test_missing_external_keys_are_contract_errors(self):
        missing = validate_external_payload({"config": {}, "registry_events": []})
        self.assertIn("oos_access_events", missing)
        self.assertIn("orders", missing)

    def test_payload_maps_to_ebta_artifacts_without_backtrader_repo_access(self):
        payload = {
            "config": {"config_id": "CFG"},
            "registry_events": [{"event_id": "EVT"}],
            "oos_access_events": [{"access_event_id": "OOS"}],
            "orders": [],
            "fills": [],
            "positions": [],
            "nav": [],
            "gate_reports": {"G0": "PASS"},
        }
        artifacts = map_payload_to_ebta_artifacts(payload)
        self.assertEqual(set(artifacts), {
            "config.json",
            "registry.jsonl",
            "oos_access_log.jsonl",
            "reports/execution.json",
            "reports/gates.json",
        })
        self.assertEqual(artifacts["reports/execution.json"]["orders"], [])

    def test_native_mapping_documents_procedure_inputs(self):
        mapping = procedure_input_requirements()
        self.assertIn("nav", mapping["procedure_input_map"])
        self.assertIn("wrc_reused_for_oos_ci", mapping["contract_errors"])
        text = (ROOT / "NATIVE_ENGINE_PROCEDURE_MAPPING.md").read_text(encoding="utf-8")
        self.assertIn("BACKTRADER role | REFERENCE_ONLY", text)
        self.assertIn("no BACKTRADER runtime dependency", text)


if __name__ == "__main__":
    unittest.main()
