from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRECTIONS = ROOT / ".agents/scripts/check-reference-corrections.py"
INTEGRITY = ROOT / ".agents/scripts/check-reference-integrity.py"
ENV_HELPER = ROOT / ".agents/scripts/_reference_env.py"
FORMAT_HELPER = ROOT / ".agents/scripts/_validate-bibtex-with-pybtex.py"
CORRECTION_HELPER = ROOT / ".agents/scripts/_validate-bibtex-correction.py"
REFERENCE_KEYS = ("BIBTEX_CHECK_MAILTO", "OPENALEX_API_KEY", "S2_API_KEY")
# Synthetic lines of a device's shared credential file: other consumers' keys around the allowlisted ones.
SHARED_FILE = (
    "# device shared credentials\n"
    "OPENAI_API_KEY=synthetic-openai\n"
    "export S2_API_KEY='synthetic-s2'\n"
    "CLAUDE_CODE_OAUTH_TOKEN=\"unmatched\n"
    "not an assignment\n"
    "OPENALEX_API_KEY=synthetic-openalex\n"
)
UNRELATED_KEYS = ("OPENAI_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def prepare(root: Path, bib: str = "") -> None:
    write(root / ".agents/scripts/check-reference-integrity.py", INTEGRITY.read_text(encoding="utf-8"))
    write(root / ".agents/scripts/_reference_env.py", ENV_HELPER.read_text(encoding="utf-8"))
    write(root / ".agents/scripts/_bounded_run.py", (ROOT / ".agents/scripts/_bounded_run.py").read_text(encoding="utf-8"))
    write(root / ".agents/scripts/_validate-bibtex-with-pybtex.py", FORMAT_HELPER.read_text(encoding="utf-8"))
    write(root / ".agents/scripts/_validate-bibtex-correction.py", CORRECTION_HELPER.read_text(encoding="utf-8"))
    write(root / ".agents/scripts/reference-integrity/uv.lock", "fixture lock\n")
    write(
        root / ".agents/references/policy.json",
        """{"schema_version":"paper-reference-integrity-policy-v1","enforcement":"enforced","ledger":".agents/references/ledger.json","bibliography":"paper/refs.bib"}
""",
    )
    write(root / "paper/refs.bib", "% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json\n" + bib)
    keys = ["real"] if bib else []
    references = [{
        "citation_key": key,
        "status": "verified",
        "identifiers": {"doi": "10.0000/example"},
        "verification": {"sources": ["crossref"], "checked_at": "2026-08-08"},
        "human_review": {"state": "human-confirmed", "rationale": "fixture"},
    } for key in keys]
    write(root / ".agents/references/ledger.json", json.dumps({
        "schema_version": "paper-reference-ledger-v1",
        "references": references,
        "citation_usages": [],
        "claim_evidence": [],
    }))


def run(root: Path, uv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CORRECTIONS), "--root", str(root), "--uv", uv, "--timeout", "5"],
        text=True, capture_output=True, check=False, env=env,
    )


def load_env_helper():
    spec = importlib.util.spec_from_file_location("test_reference_env", ENV_HELPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def without_reference_keys() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key not in REFERENCE_KEYS}


def fake_uv(root: Path, action: str = "unchanged", mutate: bool = False, record_env: Path | None = None) -> Path:
    runner = root / "fake-uv"
    record = (f"pathlib.Path({str(record_env)!r}).write_text(json.dumps("
              f"{{k: os.environ.get(k) for k in {REFERENCE_KEYS + UNRELATED_KEYS!r}}}))") if record_env else "pass"
    write(
        runner,
        f"""#!/usr/bin/env python3
import json, os, pathlib, shutil, sys
{record}
if 'bibtex-update' in sys.argv:
    assert '--in-place' not in sys.argv and '--dedupe' not in sys.argv and '--rekey' not in sys.argv
    assert '--use-scholarly' not in sys.argv and '--zotero' not in sys.argv
    assert sys.argv[sys.argv.index('--max-workers') + 1] == '4'
    source = pathlib.Path(sys.argv[sys.argv.index('bibtex-update') + 1])
    candidate = pathlib.Path(sys.argv[sys.argv.index('--output') + 1])
    report = pathlib.Path(sys.argv[sys.argv.index('--report') + 1])
    candidate.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, candidate)
    report.write_text(json.dumps({{
        'file': str(source), 'key_old': 'real', 'key_new': 'real',
        'doi_old': None, 'doi_new': None, 'action': {action!r},
        'method': None, 'confidence': 0.0, 'title_old': 'T', 'title_new': 'T'
    }}) + '\\n')
    {"pathlib.Path('paper/refs.bib').write_text('mutated')" if mutate else "pass"}
elif any('_validate-bibtex-correction.py' in arg for arg in sys.argv):
    target = pathlib.Path(sys.argv[-1])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({{
        'schema_version': 'paper-reference-correction-validation-v1',
        'passed': True,
        'changed_keys': {"['real']" if action in {"upgraded", "field_filled"} else "[]"},
        'incomplete_keys': {"['real']" if action == "failed" else "[]"},
        'errors': []
    }}) + '\\n')
else:
    target = pathlib.Path(sys.argv[-1])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('{{}}\\n')
""",
    )
    runner.chmod(0o755)
    return runner


