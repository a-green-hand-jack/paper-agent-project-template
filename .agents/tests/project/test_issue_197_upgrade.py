"""Exercise the v0.4.7 paper template with project-owned data."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_adoption_states import ROOT, CLONE, content_registry, git, shipped_tree, start_paper, tree
import test_reference_evidence as reference_fixture


class ExistingPaper197Upgrade(unittest.TestCase):
    def test_upgrade_preserves_local_skill_ledger_evidence_and_exemplar(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-197-upgrade-") as directory:
            base = Path(directory)
            template = base / "template"
            template.mkdir()
            shipped_tree(template)
            registry = template / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            data["template"]["version"] = "v0.4.8-test"
            registry.write_text(content_registry.dumps(data))
            notes = template / "RELEASE_NOTES.md"
            notes.write_text(notes.read_text().replace(
                "# 发布说明\n", "# 发布说明\n\n## v0.4.8-test\n\n"
                "### Upgrading a paper from v0.4.7\n\n1. Review the migration plan.\n", 1))
            git("add", "-A", cwd=template)
            git("commit", "-qm", "candidate", cwd=template)
            git("tag", "v0.4.8-test", cwd=template)
            git("fetch", "-q", f"file://{ROOT}", "refs/tags/v0.4.7:refs/tags/v0.4.7", cwd=template)

            paper = base / "paper"
            paper.mkdir()
            subprocess.run(["tar", "-x", "-C", str(paper)], check=True,
                           input=git("archive", "v0.4.7", cwd=template).stdout)
            git("init", "-q", cwd=paper)
            start_paper(paper)
            old_skill = paper / ".agents/skills/shared/paper-writing/SKILL.md"
            old_skill.write_text(old_skill.read_text() + "\n## In this repository\n\nLocal paper adaptation 195.\n")
            old_script = paper / ".agents/scripts/shared/reference_evidence.py"
            old_script.write_text(old_script.read_text() + "\n# Local paper adaptation 197.\n")
            reference_fixture.fixture(paper, teX="\\section{Intro}\nA fixture claim~\\citep{k1,k2}.\n")
            reference_fixture.run(paper, "inventory", check=True)
            ledger = paper / ".agents/references/ledger.json"
            occurrence = json.loads(ledger.read_text())["citation_occurrences"][0]["occurrence_id"]
            reference_fixture.run(paper, "record", "--occurrence-id", occurrence, "--key", "k1",
                                  "--verdict", "supported", "--state", "provisional",
                                  "--passage-text", "The fixture source supports the claim.",
                                  "--locator", "section 2", "--origin", "semantic-scholar-snippet",
                                  "--doi", "10.1000/example", check=True)
            before_reference_check = reference_fixture.run_checker(paper)
            self.assertEqual(before_reference_check.returncode, 0, before_reference_check.stdout)
            ledger_bytes = ledger.read_bytes()
            exemplar = paper / ".agents/knowledge/project/local-exemplar.md"
            exemplar.write_text("---\nname: local-exemplar\ndate: 2026-11-04\nsource: example\napplies_to: this paper\n---\n\n# Local exemplar\n\n## Fact\n\nExample 195.\n\n## Evidence\n\nSource 195.\n\n## Refresh\n\nReview on change.\n")
            local_skill = paper / ".agents/skills/project/local-skill/SKILL.md"
            local_skill.parent.mkdir(parents=True)
            local_skill.write_text("---\nname: local-skill\ndescription: A local paper skill.\n---\n\nLocal skill 195.\n")
            registry = paper / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            (paper / ".agents/skills/shared/credential-setup/SKILL.md").unlink()
            (paper / ".agents/skills/shared/credential-setup").rmdir()
            (paper / ".agents/knowledge/shared/credential-inventory.md").unlink()
            for entry in data["entries"]:
                if entry["path"] in (".agents/skills/shared/credential-setup/",
                                     ".agents/knowledge/shared/credential-inventory.md"):
                    entry["status"] = "rejected"
                    entry["adoption"] = "Explicit local fixture decision."
            for path, identity, kind in [
                (".agents/knowledge/project/local-exemplar.md", "local-exemplar-195", "knowledge"),
                (".agents/skills/project/local-skill/", "local-skill-195", "skill"),
            ]:
                entry = {"path": path, "id": identity, "kind": kind, "scope": "project",
                         "owner": "project-maintainers", "summary": "Local fixture.", "status": "active",
                         "source": {"issue": 195}, "updated": "2026-11-04", "supersedes": [], "superseded_by": []}
                if kind == "knowledge":
                    entry["refresh_after"] = "when the example changes"
                data["entries"].append(entry)
            registry.write_text(content_registry.dumps(data))
            clone = paper / CLONE
            clone.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", "--bare", str(template), str(clone)], check=True)
            script = template / ".agents/scripts/shared/upgrade-template.sh"
            def run(*arguments: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(["bash", str(script), *arguments], cwd=paper,
                                      capture_output=True, text=True, check=False)
            conflicting = paper / ".agents/scripts/shared/paper-references/reference_evidence.py"
            conflicting.parent.mkdir(parents=True)
            conflicting.write_text("local conflicting destination\n")
            conflict_tree = tree(paper)
            conflict = run("--check", "v0.4.8-test")
            self.assertNotEqual(conflict.returncode, 0, conflict.stdout + conflict.stderr)
            self.assertIn("conflicting existing destination", conflict.stdout + conflict.stderr)
            self.assertEqual(tree(paper), conflict_tree)
            conflicting.unlink()
            conflicting.parent.rmdir()
            before = tree(paper)
            plan = run("--check", "v0.4.8-test")
            self.assertEqual(tree(paper), before, "preflight must be read-only")
            self.assertEqual(plan.returncode, 0, plan.stdout + plan.stderr)
            self.assertNotIn("has no `## v0.4.8-test` entry", plan.stdout)
            upgraded = run("v0.4.8-test")
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            moved = paper / ".agents/skills/shared/paper-writing/SKILL.md"
            self.assertIn("Local paper adaptation 195.", moved.read_text())
            self.assertFalse((paper / ".agents/scripts/shared/reference_evidence.py").exists())
            self.assertIn("Local paper adaptation 197.", (paper / ".agents/scripts/shared/paper-references/reference_evidence.py").read_text())
            self.assertTrue((paper / ".agents/tests/shared/paper-references/test_reference_evidence.py").exists())
            self.assertEqual(ledger.read_bytes(), ledger_bytes)
            after_reference_check = reference_fixture.run_checker(paper)
            self.assertEqual(after_reference_check.returncode, 0, after_reference_check.stdout)
            self.assertIn("Example 195.", exemplar.read_text())
            self.assertIn("Local skill 195.", local_skill.read_text())
            self.assertFalse((paper / ".agents/skills/shared/credential-setup/SKILL.md").exists())
            self.assertFalse((paper / ".agents/knowledge/shared/credential-inventory.md").exists())
            development = subprocess.run(["bash", ".agents/scripts/shared/check-development.sh"],
                                         cwd=paper, capture_output=True, text=True, check=False)
            self.assertEqual(development.returncode, 0, development.stdout + development.stderr)
            after = tree(paper)
            repeat = run("v0.4.8-test")
            self.assertEqual(repeat.returncode, 0, repeat.stdout + repeat.stderr)
            self.assertEqual(tree(paper), after, "repeating the upgrade must not change bytes")
