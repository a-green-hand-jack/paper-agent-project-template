from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / ".agents/scripts/shared/paper-build/page_measure.py"
SPEC = importlib.util.spec_from_file_location("page_measure", TOOL)
measure = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = measure
SPEC.loader.exec_module(measure)


def line(y: float, words: list[tuple[float, float, str]], height: float = 10.0) -> str:
    inner = "".join(f'<word xMin="{a}" yMin="{y}" xMax="{b}" yMax="{y + height}">{w}</word>' for a, b, w in words)
    return (f'<line xMin="{words[0][0]}" yMin="{y}" xMax="{words[-1][1]}" yMax="{y + height}">'
            f"{inner}</line>")


def spaced(left: float, right: float, count: int, gap: float) -> list[tuple[float, float, str]]:
    width = (right - left - gap * (count - 1)) / count
    return [(left + i * (width + gap), left + i * (width + gap) + width, f"w{i}") for i in range(count)]


def page(lines: list[str]) -> str:
    return '<page width="600" height="800"><flow><block>' + "".join(lines) + "</block></flow></page>"


def document(pages: list[str]) -> str:
    return '<html xmlns="http://www.w3.org/1999/xhtml"><body><doc>' + "".join(pages) + "</doc></body></html>"


def two_columns(bottom: int, right_bottom: int) -> str:
    rows = []
    for i in range(bottom):
        rows.append(line(100 + 12 * i, spaced(50, 290, 8, 3)))
    for i in range(right_bottom):
        rows.append(line(100 + 12 * i, spaced(310, 550, 8, 3)))
    return page(rows)


class PageMeasureTest(unittest.TestCase):
    def lines(self, xml: str, columns: int | None = None) -> list:
        pages = measure.parse(xml, 1)
        self.columns = measure.assign_columns(pages, columns)
        return measure.body(pages)

    def test_two_columns_are_detected(self) -> None:
        self.lines(document([two_columns(40, 40)]))
        self.assertEqual(self.columns, 2)

    def test_short_last_line_is_listed(self) -> None:
        rows = [line(100 + 12 * i, spaced(50, 550, 10, 3)) for i in range(5)]
        rows.append(line(160, [(50, 90, "stub")]))
        rows.append(line(172, spaced(50, 550, 10, 3)))
        rows.append(line(184, spaced(50, 450, 8, 3)))
        found = measure.last_lines(self.lines(document([page(rows)])), 0.33)
        self.assertEqual([item[0].text for item in found], ["stub"])

    def test_heading_is_not_a_short_line(self) -> None:
        rows = [line(100 + 12 * i, spaced(50, 550, 10, 3)) for i in range(5)]
        rows.append(line(160, [(50, 120, "Method")], height=13))
        self.assertEqual(measure.last_lines(self.lines(document([page(rows)])), 0.33), [])

    def test_stretched_line_is_listed(self) -> None:
        rows = [line(100 + 12 * i, spaced(50, 550, 12, 3)) for i in range(8)]
        rows.append(line(200, spaced(50, 550, 4, 30)))
        found = measure.word_spacing(self.lines(document([page(rows)])), 1.8)
        self.assertEqual(len(found), 1)
        self.assertGreater(found[0][2], 5)

    def test_early_column_end_is_listed_but_not_on_the_last_page(self) -> None:
        xml = document([two_columns(40, 40), two_columns(40, 36), two_columns(40, 10)])
        found, last = measure.column_gaps(self.lines(xml), 1.5)
        self.assertEqual(last, 3)
        self.assertEqual([(p, c) for p, c, _ in found], [(2, 2)])
        self.assertAlmostEqual(found[0][2], 4.0)

    def test_section_height_counts_the_next_column(self) -> None:
        rows = [line(100, [(50, 120, "Method")], height=13)]
        rows += [line(115 + 12 * i, spaced(50, 290, 8, 3)) for i in range(40)]
        rows += [line(100 + 12 * i, spaced(310, 550, 8, 3)) for i in range(20)]
        rows.append(line(340, [(310, 400, "Experiments")], height=13))
        rows += [line(355 + 12 * i, spaced(310, 550, 8, 3)) for i in range(5)]
        head, stop, share, _ = measure.section_height(self.lines(document([page(rows)])), "Method", None)
        self.assertEqual(stop.text, "Experiments")
        self.assertGreater(share, 1.4)
        self.assertLess(share, 1.6)

    def test_aux_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            aux = Path(tmp) / "blind.aux"
            aux.write_text(
                "\\newlabel{PaperMainTextEnd}{{6}{9}{Limitations}{section.6}{}}\n"
                "\\@writefile{toc}{\\contentsline {section}{\\numberline {A}Proofs}{11}{appendix.A}"
                "\\protected@file@percent }\n",
                encoding="utf-8")
            self.assertEqual(measure.aux_pages(aux), (9, 11))


if __name__ == "__main__":
    unittest.main()
