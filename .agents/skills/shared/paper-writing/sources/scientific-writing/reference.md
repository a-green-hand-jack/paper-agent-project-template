---
name: scientific-writing
description: Plan, draft, restructure, diagnose, and revise scientific manuscripts. Use for paper structure, titles, abstracts, introductions, results, discussions, figures, manuscript logic, claim strength, and revision. Do not use primarily for literature searching or peer-review reports.
---

# Scientific Writing

Treat a paper as a scientific argument designed for a reader, not as a chronological record of the project.

## Core behavior

- Identify the paper's central contribution before polishing prose.
- Make every major section serve that contribution.
- Separate data, inference, interpretation, and speculation.
- Keep claims proportional to evidence.
- Fix structural problems before sentence-level style.
- Write for the intended reader, not for the author's memory of the project.

## Read only what the task needs

- Whole-paper logic or restructuring → [references/paper-structure.md](references/paper-structure.md)
- Abstract → [references/abstract.md](references/abstract.md)
- Introduction → [references/introduction.md](references/introduction.md)
- Methods → [references/methods.md](references/methods.md)
- Results → [references/results.md](references/results.md)
- Discussion → [references/discussion.md](references/discussion.md)
- Figures and figure legends → [references/figures.md](references/figures.md)
- Revision, clarity problems, or pre-submission diagnosis → [references/revision.md](references/revision.md)

Do not read every reference by default.

## In this repository

The text above is the upstream skill, unchanged; see `PROVENANCE.md` and the
attribution in `SOURCES.md`, which travels with the package.

- Role: a structure reference. `section-writing` owns drafting and
  substantive revision of `paper/`, `style-alignment` owns positioning and
  the writing policy, and `writing-router` sends structure questions here.
  This skill diagnoses and advises; it changes `paper/` only inside a task one
  of those owners runs.
- "Keep claims proportional to evidence" is settled by the cues in `PAPER.md`
  and the evidence in `.agents/memory/project/experiments.md`: a structural
  change never strengthens a `locked` or `bounded` claim, and a planned result
  is never written as an observation.
- `references/figures.md` covers what a figure must show; making or redrawing
  a figure goes to `figure-router`.
