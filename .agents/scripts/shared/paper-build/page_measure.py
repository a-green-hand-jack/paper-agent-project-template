#!/usr/bin/env python3
"""Measure the rendered pages of a build: short last lines, stretched word
spacing, columns that end early, and the height a section takes.

    page_measure.py last-lines    [--below 0.33]
    page_measure.py word-spacing  [--factor 1.8]
    page_measure.py column-gaps   [--lines 1.5]
    page_measure.py section-height --from TEXT [--to TEXT]

Every command reads the line boxes of `pdftotext -bbox-layout` (poppler) and
takes --pdf, --aux, --part main|appendix|all, --pages FIRST-LAST and --columns.
Without --pages the range comes from the aux file of the same build: the main
text ends on the page of \\label{PaperMainTextEnd}, the appendix starts on the
page of appendix A. The defaults measure the blind build. The output lists
candidates for a person to confirm on the page; it is not a check and exits 0
unless the input is unusable.
"""

from __future__ import annotations

import argparse
import re
import shutil
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

NS = "{http://www.w3.org/1999/xhtml}"
PAGE_NUMBER = re.compile(r"^(\d+|[ivxlcdm]+)$", re.IGNORECASE)


@dataclass
class Line:
    page: int
    x0: float
    y0: float
    x1: float
    y1: float
    words: list[tuple[float, float, str]] = field(default_factory=list)
    column: int = 0

    @property
    def text(self) -> str:
        return " ".join(word for _, _, word in self.words)

    @property
    def height(self) -> float:
        return self.y1 - self.y0


@dataclass
class Page:
    number: int
    width: float
    height: float
    lines: list[Line]


def parse(xml: str, first: int) -> list[Page]:
    root = ET.fromstring(re.sub(r"<!DOCTYPE[^>]*>", "", xml))
    pages = []
    for offset, page in enumerate(root.iter(NS + "page")):
        number = first + offset
        lines = []
        for element in page.iter(NS + "line"):
            words = [(float(w.get("xMin")), float(w.get("xMax")), w.text or "")
                     for w in element.iter(NS + "word")]
            if not words:
                continue
            lines.append(Line(number, float(element.get("xMin")), float(element.get("yMin")),
                              float(element.get("xMax")), float(element.get("yMax")), words))
        pages.append(Page(number, float(page.get("width")), float(page.get("height")), lines))
    return pages


def extract(pdf: Path, first: int, last: int) -> list[Page]:
    if not shutil.which("pdftotext"):
        raise SystemExit("page_measure: pdftotext (poppler) is not on PATH")
    out = subprocess.run(["pdftotext", "-bbox-layout", "-f", str(first), "-l", str(last), str(pdf), "-"],
                         capture_output=True, text=True, check=True)
    return parse(out.stdout, first)


def aux_pages(aux: Path) -> tuple[int | None, int | None]:
    """The page of PaperMainTextEnd and the first page of appendix A."""
    end = start = None
    for line in aux.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"\\newlabel\{PaperMainTextEnd\}\{\{[^}]*\}\{(\d+)\}", line)
        if match:
            end = int(match.group(1))
        match = re.search(r"\\contentsline \{section\}.*\{(\d+)\}\{appendix\.A\}", line)
        if match and start is None:
            start = int(match.group(1))
    return end, start


