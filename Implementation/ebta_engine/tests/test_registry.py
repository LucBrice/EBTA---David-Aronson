import unittest

from ebta_engine.strategies.registry import STRATEGY_REGISTRY, get_strategy, register_strategy


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self._previous = dict(STRATEGY_REGISTRY)
        STRATEGY_REGISTRY.clear()

    def tearDown(self):
        STRATEGY_REGISTRY.clear()
        STRATEGY_REGISTRY.update(self._previous)

    def test_unknown_payload_code_raises_registered_codes(self):
        with self.assertRaisesRegex(KeyError, "Unknown payload code"):
            get_strategy("Z")

    def test_returns_registered_strategy_class(self):
        class StubStrategy:
            def on_bar(self, bar):
                pass

            def should_enter(self):
                return False, None

            def should_exit(self, bar_count_since_entry):
                return False

        register_strategy("E", StubStrategy)

        self.assertIs(get_strategy("E"), StubStrategy)


if __name__ == "__main__":
    unittest.main()
