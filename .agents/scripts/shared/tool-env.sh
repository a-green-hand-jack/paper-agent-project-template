#!/usr/bin/env bash
# Project-local environments for optional CLIs. The declaration is
# tool-environments.json beside this script. Environments and their data stay
# under this worktree's .project/; make check never calls this script.
#
#   tool-env.sh list
#   tool-env.sh install <tool>
#   tool-env.sh status <tool>
#   tool-env.sh run <tool> [arguments...]
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
manifest="$script_dir/tool-environments.json"
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "ERROR tool-env: run inside a Git worktree" >&2
  exit 2
}

usage() {
  echo "usage: tool-env.sh list | install <tool> | status <tool> | run <tool> [arguments...]" >&2
  exit 2
}

tool_field() {
  python3 - "$manifest" "$1" "$2" <<'PY'
import json
import sys

manifest, tool, key = sys.argv[1:4]
try:
    record = json.load(open(manifest, encoding="utf-8"))["tools"][tool]
except (OSError, KeyError, ValueError) as error:
    raise SystemExit(f"ERROR tool-env: unknown tool {tool!r} or unreadable {manifest}: {error}")
value = record.get(key, "")
if isinstance(value, dict):
    for name, path in value.items():
        print(f"{name}={path}")
elif value is not None:
    print(value)
PY
}

project_dir() {
  printf '%s/.project/tools/%s' "$root" "$1"
}

require_tool() {
  if [ -z "$(tool_field "$1" source)" ]; then
    echo "ERROR tool-env: $1 has no source in $manifest" >&2
    exit 2
  fi
}

install_tool() {
  local tool=$1 project source revision entry
  project=$(project_dir "$tool")
  require_tool "$tool"
  source=$(tool_field "$tool" source)
  revision=$(tool_field "$tool" revision)
  entry=$(tool_field "$tool" entrypoint)
  if ! command -v uv >/dev/null 2>&1; then
    echo "ERROR tool-env: uv is required to create $project; install uv first" >&2
    exit 2
  fi
  mkdir -p "$project"
  if [ ! -x "$project/venv/bin/python" ]; then
    uv venv "$project/venv"
  fi
  VIRTUAL_ENV="$project/venv" uv pip install --python "$project/venv/bin/python" "git+$source@$revision"
  if [ ! -x "$project/venv/bin/$entry" ]; then
    echo "ERROR tool-env: $source@$revision did not install $entry" >&2
    exit 2
  fi
  while IFS='=' read -r name path; do
    if [ -n "$name" ]; then
      mkdir -p "$project/$path"
      echo "OK tool-env: $name=$project/$path"
    fi
  done < <(tool_field "$tool" env)
  echo "OK tool-env: installed $tool at $project/venv from $source@$revision"
}

run_tool() {
  local tool=$1 project entry name path
  shift
  project=$(project_dir "$tool")
  entry=$(tool_field "$tool" entrypoint)
  if [ ! -x "$project/venv/bin/$entry" ]; then
    echo "ERROR tool-env: $tool is not installed in this worktree;" >&2
    echo "run: bash .agents/scripts/shared/tool-env.sh install $tool" >&2
    exit 2
  fi
  while IFS='=' read -r name path; do
    if [ -n "$name" ]; then
      mkdir -p "$project/$path"
      export "$name=$project/$path"
    fi
  done < <(tool_field "$tool" env)
  exec "$project/venv/bin/$entry" "$@"
}

status_tool() {
  local tool=$1 project entry name path
  project=$(project_dir "$tool")
  entry=$(tool_field "$tool" entrypoint)
  if [ -x "$project/venv/bin/$entry" ]; then
    echo "$tool: installed"
  else
    echo "$tool: missing"
  fi
  echo "  source: $(tool_field "$tool" source)"
  echo "  revision: $(tool_field "$tool" revision)"
  echo "  venv: $project/venv"
  while IFS='=' read -r name path; do
    if [ -n "$name" ]; then
      echo "  $name: $project/$path"
    fi
  done < <(tool_field "$tool" env)
}

list_tools() {
  python3 - "$manifest" <<'PY'
import json
import sys

for name, record in json.load(open(sys.argv[1], encoding="utf-8"))["tools"].items():
    print(f"{name}: {record.get('summary', '')}")
PY
}

case "${1:-}" in
  list)
    list_tools
    ;;
  install)
    [ $# -eq 2 ] || usage
    install_tool "$2"
    ;;
  status)
    [ $# -eq 2 ] || usage
    status_tool "$2"
    ;;
  run)
    [ $# -ge 2 ] || usage
    tool=$2
    shift 2
    run_tool "$tool" "$@"
    ;;
  *)
    usage
    ;;
esac
