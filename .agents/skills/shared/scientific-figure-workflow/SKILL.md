---
name: scientific-figure-workflow
description: >-
  Plan, create, revise or evaluate a research-paper figure, from code-generated
  quantitative plots to text-to-image schematic drafts. Use it for figure
  workflow decisions (科研画图, paper plots, method overviews, schematics,
  figure-generation tools): how a figure is made, where its files go and when
  it is done.
---

# Scientific Figure Workflow

Own the figure-production workflow, not the scientific claim. Keep final paper
figures accurate, reproducible where they carry evidence, visually inspected
and editable enough for revision. `figure-router` routes figure work; this
skill sets the workflow, the storage and the quality gates.

## First Decision: Data Figure Or Schematic

Classify every requested figure before choosing tools.

1. **Quantitative, evidence-bearing figure**
   - Examples: benchmark bars, scaling curves, ablation plots, heatmaps,
     calibration curves, distribution plots, result tables rendered as figures.
   - Use Python or another reproducible plotting script.
   - Never use text-to-image output as the final evidence-bearing figure.

2. **Conceptual or schematic figure**
   - Examples: method overview, system pipeline, architecture diagram,
     workflow cartoon, visual metaphor, graphical abstract draft.
   - Text-to-image tools may be used for ideation or layout exploration.
   - The paper version is redrawn or cleaned into an editable vector form:
     TikZ, SVG or PDF from a vector editor, Mermaid or Graphviz, or other
     code-generated vector output.

When a figure mixes both, split the pipeline: code for the data panels, an
editable vector drawing for the schematic panels, assembled as one multi-panel
figure.

## Quantitative Figure Workflow

Use this for any figure that carries numeric evidence.

1. Identify the exact claim and evidence the figure supports, and its cue in
   `PAPER.md`.
2. Locate the data source: an entry in `assets/MANIFEST.yaml` (source
   repository, commit, run or config id, checksum, regeneration command), read
   through its `assets/<name>` link or a small committed data file. Never type
   numbers into a script.
3. Choose the plot family and reference style (`scipilot-figure-skill`).
4. Generate with a script, preferably Matplotlib or Seaborn with a publication
   style helper (`icarus-figures`).
5. Export vector-first (`.pdf`, `.svg`) plus a raster preview when useful.
6. Rebuild the paper and run the gate in
   `.agents/memory/shared/post-build-visual-inspection.md`.
7. Report the source data, script, output path and inspection result.

Candidate tools are listed in `references/github-candidates.md`. For default
paper plotting, prefer a small local script over a large new dependency unless
the task benefits from the dependency.

## Text-To-Image Schematic Workflow

Use text-to-image only as a draft or inspiration layer, unless the final figure
carries no evidence and has been checked by hand.

1. Write a prompt that names the scientific objects, arrows and labels, and the
   hallucinations to avoid.
2. Generate several drafts to explore layout and style, with a provider the
   Human has approved for this paper; an unpublished paper's content is
   confidential.
3. The Human and Agent take composition ideas from the drafts, not factual
   content.
4. Recreate the selected design in an editable medium (`thesis-figure-skill`
   with `tikz-figure-code`, or `image-to-editable-ppt` for an editable deck).
5. Replace generated text with real, editable labels.
6. Check every arrow, module, label and ordering against the manuscript.
7. Rebuild the paper and run the inspection gate.

Never let a raster-only generated image become the sole final source of a
claim-critical method or result figure.

## Tool Selection Heuristics

- Publication Matplotlib defaults: SciencePlots or a lightweight local style
  file.
- Common paper plot families with export discipline: evaluate `pubfig`.
- Visual references before coding: an AgentFigureGallery-style reference
  selection.
- Natural language to editable Matplotlib code: evaluate PlotCraft-like tools,
  but read and own the generated code.
- A schematic concept draft: text-to-image tools may help, but the final labels
  and structure are redrawn and checked.

## Quality Gates

A figure is not done until:

- the claim and the data match;
- fonts, line widths, marker sizes and colors are legible at final paper size;
- legends and labels do not crowd or mislead;
- the figure fills its allotted area densely, without large empty margins or
  sparse panels, and is placed at the full column or text width;
- in the compiled PDF at fit-page-height, the axes, ticks, legends,
  annotations, panel tags and labels are clearly readable, and in-figure text
  is not smaller than the caption text;
- colors stay readable in grayscale and for color-vision deficiency when
  relevant;
- the exported format suits LaTeX and Overleaf;
- the compiled pages pass `.agents/memory/shared/post-build-visual-inspection.md`;
- the source files and scripts are stored as the storage policy says.

## Storage Policy

- Figure scripts: in the code repository that produced the data, with its
  `assets/MANIFEST.yaml` entry, or next to their output in `paper/figures/`
  when they are tied to the manuscript.
- Final figure files that LaTeX includes: `paper/figures/`. The paper includes
  only exported files, so it compiles without `.agents/`.
- Scratch generations, prompt experiments, previews and rejected drafts:
  `.project/build/figures/<name>/`, never committed.
- Material worth keeping that cannot be rebuilt, such as selected text-to-image
  drafts or downloaded reference figures: `.project/artifacts/<topic>/`.
- Tool research notes: a dated record under `.agents/knowledge/`.

Do not add a new plotting framework to the repository just because it exists;
record why it is needed and keep the smallest reproducible workflow that
satisfies the figure task. Install figure tools into a project-local
environment, never globally.
