"""The build entry stays the paper's, the reference environment accepts a newer
uv, and the path check refuses a document this template retired.

Three defects found while upgrading two downstream papers (Issues #245, #246,
#247)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".agents/scripts/shared"))
import content_registry  # noqa: E402

REGISTRY = ROOT / ".agents/content-registry.yaml"
UV_TOML = ROOT / ".agents/scripts/shared/paper-references/reference-integrity/uv.toml"
CHECKER = ROOT / ".agents/scripts/project/check_development_paths.py"


def entries() -> dict[str, dict]:
    return {entry["path"]: entry for entry in content_registry.loads(REGISTRY.read_text(encoding="utf-8"))["entries"]}


class BuildEntryTests(unittest.TestCase):
    def test_the_build_entry_is_reviewed_and_never_merged(self) -> None:
        """A three-way merge inserted a block the paper already had, once per
        run: v0.4.12 → v0.8.0 left the same `ifneq ($(wildcard ...venv...))`
        three times in RSI_light_paper (#245). The paper reviews the diff."""
        entry = entries()["Makefile"]
        self.assertEqual(entry.get("upgrade"), "review", entry)
        self.assertIn("PAGE_BUDGET", entry["summary"])


class AuthorCommentTests(unittest.TestCase):
    def test_a_comment_may_be_written_in_chinese(self) -> None:
        """Authors write Chinese comments (#256). `\ifPaperNotes` is true in the
        main build only, so CJKutf8 is loaded there and never in the submission
        or blind build."""
        text = (ROOT / "paper/style/author-comments.sty").read_text(encoding="utf-8")
        self.assertIn("\\ifPaperNotes\\RequirePackage{CJKutf8}\\fi", text)
        body = text.split("\\newcommand{\\AuthorComment}", 1)[1]
        self.assertIn("\\begin{CJK}{UTF8}{gbsn}", body)


class ReferenceEnvironmentTests(unittest.TestCase):
    def test_uv_may_be_any_version_at_or_above_the_floor(self) -> None:
        """`required-version = "==0.11.23"` refused every host uv but one, so the
        release metadata audit could not run (#246). the lock file pins the
        dependencies; uv itself only has to be new enough."""
        required = re.search(r'(?m)^required-version = "([^"]+)"$', UV_TOML.read_text(encoding="utf-8"))
        self.assertIsNotNone(required, "uv.toml declares no required-version")
        version = required.group(1)
        self.assertFalse(version.startswith("=="), version)
        self.assertTrue(version.startswith(">="), version)


class RetiredReferenceTests(unittest.TestCase):
    def test_a_document_naming_a_retired_root_document_fails(self) -> None:
        """PAPER.md and DEV.md were retired in v0.5.0; the path check now reads
        the reference documents a house skill ships, so a pointer to a retired
        root document fails instead of rotting (#247)."""
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / ".agents/skills/shared/example/sources").mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Rules\n\nRead `PAPER.md` first.\n", encoding="utf-8")
            (root / ".agents/skills/shared/example/SKILL.md").write_text(
                "---\nname: example\ndescription: example\n---\n\n# Example\n", encoding="utf-8")
            (root / ".agents/skills/shared/example/sources/notes.md").write_text(
                "Consult `DEV.md` for the commands.\n", encoding="utf-8")
            shutil.copy2(CHECKER, root / "checker.py")
            (root / ".agents/scripts/project").mkdir(parents=True)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            result = subprocess.run([sys.executable, str(root / "checker.py"), "--root", str(root)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("AGENTS.md: PAPER.md is retired", result.stdout)
            self.assertIn("sources/notes.md: DEV.md is retired", result.stdout)


if __name__ == "__main__":
    unittest.main()
