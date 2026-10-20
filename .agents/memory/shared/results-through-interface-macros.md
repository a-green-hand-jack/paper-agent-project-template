---
name: results-through-interface-macros
date: 2026-10-20
source: Issue #156 §5; downstream papers that could not tell which code repository, commit or run produced a reported number or figure
scope: shared
applies_to: paper repositories that report numbers, tables or figures produced by experiments in code repositories
status: active
supersedes: null
superseded_by: null
---

# Reported results come through interface macros with a recorded source

## Decision

1. **A reported number reaches the text only through an interface macro** in
   `paper/macros.tex`, never typed into a section. The macro's row in the
   paper-interfaces record names its meaning, control cue and source.
2. **Every result taken from a code repository is registered** in
   `assets/MANIFEST.yaml`: a result table, a figure's data file or a single
   reported number. The entry gives the source repository, commit, run or
   configuration identifier, SHA-256 and the command that regenerates it.
3. **Planned results are never written as observations.** A value that is not
   yet measured stays a `\PaperTODO{...}` (or its manifest entry has status
   `planned`), and the text around it says what is expected, not what was
   found.
4. **A locked claim links to its evidence**: the interface macros and manifest
   entries it rests on.

## Why

Without a recorded source, nobody can check whether a number in the abstract
is the one in the table, or regenerate a figure after a fix in the code
repository. One definition per value keeps every section and every build
consistent, and a manifest entry with a commit and a run identifier turns
"where does this come from" into a lookup. Writing an expected result as if it
had been observed is the most damaging error a paper agent can make, and it is
easiest to make when a placeholder looks like a value.

## Apply

- Add the value as an interface macro (marker, definition, a row in the
  paper-interfaces record with the manifest id as source) and use the macro in
  the text; `make check` fails when an interface is not defined, documented or
  used.
- Register the asset in `assets/MANIFEST.yaml`; large files stay outside Git
  and are linked under `assets/` (see the asset-lifecycle skill).
- Keep the experiment's context (question, protocol, runs, negative results) in
  the paper's experiments record, linked from the manifest entry.
- When a result changes, update the manifest entry, the macro value and every
  claim that rests on it in the same change, and say so in the PR.
