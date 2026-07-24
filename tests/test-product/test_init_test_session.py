import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills/test-product/scripts/init-test-session.py"
TEMPLATES = REPO_ROOT / "skills/test-product/assets/templates"
EXPECTED_FILES = {
    "test-charter.md",
    "rtm.md",
    "test-plan.md",
    "test-cases.md",
    "defect-log.md",
    "test-summary.md",
}


class InitTestSessionTests(unittest.TestCase):
    def run_script(self, root: Path, scope: str):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--scope",
                scope,
                "--date",
                "2026-07-24",
            ],
            capture_output=True,
            text=True,
        )

    def test_creates_complete_session_and_replaces_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = {
                path.name: path.read_text(encoding="utf-8")
                for path in TEMPLATES.glob("*.md")
            }

            result = self.run_script(root, "Checkout Flow")

            target = root / "docs/tests/2026-07-24-checkout-flow"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(result.stdout.strip()), target.resolve())
            self.assertEqual({path.name for path in target.iterdir()}, EXPECTED_FILES)
            for path in target.iterdir():
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("{{SESSION_DATE}}", content)
                self.assertNotIn("{{SCOPE}}", content)
                self.assertNotIn("{{SCOPE_SLUG}}", content)
                self.assertIn("2026-07-24", content)
            after = {
                path.name: path.read_text(encoding="utf-8")
                for path in TEMPLATES.glob("*.md")
            }
            self.assertEqual(before, after)

    def test_refuses_to_overwrite_existing_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self.run_script(root, "Checkout Flow")
            second = self.run_script(root, "Checkout Flow")

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("already exists", second.stderr)

    def test_rejects_blank_or_path_like_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for scope in ("   ", "../checkout", "checkout/flow", r"checkout\flow"):
                with self.subTest(scope=scope):
                    result = self.run_script(root, scope)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("scope", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
