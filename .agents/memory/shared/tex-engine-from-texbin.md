---
name: tex-engine-from-texbin
date: 2026-10-20
source: Issue #156 §2; downstream paper repositories where a wrapper earlier on PATH launched an unavailable container instead of TeX, or a Makefile hard-coded one machine's TeX Live path
scope: shared
applies_to: repositories that build LaTeX on more than one machine or in CI
status: active
supersedes: null
superseded_by: null
---

# The build takes its TeX binaries from an overridable TEXBIN

## Decision

1. **The product Makefile never hard-codes a machine's TeX path.** It runs
   `latexmk` from `PATH`, and an overridable `TEXBIN` (a TeX Live `bin`
   directory) is put first on `PATH` when set.
2. **Build leftovers stay out of every tracked tree.** Output and
   intermediates go to the build directory (`.project/build/` in a worktree,
   `paper/build/` in a copy of `paper/` alone), never next to the sources, and
   a tree projected elsewhere (Overleaf) carries none of them.
3. **Run builds with their output redirected to a file**, and read the log
   from there.

## Why

A `pdflatex` wrapper earlier on `PATH` started a container image that was not
available, and the build failed with an unrelated "pull access denied". A
Makefile with one user's TeX Live path failed on every other machine. Tracked
`.bbl`, `.pdf` and aux files from one form drifted against the others and
reached a projected tree.

## Apply

- Build with `make pdf TEXBIN=/path/to/texlive/<year>/bin/<platform>` when the
  right `latexmk` is not first on `PATH`; `setup-project.sh` prints the TeX
  tools a build will use.
- Match Overleaf's TeX Live version (Menu, Settings) to the local one when both
  build the same paper.
- Nothing under `paper/` is generated: `.gitignore` excludes LaTeX leftovers
  and PDFs there as a safety net, not as their destination.
