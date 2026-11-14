---
name: appendix-as-its-own-tree
date: 2026-11-14
source: ResearchWorld_paper's paper/appendix/ (one file per appendix, a-related-work … j-improvement) and its `paper-organization` record; the template's single sections/10_appendix.tex before #238
applies_to: paper repositories whose appendix is longer than a page
---

# The appendix is its own tree inside paper/

## Decision

Every appendix is a file in `paper/appendix/`, named `<letter>-<topic>.tex`, and
`paper/main.tex` inputs them after `\appendix` in the order the main text refers
to them. Appendix material never lives in `paper/sections/`, and `sections/`
holds only main-text sections in reading order.

## Why

An appendix grows independently of the main text and rarely in one piece:
proofs, protocols, implementation detail and task lists arrive from different
authors at different times. Mixing it into `sections/` renumbers the section
sequence whenever it changes, puts appendix diffs next to main-text diffs, and
turns one large file into the least reviewable file in the repository. A tree of
small files keeps each review local and makes a missing appendix visible as a
missing file rather than as a missing paragraph.

## Apply

- Name by letter and topic: `a-related-work.tex`, `b-protocol.tex`; the letter
  fixes the order, the topic says what it holds.
- Keep the main-text budget intact: `\label{PaperMainTextEnd}` stays before the
  bibliography, so a growing appendix never changes the measured main text.
- Move supporting detail out of a section into its appendix instead of deleting
  it, and point to it from the section that needs it.
- Give a float-heavy appendix its own `\FloatBarrier` where floats would
  otherwise drift past their text.
- An appendix is still part of the same source: all three builds carry it, and
  `paper/` stays self-contained.
