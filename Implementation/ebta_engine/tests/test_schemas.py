import unittest
from pathlib import Path

from ebta_engine.manifests.manifest_builder import build_manifest
from ebta_engine.validators.artifact_validators import load_schema, validate_json_file, validate_jsonl_file
from ebta_engine.schema_validation import validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


class SchemaTests(unittest.TestCase):
    def test_valid_minimal_config_passes(self):
        errors = validate_json_file(FIXTURES / "valid_minimal" / "config.json", "config.schema.json")
        self.assertEqual(errors, [])

    def test_invalid_config_missing_required_fails(self):
        errors = validate_json_file(
            FIXTURES / "invalid_missing_required" / "config_missing_project_id.json",
            "config.schema.json",
        )
        self.assertTrue(any(error.path == "$.project_id" for error in errors))

    def test_registry_jsonl_passes(self):
        errors = validate_jsonl_file(
            FIXTURES / "valid_minimal" / "registry.jsonl",
            "experiment_registry_event.schema.json",
        )
        self.assertEqual(errors, [])

    def test_oos_access_jsonl_passes(self):
        errors = validate_jsonl_file(
            FIXTURES / "valid_minimal" / "oos_access_log.jsonl",
            "oos_access_event.schema.json",
        )
        self.assertEqual(errors, [])

    def test_reproducibility_manifest_requires_sop12_sections(self):
        manifest = build_manifest(
            FIXTURES / "valid_minimal",
            [
                "config.json",
                "registry.jsonl",
                "oos_access_log.jsonl",
                "reports/gates.json",
                "reports/wrc.json",
                "reports/search_space.json",
                "series/oos_primary_returns.json",
            ],
            "VALIDATION_READY",
        )
        schema = load_schema("reproducibility_manifest.schema.json")
        errors = validate(manifest, schema)
        self.assertEqual(errors, [])
        self.assertIn("configuration", manifest)
        self.assertIn("random_seeds", manifest)
        self.assertTrue(all("source_normative" in artifact for artifact in manifest["artifacts"]))


if __name__ == "__main__":
    unittest.main()
