"""The adoption states this template documents, built from its shipped files in
a temporary root and run through the real gates before each release (DEV.md,
"Releases"), and the upgrade of a paper from an earlier release to them. A paper
deletes this file with the rest of `scope: template`."""
from __future__ import annotations

import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable

import yaml

import test_reference_integrity as reference_tests  # its fixtures, without collecting its tests here

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDER_ERROR = "still declares the template placeholder"
# Variables a calling make or shell may set that would change a state's gates.
CALLER_VARIABLES = ("PAGE_BUDGET", "BUILD_DIR", "MAKEFLAGS", "MAKELEVEL", "MFLAGS", "PYTHONPYCACHEPREFIX")
ENTRIES = 100
# The release a paper is upgraded from with upgrade-template.sh.
UPGRADE_SOURCE = "v0.4.1"
CLONE = ".project/state/template-upgrade/paper-agent-project-template.git"

# A stand-in for a venue's official kit, with the kind of text real kits carry
# about authors; no real kit's text.
VENUE_KIT = r"""% venuekit.sty: synthetic venue kit for the adoption-state tests. Its macros
% handle formatting the paper title, author names, and addresses.
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{venuekit}[2099/01/01 synthetic venue kit]
\newcommand{\venueauthor}[2]{\PackageError{venuekit}{Write \string\venueauthor\{author name\}\{labels here\}}{}}
"""


def shipped_tree(root: Path) -> None:
    """The working tree's tracked and new files, without this module (the copy
    runs make check, which runs every test under .agents/tests)."""
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode().split("\0")
    for name in filter(None, listed):
        source = ROOT / name
        if source == Path(__file__).resolve() or not (source.is_file() or source.is_symlink()):
            continue
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        else:
            shutil.copy2(source, target)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)


def drop_bullets(text: str, matches: Callable[[str], bool]) -> str:
    """Remove each Markdown or YAML list item whose first line matches, with
    its more-indented continuation lines."""
    kept: list[str] = []
    dropping = None
    for line in text.splitlines(keepends=True):
        indent = len(line) - len(line.lstrip())
        if dropping is not None and line.strip() and indent > dropping:
            continue
        dropping = None
        if line.lstrip().startswith("- ") and matches(line):
            dropping = indent
            continue
        kept.append(line)
    return "".join(kept)


def start_paper(root: Path) -> None:
    """README.md "Start a paper", steps 4 and 5."""
    registry_path = root / ".agents/content-registry.yaml"
    registry = registry_path.read_text(encoding="utf-8")
    template_paths = [entry["path"] for entry in yaml.safe_load(registry)["entries"] if entry.get("scope") == "template"]
    registry = re.sub(r"\n  upstream:\n(?:    .*\n)+", "\n", registry)
    registry = drop_bullets(registry, lambda line: line.strip()[len("- path: "):] in template_paths)
    registry_path.write_text(registry, encoding="utf-8")
    for path in template_paths:
        (root / path).unlink(missing_ok=True)
        name = Path(path).name
        for index in (root / ".agents").rglob("AGENTS.md"):
            index.write_text(drop_bullets(index.read_text(encoding="utf-8"), lambda line: f"]({name})" in line),
                             encoding="utf-8")
    agents = root / "AGENTS.md"
    agents.write_text(drop_bullets(agents.read_text(encoding="utf-8"),
                                   lambda line: "protects the case branches" in line), encoding="utf-8")
    (root / "RELEASE_NOTES.md").write_text("# Release notes\n", encoding="utf-8")
    (root / "README.md").write_text("# A paper\n\nBuild it with `make check`.\n", encoding="utf-8")
    for record, slots in ((".agents/memory/shared/page-budget-on-blind-build.md", ("PAGE_MARGIN",)),
                          (".agents/memory/shared/post-build-visual-inspection.md", ("MIN_FIGURE_TEXT", "LAST_LINE_FILL"))):
        rows = "".join(f"| `{slot}` | to be set for the venue |\n" for slot in slots)
        with (root / record).open("a", encoding="utf-8") as handle:
            handle.write(f"\n## In this repository\n\n| Slot | Value |\n| --- | --- |\n{rows}")


def existing_bibliography(root: Path) -> list[str]:
    """A bibliography the paper already had, cited from the introduction."""
    keys = [f"prior{number:03d}" for number in range(ENTRIES)]
    with (root / "paper/refs.bib").open("a", encoding="utf-8") as handle:
        for key in keys:
            handle.write(f"@article{{{key}, title={{Synthetic Prior Study {key}}}, author={{Example, Ada}},"
                         f" journal={{Journal of Examples}}, year={{2024}}}}\n")
    with (root / "paper/sections/02_intro.tex").open("a", encoding="utf-8") as handle:
        handle.write("Earlier studies cover this setting~\\cite{" + ",".join(keys) + "}.\n")
    return keys


