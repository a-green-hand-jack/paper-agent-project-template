"""The adoption states this template documents, built from its shipped files in
a temporary root and run through the real gates before each release (DEV.md,
"Releases"). A paper deletes this file with the rest of `scope: template`."""
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
