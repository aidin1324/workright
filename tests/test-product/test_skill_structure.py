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
    "code-quality-and-maintainability.md",
    "environment-data-and-live-testing.md",
    "contracts-and-distributed-systems.md",
    "security-testing.md",
    "performance-testing.md",
    "resilience-testing.md",
    "usability-accessibility-and-uat.md",
    "defects-metrics-and-closure.md",
}
TEMPLATES = {
    "test-charter.md": ("Objective", "user outcome", "Approvals"),
    "risk-register.md": ("Likelihood", "Impact", "Residual risk"),
    "rtm.md": ("Requirement ID", "Technique", "Evidence", "Defect IDs"),
    "test-plan.md": ("Entry criteria", "Exit and completion criteria", "Selected tests"),
    "test-cases.md": ("Requirement/acceptance criterion/risk IDs", "Expected output", "Cleanup"),
    "defect-log.md": ("Severity", "Expected", "Actual", "evidence"),
    "evidence-index.md": ("Evidence ID", "Commit/build", "Redaction"),
    "test-summary.md": ("Residual risks", "Entry, exit, and cleanup criteria", "Verdict"),
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
                path = SKILL_ROOT / "references" / filename
                self.assertTrue(path.is_file())
                self.assertIn(filename, self.skill_text)
                content = path.read_text(encoding="utf-8")
                self.assertGreaterEqual(len(content.splitlines()), 100)
                for operational_term in ("evidence", "risk"):
                    self.assertIn(operational_term, content.lower())

    def test_progressive_disclosure_and_local_links(self):
        self.assertLessEqual(len(self.skill_text.splitlines()), 500)
        links = re.findall(r"\]\((references/[^)]+\.md)\)", self.skill_text)
        for link in links:
            with self.subTest(link=link):
                self.assertTrue((SKILL_ROOT / link).is_file())
        self.assertLess(
            self.skill_text.index("## Conditional reference router"),
            self.skill_text.index("## 5. Build and maintain the RTM"),
        )

    def test_controlled_result_vocabulary_is_consistent(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                SKILL,
                *sorted((SKILL_ROOT / "references").glob("*.md")),
                *sorted((SKILL_ROOT / "assets/templates").glob("*.md")),
            )
        )
        self.assertNotIn("Not tested", corpus)
        self.assertNotIn("security-performance-and-resilience.md", corpus)
        self.assertIn("Required", corpus)
        self.assertIn("Supporting", corpus)
        self.assertIn("Effective risk weight", corpus)

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
            "Never fix a defect",
            "production code",
            "Critical",
            "High",
            "Medium",
            "Low",
            "stop",
            "continue",
            "RTM",
            "Contract & Synchronization Gate",
            "Focused",
            "Full ride",
            "implementation absent",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill_text)

    def test_initializer_exists(self):
        self.assertTrue((SKILL_ROOT / "scripts/init-test-session.py").is_file())


if __name__ == "__main__":
    unittest.main()
