#!/usr/bin/env python3
"""Check the development plane's skills, memory and knowledge records.

- Every SKILL.md under .agents/skills/ starts with YAML front matter that
  parses, whose `name` is the skill's directory and whose `description` is set;
  the skill is registered as `kind: skill` in .agents/content-registry.yaml,
  listed in its group's generated index (.agents/skills/<group>/AGENTS.md), and
  its package holds no README.md or AGENTS.md.
- A skill with a PROVENANCE.md lists every file of its package with the SHA-256
  of the upstream bytes. A file marked `unchanged` must still hash to it; a
  SKILL.md marked `unchanged above ## In this repository` must hash to it once
  the trailing section is cut off. `patched` files are described under
  "Local changes" and are not hashed.
- Every Markdown file in .agents/{memory,knowledge}/{shared,project}/ is
  registered; a record (`kind: memory` or `knowledge`) has the front matter and
  sections of its entry-template.md, a `name` equal to its file name and a link
  in that directory's generated index. Scope, lifecycle and refresh condition
  live in the registry, which check-development.sh validates.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_registry  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover - depends on the machine
    print("ERROR PyYAML is required: install python3-yaml (apt) or pyyaml (pip)")
    sys.exit(2)

SECTION = "\n## In this repository\n"
RECORD_KEYS = {
    "memory": ("name", "date", "source", "applies_to"),
    "knowledge": ("name", "date", "source", "applies_to"),
}
RECORD_SECTIONS = {
    "memory": ("## Decision", "## Why", "## Apply"),
    "knowledge": ("## Fact", "## Evidence", "## Refresh"),
}
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`?([^|`]*)`?\s*\|\s*([0-9a-fA-F]{64})\s*\|\s*(.+?)\s*\|\s*$")


class Report:
    def __init__(self) -> None:
        self.failed = False

    def error(self, message: str) -> None:
        print(f"ERROR {message}")
        self.failed = True


def front_matter(path: Path, report: Report, shown: str) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        report.error(f"{shown}: does not start with YAML front matter (---)")
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        report.error(f"{shown}: the front matter is not closed by a --- line")
        return None
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        where = getattr(exc, "problem_mark", None)
        line = f" at line {where.line + 2}" if where else ""
        report.error(f"{shown}: front matter is not valid YAML{line}: {getattr(exc, 'problem', exc)};"
                     " quote a value that contains ': ' or fold it with >-")
        return None
    if not isinstance(data, dict):
        report.error(f"{shown}: front matter is not a mapping")
        return None
    return data


def upstream_bytes(path: Path, status: str) -> bytes:
    data = path.read_bytes()
    if "above" in status:
        cut = data.find(SECTION.encode())
        if cut >= 0:
            return data[:cut]
    return data


def check_provenance(skill: Path, root: Path, report: Report) -> int:
    provenance = skill / "PROVENANCE.md"
    shown = provenance.relative_to(root).as_posix()
    listed: dict[str, tuple[str, str]] = {}
    for line in provenance.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            listed[match.group(1)] = (match.group(3).lower(), match.group(4).replace("`", "").strip())
    if not listed:
        report.error(f"{shown}: no file table with SHA-256 values")
        return 0
    files = sorted(p.relative_to(skill).as_posix() for p in skill.rglob("*")
                   if p.is_file() and p.name != "PROVENANCE.md" and "__pycache__" not in p.parts)
    for name in files:
        if name not in listed:
            report.error(f"{shown}: {name} is in the package but not in the file table")
    hashed = 0
    for name, (digest, status) in listed.items():
        path = skill / name
        if not path.is_file():
            report.error(f"{shown}: lists {name}, which is not in the package")
            continue
        if status.startswith("patched"):
            continue
        if not status.startswith("unchanged"):
            report.error(f"{shown}: {name} has status '{status}'; use unchanged,"
                         " unchanged above ## In this repository, or patched")
            continue
        data = upstream_bytes(path, status)
        candidates = {hashlib.sha256(data).hexdigest()}
        if "above" in status and data.endswith(b"\n"):
            # An upstream file without a final newline gets one before the section.
            candidates.add(hashlib.sha256(data[:-1]).hexdigest())
        if digest not in candidates:
            report.error(f"{shown}: {name} no longer matches its upstream SHA-256 ({status});"
                         " move a local change into the trailing section or record it as patched")
        hashed += 1
    return hashed


def check_skills(root: Path, entries: dict, report: Report) -> None:
    skills_root = root / ".agents/skills"
    count = hashed = 0
    for entry in sorted(skills_root.rglob("SKILL.md")):
        skill = entry.parent
        relative = skill.relative_to(skills_root).as_posix()
        shown = entry.relative_to(root).as_posix()
        count += 1
        data = front_matter(entry, report, shown)
        if data is not None:
            if data.get("name") != skill.name:
                report.error(f"{shown}: front matter name '{data.get('name')}' is not the directory name '{skill.name}'")
            if not isinstance(data.get("description"), str) or not data["description"].strip():
                report.error(f"{shown}: front matter has no description")
        group = relative.split("/", 1)[0]
        index_path = skills_root / group / "AGENTS.md"
        index = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
        if f"]({skill.name}/SKILL.md)" not in index:
            report.error(f"{shown}: `{relative}/` is not listed in {index_path.relative_to(root).as_posix()}")
        if entries.get(f".agents/skills/{relative}/", {}).get("kind") != "skill":
            report.error(f"{shown}: .agents/skills/{relative}/ has no skill entry in .agents/content-registry.yaml")
        for stray in ("README.md", "AGENTS.md"):
            if (skill / stray).exists():
                report.error(f"{shown}: the skill package holds {stray}; keep only the skill and its resources")
    for provenance in sorted(skills_root.rglob("PROVENANCE.md")):
        hashed += check_provenance(provenance.parent, root, report)
    print(f"CHECKED {count} skills, {hashed} vendored files hashed against their provenance")


def check_records(root: Path, plane: str, entries: dict, report: Report) -> None:
    count = 0
    for scope in ("shared", "project"):
        directory = root / ".agents" / plane / scope
        if not directory.is_dir():
            continue
        index_path = directory / "AGENTS.md"
        index = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
        for path in sorted(directory.glob("*.md")):
            if path.name == "AGENTS.md":
                continue
            shown = path.relative_to(root).as_posix()
            kind = entries.get(shown, {}).get("kind")
            if kind is None:
                report.error(f"{shown}: has no entry in .agents/content-registry.yaml")
                continue
            if kind != plane:
                continue  # a registered document, such as a record template
            count += 1
            data = front_matter(path, report, shown)
            if data is not None:
                for key in RECORD_KEYS[plane]:
                    if key not in data:
                        report.error(f"{shown}: front matter has no '{key}'")
                if data.get("name") != path.stem:
                    report.error(f"{shown}: front matter name '{data.get('name')}' is not the file name '{path.stem}'")
                date = data.get("date")
                if not isinstance(date, datetime.date) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date)):
                    report.error(f"{shown}: date must be YYYY-MM-DD")
            text = path.read_text(encoding="utf-8")
            positions = [text.find(f"\n{heading}\n") for heading in RECORD_SECTIONS[plane]]
            if -1 in positions or positions != sorted(positions):
                report.error(f"{shown}: needs the sections {', '.join(RECORD_SECTIONS[plane])} in this order")
            if f"]({path.name})" not in index:
                report.error(f"{shown}: not linked from {index_path.relative_to(root).as_posix()}")
    print(f"CHECKED {count} {plane} records")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    root = parser.parse_args().root.expanduser().resolve()
    registry_path = root / ".agents/content-registry.yaml"
    report = Report()
    entries: dict = {}
    if registry_path.is_file():
        try:
            data = content_registry.loads(registry_path.read_text(encoding="utf-8"))
            entries = {entry["path"]: entry for entry in data.get("entries", [])}
        except content_registry.RegistryError as exc:
            report.error(f".agents/content-registry.yaml does not parse: {exc}")
    else:
        report.error("missing .agents/content-registry.yaml")
    check_skills(root, entries, report)
    check_records(root, "memory", entries, report)
    check_records(root, "knowledge", entries, report)
    if report.failed:
        return 1
    print("OK agent_content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
