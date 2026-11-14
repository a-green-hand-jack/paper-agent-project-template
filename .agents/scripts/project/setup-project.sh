#!/usr/bin/env bash
# Paper setup, run by setup-worktree.sh: create the build directory the root
# Makefile writes to and say which TeX tools a build will use.
set -euo pipefail

root=$(git rev-parse --show-toplevel)
cd "$root"
mkdir -p .project/build

path=$PATH
[[ -z "${TEXBIN:-}" ]] || path=$TEXBIN:$PATH
for tool in latexmk pdflatex bibtex; do
  found=$(PATH=$path command -v "$tool" || true)
  if [[ -n $found ]]; then
    printf 'paper: %s %s\n' "$tool" "$found"
  else
    echo "warning: $tool not found; install TeX Live or set TEXBIN to its bin directory" >&2
  fi
done
for tool in pdftotext pdfinfo; do
  command -v "$tool" >/dev/null || echo "warning: $tool not found; make check needs poppler-utils" >&2
done

if command -v uv >/dev/null 2>&1; then
  [[ -x .project/venv/bin/python3 ]] || uv venv --quiet .project/venv
  .project/venv/bin/python3 -I -c 'import yaml, markdown_it' 2>/dev/null ||
    uv pip install --quiet --python .project/venv/bin/python3 PyYAML markdown-it-py ||
    echo "warning: could not install PyYAML and markdown-it-py into .project/venv" >&2
fi

python=${AGENTS_PYTHON:-}
if [[ -z $python ]]; then
  if [[ -x .project/venv/bin/python3 ]]; then python=.project/venv/bin/python3; else python=python3; fi
fi
"$python" -I -c 'import yaml, markdown_it' 2>/dev/null || {
  echo "warning: make check needs PyYAML and markdown-it-py under isolated Python (queried $python)" >&2
  echo "warning: install uv and rerun this setup, or set AGENTS_PYTHON to an interpreter that has them" >&2
}
