"""Exercise the v0.4.7 paper template with project-owned data."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_template_adoption_states import ROOT, CLONE, content_registry, drop_bullets, git, refused_paths, setUpModule, shipped_tree, start_paper, tree
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
            old_brief = paper / ".agents/memory/project/brief.md"
            old_brief.write_text(old_brief.read_text() + "\nLocal paper decision: preserve me. [Reference](../shared/reference-integrity.md).\n")
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
            brief_entry = next(entry for entry in data["entries"] if entry["path"] == ".agents/memory/project/brief.md")
            upstream_brief_id = brief_entry["id"]
            brief_entry["id"] = "local-brief-197"
            for migration in data.get("migrations", []):
                for destination in migration.get("to", []):
                    if destination["id"] == upstream_brief_id:
                        destination["upstream_id"] = upstream_brief_id
                        destination["id"] = "local-brief-197"
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
            linked_parent = paper / ".agents/memory/project/paper-foundation"
            linked_parent.symlink_to("../../knowledge/project", target_is_directory=True)
            symlink_tree = tree(paper)
            symlink_conflict = run("--check", "v0.4.8-test")
            self.assertNotEqual(symlink_conflict.returncode, 0, symlink_conflict.stdout + symlink_conflict.stderr)
            self.assertIn("symbolic-link parent", symlink_conflict.stdout + symlink_conflict.stderr)
            self.assertEqual(tree(paper), symlink_tree)
            linked_parent.unlink()
            project_conflict = paper / ".agents/memory/project/paper-foundation/brief.md"
            project_conflict.parent.mkdir(parents=True)
            project_conflict.write_text("existing project record\n")
            conflict_tree = tree(paper)
            conflict = run("--check", "v0.4.8-test")
            self.assertNotEqual(conflict.returncode, 0, conflict.stdout + conflict.stderr)
            self.assertIn("project-owned destination already exists", conflict.stdout + conflict.stderr)
            self.assertEqual(tree(paper), conflict_tree)
            project_conflict.unlink()
            project_conflict.parent.rmdir()
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
            self.assertNotEqual(plan.returncode, 0, plan.stdout + plan.stderr)
            self.assertEqual(refused_paths(plan.stdout), ["AGENTS.md"], plan.stdout + plan.stderr)
            self.assertNotIn("has no `## v0.4.8-test` entry", plan.stdout)
            blocked = run("v0.4.8-test")
            self.assertNotEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
            self.assertEqual(tree(paper), before, "unresolved conflicts must not move project-owned records")
            target_agents = git("show", "v0.4.8-test:AGENTS.md", cwd=template).stdout.decode()
            (paper / "AGENTS.md").write_text(drop_bullets(target_agents, lambda line: "protects the case branches" in line))
            upgraded = run("--resolved", "AGENTS.md", "v0.4.8-test")
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            moved = paper / ".agents/skills/shared/paper-writing/SKILL.md"
            self.assertIn("Local paper adaptation 195.", moved.read_text())
            self.assertFalse((paper / ".agents/memory/project/brief.md").exists())
            self.assertIn("Local paper decision: preserve me.", (paper / ".agents/memory/project/paper-foundation/brief.md").read_text())
            self.assertIn("[Reference](../../shared/paper-references/reference-integrity.md)", (paper / ".agents/memory/project/paper-foundation/brief.md").read_text())
            upgraded_registry = content_registry.loads((paper / ".agents/content-registry.yaml").read_text())
            self.assertEqual(next(entry for entry in upgraded_registry["entries"] if entry["path"] == ".agents/memory/project/paper-foundation/brief.md")["id"], "local-brief-197")
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
