from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / ".agents/scripts/check-paper-interfaces.py"
DOCUMENTATION = ".agents/memory/project/paper-interfaces.md"


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def fixture(root: Path) -> None:
    (root / "paper/sections").mkdir(parents=True)
    (root / ".agents/memory/project").mkdir(parents=True)
    (root / "paper/macros.tex").write_text(
        """% Fixture interface definitions.

% Interface: PaperTODO
\\providecommand{\\PaperTODO}[1]{\\textbf{[TODO: #1]}}

% Interface: PaperNote
\\providecommand{\\PaperNote}[1]{}

% Interface: PaperIdentity
\\providecommand{\\PaperIdentity}[1]{}

% Interface: PaperTitle
\\providecommand{\\PaperTitle}{Fixture Title}

% Interface: MethodName
\\providecommand{\\MethodName}{Fixture Method}

% Interface: CoreTerm
\\providecommand{\\CoreTerm}{fixture core term}

% Interface: MainResult
\\providecommand{\\MainResult}{\\PaperTODO{main result}}

% Interface: MainResultUncertainty
\\providecommand{\\MainResultUncertainty}{\\PaperTODO{main-result uncertainty}}
""",
        encoding="utf-8",
    )
    (root / "paper/main.tex").write_text("\\title{\\PaperTitle}\n", encoding="utf-8")
    (root / "paper/sections/01_abstract.tex").write_text(
        "\\MethodName{} \\CoreTerm{} 50\\% of \\MainResult{} \\MainResultUncertainty{}\n",
        encoding="utf-8",
    )
    (root / DOCUMENTATION).write_text(
        """# Paper interfaces

| Interface | Meaning |
| --- | --- |
| `\\PaperTODO{...}` | placeholder |
| `\\PaperNote{...}` | author note |
| `\\PaperIdentity{...}` | identity string |
| `\\PaperTitle{}` | title |
| `\\MethodName{}` | method name |
| `\\CoreTerm{}` | central term |
| `\\MainResult{}` | main result |
| `\\MainResultUncertainty{}` | paired uncertainty |
""",
        encoding="utf-8",
    )


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new), encoding="utf-8")


class PaperInterfaceChecks(unittest.TestCase):
    def test_repository_interfaces_pass(self) -> None:
        result = run(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fixture_passes_without_uses_of_the_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            result = run(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("OK paper_interfaces: 8 interfaces", result.stdout)

    def test_a_project_interface_can_be_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/macros.tex", "% Interface: CoreTerm\n\\providecommand{\\CoreTerm}{fixture core term}\n", "")
            edit(root / "paper/sections/01_abstract.tex", "\\CoreTerm{} ", "")
            edit(root / DOCUMENTATION, "| `\\CoreTerm{}` | central term |\n", "")
            result = run(root)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_required_interface_marker_cannot_be_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/macros.tex", "% Interface: PaperNote\n", "")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing the required interface marker: % Interface: PaperNote", result.stdout)

    def test_longer_command_cannot_satisfy_a_definition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/macros.tex", "\\providecommand{\\MainResult}{\\PaperTODO{main result}}\n", "")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("marks MainResult as an interface but does not define \\MainResult", result.stdout)

    def test_longer_marker_cannot_mark_a_definition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/macros.tex", "% Interface: MainResult\n", "")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("defines \\MainResult without an '% Interface: MainResult' marker", result.stdout)

    def test_unmarked_definition_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/macros.tex", "% Fixture interface definitions.\n",
                 "% Fixture interface definitions.\n\\newcommand{\\Accuracy}{93.1}\n")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("defines \\Accuracy without an '% Interface: Accuracy' marker", result.stdout)

    def test_longer_command_cannot_satisfy_a_consumer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/sections/01_abstract.tex", "\\MainResult{}", "\\MainResultUncertainty{}")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("interface \\MainResult is not used anywhere in paper/", result.stdout)

    def test_commented_use_is_not_a_consumer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/sections/01_abstract.tex", "\\MethodName{} ", "% \\MethodName{}\n")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("interface \\MethodName is not used anywhere in paper/", result.stdout)

    def test_longer_command_cannot_satisfy_the_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / DOCUMENTATION, "| `\\MainResult{}` | main result |\n", "")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not document \\MainResult", result.stdout)

    def test_bare_control_word_call_followed_by_text_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/sections/01_abstract.tex", "\\CoreTerm{} ", "\\CoreTerm has ")
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("paper/sections/01_abstract.tex:1: call \\CoreTerm as \\CoreTerm{}", result.stdout)

    def test_macro_with_arguments_may_be_followed_by_a_space(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            edit(root / "paper/sections/01_abstract.tex", "\\CoreTerm{} ", "\\CoreTerm{} \\PaperTODO {later} ")
            result = run(root)
            self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
