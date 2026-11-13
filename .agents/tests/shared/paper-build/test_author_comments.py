"""The release-check leftovers gate rejects author comments."""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHECKER = ROOT / ".agents/scripts/shared/paper-build/check_paper_build.py"


def checker():
    spec = importlib.util.spec_from_file_location("check_paper_build", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.pdf_text = lambda pdf: ""
    return module


class AuthorCommentLeftovers(unittest.TestCase):
    def test_the_paper_loads_the_author_comment_style(self) -> None:
        style = (ROOT / "paper/style/author-comments.sty").read_text(encoding="utf-8")
        for command in (r"\newcommand{\AuthorComment}", r"\newcommand{\agent}", r"\ifPaperNotes"):
            self.assertIn(command, style)
        main = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
        self.assertIn(r"\usepackage{style/author-comments}", main)

    def test_names_are_read_past_a_comment_header(self) -> None:
        module = checker()
        with tempfile.TemporaryDirectory() as directory:
            paper = Path(directory) / "paper"
            style = paper / "style/author-comments.sty"
            style.parent.mkdir(parents=True)
            style.write_text(
                "% author-comments.sty\n"
                "%   \\newcommand{\\bob}[1]{\\AuthorComment{red}{BO}{#1}}\n"
                "\\newcommand{\\AuthorComment}[3]{\\ifPaperNotes{\\color{#1}[#2: #3]}\\fi}\n"
                "\\newcommand{\\alice}[1]{\\AuthorComment{blue}{AL}{#1}} % 50\\% done\n",
                encoding="utf-8",
            )
            names = module.author_comment_names(paper)
        self.assertEqual(names, ["alice"])

    def test_commands_declared_outside_the_style_file_are_found(self) -> None:
        module = checker()
        with tempfile.TemporaryDirectory() as directory:
            paper = Path(directory) / "paper"
            style = paper / "style/author-comments.sty"
            main = paper / "main.tex"
            intro = paper / "sections/intro.tex"
            style.parent.mkdir(parents=True)
            intro.parent.mkdir()
            style.write_text(
                "% author-comments.sty\n"
                "\\newcommand{\\AuthorComment}[3]{\\ifPaperNotes{\\color{#1}[#2: #3]}\\fi}\n",
                encoding="utf-8",
            )
            main.write_text(
                "\\newcommand{\\bob}[1]{%\n"
                "  \\AuthorComment{red}{BO}{#1}%\n"
                "}\n"
                "\\NewDocumentCommand{\\carol}{m}{\\AuthorComment{green}{CA}{#1}}\n"
                "\\def\\dave#1{\\AuthorComment{teal}{DA}{#1}}\n"
                "\\newcommand{\\method}{Ours}\n",
                encoding="utf-8",
            )
            intro.write_text("\\method{} works.\n\\bob{one}\n\\carol{two} \\dave{three}\n", encoding="utf-8")
            fls = paper / "aux/submission/submission.fls"
            fls.parent.mkdir(parents=True)
            fls.write_text("".join(f"INPUT {path}\n" for path in (style, main, intro)), encoding="utf-8")
            arguments = argparse.Namespace(build_dir=paper, job="submission", paper=paper)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = module.cmd_leftovers(arguments)
            self.assertEqual(result, 1)
            self.assertEqual(
                [line.rsplit(" ", 1)[-1] for line in output.getvalue().splitlines()],
                ["paper/sections/intro.tex:2", "paper/sections/intro.tex:3", "paper/sections/intro.tex:3"],
                output.getvalue(),
            )
            for command in ("\\bob", "\\carol", "\\dave"):
                self.assertIn(f"unresolved {command} ", output.getvalue())

            intro.write_text("\\method{} works.\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = module.cmd_leftovers(arguments)
            self.assertEqual(result, 0, output.getvalue())
            self.assertIn("(checked: \\PaperTODO, \\PaperNote, \\AuthorComment, \\agent, \\bob, \\carol, \\dave)",
                          output.getvalue())

    def test_leftovers_flags_generic_and_per_author_calls(self) -> None:
        module = checker()
        with tempfile.TemporaryDirectory() as directory:
            paper = Path(directory) / "paper"
            style = paper / "style/author-comments.sty"
            intro = paper / "sections/intro.tex"
            style.parent.mkdir(parents=True)
            intro.parent.mkdir()
            style.write_text(
                "\\RequirePackage{xcolor}\n"
                "\\newcommand{\\AuthorComment}[3]{\\ifPaperNotes{\\color{#1}[#2: #3]}\\fi}\n"
                "\\newcommand{\\agent}[1]{\\AuthorComment{black}{Agent}{#1}}\n"
                "\\newcommand{\\alice}[1]{\\AuthorComment{blue}{AL}{#1}}\n",
                encoding="utf-8",
            )
            intro.write_text("\\alice{check this}\\agent{and this}\\PaperNote{old}\n", encoding="utf-8")
            fls = paper / "aux/submission/submission.fls"
            fls.parent.mkdir(parents=True)
            fls.write_text(
                "".join(f"INPUT {path}\n" for path in (style, intro)),
                encoding="utf-8",
            )
            arguments = argparse.Namespace(build_dir=paper, job="submission", paper=paper)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = module.cmd_leftovers(arguments)
            self.assertEqual(result, 1)
            for command in ("\\alice", "\\agent", "\\PaperNote"):
                self.assertIn(command, output.getvalue())

            intro.write_text("A clean sentence.\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = module.cmd_leftovers(arguments)
            self.assertEqual(result, 0, output.getvalue())


if __name__ == "__main__":
    unittest.main()
