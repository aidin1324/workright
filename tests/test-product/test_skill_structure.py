import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills/test-product"
SKILL = SKILL_ROOT / "SKILL.md"
AGENT = SKILL_ROOT / "agents/openai.yaml"
REFERENCES = {
    "requirements-rtm-and-risk.md",
    "test-planning.md",
    "test-design-techniques.md",
    "automated-test-levels.md",
    "environment-data-and-live-testing.md",
    "contracts-and-distributed-systems.md",
    "security-performance-and-resilience.md",
    "usability-accessibility-and-uat.md",
    "defects-metrics-and-closure.md",
}
TEMPLATES = {
    "test-charter.md": ("Objective", "User outcome", "Approvals"),
    "rtm.md": ("Requirement ID", "Technique", "Evidence", "Defect IDs"),
    "test-plan.md": ("Entry criteria", "Exit criteria", "Selected tests"),
    "test-cases.md": ("Requirement IDs", "Expected result", "Cleanup"),
    "defect-log.md": ("Severity", "Expected", "Actual", "Evidence"),
    "test-summary.md": ("Residual risks", "Exit criteria", "Verdict"),
}


class SkillStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = SKILL.read_text(encoding="utf-8")

    def test_frontmatter_and_implicit_invocation(self):
        self.assertRegex(self.skill_text, r"(?m)^name: test-product$")
        description = re.search(r"(?m)^description: (.+)$", self.skill_text)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when"))
        self.assertNotIn("disable-model-invocation", self.skill_text)
        self.assertIn("allow_implicit_invocation: true", AGENT.read_text(encoding="utf-8"))

    def test_all_references_exist_and_are_routed(self):
        for filename in REFERENCES:
            with self.subTest(filename=filename):
                self.assertTrue((SKILL_ROOT / "references" / filename).is_file())
                self.assertIn(filename, self.skill_text)

    def test_all_templates_exist_with_required_contracts(self):
        for filename, required_terms in TEMPLATES.items():
            with self.subTest(filename=filename):
                path = SKILL_ROOT / "assets/templates" / filename
                self.assertTrue(path.is_file())
                content = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, content)

    def test_workflow_contains_non_negotiable_boundaries(self):
        required_phrases = (
            "Never fix defects",
            "production code",
            "Critical",
            "High",
            "Medium",
            "Low",
            "stop",
            "continue",
            "Requirement Traceability Matrix",
            "Contract & Synchronization Gate",
            "Focused",
            "Full ride",
            "Not run — implementation absent",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill_text)

    def test_initializer_exists(self):
        self.assertTrue((SKILL_ROOT / "scripts/init-test-session.py").is_file())


if __name__ == "__main__":
    unittest.main()
