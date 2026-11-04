---
name: figure-router
description: >-
  Entry point for paper-figure work: route a request to create, fix, beautify,
  redraw or inspect a figure to the owning figure skill, and run the
  cross-checks between figure skills. Use it before loading an individual
  figure skill.
---

# Figure Router

Load this skill first for any figure request. It picks the owning skill, then
requires an independent cross-check, so no single pass ships a wrong or
illegible figure.

## Boundary

- A figure never misrepresents data. Never invent numbers, citations, labels or
  topology that the paper does not support.
- Quantitative figures are code-generated and reproducible from registered data
  (`assets/MANIFEST.yaml`); text-to-image output is never the source of a data
  panel.
- A text-to-image schematic is only a blueprint: the publication figure is
  redrawn in an editable form and checked by hand.
- `PAPER.md`, the repository's other contracts, its terminology and Human
  decisions take precedence over this router's defaults. A figure change that
  touches a `locked` item goes to `control-review` first.
- Space use and fit-height legibility are required. A figure fills its allotted
  area densely, without large empty margins or sparse panels, is placed at the
  full column or text width, and stays clearly legible (axes, ticks, legends,
  annotations, panel tags, labels) when the compiled page is viewed at
  fit-page-height. A sparse or fit-height-illegible figure is a defect.

## Route The Request

| Job | Owner skill |
| --- | --- |
| Choose the chart, diagnose a misleading chart, journal spec, publication checklist | `scipilot-figure-skill` |
| Produce or repair a data figure (matplotlib/seaborn), style preset, critique gate | `icarus-figures` |
| Method, architecture, pipeline or flowchart diagram in TikZ or draw.io | `thesis-figure-skill` |
| TikZ code correctness: clean compile, edit-safe idioms, `lint.sh` | `tikz-figure-code` |
| Plan a figure, decide data figure versus schematic, text-to-image drafts, storage | `scientific-figure-workflow` |
| Rebuild a raster figure or slide as an editable PowerPoint deck | `image-to-editable-ppt` |

A text-to-image draft goes through `scientific-figure-workflow`; this template
ships no image-generation skill. Once the Human selects a draft, its redraw
follows the diagram track below and is checked against the draft, the
manuscript and the paper's terminology.

## Cross-Checks

- **Data figure**: `scipilot-figure-skill` chooses the chart and the journal
  spec → `icarus-figures` plots it from registered data and passes
  `scripts/critique.py` with no FAIL → `scipilot-figure-skill` runs its
  publication checklist and its render-and-read visual check. A chart that
  fails a critique ships only after an explicit Human decision.
- **Diagram**: `thesis-figure-skill` composes from its snippets →
  `tikz-figure-code` hard constraints and `lint.sh` (compile, missing-character
  gate, overlap check) → an independent visual review → an SSIM or overlap
  comparison when a reference figure exists.
- A skill never both creates a figure and acts as its only certifier.

## Gate After The Build

Every track ends with the paper build, not with the figure file. Rebuild the
job in question (`make pdf`, `make blind` or `make submission`), render the
pages that carry the figure into `.project/build/inspect/<job>/`, and follow
`.agents/memory/shared/post-build-visual-inspection.md`: the figure is dense,
placed at full width, legible at fit-page-height, and its in-figure text is not
smaller than the caption text. Reject and revise a sparse or illegible figure.

## Conflict Rules

- Reproducibility wins: a data figure that cannot be regenerated from a script
  and registered data is not done.
- `icarus-figures` owns the plot and its gate; `scipilot-figure-skill` owns
  chart selection and publication checks; neither overrides the other's scope.
- `thesis-figure-skill` owns the editable diagram; a text-to-image draft only
  supplies a blueprint and never enters the paper as a raster.
- Preserve every supported claim and label. When a beautification would change
  meaning, stop and report instead of editing.

## Report

State which skill owned the figure, which cross-checks ran and their results,
the artifact paths (draft, editable source, file in `paper/figures/`, compiled
PDF), which pages were inspected (renders in `.project/build/inspect/<job>/`),
and any unresolved defect.
