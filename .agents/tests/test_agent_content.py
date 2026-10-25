from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / ".agents/scripts/check-agent-content.py"
UPSTREAM_SKILL = "---\nname: vendored\ndescription: Use when testing provenance.\n---\n\n# Vendored\n\nUpstream text.\n"
UPSTREAM_REFERENCE = "Upstream reference.\n"


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(TOOL), "--root", str(root)],
                          text=True, capture_output=True, check=False)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def record(name: str, scope: str, sections: tuple[str, ...], extra: str = "") -> str:
    body = "".join(f"\n{heading}\n\nText.\n" for heading in sections)
    return (f"---\nname: {name}\ndate: 2026-10-20\nsource: a test\nscope: {scope}\n"
            f"applies_to: tests\nstatus: active\n{extra}supersedes: null\nsuperseded_by: null\n---\n\n# Title\n{body}")


def fixture(root: Path) -> None:
    write(root / ".agents/content-registry.yaml",
          "entries:\n  - path: .agents/skills/shared/house/\n    scope: shared\n"
          "  - path: .agents/skills/shared/vendored/\n    scope: shared\n")
    write(root / ".agents/skills/AGENTS.md", "- `shared/house/`\n- `shared/vendored/`\n")
    write(root / ".agents/skills/shared/house/SKILL.md",
          "---\nname: house\ndescription: >-\n  Use when: a value with a colon is folded.\n---\n\n# House\n")
    vendored = root / ".agents/skills/shared/vendored"
    write(vendored / "SKILL.md", UPSTREAM_SKILL + "\n## In this repository\n\n- A local note.\n")
    write(vendored / "references/guide.md", UPSTREAM_REFERENCE)
    write(vendored / "PROVENANCE.md",
          "# Provenance\n\n## Files\n\n| File | Upstream path | SHA-256 of the upstream bytes | Status |\n"
          "| --- | --- | --- | --- |\n"
          f"| `SKILL.md` | `skill/SKILL.md` | {sha(UPSTREAM_SKILL)} | unchanged above `## In this repository` |\n"
          f"| `references/guide.md` | `skill/references/guide.md` | {sha(UPSTREAM_REFERENCE)} | unchanged |\n")
    write(root / ".agents/memory/shared/a-lesson.md", record("a-lesson", "shared", ("## Decision", "## Why", "## Apply")))
    write(root / ".agents/memory/shared/AGENTS.md", "- [`a-lesson.md`](a-lesson.md) — a lesson.\n")
    write(root / ".agents/knowledge/shared/a-fact.md",
          record("a-fact", "shared", ("## Fact", "## Evidence", "## Refresh"), "refresh_after: 2027-01-01\n"))
    write(root / ".agents/knowledge/shared/AGENTS.md", "- [`a-fact.md`](a-fact.md) — a fact.\n")


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new), encoding="utf-8")


class AgentContentChecks(unittest.TestCase):
    def check_fails(self, root: Path, message: str) -> None:
        result = run(root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)

    def test_repository_content_passes(self) -> None:
        result = run(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_adoption_diagnostics_only_warn_before_dev_exists(self) -> None:
        # While an adoption branch has no dev anywhere, the inherited diagnostics
        # warn about the three branch-model checks and do not fail
        # (template-adoption step 6); this section must not say they fail.
        script = (ROOT / ".agents/scripts/diagnose-environment.sh").read_text(encoding="utf-8")
        branch_checks = re.findall(r"branch_problem ['\"]([^'\":]+)", script)
        self.assertEqual(branch_checks, ["local dev branch", "origin/dev branch", "GitHub default branch"])
        self.assertIn("branch_level=warn", script)
        skill = (ROOT / ".agents/skills/shared/template-adoption/SKILL.md").read_text(encoding="utf-8")
        shared, section = skill.split("\n## In this repository\n", 1)
        self.assertIn("expected warnings", shared)
        self.assertNotIn("FAIL local dev branch", section)

    def test_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            result = run(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("CHECKED 2 skills, 2 vendored files hashed", result.stdout)

    def test_unquoted_colon_in_front_matter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/skills/shared/house/SKILL.md",
                 "description: >-\n  Use when: a value with a colon is folded.\n",
                 "description: Use when: a value with a colon is not quoted.\n")
            self.check_fails(root, "house/SKILL.md: front matter is not valid YAML")

    def test_name_must_be_the_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/skills/shared/house/SKILL.md", "name: house\n", "name: home\n")
            self.check_fails(root, "front matter name 'home' is not the directory name 'house'")

    def test_unlisted_and_unregistered_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            write(root / ".agents/skills/shared/extra/SKILL.md", "---\nname: extra\ndescription: Extra.\n---\n")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("`shared/extra/` is not listed in .agents/skills/AGENTS.md", result.stdout)
            self.assertIn(".agents/skills/shared/extra/ has no entry in .agents/content-registry.yaml", result.stdout)

    def test_local_edit_above_the_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/skills/shared/vendored/SKILL.md", "Upstream text.", "Upstream text, edited.")
            self.check_fails(root, "SKILL.md no longer matches its upstream SHA-256")

    def test_edit_inside_the_section_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/skills/shared/vendored/SKILL.md", "- A local note.\n", "- A changed local note.\n")
            self.assertEqual(run(root).returncode, 0)

    def test_upstream_without_final_newline_may_gain_one_before_the_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            unterminated = UPSTREAM_SKILL.rstrip("\n")
            edit(root / ".agents/skills/shared/vendored/PROVENANCE.md", sha(UPSTREAM_SKILL), sha(unterminated))
            write(root / ".agents/skills/shared/vendored/SKILL.md", unterminated + "\n\n## In this repository\n\n- Note.\n")
            self.assertEqual(run(root).returncode, 0, run(root).stdout)

    def test_changed_unchanged_file_and_unlisted_file_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            write(root / ".agents/skills/shared/vendored/references/guide.md", "Changed.\n")
            write(root / ".agents/skills/shared/vendored/extra.py", "print()\n")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("references/guide.md no longer matches its upstream SHA-256", result.stdout)
            self.assertIn("extra.py is in the package but not in the file table", result.stdout)

    def test_record_needs_keys_sections_and_an_index_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/knowledge/shared/a-fact.md", "refresh_after: 2027-01-01\n", "")
            edit(root / ".agents/memory/shared/a-lesson.md", "\n## Why\n", "\n## Reason\n")
            write(root / ".agents/memory/shared/AGENTS.md", "No links.\n")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("a-fact.md: front matter has no 'refresh_after'", result.stdout)
            self.assertIn("a-lesson.md: needs the sections ## Decision, ## Why, ## Apply", result.stdout)
            self.assertIn("a-lesson.md: not linked from .agents/memory/shared/AGENTS.md", result.stdout)

    def test_record_scope_must_match_its_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / ".agents/memory/shared/a-lesson.md", "scope: shared\n", "scope: project\n")
            self.check_fails(root, "scope 'project' does not match its directory shared/")


if __name__ == "__main__":
    unittest.main()
