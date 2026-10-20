---
name: brief
date: 2026-10-20
source: the template's starter brief (BRIEF.md before v0.4.0), moved into a record by Issue #156
scope: project
applies_to: this paper
status: active
supersedes: null
superseded_by: null
---

# Paper brief

## Decision

This record holds the Human-authored brief the paper starts from. A brief
written in a separate brief repository is ingested here with
`paper-brief-ingest`, which also copies its decided fields into `PAPER.md`; a
brief can also be written here directly. Fill only what is decided: a field left
empty or `TODO` stays `unresolved` in `PAPER.md`, and the agent never invents
one. Mark as locked only the high-impact commitments that must not change
silently.

## Why

The brief is the Human's input contract for the paper. Keeping it as a record
shows where each contract item came from and keeps the inventory of supplied
materials.

## Apply

The brief stays authoritative for evidence, delivery, authors, constraints and
the first deliverable until their owner workflows update
`.agents/memory/project/experiments.md`, `publication.md` and
`paper/authors.tex`. Change it only with the Human, then ingest it again.

## Paper identity

- Working title: TODO
- Target venue: unresolved (verify current official rules before submission work)
- Paper type: unresolved
- Intended readers: TODO
- One-sentence positioning: TODO

## What readers should believe

### Central thesis

TODO: the single most important conclusion the paper wants readers to accept.

### Contributions

- TODO: one entry per defensible contribution (central / supporting / optional)

## Operating mode

- Mode: unresolved (`collaborative` or `autonomous`)
- Approval boundary: in autonomous mode the agent drafts, self-reviews,
  polishes and builds without step-by-step confirmation; it stops for Human
  review before changing a locked item, approving a release or the final
  submission. In collaborative mode the Human stays in the loop for each
  substantive step.

## Evidence and materials

Inventory what the Human supplies; keep it concrete (repositories, commits,
runs, URLs, or `none yet`):

- Code / data / results: TODO
- Figures / tables: TODO
- Prior draft or notes: TODO
- References or bibliography: TODO
- Experiment questions the paper must answer: TODO

## What must not change silently

- TODO: locked claims, comparisons, limitations or interface meaning

## What may evolve

- TODO: bounded areas where the agent may work without asking again

## Target and delivery

- Venue / year / track and deadline: unresolved
- Builds needed: unresolved (main, submission and blind are built from one source)
- Release authority: Human (approves each release tag and the final submission)

## Authors and identity

- Author list: unresolved
- Anonymity / disclosure constraints: unresolved

## Constraints

- Language and length limits: TODO
- Compute / data limits: TODO
- Style examples: TODO

## First deliverable

- TODO: idea clarification, evidence plan, outline or a named section draft

## Template usage note

Write this paper in a repository made from the `paper-agent-project-template`
GitHub template. Ingest this brief with `paper-brief-ingest`
(`python3 .agents/skills/shared/paper-brief-ingest/scripts/paper-brief.py ingest --brief <path>`),
then draft under the declared operating mode; `README.md` and `DEV.md` of the
paper repository describe the workflow.
