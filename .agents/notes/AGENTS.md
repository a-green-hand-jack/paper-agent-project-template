# Notes: work in progress

This root holds material that is being worked on: plans, figure briefs and
decks, literature reading, experiment design drafts, revision reports. It is
tracked, and it is not guidance: a conclusion that others must follow belongs in
`memory/` (a decision with its reason) or `knowledge/` (a sourced fact with a
refresh date), and a repeatable procedure belongs in `skills/`.

## Rules

- One directory per topic (`figures/`, `literature/`, `reports/`, ...); a file
  that outlives its topic is distilled and deleted, not archived here.
- Keep figures' editable sources together: one deck per paper under `figures/`,
  one slide per figure, the export script in `scripts/project/`.
- Never put build output, logs, renders or a downloaded archive here; those go
  to the ignored `.project/` tree.
- Write the date in the file name for dated material (`plan-2026-11-14.md`),
  never a version number.
- Nothing here enters `paper/` and nothing here is copied to Overleaf.

## In this repository

- The paper reads nothing from this directory: `paper/` builds on its own.
- A figure deck under `figures/` is the editable source for the conceptual
  figures of `paper/`; only the exported asset enters `paper/`
  (`.agents/memory/shared/paper-figures/figure-deck-and-export.md`).
