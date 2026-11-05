#!/usr/bin/env python3
"""Check the paper's interface macros.

The interfaces are the commands marked `% Interface: Name` in paper/macros.tex.
Every interface must be defined there and documented in
.agents/memory/project/paper-interfaces.md; every interface except the authoring
helpers must be used somewhere in paper/; a command without arguments must be
called with braces (\\Name{}) so that the space after it survives; and
paper/macros.tex defines nothing that is not marked as an interface.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MACROS = "paper/macros.tex"
DOCUMENTATION = ".agents/memory/project/paper-interfaces.md"
REQUIRED = ("PaperTODO", "PaperNote", "PaperIdentity", "PaperTitle")
# Authoring helpers: a finished paper uses none of them, so none needs a consumer.
HELPERS = ("PaperTODO", "PaperNote", "PaperIdentity")
MARKER = re.compile(r"^\s*%\s*Interface:\s*([A-Za-z@]+)\s*$", re.M)
DEFINITION = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?\s*"
    r"(?:\{\s*\\([A-Za-z@]+)\s*\}|\\([A-Za-z@]+))\s*(\[\s*\d\s*\])?"
)


def command(name: str) -> str:
    return rf"\\{re.escape(name)}(?![A-Za-z@])"


def active(text: str) -> str:
    """Drop TeX comments, keeping an escaped percent sign."""
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines())


def error(message: str) -> int:
    print(f"ERROR {message}")
    return 1


def check(root: Path) -> int:
    macros_path = root / MACROS
    if not macros_path.is_file():
        return error(f"missing {MACROS}")
    raw = macros_path.read_text(encoding="utf-8")
    code = 0

    interfaces: list[str] = []
    for name in MARKER.findall(raw):
        if name in interfaces:
            code |= error(f"{MACROS} marks {name} as an interface twice")
        else:
            interfaces.append(name)
    for name in REQUIRED:
        if name not in interfaces:
            code |= error(f"{MACROS} is missing the required interface marker: % Interface: {name}")

    takes_arguments: dict[str, bool] = {}
    for match in DEFINITION.finditer(active(raw)):
        name = match.group(1) or match.group(2)
        takes_arguments[name] = bool(match.group(3))
    for name in interfaces:
        if name not in takes_arguments:
            code |= error(f"{MACROS} marks {name} as an interface but does not define \\{name}")
    for name in takes_arguments:
        if name not in interfaces:
            code |= error(
                f"{MACROS} defines \\{name} without an '% Interface: {name}' marker;"
                " mark and document it, or move a display helper to paper/style/"
            )

    consumers: dict[str, list[str]] = {name: [] for name in interfaces if name not in HELPERS}
    for path in sorted((root / "paper").rglob("*.tex")):
        relative = path.relative_to(root).as_posix()
        text = active(path.read_text(encoding="utf-8"))
        for name in interfaces:
            if relative != MACROS and name in consumers and re.search(command(name), text):
                consumers[name].append(relative)
            if not takes_arguments.get(name, True):
                for match in re.finditer(command(name) + r"[ \t\r\n]+", text):
                    line = text.count("\n", 0, match.start()) + 1
                    code |= error(f"{relative}:{line}: call \\{name} as \\{name}{{}} so the space after it survives")
    for name, paths in consumers.items():
        if not paths:
            code |= error(f"interface \\{name} is not used anywhere in paper/; use it or remove its marker and definition")

    documentation = root / DOCUMENTATION
    if not documentation.is_file():
        code |= error(f"missing {DOCUMENTATION}")
    else:
        text = documentation.read_text(encoding="utf-8")
        for name in interfaces:
            if not re.search(command(name), text):
                code |= error(f"{DOCUMENTATION} does not document \\{name}")

    if code == 0:
        print(f"OK paper_interfaces: {len(interfaces)} interfaces defined, used and documented")
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    return check(args.root.expanduser().resolve())


if __name__ == "__main__":
    sys.exit(main())
