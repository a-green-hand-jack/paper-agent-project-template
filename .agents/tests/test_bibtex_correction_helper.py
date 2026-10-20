from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import sys
from pathlib import Path

try:
    import bibtexparser  # noqa: F401
except ImportError:
    bibtexparser = None

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".agents/scripts/_validate-bibtex-correction.py"
sys.path.insert(0, str(HELPER.parent))


@unittest.skipIf(bibtexparser is None, "bibtexparser is installed only in the locked reference environment")
class BibtexCorrectionHelperTests(unittest.TestCase):
    def load_helper(self):
        spec = importlib.util.spec_from_file_location("paper_bibtex_correction_validator", HELPER)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_report_action_and_identity_safety(self) -> None:
        helper = self.load_helper()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.bib"
            candidate = root / "candidate.bib"
            report = root / "report.jsonl"
            source.write_text("@article{real, title={Same Title}}\n", encoding="utf-8")
            candidate.write_text("@article{real, title={Same Title}, doi={10.1/example}}\n", encoding="utf-8")
            base = {
                "file": str(source), "key_old": "real", "key_new": "real",
                "doi_old": None, "doi_new": "10.1/example", "action": "unchanged",
                "method": None, "confidence": 0.0, "title_old": "Same Title", "title_new": "Same Title",
            }
            report.write_text(json.dumps(base) + "\n", encoding="utf-8")
            rejected = helper.validate(source, candidate, report)
            self.assertFalse(rejected["passed"])
            self.assertIn("action does not match candidate content", rejected["errors"][0])

            base["action"] = "upgraded"
            report.write_text(json.dumps(base) + "\n", encoding="utf-8")
            accepted = helper.validate(source, candidate, report)
            self.assertTrue(accepted["passed"], accepted["errors"])
            self.assertEqual(accepted["changed_keys"], ["real"])
            self.assertEqual(accepted["semantic_title_change_keys"], [])

            base["title_new"] = "False report title"
            report.write_text(json.dumps(base) + "\n", encoding="utf-8")
            false_metadata = helper.validate(source, candidate, report)
            self.assertFalse(false_metadata["passed"])
            self.assertTrue(any("title_new" in error for error in false_metadata["errors"]))

    def test_latex_accents_normalize_like_unicode(self) -> None:
        helper = self.load_helper()
        for unicode_title, latex_forms in {
            "A Study of Café Models": (
                "A Study of Caf{\\'e} Models", "A Study of Caf\\'{e} Models", "A Study of Caf\\'e Models",
                "A Study of Café Models",
            ),
            "Schrödinger Bridges": ("Schr{\\\"o}dinger Bridges", "Schr\\\"{o}dinger Bridges"),
            "Hegedűs, Garçon and Wałęsa": ("Heged{\\H u}s, Gar{\\c c}on and Wa{\\l}{\\k e}sa",),
            "Martí Learns": ("Mart{\\'\\i} Learns",),
        }.items():
            for latex_title in latex_forms:
                with self.subTest(title=latex_title):
                    self.assertEqual(helper.normalize_title(latex_title), helper.normalize_title(unicode_title))
        self.assertNotEqual(helper.normalize_title("A Study of Cafe Models"),
                            helper.normalize_title("A Study of Café Models"))

    def test_accent_encoding_is_not_a_semantic_title_change(self) -> None:
        helper = self.load_helper()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.bib"
            candidate = root / "candidate.bib"
            report = root / "report.jsonl"
            source.write_text("@article{cafe, title={A Study of Caf{\\'e} Models}}\n", encoding="utf-8")
            candidate.write_text(
                "@article{cafe, title={A Study of Café Models}, doi={10.1/cafe}}\n", encoding="utf-8"
            )
            report.write_text(json.dumps({
                "file": str(source), "key_old": "cafe", "key_new": "cafe",
                "doi_old": None, "doi_new": "10.1/cafe", "action": "upgraded",
                "method": "search", "confidence": 1.0,
                "title_old": "A Study of Café Models", "title_new": "A Study of Café Models",
            }) + "\n", encoding="utf-8")
            result = helper.validate(source, candidate, report)
            self.assertTrue(result["passed"], result["errors"])
            self.assertEqual(result["semantic_title_change_keys"], [])

    def test_false_replacement_with_duplicate_identity_is_rejected(self) -> None:
        helper = self.load_helper()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.bib"
            candidate = root / "candidate.bib"
            report = root / "report.jsonl"
            source.write_text(
                "@article{first, title={First Work}, doi={10.1/first}}\n"
                "@article{second, title={Second Work}}\n",
                encoding="utf-8",
            )
            candidate.write_text(
                "@article{first, title={First Work}, doi={10.1/first}}\n"
                "@article{second, title={First Work}, doi={10.1/first}}\n",
                encoding="utf-8",
            )
            records = [
                {"file": str(source), "key_old": "first", "key_new": "first", "doi_old": "10.1/first",
                 "doi_new": "10.1/first", "action": "unchanged", "method": None, "confidence": 0.0,
                 "title_old": "First Work", "title_new": "First Work"},
                {"file": str(source), "key_old": "second", "key_new": "second", "doi_old": None,
                 "doi_new": "10.1/first", "action": "upgraded", "method": "search", "confidence": 1.0,
                 "title_old": "Second Work", "title_new": "First Work"},
            ]
            report.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")
            result = helper.validate(source, candidate, report)
            self.assertFalse(result["passed"])
            self.assertEqual(result["new_duplicate_dois"][0]["keys"], ["first", "second"])
            self.assertEqual(result["new_duplicate_titles"][0]["keys"], ["first", "second"])
            self.assertEqual(result["semantic_title_change_keys"], ["second"])


if __name__ == "__main__":
    unittest.main()
