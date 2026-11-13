"""Upgrade a paper that left template content out, from the last release."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from test_template_adoption_states import ROOT, CLONE, content_registry, git, setUpModule, shipped_tree, start_paper, tree

SOURCE = "v0.4.12"
TARGET = "v0.4.13-test"
REASON = "Template-only content this paper does not adopt; kept as provenance, not as a live entry."
DUPLICATED = ("Dockerfile", ".agents/memory/project/paper-foundation/brief.md")
LEFT_OUT = ".agents/knowledge/shared/gpt5-strict-backend-requests.md"


class OmittedContentUpgrade(unittest.TestCase):
    def test_omitted_paths_stay_out_and_duplicates_are_repaired(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-216-upgrade-") as directory:
            base = Path(directory)
            template = base / "template"
            template.mkdir()
            shipped_tree(template)
            registry = template / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            data["template"]["version"] = TARGET
            registry.write_text(content_registry.dumps(data))
            notes = template / "RELEASE_NOTES.md"
            notes.write_text(notes.read_text().replace(
                "# 发布说明\n", f"# 发布说明\n\n## {TARGET}\n\n"
                f"### Upgrading a paper from {SOURCE}\n\n**Command only.**\n", 1))
            git("add", "-A", cwd=template)
            git("commit", "-qm", "candidate", cwd=template)
            git("tag", TARGET, cwd=template)
            git("fetch", "-q", f"file://{ROOT}", f"refs/tags/{SOURCE}:refs/tags/{SOURCE}", cwd=template)

            paper = base / "paper"
            paper.mkdir()
            subprocess.run(["tar", "-x", "-C", str(paper)], check=True,
                           input=git("archive", SOURCE, cwd=template).stdout)
            git("init", "-q", cwd=paper)
            start_paper(paper)
            registry = paper / ".agents/content-registry.yaml"
            data = content_registry.loads(registry.read_text())
            entries = {entry["path"]: entry for entry in data["entries"]}
            for path in (*DUPLICATED, LEFT_OUT):
                (paper / path).unlink(missing_ok=True)
                data["omitted"].append({"id": entries[path]["id"], "path": path, "reason": REASON})
            data["entries"] = [entry for entry in data["entries"] if entry["path"] != LEFT_OUT]
            registry.write_text(content_registry.dumps(data))
            subprocess.run(["bash", ".agents/scripts/shared/check-development.sh", "--write-indexes"],
                           cwd=paper, capture_output=True, text=True, check=False)
            git("add", "-A", cwd=paper)
            git("commit", "-qm", "paper", cwd=paper)

            clone = paper / CLONE
            clone.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", "--bare", str(template), str(clone)], check=True)
            script = template / ".agents/scripts/shared/upgrade-template.sh"

            def run(*arguments: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(["bash", str(script), *arguments], cwd=paper,
                                      capture_output=True, text=True, check=False)

            before = tree(paper)
            plan = run("--check", TARGET)
            self.assertEqual(tree(paper), before, "preflight must be read-only")
            self.assertEqual(plan.returncode, 0, plan.stdout + plan.stderr)
            for path in (*DUPLICATED, LEFT_OUT):
                self.assertEqual(
                    [line.strip() for line in plan.stdout.splitlines() if f" {path}" in line or line.strip().startswith(path)],
                    [f"kept out: {path} (omitted locally)"], plan.stdout)

            upgraded = run(TARGET)
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            data = content_registry.loads(registry.read_text())
            self.assertEqual(data["template"]["version"], TARGET)
            live = {entry["id"] for entry in data["entries"]}
            for path in (*DUPLICATED, LEFT_OUT):
                self.assertFalse((paper / path).exists(), path)
                records = [record for record in data["omitted"] if record["path"] == path]
                self.assertEqual([record["reason"] for record in records], [REASON], path)
                self.assertNotIn(records[0]["id"], live, path)
                self.assertNotIn(path, {entry["path"] for entry in data["entries"]})
            self.assertEqual(live & {record["id"] for record in data["omitted"]}, set())
            development = subprocess.run(["bash", ".agents/scripts/shared/check-development.sh"],
                                         cwd=paper, capture_output=True, text=True, check=False)
            self.assertEqual(development.returncode, 0, development.stdout + development.stderr)
            after = tree(paper)
            repeat = run(TARGET)
            self.assertEqual(repeat.returncode, 0, repeat.stdout + repeat.stderr)
            self.assertEqual(tree(paper), after, "repeating the upgrade must not change bytes")


if __name__ == "__main__":
    unittest.main()
