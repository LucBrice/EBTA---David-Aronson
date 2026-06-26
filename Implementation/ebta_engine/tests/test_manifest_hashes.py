import json
import tempfile
import unittest
from pathlib import Path
from shutil import copytree

from ebta_engine.manifests.manifest_builder import build_manifest, verify_manifest
from ebta_engine.validators.artifact_validators import validate


ROOT = Path(__file__).resolve().parents[1]


class ManifestHashTests(unittest.TestCase):
    def test_manifest_detects_modified_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / "package"
            copytree(ROOT / "fixtures" / "valid_minimal", package_dir)
            manifest = build_manifest(
                package_dir,
                ["config.json", "registry.jsonl", "oos_access_log.jsonl", "reports/gates.json"],
                "PRE_OOS_SEALED",
            )
            self.assertEqual(verify_manifest(package_dir, manifest), [])
            (package_dir / "config.json").write_text(
                json.dumps({**json.loads((package_dir / "config.json").read_text()), "config_id": "MUTATED"}),
                encoding="utf-8",
            )
            self.assertIn("hash mismatch: config.json", verify_manifest(package_dir, manifest))


if __name__ == "__main__":
    unittest.main()
