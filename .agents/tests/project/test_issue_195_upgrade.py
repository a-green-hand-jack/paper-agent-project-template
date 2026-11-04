"""Exercise the last released paper template with project-owned data."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_adoption_states import ROOT, CLONE, content_registry, git, shipped_tree, start_paper, tree
import test_reference_evidence as reference_fixture


class ExistingPaperUpgrade(unittest.TestCase):
    def test_upgrade_preserves_local_skill_ledger_evidence_and_exemplar(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-195-upgrade-") as directory:
            base = Path(directory)
            template = base / "template"
            template.mkdir()
            shipped_tree(template)
            registry = template / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            data["template"]["version"] = "v0.4.7-test"
            registry.write_text(content_registry.dumps(data))
            notes = template / "RELEASE_NOTES.md"
            notes.write_text(notes.read_text().replace(
                "# 发布说明\n", "# 发布说明\n\n## v0.4.7-test\n\n"
                "### Upgrading a paper from v0.4.6\n\n1. Review the migration plan.\n", 1))
            git("add", "-A", cwd=template)
            git("commit", "-qm", "candidate", cwd=template)
            git("tag", "v0.4.7-test", cwd=template)
            git("fetch", "-q", f"file://{ROOT}", "refs/tags/v0.4.6:refs/tags/v0.4.6", cwd=template)

            paper = base / "paper"
            paper.mkdir()
            subprocess.run(["tar", "-x", "-C", str(paper)], check=True,
                           input=git("archive", "v0.4.6", cwd=template).stdout)
            git("init", "-q", cwd=paper)
            start_paper(paper)
            old_skill = paper / ".agents/skills/shared/section-writing/SKILL.md"
            old_skill.write_text(old_skill.read_text() + "\n## In this repository\n\nLocal paper adaptation 195.\n")
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
            before = tree(paper)
            plan = run("--check", "v0.4.7-test")
            self.assertEqual(tree(paper), before, "preflight must be read-only")
            self.assertEqual(plan.returncode, 0, plan.stdout + plan.stderr)
            self.assertNotIn("has no `## v0.4.7-test` entry", plan.stdout)
            upgraded = run("v0.4.7-test")
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            moved = paper / ".agents/skills/shared/paper-writing/sources/section-writing/reference.md"
            self.assertIn("Local paper adaptation 195.", moved.read_text())
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
            repeat = run("v0.4.7-test")
            self.assertEqual(repeat.returncode, 0, repeat.stdout + repeat.stderr)
            self.assertEqual(tree(paper), after, "repeating the upgrade must not change bytes")


class DerivedTemplateUpgrade(unittest.TestCase):
    def test_local_template_registry_and_extra_root_survive_upstream_upgrade(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-195-derived-") as directory:
            base = Path(directory)
            template = base / "upstream"
            template.mkdir()
            shipped_tree(template)
            shutil.copy2(ROOT / ".agents/tests/project/test_adoption_states.py",
                         template / ".agents/tests/project/test_adoption_states.py")
            notes = template / "RELEASE_NOTES.md"
            notes.write_text(notes.read_text().replace("# 发布说明\n", "# 发布说明\n\n## test-up-1\n", 1))
            git("add", "-A", cwd=template)
            git("commit", "-qm", "source", cwd=template)
            git("tag", "test-up-1", cwd=template)
            registry = template / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            data["entries"].append({"path": ".agents/memory/project/upstream-only.md",
                                    "id": "upstream-only-195", "kind": "memory", "scope": "template",
                                    "owner": "template-maintainers", "summary": "Upstream only.",
                                    "status": "rejected", "source": {"issue": 195},
                                    "updated": "2026-11-04", "supersedes": [], "superseded_by": []})
            renamed = next(entry for entry in data["entries"]
                           if entry["id"] == "content-5e1742dff7120958")
            original_path = renamed["path"]
            renamed["path"] = ".agents/memory/project/upstream-renamed-dispatch.md"
            data["migrations"].append({
                "from": [{"id": renamed["id"], "path": original_path}],
                "to": [{"id": renamed["id"], "path": renamed["path"]}],
                "action": "rename", "reason": "Exercise an upstream-only rename.",
                "source_commit": "fixture", "verification": "derived upgrade regression",
            })
            registry.write_text(content_registry.dumps(data))
            notes.write_text(notes.read_text().replace("# 发布说明\n", "# 发布说明\n\n## test-up-2\n\n"
                             "### Upgrading a project from test-up-1\n\n1. Review the plan.\n", 1))
            record = template / ".agents/memory/shared/issue-close-out.md"
            record.write_text(record.read_text() + "\n")
            git("add", "-A", cwd=template)
            git("commit", "-qm", "target", cwd=template)
            git("tag", "test-up-2", cwd=template)

            derived = base / "derived"
            derived.mkdir()
            subprocess.run(["tar", "-x", "-C", str(derived)], check=True,
                           input=git("archive", "test-up-1", cwd=template).stdout)
            git("init", "-q", cwd=derived)
            local_registry = derived / ".agents/content-registry.yaml"
            local = content_registry.loads(local_registry.read_text())
            local["template"]["upstream"]["repository"] = str(template)
            local["template"]["upstream"]["version"] = "test-up-1"
            local_registry.write_text(content_registry.dumps(local))
            expected = {entry["id"]: entry for entry in local["entries"] if entry["scope"] == "template"}
            self.assertIn("references", local["policy"]["root_files"])
            git("add", "-A", cwd=derived)
            git("commit", "-qm", "derived", cwd=derived)
            script = ROOT / ".agents/scripts/shared/upgrade-template.sh"
            result = subprocess.run(["bash", str(script), "test-up-2"], cwd=derived,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            updated = content_registry.loads(local_registry.read_text())
            entries = {entry["id"]: entry for entry in updated["entries"]}
            self.assertTrue(expected.keys() <= entries.keys())
            for identity, original in expected.items():
                self.assertEqual(entries[identity], original)
            self.assertNotIn("upstream-only-195", entries)
            self.assertTrue(any(e.get("id") == "upstream-only-195" for e in updated["omitted"]))
            self.assertIn("references", updated["policy"]["root_files"])
            check = subprocess.run(["bash", ".agents/scripts/shared/check-development.sh"], cwd=derived,
                                   capture_output=True, text=True, check=False)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)


if __name__ == "__main__":
    unittest.main()
