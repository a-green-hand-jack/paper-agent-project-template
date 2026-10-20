---
name: paper-orientation
description: Use at the start of a session or when paper context is unclear, to recover the minimum context for the task without loading the whole repository.
---

# Paper Orientation

Recover the minimum context the current task needs; do not load the entire
repository.

## Repository role

Before choosing a workflow, inspect the repository root, branch, worktree
status, origin and the template record:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git remote get-url origin
sed -n '/^template:/,/^[^[:space:]]/p' .agents/content-registry.yaml
```

Classify the repository before editing:

- **template repository**: origin is the registry's `template.repository`
  (the template itself, which also records `template.upstream`). Do not write
  paper content here; template work follows `DEV.md`. A new paper is a new
  repository made from the template as `README.md` describes, or starts from a
  brief through `paper-brief-ingest`.
- **paper repository**: the registry's `template` names the paper template and
  tag it adopted, origin is a different repository, and there is no `upstream`
  block. Use the ordinary paper workflows; template releases arrive through
  `template-upgrade`, and template defects go back through `template-feedback`.
- **existing paper repository without a template record** (no registry, or a
  registry without `template:`): map it with `template-adoption`; do not run
  ordinary paper workflows that assume the template layout until the map is
  approved.

If the origin, the registry and the repository contents disagree, stop and
report the exact conflict. Never infer the role from the directory name, the
branch name or copied template files.

## First-session packet

For a new paper, collect only what is needed to begin. The Human's packet is:

```text
Research seed: problem, setting, and proposed idea or insight
Evidence available: code, data, results, figures, prior draft, references, or "none yet"
Target: venue/year/track and deadline, or "unresolved"
Authors and identity: author list plus anonymity or disclosure constraints
First deliverable: idea clarification, evidence plan, outline, or a named section draft
Constraints: language, length, compute/data limits, style examples, and locked decisions
Operating mode: collaborative or autonomous
```

When the Human provides a brief (a brief file, a brief repository or the filled
starter record `.agents/memory/project/brief.md`), it is this packet in
structured form; use `paper-brief-ingest` instead of transcribing it.

With no evidence, limit work to clarification, an evidence plan or an outline.
A section draft requires supplied or Human-approved claims and evidence for
that section. Never invent a method, result, contribution, citation,
authorship, venue choice or approval state.

## Reading order

1. Read `PAPER.md`.
2. Read `.agents/memory/project/experiments.md` only when the task touches
   experiments, evidence, result interpretation or claim support.
3. Read `.agents/memory/project/paper-interfaces.md` and `paper/macros.tex`
   only when the task changes recurring identity, terminology, notation,
   results, claims, figures, tables or macros.
4. Read `.agents/memory/project/publication.md` only when the task touches the
   venue, page budget, the `main` / `submission` / `blind` builds, Overleaf or a
   release; read a venue entry under `.agents/knowledge/shared/` only for an
   active venue.
5. Read only the decision records in `.agents/memory/project/` that the task
   touches (the index is `.agents/memory/project/AGENTS.md`).
6. Inspect the active paper section and the current Git diff.
7. Load one owner skill from the routing in `AGENTS.md`. Language and figure
   passes are loaded through `writing-router` or `figure-router` only when the
   owner skill or the Human asks for them; never load the whole family.

## Overleaf before the first edit

If the paper has an Overleaf remote, check it before editing paper sources:

```bash
bash .agents/scripts/overleaf-sync.sh status
```

When Overleaf holds edits that this branch does not have, import them first
(`publication-planning`, `.agents/memory/shared/sync-overleaf-before-editing.md`)
instead of writing on top of a stale tree.

## Before a high-impact edit

Identify:

- the affected claim, story, experiment, style choice, interface or build;
- whether it is locked, bounded, free or unresolved;
- whether the change is low-risk and easy to reverse;
- whether scientific meaning, claim strength, experiment fairness, interface
  meaning or consistency between the builds may change;
- whether a Human decision is needed before editing.

The control words are collaboration cues, not a rigid state machine.

## Unresolved work

- Prefer low-risk and reversible progress.
- Keep uncertainty visible.
- Offer concrete alternatives when useful.
- Ask before a high-impact or hard-to-reverse choice.
- Never record an Agent preference as approved Human intent.

## Human decision requests

Retrieve context first. A useful request contains the current state, why a
decision is needed, relevant constraints, concrete options, affected surfaces,
and the Agent recommendation with tradeoffs (`decision-packet`). The Human
should answer a focused question rather than search the repository.

## Context hygiene

- Current Human contracts take priority over generic knowledge.
- Load venue knowledge only for an active venue task.
- Do not read every historical file for completeness.
- Summarize applicable guidance instead of copying large documents into
  working context.
- Surface conflicting sources rather than silently choosing one.

## Handoff

Report the changes, high-impact semantic effects, decisions made or still
open, affected interfaces, builds or experiment records, the checks run
(`make check` and any build), and the next Human decision when one remains.
