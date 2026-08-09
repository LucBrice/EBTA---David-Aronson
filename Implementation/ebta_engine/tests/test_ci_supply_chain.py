import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ebta-runtime-suite.yml"

EXPECTED_USES = {
    "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2",
    "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0",
}
EXPECTED_INSTALLS = {
    "python -m pip install jsonschema==4.23.0",
    "python -m pip install numpy==2.2.6 pandas==2.3.3",
}


def workflow_contract_errors(workflow):
    lines = [line.strip() for line in workflow.splitlines()]
    uses = {line.removeprefix("uses: ") for line in lines if line.startswith("uses: ")}
    installs = {
        line.removeprefix("run: ")
        for line in lines
        if line.startswith("run: ") and " pip install " in line
    }
    errors = []
    if uses != EXPECTED_USES:
        errors.append("actions are not the exact reviewed set")
    if installs != EXPECTED_INSTALLS:
        errors.append("direct CI dependencies are not the exact pinned set")
    if not re.search(r"(?m)^permissions:\s*\n  contents: read$", workflow):
        errors.append("workflow permissions are not contents: read")
    if not re.search(
        r"(?ms)^      - name: Checkout\n        uses: .*\n        with:\n          persist-credentials: false$",
        workflow,
    ):
        errors.append("checkout credentials are persisted or unspecified")
    if "python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation" not in workflow:
        errors.append("canonical unittest command is missing")
    return errors


class CiSupplyChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.lines = [line.strip() for line in cls.workflow.splitlines()]

    def test_actions_are_exactly_pinned_to_reviewed_commits(self):
        uses = {line.removeprefix("uses: ") for line in self.lines if line.startswith("uses: ")}

        self.assertEqual(uses, EXPECTED_USES)
        self.assertFalse(any(re.search(r"@(v\d+|main|master)(?:\s|$)", value) for value in uses))

    def test_hostile_workflow_mutations_are_rejected(self):
        mutations = {
            "mutable_tag": self.workflow.replace(
                "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2",
                "actions/checkout@v4",
            ),
            "extra_action": self.workflow.replace(
                "      - name: Set up Python",
                "      - name: Unreviewed action\n        uses: vendor/action@main\n\n      - name: Set up Python",
            ),
            "floating_dependency": self.workflow.replace("jsonschema==4.23.0", "jsonschema"),
            "write_and_credentials": self.workflow.replace("contents: read", "contents: write").replace(
                "persist-credentials: false", "persist-credentials: true"
            ),
            "missing_suite": self.workflow.replace(
                "python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation",
                "python -m unittest",
            ),
        }
        for scenario, mutated_workflow in mutations.items():
            with self.subTest(scenario=scenario):
                self.assertTrue(workflow_contract_errors(mutated_workflow))

    def test_workflow_is_read_only_and_checkout_drops_credentials(self):
        self.assertRegex(self.workflow, r"(?m)^permissions:\s*\n  contents: read$")
        self.assertRegex(
            self.workflow,
            r"(?ms)^      - name: Checkout\n        uses: .*\n        with:\n          persist-credentials: false$",
        )

    def test_direct_ci_dependencies_are_exactly_pinned(self):
        installs = {
            line.removeprefix("run: ")
            for line in self.lines
            if line.startswith("run: ") and " pip install " in line
        }
        self.assertEqual(installs, EXPECTED_INSTALLS)

    def test_triggers_and_existing_proof_steps_remain_present(self):
        for fragment in (
            '"on":\n  push:\n  workflow_dispatch:',
            "runs-on: ubuntu-latest",
            'python-version: "3.13"',
            "python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation",
            "json.load(open('.ai/checkpoint.json', encoding='utf-8'))",
            "json.load(open('Implementation/Active/tracking.json', encoding='utf-8'))",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.workflow)

        self.assertEqual(workflow_contract_errors(self.workflow), [])


if __name__ == "__main__":
    unittest.main()