class ReferenceCorrectionTests(unittest.TestCase):
    def test_empty_bibliography_skips_without_uv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            result = run(root, "missing-uv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/corrections/run.json").read_text())
            self.assertEqual(summary["outcome"], "skipped")
            self.assertFalse(summary["rewrites_bibliography"])

    def test_candidate_is_generated_without_changing_canonical_bibliography(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bib = "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n"
            prepare(root, bib)
            before = (root / "paper/refs.bib").read_bytes()
            result = run(root, str(fake_uv(root, "upgraded")))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / "paper/refs.bib").read_bytes(), before)
            summary = json.loads((root / ".project/build/reference-integrity/corrections/run.json").read_text())
            self.assertEqual(summary["outcome"], "candidates_found")
            self.assertEqual(summary["changed_keys"], ["real"])
            self.assertFalse(summary["approves_bibliography_changes"])
            self.assertFalse(summary["approves_claim_support"])

    def test_cap_ends_the_updater_that_uv_started(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n")
            runner = root / "fake-uv"
            # Like `uv run`, the stand-in waits for a child that does the work.
            write(runner, "#!/usr/bin/env python3\nimport pathlib, subprocess, sys\n"
                          "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
                          "pathlib.Path(sys.argv[0]).with_name('updater.pid').write_text(str(child.pid))\n"
                          "raise SystemExit(child.wait())\n")
            runner.chmod(0o755)
            result = subprocess.run(
                [sys.executable, str(CORRECTIONS), "--root", str(root), "--uv", str(runner), "--timeout", "2"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            pid = int((root / "updater.pid").read_text())
            stat = Path(f"/proc/{pid}/stat")
            self.assertTrue(not stat.exists() or stat.read_text().rsplit(")", 1)[1].split()[0] == "Z",
                            "the updater outlived the cap that ended its uv parent")
            summary = json.loads((root / ".project/build/reference-integrity/corrections/run.json").read_text())
            self.assertEqual(summary["outcome"], "incomplete")
            self.assertEqual(summary["unfinished_keys"], ["real"])

    def test_changed_tier_runs_only_on_entries_new_against_the_base(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n")
            runner = fake_uv(root)
            (root / ".agents/references/ledger.json").unlink()  # a policy and no ledger
            for command in (["git", "init", "-q"], ["git", "add", "-A"],
                            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "base"]):
                subprocess.run(command, cwd=root, check=True, capture_output=True)
            arguments = [sys.executable, str(CORRECTIONS), "--root", str(root), "--uv", "missing-uv",
                         "--scope", "changed", "--base", "HEAD"]
            unchanged = subprocess.run(arguments, text=True, capture_output=True, check=False)
            self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)
            self.assertIn("no provider queried", unchanged.stdout)
            with (root / "paper/refs.bib").open("a") as handle:
                handle.write("@article{added, author={B}, title={U}, journal={J}, year={2026}}\n")
            arguments[arguments.index("missing-uv")] = str(runner)
            added = subprocess.run(arguments, text=True, capture_output=True, check=False)
            self.assertIn("checks 1 of 2 entries", added.stdout)
            source = (root / ".project/build/reference-integrity/corrections/source.bib").read_text()
            self.assertIn("@article{added", source)
            self.assertNotIn("@article{real", source)

    def test_canonical_mutation_is_a_safety_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n")
            result = run(root, str(fake_uv(root, mutate=True)))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / ".project/build/reference-integrity/corrections/run.json").read_text())
            self.assertEqual(summary["outcome"], "unsafe_output")

    def test_local_env_is_allowlisted_and_does_not_override_exported_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".env", "OPENALEX_API_KEY=local\nS2_API_KEY=semantic\n")
            module = load_env_helper()
            with mock.patch.dict(os.environ, {**without_reference_keys(), "OPENALEX_API_KEY": "exported"}, clear=True):
                loaded = module.load_reference_env(root)
                self.assertEqual(os.environ["OPENALEX_API_KEY"], "exported")
                self.assertEqual(os.environ["S2_API_KEY"], "semantic")
                self.assertEqual(loaded, ["S2_API_KEY"])

            write(root / ".env", "UNSAFE=value\n")
            with self.assertRaisesRegex(ValueError, "unsupported key"):
                module.load_reference_env(root)


    def test_shared_file_exports_only_the_allowlisted_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".project/credentials/.env", SHARED_FILE)
            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                for key in UNRELATED_KEYS:
                    os.environ.pop(key, None)
                loaded = load_env_helper().load_reference_env(root)
                self.assertEqual(sorted(loaded), ["OPENALEX_API_KEY", "S2_API_KEY"])
                self.assertEqual(os.environ["S2_API_KEY"], "synthetic-s2")
                self.assertEqual(os.environ["OPENALEX_API_KEY"], "synthetic-openalex")
                for key in UNRELATED_KEYS:
                    self.assertNotIn(key, os.environ)

            write(root / ".project/credentials/.env", "S2_API_KEY='unmatched\n")
            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                with self.assertRaises(ValueError) as raised:
                    load_env_helper().load_reference_env(root)
            self.assertEqual(str(raised.exception), ".project/credentials/.env:1 has unmatched quotes")

    def test_environment_wins_over_root_env_and_root_env_over_shared_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / ".env", "OPENALEX_API_KEY=root\nS2_API_KEY=root\n")
            write(root / ".project/credentials/.env",
                  "BIBTEX_CHECK_MAILTO=shared@example.invalid\nOPENALEX_API_KEY=shared\nS2_API_KEY=shared\n")
            with mock.patch.dict(os.environ, {**without_reference_keys(), "OPENALEX_API_KEY": "exported"}, clear=True):
                loaded = load_env_helper().load_reference_env(root)
                self.assertEqual(loaded, ["S2_API_KEY", "BIBTEX_CHECK_MAILTO"])
                self.assertEqual(os.environ["OPENALEX_API_KEY"], "exported")
                self.assertEqual(os.environ["S2_API_KEY"], "root")
                self.assertEqual(os.environ["BIBTEX_CHECK_MAILTO"], "shared@example.invalid")

            write(root / ".env", "UNSAFE=value\n")
            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                with self.assertRaisesRegex(ValueError, r"^\.env:1 unsupported key: UNSAFE$"):
                    load_env_helper().load_reference_env(root)

    def test_worktree_reaches_the_shared_file_through_the_credentials_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            device = base / "device/.credentials/.env"
            write(device, SHARED_FILE)
            canonical = base / "canonical"
            (canonical / ".project/credentials").mkdir(parents=True)
            (canonical / ".project/credentials/.env").symlink_to(device)
            worktree = base / "worktree"
            prepare(worktree, "@article{real, author={A}, title={T}, journal={J}, year={2026}}\n")
            (worktree / ".project").mkdir(exist_ok=True)
            (worktree / ".project/credentials").symlink_to(canonical / ".project/credentials")

            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                self.assertEqual(sorted(load_env_helper().load_reference_env(worktree)), ["OPENALEX_API_KEY", "S2_API_KEY"])

            seen = base / "seen.json"
            environment = {key: value for key, value in without_reference_keys().items() if key not in UNRELATED_KEYS}
            result = run(worktree, str(fake_uv(worktree, record_env=seen)), env=environment)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(seen.read_text()), {
                "BIBTEX_CHECK_MAILTO": None, "OPENALEX_API_KEY": "synthetic-openalex", "S2_API_KEY": "synthetic-s2",
                "OPENAI_API_KEY": None, "CLAUDE_CODE_OAUTH_TOKEN": None,
            })
            for value in ("synthetic-openalex", "synthetic-s2", "synthetic-openai"):
                self.assertNotIn(value, result.stdout + result.stderr)

    def test_missing_files_load_nothing_and_a_missing_root_env_leaves_the_shared_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".project").mkdir()
            (root / ".project/credentials").symlink_to(root / "absent-canonical/.project/credentials")
            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                self.assertEqual(load_env_helper().load_reference_env(root), [])
                for key in REFERENCE_KEYS:
                    self.assertNotIn(key, os.environ)

            (root / ".project/credentials").unlink()
            write(root / ".project/credentials/.env", "S2_API_KEY=synthetic-s2\n")
            with mock.patch.dict(os.environ, without_reference_keys(), clear=True):
                self.assertEqual(load_env_helper().load_reference_env(root), ["S2_API_KEY"])
                self.assertEqual(os.environ["S2_API_KEY"], "synthetic-s2")


if __name__ == "__main__":
    unittest.main()
