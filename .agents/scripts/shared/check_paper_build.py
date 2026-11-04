#!/usr/bin/env python3
"""Check a finished paper build: LaTeX log problems, the main-text page count,
the PDF text layer, anonymity of the blind build and leftovers in a build.

Each subcommand reads one build job from BUILD_DIR as paper/Makefile writes it:
BUILD_DIR/<job>.pdf and BUILD_DIR/aux/<job>/<job>.{log,blg,fls,aux}. It prints
one line per finding and exits 1 when a finding fails the check.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

LOG_PATTERNS = (
    ("undefined reference", re.compile(r"Reference [`']([^']+)' on page \S+ undefined")),
    ("undefined citation", re.compile(r"Citation [`']([^']+)' on page \S+ undefined")),
    ("multiply defined label", re.compile(r"Label [`']([^']+)' multiply defined")),
    ("missing file", re.compile(r"File [`']([^']+)' not found")),
)
LATEX_ERROR = re.compile(r"^(?:\./)?([^\s:]+\.(?:tex|sty|cls)):(\d+): (.+)$", re.M)
BLG_MISSING = re.compile(r'I didn\'t find a database entry for "([^"]+)"')
MAIN_TEXT_END = re.compile(r"\\newlabel\{PaperMainTextEnd\}\{\{[^{}]*\}\{([^{}]*)\}")
IDENTITY = re.compile(r"\\PaperIdentity\{([^{}]+)\}")
# The identity paper/authors.tex ships with; a release declares the real one.
PLACEHOLDER_IDENTITIES = ("Template-Author-Name", "template-author@example.invalid", "Template-Institution")
LEFTOVER_MACROS = ("PaperTODO", "PaperNote")
DEFINITION = re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|def)\b")
UNDERSCORE_TOKEN = re.compile(r"[A-Za-z0-9.:/-]*[A-Za-z0-9](?:\\_[A-Za-z0-9.:/-]*[A-Za-z0-9])+")
SOURCE_SUFFIXES = {".tex", ".sty", ".cls", ""}


def job_files(build_dir: Path, job: str) -> dict[str, Path]:
    aux = build_dir / "aux" / job
    return {
        "pdf": build_dir / f"{job}.pdf",
        "log": aux / f"{job}.log",
        "blg": aux / f"{job}.blg",
        "fls": aux / f"{job}.fls",
        "aux": aux / f"{job}.aux",
        "bbl": aux / f"{job}.bbl",
    }


def active(line: str) -> str:
    """Drop a TeX comment, keeping an escaped percent sign."""
    return re.split(r"(?<!\\)%", line, maxsplit=1)[0]


def lines_of(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def shown(path: Path, paper: Path) -> str:
    return path.relative_to(paper.parent).as_posix()


def paper_sources(files: dict[str, Path], paper: Path) -> list[Path]:
    """The files under paper/ that the build read, from the recorder file."""
    if not files["fls"].is_file():
        raise SystemExit(f"ERROR missing {files['fls']}; build the job first")
    pwd = paper
    found: list[Path] = []
    for line in lines_of(files["fls"]):
        if line.startswith("PWD "):
            pwd = Path(line[4:])
            continue
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        path = (path if path.is_absolute() else pwd / path).resolve()
        if path.suffix not in SOURCE_SUFFIXES or not path.is_file():
            continue
        try:
            path.relative_to(paper)
        except ValueError:
            continue
        if path not in found:
            found.append(path)
    return found


def pdf_text(pdf: Path) -> str:
    if shutil.which("pdftotext") is None:
        raise SystemExit("ERROR pdftotext is required (poppler-utils)")
    if not pdf.is_file():
        raise SystemExit(f"ERROR missing {pdf}; build the job first")
    return subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True).stdout


def pdf_info(pdf: Path) -> str:
    if shutil.which("pdfinfo") is None:
        raise SystemExit("ERROR pdfinfo is required (poppler-utils)")
    return subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout


def locate(paper: Path, key: str) -> list[str]:
    hits = []
    for path in sorted(paper.rglob("*.tex")):
        for number, line in enumerate(lines_of(path), 1):
            if key in active(line):
                hits.append(f"{shown(path, paper)}:{number}")
    return hits[:3]


def cmd_log(args: argparse.Namespace) -> int:
    files = job_files(args.build_dir, args.job)
    if not files["log"].is_file():
        print(f"ERROR {args.job}: no log at {files['log']}")
        return 1
    log = files["log"].read_text(encoding="utf-8", errors="replace")
    findings: list[tuple[str, str]] = []
    for kind, pattern in LOG_PATTERNS:
        for key in dict.fromkeys(pattern.findall(log)):
            findings.append((kind, key))
    if files["blg"].is_file():
        for key in dict.fromkeys(BLG_MISSING.findall(files["blg"].read_text(errors="replace"))):
            if ("undefined citation", key) not in findings:
                findings.append(("undefined citation", key))
    failed = bool(findings)
    for kind, key in findings:
        where = ", ".join(locate(args.paper, key)) or "source location not found"
        print(f"ERROR {args.job}: {kind} {key} ({where})")
    for name, number, message in dict.fromkeys(LATEX_ERROR.findall(log)):
        if any(p.search(message) for _, p in LOG_PATTERNS):
            continue
        print(f"ERROR {args.job}: LaTeX error at paper/{name}:{number}: {message.strip()}")
        failed = True
    if not failed:
        print(f"OK {args.job}: no undefined references or citations, missing files or multiply defined labels")
    return 1 if failed else 0


def main_text_pages(files: dict[str, Path]) -> int | None:
    if not files["aux"].is_file():
        return None
    match = MAIN_TEXT_END.search(files["aux"].read_text(encoding="utf-8", errors="replace"))
    return int(match.group(1)) if match and match.group(1).isdigit() else None


def cmd_pages(args: argparse.Namespace) -> int:
    files = job_files(args.build_dir, args.job)
    main = main_text_pages(files)
    match = re.search(r"^Pages:\s+(\d+)", pdf_info(files["pdf"]), re.M)
    total = match.group(1) if match else "unknown"
    if main is None:
        print(f"ERROR {args.job}: cannot read the main-text page count; is \\label{{PaperMainTextEnd}} in main.tex?")
        return 1
    if args.budget.strip().lower() == "none":
        print(f"PAGES {args.job}: main text {main} pages, {total} in total; no page limit (PAGE_BUDGET=none)")
        return 0
    if not args.budget:
        level = "ERROR" if args.require_budget else "PAGES"
        print(f"{level} {args.job}: main text {main} pages, {total} in total; no page budget set"
              " (PAGE_BUDGET=<pages>, or PAGE_BUDGET=none for a release without a page limit)")
        return 1 if args.require_budget else 0
    if not args.budget.strip().isdigit():
        print(f"ERROR {args.job}: PAGE_BUDGET must be a number of pages or none, not '{args.budget}'")
        return 1
    budget = int(args.budget)
    if main <= budget:
        print(f"PAGES {args.job}: main text {main} of {budget} pages, {total} in total")
        return 0
    level = "ERROR" if args.fail_over else "PAGES"
    print(f"{level} {args.job}: main text {main} pages is OVER the budget of {budget}, {total} in total")
    return 1 if args.fail_over else 0


def cmd_underscores(args: argparse.Namespace) -> int:
    files = job_files(args.build_dir, args.job)
    tokens: list[tuple[str, str]] = []
    for path in paper_sources(files, args.paper):
        if path.suffix != ".tex":
            continue
        for number, line in enumerate(lines_of(path), 1):
            text = active(line)
            if DEFINITION.search(text):
                continue
            for token in UNDERSCORE_TOKEN.findall(text):
                tokens.append((token.replace("\\_", "_"), f"{shown(path, args.paper)}:{number}"))
    if not tokens:
        print(f"OK {args.job}: no escaped underscores in the sources to check in the PDF text layer")
        return 0
    flat = re.sub(r"[\s-]", "", pdf_text(files["pdf"]))
    missing = [(t, w) for t, w in tokens if t.replace("-", "") not in flat]
    for token, where in missing:
        print(f"ERROR {args.job}: '{token}' ({where}) lost its underscore in the PDF text layer; load T1 font encoding")
    if not missing:
        print(f"OK {args.job}: {len(tokens)} escaped underscores survive in the PDF text layer")
    return 1 if missing else 0


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


def bbl_text(path: Path) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\\newblock|\\bibitem(\[[^\]]*\])?\{[^}]*\}", " ", text)
    return normalize(re.sub(r"[{}]", "", text.replace("~", " ").replace("\\ ", " ")))


def cmd_identity(args: argparse.Namespace) -> int:
    files = job_files(args.build_dir, args.job)
    authors = args.paper / "authors.tex"
    identities: list[str] = []
    if authors.is_file():
        for line in lines_of(authors):
            identities += [i.strip() for i in IDENTITY.findall(active(line)) if i.strip()]
    if not identities:
        print(f"ERROR no \\PaperIdentity declarations in {shown(authors, args.paper)}")
        return 1
    failed = 0
    for identity in identities:
        if identity in PLACEHOLDER_IDENTITIES:
            print(f"ERROR {args.job}: {shown(authors, args.paper)} still declares the template placeholder"
                  f" '{identity}'; declare the paper's real identity")
            failed = 1
    text = normalize(pdf_text(files["pdf"]))
    info = normalize(pdf_info(files["pdf"]))
    bibliography = bbl_text(files["bbl"])
    sources = paper_sources(files, args.paper)
    for identity in identities:
        needle = normalize(identity)
        in_text, in_bib = text.count(needle), bibliography.count(needle)
        if in_text > in_bib:
            print(f"ERROR {args.job}: '{identity}' appears {in_text} time(s) in the PDF text"
                  + (f", only {in_bib} of them explained by the bibliography" if in_bib else ""))
            failed = 1
        elif in_text:
            print(f"NOTE {args.job}: '{identity}' appears {in_text} time(s), all in the bibliography;"
                  " cite your own work in the third person")
        if needle in info:
            print(f"ERROR {args.job}: '{identity}' appears in the PDF metadata")
            failed = 1
        for path in sources:
            for number, line in enumerate(lines_of(path), 1):
                if needle in normalize(line):
                    print(f"ERROR {args.job}: '{identity}' in {shown(path, args.paper)}:{number}, a source the blind build reads")
                    failed = 1
    if not failed:
        print(f"OK {args.job}: none of {len(identities)} identity strings in the PDF text, its metadata"
              f" or the {len(sources)} sources it read")
    return failed


def cmd_leftovers(args: argparse.Namespace) -> int:
    files = job_files(args.build_dir, args.job)
    calls = re.compile(r"\\(" + "|".join(LEFTOVER_MACROS) + r")(?![A-Za-z@])")
    failed = 0
    for path in paper_sources(files, args.paper):
        for number, line in enumerate(lines_of(path), 1):
            text = active(line)
            if DEFINITION.search(text):
                continue
            for name in calls.findall(text):
                print(f"ERROR {args.job}: unresolved \\{name} in {shown(path, args.paper)}:{number}")
                failed = 1
    for line in pdf_text(files["pdf"]).splitlines():
        if re.search(r"\bTODO\b", line):
            print(f"ERROR {args.job}: 'TODO' in the PDF text: {line.strip()[:80]}")
            failed = 1
    if not failed:
        print(f"OK {args.job}: no unresolved \\PaperTODO, \\PaperNote or TODO")
    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--paper", type=Path, default=Path("paper"))
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in (("log", cmd_log), ("pages", cmd_pages), ("underscores", cmd_underscores),
                       ("identity", cmd_identity), ("leftovers", cmd_leftovers)):
        command = sub.add_parser(name)
        command.add_argument("job")
        command.set_defaults(func=func)
        if name == "pages":
            command.add_argument("--budget", default="")
            command.add_argument("--fail-over", action="store_true")
            command.add_argument("--require-budget", action="store_true")
    args = parser.parse_args()
    args.paper = args.paper.resolve()
    args.build_dir = args.build_dir.resolve()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
