---
name: paper-brief-ingest
description: Use when a Human-provided paper brief starts a collaborative or autonomous paper session, to validate the brief and fill the decided PAPER.md fields from it in a paper repository made from this template.
---

# Paper Brief Ingest

Own the transition from a Human-provided brief to a paper repository whose
contracts are filled. This is the entry point for both collaborative and
autonomous paper sessions.

## Trigger

- The Human supplies a brief: a brief file, a brief repository, or the starter
  record `.agents/memory/project/brief.md` filled in place.
- The Human asks to start an autonomous or brief-driven paper session.

Do not use for ordinary drafting, and never for writing paper content into the
template repository.

## Minimum context

- the brief and any materials it links;
- the repository role from `paper-orientation`;
- `PAPER.md`, and `.agents/memory/project/experiments.md` and `publication.md`
  when the brief touches evidence or delivery.

## Procedure

1. Confirm the repository role with `paper-orientation`. In the template
   repository itself, first make the paper repository as `README.md`
   describes; never draft a real paper in the template.
2. Locate the brief: a brief file; a brief repository directory, which holds
   `BRIEF.md` at its root or in `brief/`; or the starter record filled in place.
   Clone a remote brief repository locally first with the normal Git workflow.
3. Validate the brief before writing anything:

   ```bash
   python3 .agents/skills/shared/paper-brief-ingest/scripts/paper-brief.py validate --brief <path>
   ```

4. From the root of the paper repository, ingest it:

   ```bash
   python3 .agents/skills/shared/paper-brief-ingest/scripts/paper-brief.py ingest --brief <path> [--commit]
   ```

   The tool writes the brief to the record `.agents/memory/project/brief.md`
   and fills only decided `PAPER.md` fields (identity, thesis, contributions,
   operating mode, locked and evolving items, unresolved queue, style).
   Missing, empty and placeholder fields stay `unresolved`, and a decided field
   with no recognized target stops the ingest before anything is written. It
   refuses the template repository and symlinked destinations. `--commit`
   needs a clean worktree and commits only the record and `PAPER.md`; commit a
   brief filled in place before using it.
5. The brief record stays authoritative for evidence, delivery, authors,
   constraints and the first deliverable until their owner workflows update
   `.agents/memory/project/experiments.md`, `publication.md`
   (`publication-planning`) and `paper/authors.tex`.
6. Confirm the declared operating mode in `PAPER.md` (`collaborative` or
   `autonomous`) and its approval boundary. Never widen the boundary silently.
7. Build and check:

   ```bash
   make pdf
   make check
   ```

8. Hand off:
   - collaborative mode → ordinary `section-writing` on Human request;
   - autonomous mode → proceed through drafting, self-review, polish and
     builds on your own; prepare idea shaping and evidence analysis as
     proposals only; stop for Human approval before changing a locked item,
     approving a release or final submission.

## Contract declaration

When the brief leaves a field empty or `TODO`, keep the corresponding contract
item `unresolved` instead of inventing a value, and report it as left open.

## Boundaries

- Never invent a title, claim, result, citation, venue, author, approval or
  release state from a missing brief field.
- Never write a real paper into the template repository.
- Do not degrade an accepted brief's decided fields to `unresolved`.
- The brief is Human-authored input and stays `unresolved`-honest; do not
  silently change its meaning during ingestion.
