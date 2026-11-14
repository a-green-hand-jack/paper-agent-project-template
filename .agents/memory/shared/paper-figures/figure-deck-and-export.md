---
name: figure-deck-and-export
date: 2026-11-14
source: RSI_light_paper `figures-drawn-in-powerpoint` record and ResearchWorld_paper `figure-generation` record; both draw conceptual figures as slides and export them with a script
applies_to: paper repositories whose conceptual figures are drawn in a presentation tool
---

# Draw conceptual figures as slides and export them with a script

## Decision

The editable source of a conceptual figure is one deck per paper, kept under
`.agents/notes/figures/`, with one slide per figure. A project script cuts each
slide to its ink and writes the PDF into `paper/`. The deck itself never enters
`paper/` or the built paper; only the exported asset does.

## Why

A conceptual figure is edited many times, and a raster screenshot cannot be
edited again. One deck keeps every figure in the same visual language, makes the
ordering of the panels visible, and leaves the export reproducible from a
recorded command. Judging a slide inside the presentation tool hides what
happens at print size and in the other renderer.

## Apply

- Keep the brief, the per-figure description and the deck together under
  `.agents/notes/figures/`, with the slide-to-figure map inside the export
  script.
- Export with the script, then judge the figure at its final size in the built
  page, not in the editor; a renderer may shrink subscripts or enlarge
  arrowheads.
- Keep the exported asset in `paper/` with the caption and label in the same
  float file, named after the section it serves.
- When a figure carries a number, register its data through the asset manifest
  as a data figure and generate it from a script instead.
