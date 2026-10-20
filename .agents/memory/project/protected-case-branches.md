---
name: protected-case-branches
date: 2026-10-20
source: DEC-0014 of this template's decision log (DECISIONS.md before v0.4.0), carried over by Issue #156
scope: project
applies_to: this template repository's case branches, case Issues and verification trackers
status: active
supersedes: null
superseded_by: null
---

# Case branches and verification trackers are protected evidence

## Decision

The real-paper case branches `case/arxiv-2505-22954`, `case/arxiv-2604-01658`,
and `case/arxiv-2605-03042`, their corresponding case issues (#23, #24, #30),
and the standing verification trackers (#21, #31) are protected evidence. Do
not propose, plan, or perform their deletion. Do not include them in routine
cleanup reports or branch/worktree/PR deletion discussions. New `case/`
branches and their case issues receive the same protection unless a Human
decision records otherwise.

The branch `case-from-scratch-writing` is left as it is.

## Why

These branches and issues carry real-paper verification evidence, source/PDF
previews, Round 2 state, and long-running validation contracts. Treating them
as ordinary stale feature branches would erase evidence and break references
used by active tracker contracts.

## Apply

- Exclude these branches and Issues from every cleanup, close-out or
  stale-branch report; a worktree close-out never deletes a `case/` branch.
- The case branches keep their own copies of tools that the default branch has
  retired (for example the arXiv reconstruction evidence tool); do not port
  them back or delete them.
- This record governs this template repository only. A paper repository made
  from the template records its own protected branches and Issues in its own
  records and removes this one (it is registered `scope: template`).
