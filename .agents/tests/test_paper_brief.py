from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / ".agents/skills/shared/paper-brief-ingest/scripts/paper-brief.py"
TEMPLATE_ORIGINS = (
    "git@github.com:a-green-hand-jack/paper-agent-project-template.git",
    "https://github.com/a-green-hand-jack/agent-writing-harness",
    "git@github.com:a-green-hand-jack/ccfa-writing-paper-template.git",
)
PAPER_ORIGIN = "git@github.com:someone/paper-repo.git"
BRIEF_RECORD = Path(".agents/memory/project/brief.md")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def make_paper_repo(root: Path, origin: str = PAPER_ORIGIN) -> None:
    write(root / "PAPER.md", FACTORY_PAPER)
    git(root, "init", "-q")
    git(root, "remote", "add", "origin", origin)
    git(root, "add", "PAPER.md")
    git(root, "-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-qm", "init")


FACTORY_PAPER = """# Paper Contract
The collaboration cues locked, bounded, free, and unresolved remain available as guidance.
## Paper identity
- Working title: TODO Paper Title
- Target venue: unresolved (verify current official rules before submission work)
- Paper type: unresolved
- Intended readers: TODO
- One-sentence positioning: TODO
## Operating mode
- Mode: unresolved (`collaborative` or `autonomous`)
## What readers should believe
### Central thesis — unresolved

TODO: state the single most important conclusion the paper wants readers to accept.
### Contributions
No contributions have been approved yet. Add one entry per contribution that
the current paper can defend; there is no required number of contributions.

For each contribution, record whether it is central, supporting, or optional and whether it may be weakened or removed if the evidence changes.
## What must not change silently
Current locked items:

- TODO
## What may evolve
- Local sentence wording: free unless it changes claim strength or scientific meaning.
- TODO
## Unresolved
- TODO: title candidates
- TODO: central thesis
- TODO: target audience and venue fit
## Story and structure
The narrative is approved.
## Writing style
### Current style — unresolved

- Positioning and voice: TODO
- Explanation density: TODO
- Claim-strength discipline: TODO
- Preferred paragraph moves: TODO
- Terms or expressions to avoid: TODO
- Venue-specific overlay: TODO; load only when the target venue is active and current rules have been verified.
## Human decisions required
Final approval belongs to the Human.
"""


def brief_fixture() -> str:
    return """# Paper Brief
## Paper identity
- Working title: A Study of X
- Target venue: ICLR 2026
- Paper type: conference
- Intended readers: ML researchers
- One-sentence positioning: We show that X works.
## What readers should believe
### Central thesis
X improves accuracy.
### Contributions
- Contribution: a new method for X
## Operating mode
- Mode: autonomous
## Evidence and materials
- Code / data / results: repo link
## What must not change silently
- the primary comparison
## What may evolve
- presentation order of experiments
## Target and delivery
- Venue / year / track and deadline: unresolved
## Authors and identity
- Author list: unresolved
## Constraints
- Language and length limits: English, 9 pages
## First deliverable
- outline
## Template usage note
Use the template to write this paper.
"""


def record_sections_in_order(text: str) -> bool:
    """The rule make check applies to every memory record (check-agent-content.py)."""
    positions = [text.find(f"\n{heading}\n") for heading in ("## Decision", "## Why", "## Apply")]
    return -1 not in positions and positions == sorted(positions)


def section(paper: str, heading: str) -> str:
    start = paper.index(heading)
    end = paper.find("\n## ", start + len(heading))
    return paper[start:] if end < 0 else paper[start:end]


