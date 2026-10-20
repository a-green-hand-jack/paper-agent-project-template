from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / ".agents/scripts/check-reference-integrity.py"
METADATA = ROOT / ".agents/scripts/check-reference-metadata.py"
FORMAT = ROOT / ".agents/scripts/check-bibtex-format.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def policy() -> str:
    return """{
  "schema_version": "paper-reference-integrity-policy-v1",
  "enforcement": "enforced",
  "ledger": ".agents/references/ledger.json",
  "bibliography": "paper/refs.bib"
}
"""


def reference(key: str, *, status: str = "verified", review: str = "human-confirmed") -> dict[str, object]:
    return {
        "citation_key": key,
        "status": status,
        "identifiers": {"doi": "10.0000/example"} if status == "verified" else {},
        "verification": {
            "sources": ["crossref"] if status == "verified" else [],
            "checked_at": "2026-08-05" if status == "verified" else None,
        },
        "human_review": {"state": review, "rationale": "Reviewed fixture."},
    }


def claim(key: str, *, state: str = "human-confirmed") -> dict[str, str]:
    return {
        "citation_key": key,
        "manuscript_claim": "The cited work reports the stated observation.",
        "manuscript_location": "paper/sections/02_intro.tex:3",
        "source_locator": "p. 4, Sec. 2",
        "evidence_excerpt_or_rationale": "The source states the observation directly.",
        "human_review_state": state,
    }


def ledger(
    references: list[dict[str, object]],
    claims: list[dict[str, str]] | None = None,
    usages: list[dict[str, str]] | None = None,
) -> str:
    return json.dumps(
        {
            "schema_version": "paper-reference-ledger-v1",
            "references": references,
            "citation_usages": usages or [],
            "claim_evidence": claims or [],
        },
        indent=2,
    ) + "\n"


def fixture(
    root: Path,
    bib: str,
    records: list[dict[str, object]],
    claims: list[dict[str, str]] | None = None,
    usages: list[dict[str, str]] | None = None,
) -> None:
    write(root / ".agents/references/policy.json", policy())
    write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n" + bib)
    write(root / ".agents/references/ledger.json", ledger(records, claims, usages))


def run_checker(root: Path, profile: str = "draft") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), "--profile", profile],
        text=True,
        capture_output=True,
        check=False,
    )


