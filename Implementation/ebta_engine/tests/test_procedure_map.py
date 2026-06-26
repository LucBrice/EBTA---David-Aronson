import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProcedureMapTests(unittest.TestCase):
    def test_phase_1_map_lists_planned_procedures(self):
        text = (ROOT / "PROCEDURE_CALCULATION_MAP.md").read_text(encoding="utf-8")
        required = [
            "search_space",
            "optimization",
            "ml_manifest",
            "complexity_selection",
            "candidate_matrix",
            "returns",
            "detrending",
            "zero_centering",
            "bootstrap",
            "wrc",
            "oos_confidence_interval",
            "data_availability",
            "walk_forward",
            "registry_lineage",
            "robustness",
            "sealing",
            "oos_access",
            "economic_gate",
            "lifecycle",
        ]
        for procedure in required:
            self.assertIn(f"`{procedure}`", text)

    def test_implementation_context_tracks_plan(self):
        context_path = ROOT / "Archives" / "completed_2026-06-26" / "implementation_context.json"
        context = json.loads(context_path.read_text(encoding="utf-8"))
        self.assertEqual(context["runtime_version"], "EBTA-ENGINE-0.1.0")
        self.assertEqual(
            context["plan_file"],
            "Implementation/Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md",
        )
        self.assertIn("No Protocole/ change", context["non_goals"])
        self.assertIn("No BACKTRADER access", context["non_goals"])


if __name__ == "__main__":
    unittest.main()