class PaperBriefChecks(unittest.TestCase):
    def test_validate_passes_on_valid_brief(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            brief = Path(directory) / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(Path(directory), "validate", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK paper_brief validated", result.stdout)

    def test_validate_rejects_missing_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            brief = Path(directory) / "BRIEF.md"
            write(brief, brief_fixture().replace("## Constraints", "## Missing constraints"))
            result = run(Path(directory), "validate", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required sections: Constraints", result.stdout + result.stderr)

    def test_validate_requires_template_usage_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            brief = Path(directory) / "BRIEF.md"
            write(
                brief,
                brief_fixture().replace(
                    "## Template usage note\nUse the template to write this paper.\n",
                    "",
                ),
            )
            result = run(Path(directory), "validate", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Template usage note", result.stdout + result.stderr)

    def test_validate_rejects_invalid_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            brief = Path(directory) / "BRIEF.md"
            write(brief, brief_fixture().replace("- Mode: autonomous", "- Mode: unsupervised"))
            result = run(Path(directory), "validate", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Mode must be collaborative, autonomous, or unresolved", result.stdout + result.stderr)

    def test_validate_accepts_directory_brief(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write(Path(directory) / "BRIEF.md", brief_fixture())
            result = run(Path(directory), "validate", "--brief", directory)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_rejects_missing_brief(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run(Path(directory), "validate", "--brief", str(Path(directory) / "nope.md"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not exist", result.stdout + result.stderr)

    def test_validate_rejects_symlinked_brief(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target.md"
            write(target, brief_fixture())
            link = Path(directory) / "link.md"
            link.symlink_to(target)
            result = run(Path(directory), "validate", "--brief", str(link))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stdout + result.stderr)

    def test_ingest_fills_decided_fields_and_leaves_missing_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            paper = (repo / "PAPER.md").read_text(encoding="utf-8")
            self.assertIn("Working title: A Study of X", paper)
            self.assertIn("Target venue: ICLR 2026", paper)
            self.assertIn("Mode: autonomous", paper)
            self.assertIn("### Central thesis\n\nX improves accuracy.", paper)
            self.assertIn("- Contribution: a new method for X", paper)
            self.assertIn("- the primary comparison", paper)
            self.assertIn("- presentation order of experiments", paper)
            # Fields not decided in the brief stay unresolved.
            self.assertIn("### Current style — unresolved", paper)
            self.assertIn("Explanation density: TODO", paper)
            self.assertFalse((repo / "BRIEF.md").exists())

    def test_ingest_writes_the_brief_as_a_project_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = (repo / BRIEF_RECORD).read_text(encoding="utf-8")
            front_matter, _, body = record.partition("\n---\n")
            self.assertTrue(front_matter.startswith("---\nname: brief\ndate: "))
            for field in (
                "source: BRIEF.md",
                "scope: project",
                "applies_to: this paper",
                "status: active",
                "supersedes: null",
                "superseded_by: null",
            ):
                self.assertIn(field, front_matter)
            self.assertNotIn(directory, record)
            # The memory-record sections come first, then the brief unchanged.
            self.assertTrue(record_sections_in_order(record))
            self.assertLess(record.index("\n## Apply\n"), record.index("\n## Paper identity\n"))
            fixture = brief_fixture()
            first = fixture.index("## Paper identity")
            self.assertTrue(body.lstrip("\n").startswith(fixture[:first] + "## Decision\n"))
            self.assertTrue(body.endswith(fixture[first:]))

    def test_ingest_keeps_the_record_sections_a_brief_already_has(self) -> None:
        # The starter record filled in place already has Decision, Why and Apply.
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            own = "## Decision\n\nOwn decision.\n\n## Why\n\nOwn reason.\n\n## Apply\n\nOwn use.\n\n"
            brief = repo / BRIEF_RECORD
            write(brief, brief_fixture().replace("## Paper identity", own + "## Paper identity", 1))
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = brief.read_text(encoding="utf-8")
            self.assertTrue(record_sections_in_order(record))
            self.assertEqual(record.count("\n## Decision\n"), 1)
            self.assertIn("Own decision.", record)

    def test_reingesting_the_record_keeps_one_front_matter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            self.assertEqual(run(repo, "ingest", "--brief", str(brief)).returncode, 0)
            write(repo / "PAPER.md", FACTORY_PAPER)
            result = run(repo, "ingest", "--brief", str(repo / BRIEF_RECORD))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = (repo / BRIEF_RECORD).read_text(encoding="utf-8")
            self.assertEqual(record.count("name: brief"), 1)
            self.assertEqual(record.count("\n## Decision\n"), 1)
            self.assertTrue(record_sections_in_order(record))
            self.assertIn("source: brief.md", record)
            self.assertIn("Working title: A Study of X", (repo / "PAPER.md").read_text(encoding="utf-8"))

    def test_ingest_commit_stages_record_and_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            git(repo, "config", "user.name", "test")
            git(repo, "config", "user.email", "test@example.com")
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief), "--commit")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            files = git(repo, "show", "--name-only", "--format=", "HEAD").stdout.split()
            self.assertEqual(sorted(files), sorted([BRIEF_RECORD.as_posix(), "PAPER.md"]))
            self.assertEqual(git(repo, "status", "--porcelain").stdout, "")

    def test_ingest_keeps_a_wrapped_locked_bullet_as_one_bullet(self) -> None:
        # Regression for #154: continuation lines were re-emitted as bullets of their own.
        wrapped = (
            "- The experimental numbers in `tables/` and the descriptions in\n"
            "  `table_summary.txt` and `figure_summary.txt`. Report them as they are, including\n"
            "  negative or inconclusive outcomes.\n"
            "- The citation keys in `references.bib`. No invented entries, no invented keys.\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture().replace("- the primary comparison\n", wrapped))
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            locked = section((repo / "PAPER.md").read_text(encoding="utf-8"), "## What must not change silently")
            bullets = [line for line in locked.splitlines() if line.startswith("- ")]
            self.assertEqual(len(bullets), 2, locked)
            self.assertIn("Current locked items:\n\n" + wrapped.rstrip("\n"), locked)

    def test_ingest_groups_continuations_in_every_list_section(self) -> None:
        brief_text = (
            brief_fixture()
            .replace(
                "- presentation order of experiments\n",
                "- presentation order of experiments, as long as\n  the primary comparison stays first\n",
            )
            .replace(
                "## Target and delivery\n",
                "## Unresolved\n- whether the second ablation belongs in the\n  main text or the appendix\n## Target and delivery\n",
            )
            .replace(
                "## First deliverable\n",
                "## Writing style\n- Positioning and voice: plain, first person plural,\n  no marketing adjectives\n## First deliverable\n",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_text)
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            paper = (repo / "PAPER.md").read_text(encoding="utf-8")
            self.assertIn("- presentation order of experiments, as long as\n  the primary comparison stays first", paper)
            self.assertIn("- whether the second ablation belongs in the\n  main text or the appendix", paper)
            self.assertIn("- Positioning and voice: plain, first person plural,\n  no marketing adjectives", paper)
            self.assertNotIn("\n- the primary comparison stays first", paper)
            self.assertNotIn("\n- main text or the appendix", paper)
            self.assertNotIn("\n- no marketing adjectives", paper)

    def test_ingest_keeps_nested_bullets_inside_their_item(self) -> None:
        nested = "- the baseline set:\n  - baseline A\n  - baseline B\n- the evaluation split\n"
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture().replace("- the primary comparison\n", nested))
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            locked = section((repo / "PAPER.md").read_text(encoding="utf-8"), "## What must not change silently")
            self.assertIn(nested.rstrip("\n"), locked)

    def test_ingest_leaves_out_an_item_that_is_still_a_placeholder(self) -> None:
        mixed = "- the primary comparison\n- TODO: decide whether the\n  limitation is locked\n"
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture().replace("- the primary comparison\n", mixed))
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            locked = section((repo / "PAPER.md").read_text(encoding="utf-8"), "## What must not change silently")
            self.assertIn("- the primary comparison", locked)
            self.assertNotIn("limitation is locked", locked)

    def test_ingest_does_not_invent_from_empty_brief(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            empty = """# Paper Brief
## Paper identity
- Working title: TODO
## What readers should believe
### Central thesis
TODO
### Contributions
- TODO
## Operating mode
- Mode: unresolved
## Evidence and materials
- Code / data / results: none yet
## What must not change silently
- TODO
## What may evolve
- TODO
## Target and delivery
- Venue / year / track and deadline: unresolved
## Authors and identity
- Author list: unresolved
## Constraints
- Language and length limits: TODO
## First deliverable
- TODO
## Template usage note
Use the template to write this paper.
"""
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, empty)
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            paper = (repo / "PAPER.md").read_text(encoding="utf-8")
            self.assertIn("Working title: TODO Paper Title", paper)
            self.assertIn("Mode: unresolved", paper)
            self.assertIn("### Central thesis — unresolved", paper)
            self.assertIn("Current locked items:\n\n- TODO", paper)

    def test_ingest_refuses_non_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            write(repo / "PAPER.md", FACTORY_PAPER)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires a Git repository", result.stdout + result.stderr)

    def test_ingest_refuses_the_template_repository(self) -> None:
        for origin in TEMPLATE_ORIGINS:
            with self.subTest(origin=origin), tempfile.TemporaryDirectory() as directory:
                repo = Path(directory) / "template"
                make_paper_repo(repo, origin=origin)
                brief = Path(directory) / "briefrepo" / "BRIEF.md"
                write(brief, brief_fixture())
                result = run(repo, "ingest", "--brief", str(brief))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("template repository itself", result.stdout + result.stderr)
                self.assertFalse((repo / BRIEF_RECORD).exists())

    def test_ingest_refuses_a_repository_that_is_its_registry_template(self) -> None:
        registry = (
            "schema_version: 1\n"
            "template:\n"
            "  repository: https://github.com/someone/derived-paper-template\n"
            "  version: v1.0.0\n"
            "  upstream:\n"
            "    repository: https://github.com/a-green-hand-jack/paper-agent-project-template\n"
            "    version: v0.4.0\n"
            "default_scope: project\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "derived"
            make_paper_repo(repo, origin="git@github.com:someone/derived-paper-template.git")
            write(repo / ".agents/content-registry.yaml", registry)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("template repository itself", result.stdout + result.stderr)

    def test_ingest_accepts_a_paper_made_from_the_template(self) -> None:
        registry = (
            "schema_version: 1\n"
            "template:\n"
            "  repository: https://github.com/a-green-hand-jack/paper-agent-project-template\n"
            "  version: v0.4.0\n"
            "default_scope: project\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            write(repo / ".agents/content-registry.yaml", registry)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ingest_rejects_invalid_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture().replace("- Mode: autonomous", "- Mode: unsupervised"))
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Mode must be collaborative, autonomous, or unresolved", result.stdout + result.stderr)

    def test_ingest_fails_closed_on_unmapped_decided_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            # Remove a recognized identity anchor so a decided field cannot map.
            path = repo / "PAPER.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "- Working title: TODO Paper Title", "- Working title is decided elsewhere"
                ),
                encoding="utf-8",
            )
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no recognized contract target", result.stdout + result.stderr)
            self.assertNotIn("Working title: A Study of X", (repo / "PAPER.md").read_text(encoding="utf-8"))
            self.assertFalse((repo / BRIEF_RECORD).exists())

    def test_ingest_preserves_explicit_unresolved_thesis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            brief_text = brief_fixture().replace("X improves accuracy.", "unresolved")
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_text)
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            paper = (repo / "PAPER.md").read_text(encoding="utf-8")
            self.assertIn("### Central thesis — unresolved", paper)
            self.assertNotIn("### Central thesis\n\nunresolved", paper)

    def test_ingest_refuses_symlinked_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            outside = Path(directory) / "outside.md"
            write(outside, "do not clobber")
            (repo / BRIEF_RECORD).parent.mkdir(parents=True)
            (repo / BRIEF_RECORD).symlink_to(outside)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlinked destination", result.stdout + result.stderr)
            self.assertEqual("do not clobber", outside.read_text(encoding="utf-8"))

    def test_ingest_refuses_symlinked_record_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "paper"
            make_paper_repo(repo)
            outside = Path(directory) / "outside"
            outside.mkdir()
            (repo / ".agents").mkdir()
            (repo / ".agents/memory").symlink_to(outside, target_is_directory=True)
            brief = Path(directory) / "briefrepo" / "BRIEF.md"
            write(brief, brief_fixture())
            result = run(repo, "ingest", "--brief", str(brief))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlinked destination: .agents/memory", result.stdout + result.stderr)
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