def fresh_paper(root: Path) -> None:
    start_paper(root)


def bibliography_without_ledger(root: Path) -> None:
    start_paper(root)
    (root / ".agents/references/ledger.json").unlink()
    existing_bibliography(root)


def bibliography_with_migrated_ledger(root: Path) -> None:
    start_paper(root)
    keys = existing_bibliography(root)
    # A v1 ledger as Draft accepted it: every reference and its use recorded,
    # nothing reviewed yet.
    usages = [{"citation_key": key, "manuscript_location": "paper/sections/02_intro.tex",
               "classification": "background", "human_review_state": "pending"} for key in keys]
    (root / ".agents/references/ledger.json").write_text(
        reference_tests.ledger([reference_tests.reference(key, status="unverified", review="pending") for key in keys],
                               usages=usages),
        encoding="utf-8")
    subprocess.run([sys.executable, ".agents/scripts/reference-evidence.py", "migrate"],
                   cwd=root, check=True, capture_output=True, text=True)


def venue_kit(root: Path) -> None:
    start_paper(root)
    (root / "paper/style/venuekit.sty").write_text(VENUE_KIT, encoding="utf-8")
    main = root / "paper/main.tex"
    main.write_text(main.read_text(encoding="utf-8").replace(
        "\\usepackage{style/paper-harness}\n", "\\usepackage{style/paper-harness}\n\\usepackage{style/venuekit}\n"),
        encoding="utf-8")


STATES = {
    "fresh paper": fresh_paper,
    "existing bibliography, no ledger": bibliography_without_ledger,
    "existing bibliography, migrated ledger": bibliography_with_migrated_ledger,
    "venue kit": venue_kit,
}


def documented_failures() -> dict[str, set[str]]:
    """The newest release's "Adoption states" table: the make release-check
    steps that fail in each state."""
    text = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    latest = re.split(r"^## ", text, flags=re.M)[1]
    table = latest.split("### Adoption states", 1)[1]
    rows: dict[str, set[str]] = {}
    for line in table.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) == 2 and cells[0] in STATES:
            rows[cells[0]] = set(re.findall(r"`([^`]+)`", cells[1]))
    return rows


def caller_environment() -> dict[str, str]:
    return {name: value for name, value in os.environ.items() if name not in CALLER_VARIABLES}


def stub_uv(directory: Path) -> Path:
    """A `uv` that runs the stub checker of the reference tests instead of the
    locked tools, so that no gate here calls a live service."""
    directory.mkdir(parents=True, exist_ok=True)
    runner = directory / "uv"
    runner.write_text(reference_tests.ReferenceMetadataTests.STREAMING_CHECKER, encoding="utf-8")
    runner.chmod(0o755)
    return runner


def offline_environment(bin_directory: Path) -> dict[str, str]:
    environment = caller_environment()
    environment["PATH"] = f"{bin_directory}{os.pathsep}{environment.get('PATH', '')}"
    return environment


def run_state(build: Callable[[Path], None], directory: Path) -> dict[str, subprocess.CompletedProcess[str]]:
    shipped_tree(directory)
    build(directory)
    environment = offline_environment(stub_uv(directory.with_name(directory.name + "-bin")).parent)
    results = {}
    for target in ("check", "release-check"):
        results[target] = subprocess.run(["make", target], cwd=directory, env=environment,
                                         capture_output=True, text=True, check=False)
    return results


def failed_steps(output: str) -> set[str]:
    match = re.search(r"^FAILED make release-check: (.+)$", output, re.M)
    return set(match.group(1).split(", ")) if match else set()


@unittest.skipIf(shutil.which("latexmk") is None or shutil.which("pdftotext") is None,
                 "the adoption states run the real builds")
class AdoptionStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.directory = tempfile.TemporaryDirectory(prefix="adoption-states-")
        base = Path(cls.directory.name)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(STATES)) as pool:
            futures = {name: pool.submit(run_state, build, base / str(number))
                       for number, (name, build) in enumerate(STATES.items())}
            cls.results = {name: future.result() for name, future in futures.items()}

    @classmethod
    def tearDownClass(cls) -> None:
        cls.directory.cleanup()

    def test_release_notes_name_the_expected_failures_of_each_state(self) -> None:
        self.assertEqual(set(documented_failures()), set(STATES))

    def test_make_check_passes_in_each_state(self) -> None:
        for name, results in self.results.items():
            with self.subTest(state=name):
                check = results["check"]
                self.assertEqual(check.returncode, 0, check.stdout[-4000:] + check.stderr[-2000:])

    def test_release_check_fails_only_as_documented(self) -> None:
        expected = documented_failures()
        for name, results in self.results.items():
            with self.subTest(state=name):
                release = results["release-check"]
                self.assertNotEqual(release.returncode, 0)
                self.assertEqual(failed_steps(release.stdout), expected[name], release.stdout[-4000:])

    def test_identity_fails_only_on_the_placeholder(self) -> None:
        for name, results in self.results.items():
            with self.subTest(state=name):
                anonymity = results["release-check"].stdout.split("== anonymity (blind)", 1)[1].split("\n== ", 1)[0]
                errors = [line for line in anonymity.splitlines() if line.startswith("ERROR")]
                self.assertTrue(errors)
                self.assertEqual([line for line in errors if PLACEHOLDER_ERROR not in line], [], anonymity)


def release_entries() -> list[tuple[str, str]]:
    """Each `## <tag>` entry of RELEASE_NOTES.md, newest first."""
    text = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    return [(entry.split(None, 1)[0], entry) for entry in re.split(r"^## ", text, flags=re.M)[1:]
            if re.match(r"v\d", entry)]


def git(*arguments: str, cwd: Path, **options) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", *arguments],
                          cwd=cwd, check=True, capture_output=True, **options)


def tree(root: Path) -> dict[str, bytes]:
    return {str(path.relative_to(root)): os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
            for path in root.rglob("*")
            if (path.is_file() or path.is_symlink()) and path.relative_to(root).parts[0] not in (".git", ".project")}


class ReleaseNotesTests(unittest.TestCase):
    def test_each_release_says_whether_the_command_completes_its_upgrade(self) -> None:
        """release-doc-audit: every release a paper can cross with
        upgrade-template.sh (those after v0.4.0) marks its upgrade section
        **Command only.** or lists the manual steps."""
        for tag, entry in release_entries():
            if tag == "v0.4.0":
                break
            with self.subTest(release=tag):
                section = re.search(r"^### Upgrading a paper from \S+\n(.*?)(?=^### |\Z)", entry, re.M | re.S)
                self.assertIsNotNone(section, "no `### Upgrading a paper from <tag>` section")
                body = section.group(1).strip()
                self.assertTrue(body.startswith("**Command only.**") or re.search(r"^1\. ", body, re.M), body)


