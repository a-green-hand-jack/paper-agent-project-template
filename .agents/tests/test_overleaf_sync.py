"""overleaf-sync.sh against a local bare repository that stands in for Overleaf."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / ".agents/scripts/overleaf-sync.sh"
ENV = {key: value for key, value in os.environ.items()
       if not key.startswith("GIT_") and key != "OVERLEAF_BRANCH"}
ENV.update({
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.org",
    "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.org",
})


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, check=True,
                          capture_output=True, text=True).stdout.strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class OverleafSync(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        base = Path(self.directory.name)
        self.overleaf = base / "overleaf.git"
        git(base, "init", "--quiet", "--bare", "--initial-branch=master", str(self.overleaf))
        editor = base / "editor"
        git(base, "clone", "--quiet", str(self.overleaf), str(editor))
        write(editor / "main.tex", "Overleaf starter\n")
        git(editor, "add", ".")
        git(editor, "commit", "--quiet", "-m", "Overleaf starter")
        git(editor, "push", "--quiet", "origin", "HEAD:master")
        self.editor = editor
        self.starter = git(self.overleaf, "rev-parse", "master")
        self.repo = base / "repo"
        git(base, "init", "--quiet", "--initial-branch=dev", str(self.repo))
        write(self.repo / "README.md", "A root file that never reaches Overleaf.\n")
        write(self.repo / "paper/main.tex", "Paper v1\n")
        write(self.repo / "paper/sections/intro.tex", "Intro v1\n")
        self.commit("paper v1")
        git(self.repo, "remote", "add", "overleaf", str(self.overleaf))

    def tearDown(self) -> None:
        self.directory.cleanup()

    def commit(self, message: str) -> str:
        git(self.repo, "add", ".")
        git(self.repo, "commit", "--quiet", "-m", message)
        return git(self.repo, "rev-parse", "HEAD")

    def sync(self, *args: str, expect: int = 0) -> str:
        result = subprocess.run(["bash", str(TOOL), *args], cwd=self.repo, env=ENV,
                                capture_output=True, text=True, check=False)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, expect, output)
        return output

    def overleaf_edit(self, name: str, text: str) -> None:
        git(self.editor, "pull", "--quiet", "--ff-only", "origin", "master")
        write(self.editor / name, text)
        git(self.editor, "commit", "--quiet", "-am", "Overleaf edit")
        git(self.editor, "push", "--quiet", "origin", "HEAD:master")

    def overleaf_tree(self) -> str:
        return git(self.overleaf, "rev-parse", "master^{tree}")

    def paper_tree(self) -> str:
        return git(self.repo, "rev-parse", "HEAD:paper")

    def test_push_pull_merge_and_push_again(self) -> None:
        self.assertIn("STATE unrelated", self.sync("status"))
        self.assertIn("Overleaf holds edits that HEAD does not have (state unrelated)", self.sync("push", expect=1))

        output = self.sync("push", "--replace")
        self.assertIn("OK pushed HEAD:paper to overleaf/master", output)
        self.assertEqual(self.overleaf_tree(), self.paper_tree())
        self.assertEqual(git(self.overleaf, "rev-parse", "master^"), self.starter)
        self.assertEqual(git(self.overleaf, "ls-tree", "--name-only", "master").split(), ["main.tex", "sections"])
        self.assertIn(f"Paper-Source-Commit: {git(self.repo, 'rev-parse', 'HEAD')}",
                      git(self.overleaf, "log", "-1", "--format=%B", "master"))
        self.assertIn("STATE in-sync", self.sync("status"))
        shared = git(self.repo, "rev-parse", "HEAD")

        self.overleaf_edit("main.tex", "Paper v1, edited on Overleaf\n")
        write(self.repo / "paper/sections/intro.tex", "Intro v2, edited in Git\n")
        self.commit("intro v2")
        self.assertIn("STATE diverged", self.sync("status"))
        self.assertIn("state diverged", self.sync("push", expect=1))

        head_before = git(self.repo, "rev-parse", "HEAD")
        tip = git(self.overleaf, "rev-parse", "master")
        output = self.sync("pull")
        branch = f"sync/overleaf-{tip[:12]}"
        self.assertIn(f"OK {branch} holds Overleaf's paper/", output)
        self.assertEqual(git(self.repo, "rev-parse", f"{branch}:paper"), self.overleaf_tree())
        self.assertEqual(git(self.repo, "rev-parse", f"{branch}^"), shared)
        self.assertEqual(git(self.repo, "rev-parse", f"{branch}:README.md"), git(self.repo, "rev-parse", f"{shared}:README.md"))
        self.assertIn(f"Overleaf-Commit: {tip}", git(self.repo, "log", "-1", "--format=%B", branch))
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), head_before)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertIn("already holds Overleaf's edits", self.sync("pull"))

        git(self.repo, "merge", "--quiet", "--no-edit", branch)
        self.assertEqual((self.repo / "paper/main.tex").read_text(), "Paper v1, edited on Overleaf\n")
        self.assertEqual((self.repo / "paper/sections/intro.tex").read_text(), "Intro v2, edited in Git\n")
        self.assertIn("STATE overleaf-behind", self.sync("status"))
        self.sync("push")
        self.assertEqual(self.overleaf_tree(), self.paper_tree())

    def test_rewrapped_commit_with_the_same_tree_is_in_sync(self) -> None:
        self.sync("push", "--replace")
        tip = git(self.overleaf, "rev-parse", "master")
        rewrapped = git(self.overleaf, "commit-tree", f"{tip}^{{tree}}", "-p", f"{tip}^", "-m", "Overleaf's own commit")
        git(self.overleaf, "update-ref", "refs/heads/master", rewrapped)
        self.assertIn("STATE in-sync", self.sync("status"))
        self.assertIn("OK nothing to push", self.sync("push"))

    def test_pull_when_only_overleaf_changed(self) -> None:
        self.sync("push", "--replace")
        self.overleaf_edit("sections/intro.tex", "Intro, edited on Overleaf\n")
        self.assertIn("STATE overleaf-ahead", self.sync("status"))
        self.sync("pull")
        tip = git(self.overleaf, "rev-parse", "master")
        git(self.repo, "merge", "--quiet", "--ff-only", f"sync/overleaf-{tip[:12]}")
        self.assertEqual(self.paper_tree(), self.overleaf_tree())
        self.assertIn("STATE in-sync", self.sync("status"))

    def test_uncommitted_paper_changes_are_reported_not_pushed(self) -> None:
        self.sync("push", "--replace")
        write(self.repo / "paper/main.tex", "Uncommitted\n")
        output = self.sync("push")
        self.assertIn("NOTE uncommitted changes in paper/", output)
        self.assertEqual(self.overleaf_tree(), self.paper_tree())

    def test_refuses_a_token_in_the_remote_url(self) -> None:
        git(self.repo, "remote", "set-url", "overleaf", "https://git:s3cret-token@git.overleaf.com/0000")
        output = self.sync("status", expect=1)
        self.assertIn("holds a password or token", output)
        self.assertNotIn("s3cret-token", output)

    def test_never_uses_the_repository_root(self) -> None:
        for tree in (".", "./", "/", "paper/../.."):
            with self.subTest(tree=tree):
                self.assertIn("never its root", self.sync("push", "--tree", tree, expect=1))

    def test_a_second_tree_syncs_to_its_own_remote(self) -> None:
        write(self.repo / "poster/poster.tex", "Poster\n")
        self.commit("poster")
        base = Path(self.directory.name)
        poster = base / "poster.git"
        git(base, "init", "--quiet", "--bare", "--initial-branch=main", str(poster))
        git(self.repo, "remote", "add", "overleaf-poster", str(poster))
        self.assertIn("cannot fetch branch 'main'", self.sync("push", "--remote", "overleaf-poster", "--tree", "poster", expect=1))
        git(self.repo, "push", "--quiet", "overleaf-poster", f"{git(self.repo, 'commit-tree', 'HEAD:poster', '-m', 'start')}:refs/heads/main")
        self.assertIn("STATE in-sync", self.sync("status", "--remote", "overleaf-poster", "--tree", "poster"))


if __name__ == "__main__":
    unittest.main()
