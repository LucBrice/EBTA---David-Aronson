"""Mechanical ratchet for the canonical unittest inventory.

The text snapshot makes every added or removed test ID visible in review.  It
is not tamper-proof: deleting this guard and its snapshot together removes the
mechanism, a residual explicitly documented by the governing plan.
"""

from collections.abc import Iterator
from pathlib import Path
import unittest


TESTS_DIR = Path(__file__).resolve().parent
TOP_LEVEL_DIR = TESTS_DIR.parents[1]
INVENTORY_PATH = TESTS_DIR / "test_inventory.txt"


def _iter_test_ids(test: unittest.TestSuite | unittest.TestCase) -> Iterator[str]:
    if isinstance(test, unittest.TestSuite):
        for nested_test in test:
            yield from _iter_test_ids(nested_test)
        return
    yield test.id()


def _discover_test_ids() -> list[str]:
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(TESTS_DIR),
        top_level_dir=str(TOP_LEVEL_DIR),
    )
    return sorted(_iter_test_ids(suite))


def _load_expected_ids() -> list[str]:
    return [
        line.strip()
        for line in INVENTORY_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TestInventoryGuardTests(unittest.TestCase):
    def test_discovered_test_ids_match_versioned_inventory(self):
        expected = _load_expected_ids()
        actual = _discover_test_ids()

        self.assertEqual(expected, sorted(expected), "test_inventory.txt must remain sorted")
        self.assertEqual(len(expected), len(set(expected)), "test_inventory.txt contains duplicate IDs")
        self.assertEqual(len(actual), len(set(actual)), "unittest discovery produced duplicate IDs")

        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        self.assertEqual(
            (missing, unexpected),
            ([], []),
            "The canonical unittest inventory changed. Review the missing/unexpected IDs, then "
            "update test_inventory.txt in the same commit only when the change is intentional.",
        )


if __name__ == "__main__":
    unittest.main()