class ReferenceIntegrityTests(unittest.TestCase):
    def test_factory_template_passes_draft_and_release(self) -> None:
        # The factory state, built here: this repository's own ledger may be
        # absent (a policy without a ledger passes Draft) or at Draft strength,
        # and make release-check, not make check, holds it to Release.
        factory = {
            "schema_version": "paper-reference-ledger-v2",
            "references": [],
            "citation_usages": [],
            "citation_occurrences": [],
            "claim_evidence": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(root / ".agents/references/ledger.json", json.dumps(factory, indent=2) + "\n")
            write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n")
            for profile in ("draft", "release"):
                with self.subTest(profile=profile):
                    result = run_checker(root, profile)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_policy_skips_for_legacy_downstream(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_checker(Path(directory))
            self.assertEqual(result.returncode, 0)
            self.assertIn("SKIP reference_integrity policy not enabled", result.stdout)

    def test_activation_marker_prevents_policy_deletion_or_disable(self) -> None:
        for policy_text in (None, policy().replace('"enforced"', '"disabled"')):
            with self.subTest(deleted=policy_text is None), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                if policy_text is not None:
                    write(root / ".agents/references/policy.json", policy_text)
                write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n")
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("activation marker", result.stdout)

    def test_enforced_policy_requires_the_activation_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(root / "paper/refs.bib", "")
            result = run_checker(root, "release")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires '% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json'", result.stdout)

    def test_policy_bibliography_origin_must_be_known(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json",
                  policy().replace('"bibliography": "paper/refs.bib"',
                                   '"bibliography": "paper/refs.bib", "bibliography_origin": "found-online"'))
            write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bibliography_origin must be one of agent-curated, supplied-fixed", result.stdout)

    def test_marker_naming_the_old_ledger_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: references/ledger.json\n")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("activation marker must read", result.stdout)

    def test_draft_degrades_when_no_ledger_exists(self) -> None:
        """A supplied bibliography that was never migrated is a legitimate state.

        Before this, an adopted policy with no ledger had two outcomes: enforce
        a ledger that does not exist, or disable the policy and skip every
        check. The second is what let a manuscript citing nothing at all pass a
        full pipeline, so a draft profile now checks what the downstream task
        actually needs.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(
                root / "paper/refs.bib",
                "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n"
                "@article{real2024, title={Real}, year={2024}}\n",
            )
            write(root / "paper/sections/02_intro.tex", "As shown \\cite{real2024}.\n")

            result = run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("ledger absent", result.stdout)

    def test_ci_runs_ledger_commands_only_when_a_ledger_exists(self) -> None:
        workflow = (ROOT / ".github/workflows/reference-validation.yml").read_text(encoding="utf-8")
        steps = workflow.split("\n      - name: ")[1:]
        ledger_steps = [step for step in steps if "reference-evidence.py" in step]
        self.assertTrue(ledger_steps)
        for step in ledger_steps:
            with self.subTest(step=step.splitlines()[0]):
                self.assertIn("if: hashFiles('.agents/references/ledger.json') != ''", step)

    def test_ledgerless_draft_still_rejects_an_invented_citation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(
                root / "paper/refs.bib",
                "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n"
                "@article{real2024, title={Real}, year={2024}}\n",
            )
            write(root / "paper/sections/02_intro.tex", "As shown \\cite{invented2024}.\n")

            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invented2024", result.stdout)

    def test_release_still_requires_a_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".agents/references/policy.json", policy())
            write(
                root / "paper/refs.bib",
                "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n",
            )
            result = run_checker(root, "release")
            self.assertNotEqual(result.returncode, 0)

    def test_v1_policy_paths_are_canonical(self) -> None:
        for field, replacement in (("bibliography", "alternate.bib"), ("ledger", "alternate.json")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                fixture(root, "", [])
                publication = (root / ".agents/references/policy.json").read_text(encoding="utf-8")
                canonical = "paper/refs.bib" if field == "bibliography" else ".agents/references/ledger.json"
                write(root / ".agents/references/policy.json", publication.replace(canonical, replacement))
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"policy {field} must be", result.stdout)

    def test_policy_rejects_repository_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".agents/references/policy.json",
                policy().replace('"paper/refs.bib"', '"../outside.bib"'),
            )
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("policy bibliography must be paper/refs.bib", result.stdout)

    def test_nested_braces_and_non_reference_entries_parse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(
                root,
                """@string{venue = "Journal"}
@comment{ignored @article{fake, title={Fake}}}
@preamble{"ignored"}
@article{real,
  title = {{A {Nested} Title}},
  note = "quoted {value}",
  journal = venue
}
""",
                [reference("real")],
            )
            result = run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("references=1", result.stdout)

    def test_parenthesis_bibtex_tracks_braces_and_starred_citation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(
                root,
                "@article(real, title={A ) with @article{fake, nested}}, year={2026})\n",
                [reference("real")],
            )
            write(root / "paper/section.tex", "\\citep*{missing}\n")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("paper cites a key missing from BibTeX: missing", result.stdout)
            self.assertNotIn("fake", result.stdout)

    def test_every_cited_key_requires_reviewed_usage_classification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{real, title={A}}\n", [reference("real")])
            write(root / "paper/section.tex", "\\cite{real}\n")
            missing = run_checker(root)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("lacks a reviewed citation_usages record", missing.stdout)

            write(
                root / ".agents/references/ledger.json",
                ledger(
                    [reference("real")],
                    usages=[{
                        "citation_key": "real",
                        "manuscript_location": "paper/section.tex:1",
                        "classification": "background",
                        "human_review_state": "human-confirmed",
                    }],
                ),
            )
            passed = run_checker(root, "release")
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_claim_support_usage_requires_claim_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(
                root,
                "@article{real, title={A}}\n",
                [reference("real")],
                usages=[{
                    "citation_key": "real",
                    "manuscript_location": "paper/section.tex:1",
                    "classification": "claim-support",
                    "human_review_state": "human-confirmed",
                }],
            )
            write(root / "paper/section.tex", "\\cite{real}\n")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("without claim_evidence", result.stdout)

    def test_duplicate_bibtex_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{dup, title={A}}\n@book{dup, title={B}}\n", [reference("dup")])
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate BibTeX citation key: dup", result.stdout)

    def test_missing_and_extra_ledger_keys_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{bib_only, title={A}}\n", [reference("ledger_only")])
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BibTeX citation key missing from reference ledger: bib_only", result.stdout)
            self.assertIn("reference ledger key missing from BibTeX: ledger_only", result.stdout)

    def test_duplicate_ledger_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{dup, title={A}}\n", [reference("dup"), reference("dup")])
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate reference ledger citation key: dup", result.stdout)

    def test_unverified_warns_in_draft_but_blocks_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified", review="pending")])
            draft = run_checker(root, "draft")
            self.assertEqual(draft.returncode, 0, draft.stdout + draft.stderr)
            self.assertIn("WARN reference unknown is unverified", draft.stdout)
            release = run_checker(root, "release")
            self.assertNotEqual(release.returncode, 0)
            self.assertIn("remains unverified for release", release.stdout)

    def test_problematic_blocks_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{bad, title={A}}\n", [reference("bad", status="problematic")])
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reference bad is problematic", result.stdout)

    def test_agent_resolved_verified_identity_passes_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = reference("real")
            record["human_review"] = {"state": "agent-resolved", "rationale": "Matched exact DOI and publisher record."}
            fixture(root, "@article{real, title={A}}\n", [record])
            result = run_checker(root, "release")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_agent_resolved_cannot_mark_unverified_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = reference("real", status="unverified")
            record["human_review"] = {"state": "agent-resolved", "rationale": "Insufficient evidence."}
            fixture(root, "@article{real, title={A}}\n", [record])
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot be agent-resolved unless verified", result.stdout)

    def test_agent_resolved_identity_does_not_bypass_pending_usage_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = reference("real")
            record["human_review"] = {"state": "agent-resolved", "rationale": "Exact DOI and publisher match."}
            fixture(
                root,
                "@article{real, title={A}}\n",
                [record],
                usages=[{
                    "citation_key": "real",
                    "manuscript_location": "paper/section.tex:1",
                    "classification": "background",
                    "human_review_state": "pending",
                }],
            )
            write(root / "paper/section.tex", "\\cite{real}\n")
            result = run_checker(root, "release")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("lacks Human confirmation for release", result.stdout)

    def test_claim_evidence_required_fields(self) -> None:
        for field in (
            "citation_key",
            "manuscript_claim",
            "manuscript_location",
            "source_locator",
            "evidence_excerpt_or_rationale",
            "human_review_state",
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                evidence = claim("real")
                evidence[field] = ""
                fixture(root, "@article{real, title={A}}\n", [reference("real")], [evidence])
                result = run_checker(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f".{field} must be non-empty", result.stdout)

    def test_pending_claim_blocks_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, "@article{real, title={A}}\n", [reference("real")], [claim("real", state="pending")])
            draft = run_checker(root, "draft")
            self.assertEqual(draft.returncode, 0, draft.stdout + draft.stderr)
            release = run_checker(root, "release")
            self.assertNotEqual(release.returncode, 0)
            self.assertIn("lacks Human confirmation for release", release.stdout)


class ReferenceMetadataTests(unittest.TestCase):
    def run_metadata(self, root: Path, uv: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(METADATA), "--root", str(root), "--uv", uv, "--attempts", "1", "--timeout", "5"],
            text=True,
            capture_output=True,
            check=False,
        )

    def add_lock(self, root: Path) -> None:
        write(root / ".agents/scripts/reference-integrity/uv.lock", "fixture lock\n")
        write(root / ".agents/scripts/check-reference-integrity.py", CHECKER.read_text(encoding="utf-8"))
        write(root / ".agents/scripts/_reference_env.py", (ROOT / ".agents/scripts/_reference_env.py").read_text(encoding="utf-8"))
        write(root / ".agents/scripts/_bounded_run.py", (ROOT / ".agents/scripts/_bounded_run.py").read_text(encoding="utf-8"))

    def test_policy_absent_skips_without_uv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            result = self.run_metadata(root, "definitely-missing-uv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "skipped")

    def test_missing_uv_is_infrastructure_error_not_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            result = self.run_metadata(root, "definitely-missing-uv")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "infrastructure_error")
            self.assertFalse(summary["approves_claim_support"])

    def test_valid_checker_report_never_approves_claim_support(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{real, title={A}}\n", [reference("real")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
assert sys.argv[sys.argv.index('--rate-limit') + 1] == '30'
assert sys.argv[sys.argv.index('--workers') + 1] == '4'
assert '--no-google-books' in sys.argv
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'real', 'status': 'verified', 'abstained': False,
    'coverage_incomplete': False, 'errors': []
}) + '\\n')
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "passed")
            self.assertFalse(summary["approves_claim_support"])

    def test_not_found_report_is_unverified_not_fabricated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'not_found', 'abstained': True,
    'coverage_incomplete': False, 'errors': []
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("not evidence of fabrication", result.stdout)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "unverified")

    def test_api_error_is_infrastructure_error_even_with_zero_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{real, title={A}}\n", [reference("real")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'real', 'status': 'api_error', 'abstained': False,
    'coverage_incomplete': True, 'errors': ['API_ERROR']
}) + '\\n')
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "infrastructure_error")

    def test_rate_limit_is_advisory_not_a_reference_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'strict_warn_cnv', 'abstained': False,
    'coverage_incomplete': False, 'errors': []
}) + '\\n')
print("Service 'dblp' is rate-limited/unavailable", file=sys.stderr)
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("CI not blocked", result.stdout)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "rate_limited")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_rate_limit_does_not_hide_positive_metadata_problem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{bad, title={A}}\n", [reference("bad")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'bad', 'status': 'author_mismatch', 'abstained': False,
    'coverage_incomplete': False, 'errors': []
}) + '\\n')
print("Service 'semanticscholar' is rate-limited/unavailable", file=sys.stderr)
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "reference_problem")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_authenticated_rate_limit_banner_is_not_throttling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'strict_warn_cnv', 'abstained': False,
    'coverage_incomplete': False, 'errors': []
}) + '\\n')
print('Using Semantic Scholar API key (authenticated rate limits)')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "unverified")
            self.assertFalse(summary["rate_limit_degraded"])

    def test_cached_rate_limit_circuit_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'api_error', 'abstained': True,
    'coverage_incomplete': True,
    'errors': ['circuit open for service semanticscholar']
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "rate_limited")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_rate_limit_does_not_hide_unrelated_infrastructure_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(
                root,
                "@article{limited, title={A}}\n@article{broken, title={B}}\n",
                [reference("limited", status="unverified"), reference("broken", status="unverified")],
            )
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
records = [
    {'key': 'limited', 'status': 'api_error', 'abstained': True,
     'coverage_incomplete': True, 'errors': ['circuit open for service dblp']},
    {'key': 'broken', 'status': 'api_error', 'abstained': True,
     'coverage_incomplete': True, 'errors': ['unexpected parser failure']},
]
target.write_text(''.join(json.dumps(record) + '\\n' for record in records))
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "infrastructure_error")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_active_rate_limit_circuit_with_network_retry_error_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'api_error', 'abstained': True,
    'coverage_incomplete': True,
    'errors': ['Network failure after retries for Semantic Scholar']
}) + '\\n')
print("Service 'semanticscholar' is rate-limited/unavailable", file=sys.stderr)
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "rate_limited")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_rate_limit_status_does_not_hide_parser_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{broken, title={A}}\n", [reference("broken", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'broken', 'status': 'rate_limit', 'abstained': True,
    'coverage_incomplete': True, 'errors': ['unexpected parser failure']
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "infrastructure_error")
            self.assertTrue(summary["rate_limit_degraded"])

    def test_parser_timeout_text_is_not_a_provider_outage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{broken, title={A}}\n", [reference("broken", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'broken', 'status': 'api_error', 'abstained': True,
    'coverage_incomplete': True, 'errors': ['Exception: bibliography parser timed out']
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "infrastructure_error")

    def test_upstream_request_timeout_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'api_error', 'abstained': True,
    'coverage_incomplete': True, 'errors': ['Request timed out']
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "provider_unavailable")

    def test_provider_network_failures_are_advisory_without_claiming_rate_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(
                root,
                "@article{dblp, title={A}}\n@article{openalex, title={B}}\n",
                [reference("dblp", status="unverified"), reference("openalex", status="unverified")],
            )
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
records = [
    {'key': 'dblp', 'status': 'api_error', 'abstained': True,
     'coverage_incomplete': True, 'errors': ['Network failure after retries for DBLP']},
    {'key': 'openalex', 'status': 'api_error', 'abstained': True,
     'coverage_incomplete': True, 'errors': ['Network failure after retries for OpenAlex']},
]
target.write_text(''.join(json.dumps(record) + '\\n' for record in records))
print("Service 'dblp' is rate-limited/unavailable", file=sys.stderr)
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "provider_unavailable")
            self.assertEqual(summary["rate_limited_services"], ["dblp"])

    def test_pre_circuit_provider_network_failure_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{unknown, title={A}}\n", [reference("unknown", status="unverified")])
            runner = root / "fake-uv"
            write(
                runner,
                """#!/usr/bin/env python3
import json, pathlib, sys
target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({
    'key': 'unknown', 'status': 'api_error', 'abstained': True,
    'coverage_incomplete': True,
    'errors': ['Network failure after retries for https://api.semanticscholar.org']
}) + '\\n')
raise SystemExit(4)
""",
            )
            runner.chmod(0o755)
            result = self.run_metadata(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "provider_unavailable")
            self.assertFalse(summary["rate_limit_degraded"])

    def test_malformed_or_wrong_key_report_is_infrastructure_error(self) -> None:
        cases = (
            {"key": "real", "status": "verified"},
            {
                "key": "extra", "status": "verified", "abstained": False,
                "coverage_incomplete": False, "errors": [],
            },
        )
        for record in cases:
            with self.subTest(record=record), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.add_lock(root)
                fixture(root, "@article{real, title={A}}\n", [reference("real")])
                runner = root / "fake-uv"
                write(
                    runner,
                    "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
                    "target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])\n"
                    "target.parent.mkdir(parents=True, exist_ok=True)\n"
                    f"target.write_text(json.dumps({record!r}) + '\\\\n')\n",
                )
                runner.chmod(0o755)
                result = self.run_metadata(root, str(runner))
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
                self.assertEqual(summary["outcome"], "infrastructure_error")

    def fake_checker(self, root: Path, records: list[dict[str, object]], stderr: str = "", code: int = 0) -> str:
        """A uv stand-in that writes the given bibtex-check records and log."""
        runner = root / "fake-uv"
        write(
            runner,
            "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
            "assert '--verbose' in sys.argv\n"
            "target = pathlib.Path(sys.argv[sys.argv.index('--jsonl') + 1])\n"
            "target.parent.mkdir(parents=True, exist_ok=True)\n"
            f"target.write_text(''.join(json.dumps(record) + '\\n' for record in {records!r}))\n"
            f"sys.stderr.write({stderr!r})\n"
            f"raise SystemExit({code})\n",
        )
        runner.chmod(0o755)
        return str(runner)

    def openreview_reference(self, key: str, review: str = "agent-resolved") -> dict[str, object]:
        record = reference(key, review=review)
        record["identifiers"] = {"openreview": "forum-id"}
        record["verification"] = {"sources": ["openreview"], "checked_at": "2026-10-20"}
        return record

    @staticmethod
    def checker_record(key: str, status: str, fields: list[str], sources: list[str]) -> dict[str, object]:
        return {
            "key": key, "status": status, "abstained": False, "coverage_incomplete": False,
            "mismatched_fields": fields, "api_sources": sources, "errors": [],
        }

    DBLP_CHALLENGE = (
        "INFO: Checking 1/1: entry\n"
        'INFO: HTTP Request: GET https://dblp.org/search/publ/api?q=A+title&h=3&format=json "HTTP/1.1 202 Accepted"\n'
        "DEBUG: request detail https://api.example.org/?api_key=not-for-logs\n"
    )

    def test_dblp_bot_challenge_is_provider_unavailable_not_a_miss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@inproceedings{entry, title={A}}\n", [reference("entry", status="unverified")])
            runner = self.fake_checker(
                root,
                [self.checker_record("entry", "strict_warn_cnv", ["year"], ["crossref", "openreview"])],
                self.DBLP_CHALLENGE,
                4,
            )
            result = self.run_metadata(root, runner)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("dblp answered with a bot challenge", result.stdout)
            self.assertIn("Checking 1/1", result.stderr)
            self.assertNotIn("HTTP Request", result.stdout + result.stderr)
            self.assertNotIn("api_key", result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "provider_unavailable")
            self.assertEqual(summary["bot_challenged_services"], ["dblp"])

    def test_dblp_bot_challenge_does_not_hide_positive_problem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@inproceedings{entry, title={A}}\n", [reference("entry")])
            runner = self.fake_checker(
                root, [self.checker_record("entry", "venue_mismatch", ["venue"], ["openreview"])], self.DBLP_CHALLENGE, 4
            )
            result = self.run_metadata(root, runner)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "reference_problem")

    def test_reviewed_openreview_identity_reports_year_or_venue_residue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(
                root,
                "@inproceedings{full, title={A}}\n@inproceedings{alias, title={B}}\n",
                [self.openreview_reference("full"), self.openreview_reference("alias", "human-confirmed")],
            )
            runner = self.fake_checker(
                root,
                [
                    self.checker_record("full", "venue_mismatch", ["venue"], ["crossref", "openreview"]),
                    self.checker_record("alias", "strict_warn_cnv", ["year"], ["openreview"]),
                ],
                code=4,
            )
            result = self.run_metadata(root, runner)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("full: venue_mismatch on venue against OpenReview", result.stdout)
            self.assertIn("alias: strict_warn_cnv on year against OpenReview", result.stdout)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "passed")
            self.assertEqual(summary["ledger_reviewed_openreview_keys"], ["alias", "full"])
            self.assertFalse(summary["approves_claim_support"])

    def test_openreview_residue_needs_a_reviewed_openreview_identity_and_only_year_or_venue(self) -> None:
        cases = {
            "identity from another source": (
                reference("entry", review="agent-resolved"),
                self.checker_record("entry", "venue_mismatch", ["venue"], ["openreview"]),
            ),
            "identity awaiting review": (
                self.openreview_reference("entry", review="pending"),
                self.checker_record("entry", "venue_mismatch", ["venue"], ["openreview"]),
            ),
            "author mismatch as well": (
                self.openreview_reference("entry"),
                self.checker_record("entry", "venue_mismatch", ["author", "venue"], ["openreview"]),
            ),
            "wrong year": (
                self.openreview_reference("entry"),
                self.checker_record("entry", "year_mismatch", ["year"], ["openreview"]),
            ),
            "not matched on OpenReview": (
                self.openreview_reference("entry"),
                self.checker_record("entry", "venue_mismatch", ["venue"], ["crossref"]),
            ),
        }
        for name, (ledger_record, checker_record) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.add_lock(root)
                fixture(root, "@inproceedings{entry, title={A}}\n", [ledger_record])
                result = self.run_metadata(root, self.fake_checker(root, [checker_record], code=4))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
                self.assertEqual(summary["ledger_reviewed_openreview_keys"], [])

    # A uv stand-in that, like `uv run`, starts the checker as a child in its
    # process group. The checker streams one record per entry, with a cache
    # keyed by the entry text, as bibtex-check does: a cached entry costs
    # nothing, an uncached one SECONDS and a query logged to queries.log.
    STREAMING_CHECKER = """#!/usr/bin/env python3
import hashlib, json, os, pathlib, re, sqlite3, subprocess, sys, time
if os.environ.get('FAKE_CHECKER_CHILD') != '1':
    pidfile = pathlib.Path(sys.argv[0]).with_name('checker.pid')
    child = subprocess.Popen([sys.executable] + sys.argv, env=dict(os.environ, FAKE_CHECKER_CHILD='1'))
    pidfile.write_text(str(child.pid))
    raise SystemExit(child.wait())
seconds = float(os.environ.get('FAKE_CHECKER_SECONDS', '0'))
argv = sys.argv
bib = pathlib.Path(argv[argv.index('bibtex-check') + 1]).read_text()
target = pathlib.Path(argv[argv.index('--jsonl') + 1])
cache_file = pathlib.Path(argv[argv.index('--cache-file') + 1])
cache_file.parent.mkdir(parents=True, exist_ok=True)
cache = sqlite3.connect(cache_file)
cache.execute('CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT NOT NULL, timestamp REAL NOT NULL)')
log = pathlib.Path(sys.argv[0]).with_name('queries.log')
key = os.environ.get('OPENALEX_API_KEY', '')
target.parent.mkdir(parents=True, exist_ok=True)
with target.open('a') as report:
    for entry in re.findall(r'@\\w+\\{[^@]*', bib):
        name = re.match(r'@\\w+\\{([^,]+),', entry).group(1)
        request = 'https://api.openalex.org/works?search=' + hashlib.sha256(entry.encode()).hexdigest()
        if key:
            request += '&api_key=' + key
        if cache.execute('SELECT 1 FROM cache WHERE key = ?', (request,)).fetchone() is None:
            with log.open('a') as queries:
                queries.write(name + '\\n')
            time.sleep(seconds)
            cache.execute('INSERT INTO cache VALUES (?, ?, ?)', (request, '{}', time.time()))
            cache.commit()
        status = 'year_mismatch' if name.startswith('wrong') else 'verified'
        report.write(json.dumps({'key': name, 'status': status, 'abstained': False,
                                 'coverage_incomplete': False, 'errors': []}) + '\\n')
        report.flush()
"""

    def streaming_checker(self, root: Path) -> str:
        runner = root / "fake-uv"
        write(runner, self.STREAMING_CHECKER)
        runner.chmod(0o755)
        return str(runner)

    def run_capped(self, root: Path, runner: str, timeout: int, **env: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(METADATA), "--root", str(root), "--uv", runner, "--timeout", str(timeout)],
            text=True, capture_output=True, check=False, env={**os.environ, **env},
        )

    @staticmethod
    def alive(pid: int) -> bool:
        try:
            state = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
        except (FileNotFoundError, IndexError):
            return False
        return state != "Z"

    def test_cap_ends_the_checker_and_reports_finished_and_unfinished_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "".join(f"@article{{e{i}, title={{T{i}}}}}\n" for i in range(3)),
                    [reference(f"e{i}", status="unverified") for i in range(3)])
            started = time.monotonic()
            result = self.run_capped(root, self.streaming_checker(root), 3, FAKE_CHECKER_SECONDS="2")
            elapsed = time.monotonic() - started
            self.assertLess(elapsed, 12, "the run outlived its cap")
            pid = int((root / "checker.pid").read_text())
            deadline = time.monotonic() + 5
            while self.alive(pid) and time.monotonic() < deadline:
                time.sleep(0.1)
            self.assertFalse(self.alive(pid), "the checker outlived the cap that ended its uv parent")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "incomplete")
            self.assertEqual(summary["checked_keys"], ["e0"])
            self.assertEqual(summary["unfinished_keys"], ["e1", "e2"])
            self.assertIn("unfinished: e1, e2", result.stdout)

    def test_cap_keeps_a_positive_problem_among_finished_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{wrong, title={A}}\n@article{later, title={B}}\n",
                    [reference("wrong"), reference("later")])
            result = self.run_capped(root, self.streaming_checker(root), 2, FAKE_CHECKER_SECONDS="1.5")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("ERROR reference_metadata wrong: year_mismatch", result.stdout)
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual(summary["outcome"], "reference_problem")
            self.assertEqual(summary["unfinished_keys"], ["later"])

    def test_kept_cache_queries_only_new_or_changed_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{same, title={A}}\n@article{edited, title={B}}\n",
                    [reference("same"), reference("edited")])
            runner = self.streaming_checker(root)
            first = self.run_capped(root, runner, 30)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n"
                  "@article{same, title={A}}\n@article{edited, title={B, revised}}\n")
            second = self.run_capped(root, runner, 30)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual((root / "queries.log").read_text().split(), ["same", "edited", "edited"])

    def test_cache_keeps_no_credential(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{real, title={A}}\n", [reference("real")])
            runner = self.streaming_checker(root)
            keyless = self.run_capped(root, runner, 30, OPENALEX_API_KEY="")
            keyed = self.run_capped(root, runner, 30, OPENALEX_API_KEY="fixture-secret-value")
            self.assertEqual(keyed.returncode, 0, keyed.stdout + keyed.stderr)
            cache = root / ".project/build/reference-integrity/cache"
            for path in cache.iterdir():
                self.assertNotIn(b"fixture-secret-value", path.read_bytes(), path.name)
            rows = sqlite3.connect(cache / "metadata.db").execute(
                "SELECT key FROM cache WHERE key LIKE 'https://%'").fetchall()
            self.assertEqual(len(rows), 1, rows)  # the keyless response stays cached
            self.assertEqual(keyless.returncode, 0, keyless.stdout + keyless.stderr)

    def test_keyless_run_skips_openalex_through_the_checker_circuit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{real, title={A}}\n", [reference("real")])
            runner = self.streaming_checker(root)
            summary_path = root / ".project/build/reference-integrity/run.json"
            database = root / ".project/build/reference-integrity/cache/metadata.db"

            def circuit() -> dict[str, float]:
                row = sqlite3.connect(database).execute(
                    "SELECT value FROM cache WHERE key = '__bibtex_updater_circuit_open_until__'").fetchone()
                return json.loads(row[0])

            keyless = self.run_capped(root, runner, 30, OPENALEX_API_KEY="")
            self.assertIn("skips OpenAlex", keyless.stdout)
            self.assertEqual(json.loads(summary_path.read_text())["skipped_services"], ["openalex"])
            self.assertGreater(circuit()["openalex"], time.time())
            keyed = self.run_capped(root, runner, 30, OPENALEX_API_KEY="fixture-secret-value")
            self.assertNotIn("skips OpenAlex", keyed.stdout)
            self.assertEqual(json.loads(summary_path.read_text())["skipped_services"], [])
            self.assertNotIn("openalex", circuit())

    def test_ci_runs_three_tiers_and_keeps_each_audit_cache(self) -> None:
        workflow = yaml.safe_load((ROOT / ".github/workflows/reference-validation.yml").read_text(encoding="utf-8"))
        self.assertIn("schedule", workflow[True])
        self.assertIn("workflow_dispatch", workflow[True])
        jobs = workflow["jobs"]
        self.assertIn("pull_request", jobs["references"]["if"])
        self.assertIn("push", jobs["references"]["if"])
        self.assertNotIn("pull_request", jobs["references-full"]["if"])
        tier = next(step for step in jobs["references"]["steps"] if step.get("id") == "tier")["run"]
        self.assertIn('"$BASE_REF" == main', tier)  # the release path audits everything
        self.assertIn("--scope all", tier)
        self.assertIn("--scope changed --base $BASE_SHA", tier)
        # The scheduled full audit runs both audits in parallel.
        self.assertEqual({entry["audit"] for entry in jobs["references-full"]["strategy"]["matrix"]["include"]},
                         {"corrections", "metadata"})
        for name, job in jobs.items():
            steps = job["steps"]
            names = [step["name"] for step in steps]
            audits = [index for index, step in enumerate(steps) if "check-reference-" in str(step.get("run", ""))
                      and "integrity" not in str(step.get("run", ""))]
            restores = [index for index, step in enumerate(steps) if "actions/cache/restore@" in step.get("uses", "")]
            saves = [steps[index] for index, step in enumerate(steps) if "actions/cache/save@" in step.get("uses", "")]
            with self.subTest(job=name):
                self.assertTrue(audits and restores and saves, names)
                self.assertLess(max(restores), min(audits))
                for save in saves:  # saved even when an audit fails or reaches its cap
                    self.assertTrue(save["if"].startswith("always()"), save)
                    self.assertIn("github.run_id", save["with"]["key"])
                for step in steps:
                    if "upload-artifact" in step.get("uses", ""):
                        self.assertNotIn("/cache", step["with"]["path"])

    def commit(self, root: Path) -> None:
        for command in (["git", "init", "-q"], ["git", "add", "-A"],
                        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                         "commit", "-q", "--allow-empty", "-m", "state"]):
            subprocess.run(command, cwd=root, check=True, capture_output=True)

    def run_scoped(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(METADATA), "--root", str(root), "--uv", str(root / "fake-uv"), "--timeout", "30",
             *arguments],
            text=True, capture_output=True, check=False,
        )

    def test_changed_tier_queries_nothing_for_an_unchanged_verified_bibliography(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            keys = [f"entry{number:03d}" for number in range(100)]
            fixture(root, "".join(f"@article{{{key}, title={{T {key}}}}}\n" for key in keys),
                    [reference(key) for key in keys])
            self.streaming_checker(root)
            full = self.run_scoped(root, "--record")
            self.assertEqual(full.returncode, 0, full.stdout + full.stderr)
            self.assertIn("recorded 100 fingerprints", full.stdout)
            self.commit(root)
            (root / "queries.log").unlink()
            changed = self.run_scoped(root, "--scope", "changed", "--base", "HEAD")
            self.assertEqual(changed.returncode, 0, changed.stdout + changed.stderr)
            self.assertIn("no provider queried", changed.stdout)
            self.assertFalse((root / "queries.log").exists(), "the changed tier ran the checker")
            summary = json.loads((root / ".project/build/reference-integrity/run.json").read_text())
            self.assertEqual((summary["outcome"], summary["selected_keys"]), ("skipped", []))

    def test_changed_tier_selects_new_changed_and_stale_entries_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            fixture(root, "@article{kept, title={A}}\n@article{edited, title={B}}\n@article{stale, title={C}}\n"
                          "@article{unrecorded, title={D}}\n",
                    [reference(key) for key in ("kept", "edited", "stale", "unrecorded")])
            self.streaming_checker(root)
            ledger_path = root / ".agents/references/ledger.json"
            self.assertEqual(self.run_scoped(root, "--record").returncode, 0)
            recorded = json.loads(ledger_path.read_text())
            for record in recorded["references"]:
                if record["citation_key"] == "stale":  # verified in another form than the one committed
                    record["verification"]["bibtex_fingerprint"] = "sha256:" + "0" * 64
                if record["citation_key"] == "unrecorded":
                    del record["verification"]["bibtex_fingerprint"]
            ledger_path.write_text(json.dumps(recorded))
            self.commit(root)
            write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n"
                  "@article{kept, title={A}}\n@article{edited, title={B, revised}}\n@article{stale, title={C}}\n"
                  "@article{unrecorded, title={D}}\n@article{added, title={E}}\n")
            recorded["references"].append(reference("added"))
            ledger_path.write_text(json.dumps(recorded))
            (root / "queries.log").unlink()
            changed = self.run_scoped(root, "--scope", "changed", "--base", "HEAD", "--record")
            self.assertEqual(changed.returncode, 0, changed.stdout + changed.stderr)
            report = (root / ".project/build/reference-integrity/metadata.jsonl").read_text().splitlines()
            self.assertEqual([json.loads(line)["key"] for line in report], ["edited", "stale", "added"])
            self.assertEqual((root / "queries.log").read_text().split(), ["edited", "added"])  # stale was cached
            fingerprints = {record["citation_key"]: record["verification"].get("bibtex_fingerprint")
                            for record in json.loads(ledger_path.read_text())["references"]}
            self.assertIsNone(fingerprints["unrecorded"])  # unchanged against the base: left to the full audit
            self.assertNotEqual(fingerprints["stale"], "sha256:" + "0" * 64)

    def test_record_drops_the_fingerprint_of_a_positive_problem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_lock(root)
            record = reference("wrong")
            record["verification"]["bibtex_fingerprint"] = "sha256:" + "1" * 64
            fixture(root, "@article{wrong, title={A}}\n", [record])
            self.streaming_checker(root)
            result = self.run_scoped(root, "--record")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            stored = json.loads((root / ".agents/references/ledger.json").read_text())["references"][0]
            self.assertNotIn("bibtex_fingerprint", stored["verification"])

class BibtexFormatTests(unittest.TestCase):
    def run_format(self, root: Path, uv: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(FORMAT), "--root", str(root), "--uv", uv, "--timeout", "5"],
            text=True,
            capture_output=True,
            check=False,
        )

    def add_tools(self, root: Path) -> None:
        write(root / ".agents/scripts/reference-integrity/uv.lock", "fixture lock\n")
        write(root / ".agents/scripts/check-reference-integrity.py", CHECKER.read_text(encoding="utf-8"))
        write(root / ".agents/scripts/_validate-bibtex-with-pybtex.py", "# fixture helper\n")

    def test_empty_bibliography_skips_without_uv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_tools(root)
            fixture(root, "", [])
            result = self.run_format(root, "definitely-missing-uv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/format-run.json").read_text())
            self.assertEqual(summary["outcome"], "skipped")
            self.assertFalse(summary["rewrites_bibliography"])

    def test_valid_complete_pybtex_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_tools(root)
            fixture(root, "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n", [reference("real")])
            runner = root / "fake-uv"
            write(
                runner,
                "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
                "target = pathlib.Path(sys.argv[-1])\n"
                "target.parent.mkdir(parents=True, exist_ok=True)\n"
                "target.write_text(json.dumps({'schema_version': 'paper-bibtex-format-report-v1', "
                "'checker': 'pybtex', 'passed': True, 'keys': ['real'], 'errors': []}) + '\\n')\n",
            )
            runner.chmod(0o755)
            result = self.run_format(root, str(runner))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/format-run.json").read_text())
            self.assertEqual(summary["outcome"], "passed")

    def test_pybtex_format_problem_is_not_infrastructure_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_tools(root)
            fixture(root, "@article{bad, title={T}}\n", [reference("bad")])
            runner = root / "fake-uv"
            write(
                runner,
                "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
                "target = pathlib.Path(sys.argv[-1])\n"
                "target.parent.mkdir(parents=True, exist_ok=True)\n"
                "target.write_text(json.dumps({'schema_version': 'paper-bibtex-format-report-v1', "
                "'checker': 'pybtex', 'passed': False, 'keys': ['bad'], "
                "'errors': [{'key': 'bad', 'message': 'missing required field: author'}]}) + '\\n')\n"
                "raise SystemExit(1)\n",
            )
            runner.chmod(0o755)
            result = self.run_format(root, str(runner))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/format-run.json").read_text())
            self.assertEqual(summary["outcome"], "format_problem")

    def test_contradictory_pybtex_report_is_infrastructure_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_tools(root)
            fixture(root, "@article{real, title={T}}\n", [reference("real")])
            runner = root / "fake-uv"
            write(
                runner,
                "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
                "target = pathlib.Path(sys.argv[-1])\n"
                "target.parent.mkdir(parents=True, exist_ok=True)\n"
                "target.write_text(json.dumps({'schema_version': 'paper-bibtex-format-report-v1', "
                "'checker': 'pybtex', 'passed': True, 'keys': ['real'], "
                "'errors': [{'key': 'real', 'message': 'contradiction'}]}) + '\\n')\n",
            )
            runner.chmod(0o755)
            result = self.run_format(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("contradicts", result.stdout)

    def test_stale_report_cannot_mask_helper_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.add_tools(root)
            fixture(root, "@article{real, title={T}}\n", [reference("real")])
            stale = root / ".project/build/reference-integrity/format.json"
            write(
                stale,
                json.dumps({
                    "schema_version": "paper-bibtex-format-report-v1",
                    "checker": "pybtex",
                    "passed": False,
                    "keys": ["real"],
                    "errors": [{"key": "real", "message": "old finding"}],
                }) + "\n",
            )
            runner = root / "fake-uv"
            write(runner, "#!/usr/bin/env python3\nraise SystemExit(2)\n")
            runner.chmod(0o755)
            result = self.run_format(root, str(runner))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("invalid or missing Pybtex report", result.stdout)


if __name__ == "__main__":
    unittest.main()
