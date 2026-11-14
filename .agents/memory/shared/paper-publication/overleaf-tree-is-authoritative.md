---
name: overleaf-tree-is-authoritative
date: 2026-11-14
source: ResearchWorld_paper `overleaf-spacing-sync` record, written after a sync replay of intermediate commits lost the Overleaf-side spacing edits
applies_to: paper repositories that mirror paper/ to an Overleaf project
---

# The Overleaf tip's tree is authoritative

## Decision

When the Overleaf project has edits this repository does not, take them in **by
tree, byte for byte**, and compare the whole `paper/` tree against the tip. Do
not replay the Overleaf intermediate commits into this repository, and do not
reconcile file by file from a diff summary.

## Why

Overleaf's own commits record saves, not decisions: they interleave reviewers'
spacing and wording changes with no-op saves, and replaying them produces
conflicts that are resolved by guessing. The tip's tree is the only state that
someone actually edited, and a tree comparison makes every difference visible
before it is applied.

## Apply

- Fetch the Overleaf project, compare trees, and apply the whole tree once,
  then rebuild and inspect the pages.
- Keep the sync in `paper/` only; the repository root and the development plane
  never go to Overleaf.
- Do not pipe a build into `head` or another early-closing command: the SIGPIPE
  kills `latexmk` mid-run and leaves a truncated PDF that later checks read as
  the real output.
- Record the sync point (commit and time) so a later sync knows what was
  already taken in.
