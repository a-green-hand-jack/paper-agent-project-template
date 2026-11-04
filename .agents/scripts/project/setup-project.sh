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
python3 -I -c 'import yaml, markdown_it' 2>/dev/null || echo 'warning: make check needs PyYAML and markdown-it-py available to isolated Python' >&2
