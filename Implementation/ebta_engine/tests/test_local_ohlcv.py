import unittest
from pathlib import Path

from ebta_engine.data.local_ohlcv import DEFAULT_DATA_ROOT, resolve_data_root


class DataRootResolutionTests(unittest.TestCase):
    def test_explicit_path_has_priority_over_environment(self):
        explicit = Path("explicit-data")
        resolved = resolve_data_root(explicit, environ={"EBTA_DATA_ROOT": "environment-data"})
        self.assertEqual(resolved, explicit)

    def test_environment_path_is_used_when_argument_is_absent(self):
        resolved = resolve_data_root(None, environ={"EBTA_DATA_ROOT": "environment-data"})
        self.assertEqual(resolved, Path("environment-data"))

    def test_legacy_default_is_used_when_no_override_exists(self):
        resolved = resolve_data_root(None, environ={})
        self.assertEqual(resolved, DEFAULT_DATA_ROOT)

    def test_blank_environment_value_falls_back_to_legacy_default(self):
        resolved = resolve_data_root(None, environ={"EBTA_DATA_ROOT": "  "})
        self.assertEqual(resolved, DEFAULT_DATA_ROOT)


if __name__ == "__main__":
    unittest.main()
