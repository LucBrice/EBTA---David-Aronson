import unittest

from ebta_engine.procedures.oos_confidence_interval import oos_confidence_interval


class OosConfidenceIntervalTests(unittest.TestCase):
    def test_oos_ci_uses_separate_oos_bootstrap_source(self):
        report = oos_confidence_interval(
            [0.01, 0.02, 0.015, 0.01],
            replications=29,
            mean_block_length=2,
            seed=23,
        )
        self.assertEqual(report["source"], "OOS_STATIONARY_BLOCK")
        self.assertEqual(report["statistical_gate"], "PASS")
        self.assertEqual(len(report["bootstrap_means"]), 29)

    def test_oos_ci_rejects_wrc_test_distribution(self):
        with self.assertRaises(ValueError):
            oos_confidence_interval(
                [0.01, 0.02],
                replications=10,
                mean_block_length=2,
                seed=1,
                bootstrap_source="WRC_TEST_DISTRIBUTION",
            )

    def test_oos_ci_verdicts_are_mechanical(self):
        fail = oos_confidence_interval([-0.01, 0.0], replications=10, mean_block_length=2, seed=3)
        self.assertEqual(fail["statistical_gate"], "FAIL")
        inconclusive = oos_confidence_interval([0.01, 0.01], replications=10, mean_block_length=2, seed=3, power=0.5)
        self.assertEqual(inconclusive["statistical_gate"], "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
