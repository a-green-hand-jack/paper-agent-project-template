---
name: results-ledger
date: 2026-11-15
source: Issue #243; the entries `assets/MANIFEST.yaml` held while this template kept an asset folder
applies_to: every reported number, table or figure data file the paper takes from a code repository
---

# Reported results have one ledger row and no asset folder

## Decision

1. Every value the paper reports from a code repository — a number, a table, a
   figure's data file — has one row in the table below, and that row is the only
   place its provenance is written down.
2. A row gives the stable id, the kind, whether the value is `observed` or
   `planned`, the source repository with its commit and run or configuration,
   the file with its SHA-256, the command that regenerates it, the interface
   macro that carries it into `paper/macros.tex`, and where the paper uses it.
3. This repository keeps no `assets/` directory and no asset links. A small file
   the paper includes is committed under `paper/tables/` or `paper/figures/`; a
   large payload (raw logs, checkpoints, a dataset) stays in the code repository
   or managed storage that produces it and never enters this repository.
4. A planned value is never written as an observation: the text carries
   `\PaperTODO{...}` until the row says `observed`.

| Id | Kind | Status | Source | File and SHA-256 | Regenerate | Macro | Used in |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | number, table or figure-data | observed or planned | `OWNER/REPOSITORY@COMMIT`, run or configuration | `path/in/the/repository`; `sha256:…` | the command that rebuilds it | `\MainResult` or — | `paper/tables/main.tex` or — |

## Why

Without a recorded source nobody can tell whether the abstract reports the
number in the table, or rebuild a figure after the code repository changes. One
row per value turns "where does this come from" into a lookup, and it keeps a
value, its macro and the claims that rest on it changing together.

A separate top-level asset folder held the same information in a second
vocabulary: the entries named sources the memory records already cite, its links
exposed machine paths that no fresh clone can resolve, and every worktree setup
had to recreate them. The ledger lives with the records that cite it instead.

## Apply

- Add the row before the value reaches `paper/macros.tex`, and give the macro's
  row in [`paper-interfaces.md`](paper-interfaces.md) the ledger id as its
  source. `make check` fails when an interface is undefined, undocumented or
  unused.
- Keep the experiment's question, protocol, runs and negative results in
  [`experiments.md`](experiments.md), and name the ledger ids it produced.
- When a value changes, update the row, the macro value and every claim that
  rests on it in the same change, and say so in the PR.
