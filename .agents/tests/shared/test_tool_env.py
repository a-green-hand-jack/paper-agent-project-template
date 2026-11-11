"""The project-local tool environment pins, isolates and never falls back."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / ".agents/scripts/shared/tool-env.sh"
MANIFEST = ROOT / ".agents/scripts/shared/tool-environments.json"
BENCHMARK_RADAR = ROOT / ".agents/skills/shared/benchmark-radar"


def fixture(root: Path) -> Path:
    target = root / ".agents/scripts/shared"
    target.mkdir(parents=True)
    shutil.copy2(SCRIPT, target / SCRIPT.name)
    shutil.copy2(MANIFEST, target / MANIFEST.name)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return target / SCRIPT.name


def fake_uv(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "uv"
    path.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env bash
            set -euo pipefail
            if [ "$1" = "venv" ]; then
              mkdir -p "$2/bin"
              cat > "$2/bin/benchmark-radar" <<'CLI'
            #!/usr/bin/env bash
            printf '%s\\n' "${BENCHMARK_RADAR_HOME:-}"
            CLI
              chmod +x "$2/bin/benchmark-radar"
            elif [ "$1" = "pip" ]; then
              :
            else
              echo "unexpected uv $*" >&2
              exit 1
            fi
            """
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)
    return directory


class ToolEnvironment(unittest.TestCase):
    def test_manifest_pins_the_vendored_skill_commit(self) -> None:
        record = json.loads(MANIFEST.read_text(encoding="utf-8"))["tools"]["benchmark-radar"]
        provenance = (BENCHMARK_RADAR / "PROVENANCE.md").read_text(encoding="utf-8")
        commit = re.search(r"^- Commit: ([0-9a-f]{40})", provenance, re.M)
        self.assertIsNotNone(commit)
        self.assertEqual(record["revision"], commit.group(1))
        self.assertEqual(record["source"], "https://github.com/ktwu01/benchmark-radar.git")
        self.assertEqual(record["env"], {"BENCHMARK_RADAR_HOME": "data"})

    def test_missing_environment_does_not_use_a_global_binary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "paper"
            root.mkdir()
            script = fixture(root)
            bin_directory = Path(directory) / "bin"
            bin_directory.mkdir()
            marker = Path(directory) / "called"
            global_binary = bin_directory / "benchmark-radar"
            global_binary.write_text(f"#!/usr/bin/env bash\nprintf called > {marker}\n", encoding="utf-8")
            global_binary.chmod(0o755)
            result = subprocess.run(
                ["bash", str(script), "run", "benchmark-radar", "status"],
                cwd=root,
                env={**os.environ, "PATH": f"{bin_directory}{os.pathsep}{os.environ['PATH']}"},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not installed", result.stderr)
            self.assertFalse(marker.exists(), "a global binary was used")

    def test_install_and_run_keep_data_in_each_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            paths: list[str] = []
            for name in ("first", "second"):
                root = base / name / "paper"
                root.mkdir(parents=True)
                script = fixture(root)
                bin_directory = fake_uv(base / f"{name}-bin")
                env = {**os.environ, "PATH": f"{bin_directory}{os.pathsep}{os.environ['PATH']}"}
                installed = subprocess.run(
                    ["bash", str(script), "install", "benchmark-radar"],
                    cwd=root, env=env, capture_output=True, text=True, check=False,
                )
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                status = subprocess.run(
                    ["bash", str(script), "status", "benchmark-radar"],
                    cwd=root, env=env, capture_output=True, text=True, check=False,
                )
                self.assertIn("benchmark-radar: installed", status.stdout)
                self.assertIn(f"{root}/.project/tools/benchmark-radar/data", status.stdout)
                run = subprocess.run(
                    ["bash", str(script), "run", "benchmark-radar"],
                    cwd=root, env=env, capture_output=True, text=True, check=False,
                )
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                paths.append(run.stdout.strip())
            self.assertEqual(
                paths,
                [f"{base}/first/paper/.project/tools/benchmark-radar/data",
                 f"{base}/second/paper/.project/tools/benchmark-radar/data"],
            )
            self.assertNotEqual(paths[0], paths[1])


if __name__ == "__main__":
    unittest.main()
