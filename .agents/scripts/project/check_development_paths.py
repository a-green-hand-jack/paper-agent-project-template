#!/usr/bin/env python3
"""Check that the paths and links the development plane names really exist, and
that no document still points at a root document this template retired."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOTS = ("AGENTS.md", "README.md", ".agents/AGENTS.md", ".agents/notes/AGENTS.md",
         ".agents/scripts/AGENTS.md", ".agents/skills/AGENTS.md")
TREES = (".agents/memory", ".agents/knowledge", ".agents/execution")
PATH = re.compile(r"(?<![\w/.-])((?:\.agents|paper)/[A-Za-z0-9_./-]+)")
# PAPER.md and DEV.md were retired in v0.5.0; their content lives in the records
# under .agents/memory/project/paper-foundation/.
RETIRED = ("PAPER.md", "DEV.md")
RETIRED_NAME = re.compile(r"(?<![\w/.-])(" + "|".join(re.escape(name) for name in RETIRED) + r")(?![\w-])")
SKIP_PREFIX = ("paper/images/",)
SKIP_TREE = (".agents/memory/project/template-maintenance/",)
ALLOW = ".agents/scripts/project/check-development-paths.allow"


def tracked(root: Path) -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, text=True, capture_output=True, check=True)
    return [p for p in out.stdout.split("\0") if p]


def vendored_skills(files: list[str]) -> set[str]:
    return {os.path.dirname(name) + "/" for name in files if name.endswith("/PROVENANCE.md")}


def skill_files(root: Path, files: list[str]) -> list[str]:
    vendored = vendored_skills(files)
    found = []
    for name in files:
        if not name.endswith("/SKILL.md"):
            continue
        if any(name.startswith(prefix) for prefix in vendored):
            continue
        found.append(name)
    return found


def skill_sources(root: Path, files: list[str]) -> list[str]:
    """The reference documents a house skill ships beside its SKILL.md."""
    vendored = vendored_skills(files)
    return [name for name in files
            if name.startswith(".agents/skills/") and name.endswith(".md") and "/sources/" in name
            and not any(name.startswith(prefix) for prefix in vendored)]


def documents(root: Path, files: list[str]) -> list[str]:
    chosen = [name for name in ROOTS if name in files and (root / name).is_file()]
    for name in files:
        if not name.endswith(".md"):
            continue
        if any(name.startswith(tree) for tree in SKIP_TREE):
            continue
        if any(name.startswith(tree + "/") for tree in TREES):
            chosen.append(name)
    chosen.extend(skill_files(root, files))
    chosen.extend(skill_sources(root, files))
    return sorted(set(chosen))


def references(root: Path, files: list[str]) -> list[tuple[str, str]]:
    found = []
    for name in documents(root, files):
        if not (root / name).is_file():
            continue  # listed by Git, deleted in the working tree
        text = (root / name).read_text(encoding="utf-8", errors="replace")
        for raw in PATH.findall(text):
            path = raw.rstrip(".,;:)`'\"")
            if not path or "<" in path or "{" in path or path.endswith(("-", "_")):
                continue
            if path.startswith(SKIP_PREFIX):
                continue
            found.append((name, path))
    return found


def retired_references(root: Path, files: list[str]) -> list[tuple[str, str]]:
    found = []
    for name in documents(root, files):
        if not (root / name).is_file():
            continue
        text = (root / name).read_text(encoding="utf-8", errors="replace")
        found.extend((name, match) for match in RETIRED_NAME.findall(text))
    return found


def allowed(root: Path) -> dict[tuple[str, str], str]:
    file = root / ALLOW
    granted = {}
    if not file.is_file():
        return granted
    for line in file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, path, reason = (part.strip() for part in line.split("\t", 2))
        granted[(name.rstrip("/"), path.rstrip("/"))] = reason
    return granted


def missing(root: Path, name: str, path: str) -> bool:
    target = root / path.rstrip("/")
    return not (target.exists() or target.is_symlink())


def link_errors(root: Path, files: list[str]) -> list[str]:
    problems = []
    for name in (".claude", ".pi"):
        if name not in files:
            continue
        link = root / name
        if not link.is_symlink() or os.readlink(link) != ".agents":
            problems.append(f"{name}: expected a relative symlink to .agents")
    for name in files:
        if not name.endswith("CLAUDE.md"):
            continue
        link = root / name
        if not link.is_symlink() or os.readlink(link) != "AGENTS.md":
            problems.append(f"{name}: expected a relative symlink to AGENTS.md")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()
    root = (args.root or Path(__file__).resolve().parents[3]).resolve()
    files = tracked(root)
    failures = []
    granted = allowed(root)
    checked = references(root, files)
    exempt = 0
    for name, path in checked:
        if (name, path.rstrip("/")) in granted:
            exempt += 1
            continue
        if missing(root, name, path):
            failures.append(f"{name}: {path} does not exist")
    retired = retired_references(root, files)
    for name, path in retired:
        if (name, path) in granted:
            exempt += 1
            continue
        failures.append(f"{name}: {path} is retired; name the record that replaced it")
    failures.extend(link_errors(root, files))
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"FAILED paths: {len(failures)} problem(s) in {len(checked)} references")
        return 1
    print(f"OK paths: {len(checked) - exempt} references and their links exist; "
          f"no reference to a retired {', '.join(RETIRED)}; "
          f"{exempt} allowed by {ALLOW}; {len(SKIP_TREE)} historical tree(s) not scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