def page_count(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    match = re.search(r"^Pages:\s+(\d+)", out, re.MULTILINE)
    if not match:
        raise SystemExit(f"page_measure: no page count for {pdf}")
    return int(match.group(1))


def page_range(args: argparse.Namespace) -> tuple[int, int]:
    if args.pages:
        first, _, last = args.pages.partition("-")
        return int(first), int(last or first)
    total = page_count(args.pdf)
    if args.part == "all":
        return 1, total
    if not args.aux.is_file():
        raise SystemExit(f"page_measure: {args.aux} is missing; build first or pass --pages")
    end, start = aux_pages(args.aux)
    if args.part == "main":
        if end is None:
            raise SystemExit(f"page_measure: no PaperMainTextEnd label in {args.aux}; pass --pages")
        return 1, end
    if start is None:
        raise SystemExit(f"page_measure: no appendix A in {args.aux}; pass --pages")
    return start, total


def assign_columns(pages: list[Page], columns: int | None) -> int:
    """Set each line's column (1..n, 0 for a line across columns); return n."""
    if columns is None:
        left = right = across = 0
        for page in pages:
            middle = page.width / 2
            for line in page.lines:
                if line.x1 < middle:
                    left += 1
                elif line.x0 > middle:
                    right += 1
                else:
                    across += 1
        total = left + right + across
        columns = 2 if total and left > 0.3 * total and right > 0.3 * total else 1
    for page in pages:
        for line in page.lines:
            if columns == 1:
                line.column = 1
                continue
            share = page.width / columns
            first = int(line.x0 // share) + 1
            last = int((line.x1 - 0.01) // share) + 1
            line.column = first if first == last else 0
    return columns


def body(pages: list[Page]) -> list[Line]:
    return [line for page in pages for line in page.lines
            if line.column and not PAGE_NUMBER.match(line.text.strip())]


def percentile(values: list[float], share: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(share * len(ordered)))]


def geometry(lines: list[Line]) -> dict[int, tuple[float, float]]:
    """Each column's left and right edge, from the lines of all measured pages."""
    edges = {}
    for column in sorted({line.column for line in lines}):
        mine = [line for line in lines if line.column == column]
        edges[column] = (percentile([l.x0 for l in mine], 0.05), percentile([l.x1 for l in mine], 0.9))
    return edges


def line_pitch(lines: list[Line]) -> float:
    steps = []
    ordered = sorted(lines, key=lambda l: (l.page, l.column, l.y0))
    for before, after in zip(ordered, ordered[1:]):
        if (before.page, before.column) == (after.page, after.column):
            step = after.y0 - before.y0
            if step > 0:
                steps.append(step)
    return statistics.median(steps) if steps else 12.0


def ordered(lines: list[Line]) -> list[Line]:
    return sorted(lines, key=lambda l: (l.page, l.column, l.y0))


def text_height(lines: list[Line]) -> float:
    return statistics.median(line.height for line in lines)


def last_lines(lines: list[Line], below: float, tolerance: float = 2.0) -> list[tuple[Line, float]]:
    edges = geometry(lines)
    larger = 1.1 * text_height(lines)
    found = []
    for line in ordered(lines):
        left, right = edges[line.column]
        if right - line.x1 <= tolerance or line.height > larger:
            continue
        fill = (line.x1 - left) / (right - left)
        if fill < below:
            found.append((line, fill))
    return found


def gaps(line: Line) -> list[float]:
    return [after[0] - before[1] for before, after in zip(line.words, line.words[1:])]


def word_spacing(lines: list[Line], factor: float, tolerance: float = 2.0) -> list[tuple[Line, float, float]]:
    edges = geometry(lines)
    full = [line for line in lines if edges[line.column][1] - line.x1 <= tolerance and len(line.words) > 2]
    found = []
    for page in sorted({line.page for line in full}):
        mine = [line for line in full if line.page == page]
        everything = [gap for line in mine for gap in gaps(line)]
        if not everything:
            continue
        typical = statistics.median(everything)
        for line in mine:
            spacing = statistics.median(gaps(line))
            if typical > 0 and spacing > factor * typical:
                found.append((line, spacing, spacing / typical))
    return sorted(found, key=lambda item: (item[0].page, item[0].column, item[0].y0))


def column_gaps(lines: list[Line], limit: float) -> tuple[list[tuple[int, int, float]], int]:
    pitch = line_pitch(lines)
    bottoms: dict[tuple[int, int], float] = {}
    for line in lines:
        key = (line.page, line.column)
        bottoms[key] = max(bottoms.get(key, 0.0), line.y1)
    last = max(page for page, _ in bottoms)
    floor = max(bottom for (page, _), bottom in bottoms.items() if page != last) if len(
        {page for page, _ in bottoms}) > 1 else max(bottoms.values())
    found = []
    for (page, column), bottom in sorted(bottoms.items()):
        if page == last:
            continue
        short = (floor - bottom) / pitch
        if short > limit:
            found.append((page, column, short))
    return found, last


def section_height(lines: list[Line], start: str, stop: str | None) -> tuple[Line, Line | None, float, float]:
    sequence = ordered(lines)
    begin = next((i for i, line in enumerate(sequence) if start in line.text), None)
    if begin is None:
        raise SystemExit(f"page_measure: no line contains {start!r}")
    head = sequence[begin]
    if stop is None and head.height <= 1.1 * text_height(lines):
        raise SystemExit(f"page_measure: {head.text!r} is set at text size; pass --to")
    end = None
    for i in range(begin + 1, len(sequence)):
        line = sequence[i]
        if stop is not None:
            if stop in line.text:
                end = i
                break
        elif line.height >= head.height - 0.5 and len(line.words) <= 12:
            end = i
            break
    tops: dict[tuple[int, int], float] = {}
    bottoms: dict[tuple[int, int], float] = {}
    for line in lines:
        key = (line.page, line.column)
        tops[key] = min(tops.get(key, line.y0), line.y0)
        bottoms[key] = max(bottoms.get(key, 0.0), line.y1)
    floor = max(bottoms.values())
    ceiling = statistics.median(tops.values())
    span = sequence[begin:end] if end is not None else sequence[begin:]
    after = (sequence[end].page, sequence[end].column) if end is not None else None
    keys = sorted({(line.page, line.column) for line in span})
    used = 0.0
    for key in keys:
        top = min(line.y0 for line in span if (line.page, line.column) == key)
        if key == after:
            bottom = sequence[end].y0
        elif key == keys[-1] and after is None:
            bottom = max(line.y1 for line in span if (line.page, line.column) == key)
        else:
            bottom = floor
        used += bottom - top
    return head, sequence[end] if end is not None else None, used / (floor - ceiling), used / line_pitch(lines)


def where(line: Line, columns: int) -> str:
    return f"p{line.page}" + (f" col {line.column}" if columns > 1 else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--pdf", type=Path, default=Path(".project/build/blind.pdf"))
    common.add_argument("--aux", type=Path, default=None, help="default: the aux file of the --pdf build")
    common.add_argument("--part", choices=("main", "appendix", "all"), default="main")
    common.add_argument("--pages", help="FIRST-LAST; overrides --part")
    common.add_argument("--columns", type=int, choices=(1, 2), help="default: detected from the line boxes")
    commands = parser.add_subparsers(dest="command", required=True)
    one = commands.add_parser("last-lines", parents=[common], help="lines that stop short of the column end")
    one.add_argument("--below", type=float, default=0.33, help="list fills below this share (LAST_LINE_FILL)")
    two = commands.add_parser("word-spacing", parents=[common], help="justified lines with stretched spaces")
    two.add_argument("--factor", type=float, default=1.8, help="median space above this multiple of the page's")
    three = commands.add_parser("column-gaps", parents=[common], help="columns that end above the text area")
    three.add_argument("--lines", type=float, default=1.5, help="list gaps above this many lines")
    four = commands.add_parser("section-height", parents=[common], help="the column height a section takes")
    four.add_argument("--from", dest="start", required=True, help="text of the section's heading line")
    four.add_argument("--to", dest="stop", help="text of the first line after it; default the next heading")
    args = parser.parse_args()
    if args.aux is None:
        args.aux = args.pdf.parent / "aux" / args.pdf.stem / (args.pdf.stem + ".aux")
    if not args.pdf.is_file():
        raise SystemExit(f"page_measure: {args.pdf} is missing; build first")
    first, last = page_range(args)
    pages = extract(args.pdf, first, last)
    columns = assign_columns(pages, args.columns)
    lines = body(pages)
    if not lines:
        raise SystemExit(f"page_measure: no text on pages {first}-{last}")
    print(f"{args.pdf} pages {first}-{last}, {columns} column(s)")
    if args.command == "last-lines":
        found = last_lines(lines, args.below)
        for line, fill in found:
            print(f"{where(line, columns)}  fill {fill:.2f}  {line.text}")
        print(f"{len(found)} line(s) below {args.below:.2f}; headings, display math and footnotes are judged on the page")
    elif args.command == "word-spacing":
        found = word_spacing(lines, args.factor)
        for line, spacing, ratio in found:
            print(f"{where(line, columns)}  space {spacing:.1f}pt ({ratio:.1f}x)  {line.text}")
        print(f"{len(found)} justified line(s) above {args.factor:.1f}x the page's median space")
    elif args.command == "column-gaps":
        found, final = column_gaps(lines, args.lines)
        for page, column, short in found:
            print(f"p{page}" + (f" col {column}" if columns > 1 else "") + f"  ends {short:.1f} lines early")
        print(f"{len(found)} column(s) more than {args.lines:.1f} lines short; page {final} is judged by eye")
    else:
        head, stop, share, count = section_height(lines, args.start, args.stop)
        print(f"from {where(head, columns)}: {head.text}")
        print(f"to   {where(stop, columns) + ': ' + stop.text if stop else 'the end of the range'}")
        print(f"{share:.2f} column(s), about {count:.0f} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