class UpgradeStateTests(unittest.TestCase):
    """A fresh paper at UPGRADE_SOURCE, upgraded with this release's
    upgrade-template.sh to this tree, tagged as the newest release."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory = tempfile.TemporaryDirectory(prefix="adoption-upgrade-")
        base = Path(cls.directory.name)
        cls.target = release_entries()[0][0]
        template = base / "template"
        shipped_tree(template)
        git("add", "-A", cwd=template)
        git("commit", "-qm", cls.target, cwd=template)
        git("tag", cls.target, cwd=template)
        git("fetch", "-q", "--depth", "1", f"file://{ROOT}", f"refs/tags/{UPGRADE_SOURCE}:refs/tags/{UPGRADE_SOURCE}",
            cwd=template)
        cls.paper = base / "paper"
        cls.paper.mkdir()
        subprocess.run(["tar", "-x", "-C", str(cls.paper)], check=True,
                       input=git("archive", UPGRADE_SOURCE, cwd=template).stdout)
        git("init", "-q", cwd=cls.paper)
        start_paper(cls.paper)
        cls.before = tree(cls.paper)
        # README "Template versions": the clone, and the target release's own copy of the command.
        git("clone", "-q", "--bare", str(template), str(cls.paper / CLONE), cwd=base)
        script = base / "upgrade-template.sh"
        script.write_bytes(git("show", f"{cls.target}:.agents/scripts/upgrade-template.sh", cwd=template).stdout)
        run = lambda *arguments: subprocess.run(["bash", str(script), *arguments], cwd=cls.paper,
                                                capture_output=True, text=True, check=False)
        cls.check = run("--check", cls.target)
        cls.after_check = tree(cls.paper)
        cls.upgrade = run(cls.target)
        cls.expected = base / "expected"
        shipped_tree(cls.expected)
        start_paper(cls.expected)
        registry = cls.expected / ".agents/content-registry.yaml"
        registry.write_text(re.sub(r"(?m)^  version: \S+$", f"  version: {cls.target}",
                                   registry.read_text(encoding="utf-8"), count=1), encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.directory.cleanup()

    def test_check_plans_without_conflicts_and_changes_nothing(self) -> None:
        self.assertEqual(self.check.returncode, 0, self.check.stdout + self.check.stderr)
        self.assertEqual(self.after_check, self.before)

    def test_the_upgrade_reaches_a_fresh_paper_of_this_release(self) -> None:
        """Every path equals a paper started from this tree, except the
        project-owned paper files, the Human documents marked `upgrade: review`,
        which keep the paper's own text, and optional content that is new in
        this release, which the command leaves to a manual adoption."""
        self.assertEqual(self.upgrade.returncode, 0, self.upgrade.stdout + self.upgrade.stderr)
        upgraded, expected = tree(self.paper), tree(self.expected)
        registry = yaml.safe_load((ROOT / ".agents/content-registry.yaml").read_text(encoding="utf-8"))
        owned = {entry["path"] for entry in registry["entries"] if entry.get("upgrade") == "review"}
        optional = tuple(entry["path"] for entry in registry["entries"] if entry.get("optional"))
        differing = {path for path in upgraded.keys() | expected.keys() if upgraded.get(path) != expected.get(path)}
        for path in sorted(differing):
            with self.subTest(path=path):
                new_optional = path not in upgraded and path.startswith(optional)
                self.assertTrue(path.startswith("paper/") or path in owned or new_optional, self.upgrade.stdout)
                self.assertEqual(upgraded.get(path), self.before.get(path))

    @unittest.skipIf(shutil.which("latexmk") is None or shutil.which("pdftotext") is None, "make check builds the paper")
    def test_make_check_passes_after_the_upgrade(self) -> None:
        self.assertEqual(self.upgrade.returncode, 0)
        result = subprocess.run(["make", "check"], cwd=self.paper, env=caller_environment(),
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout[-4000:] + result.stderr[-2000:])


class OnlineAuditStateTests(unittest.TestCase):
    """An existing bibliography of realistic size in the online metadata audit,
    with the stub checker, which costs time per entry it has not cached."""

    def audit(self, root: Path, *arguments: str, seconds: str = "0") -> tuple[int, dict[str, object]]:
        result = subprocess.run(
            [sys.executable, ".agents/scripts/check-reference-metadata.py", *arguments],
            cwd=root, env={**offline_environment(root.parent / "bin"), "FAKE_CHECKER_SECONDS": seconds},
            capture_output=True, text=True, check=False,
        )
        summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text(encoding="utf-8"))
        return result.returncode, summary

    def test_capped_full_audit_names_unfinished_entries_and_the_kept_cache_finishes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="adoption-online-") as directory:
            root = Path(directory) / "paper-repository"
            stub_uv(Path(directory) / "bin")
            shipped_tree(root)
            bibliography_without_ledger(root)
            code, summary = self.audit(root, "--timeout", "4", seconds="0.1")
            self.assertEqual((code, summary["outcome"]), (2, "incomplete"), summary)
            self.assertTrue(summary["checked_keys"] and summary["unfinished_keys"], summary)
            self.assertEqual(len(summary["checked_keys"]) + len(summary["unfinished_keys"]), ENTRIES)
            for _ in range(5):
                code, summary = self.audit(root, "--timeout", "4", seconds="0.1")
                if summary["outcome"] != "incomplete":
                    break
            self.assertEqual((code, summary["outcome"]), (0, "passed"), summary)

    def test_changed_tier_queries_nothing_for_an_unchanged_verified_bibliography(self) -> None:
        with tempfile.TemporaryDirectory(prefix="adoption-online-") as directory:
            root = Path(directory) / "paper-repository"
            queries = stub_uv(Path(directory) / "bin").with_name("queries.log")
            shipped_tree(root)
            bibliography_with_migrated_ledger(root)
            code, summary = self.audit(root, "--record")  # the one-time full audit writes the fingerprints
            self.assertEqual((code, summary["outcome"]), (0, "passed"), summary)
            for command in (["git", "add", "-A"], ["git", "-c", "user.name=Test", "-c",
                                                    "user.email=test@example.invalid", "commit", "-qm", "adopted"]):
                subprocess.run(command, cwd=root, check=True, capture_output=True)
            queries.unlink()
            code, summary = self.audit(root, "--scope", "changed", "--base", "HEAD")
            self.assertEqual((code, summary["outcome"], summary["selected_keys"]), (0, "skipped", []), summary)
            self.assertFalse(queries.exists(), "the changed tier sent a query")

if __name__ == "__main__":
    unittest.main()
