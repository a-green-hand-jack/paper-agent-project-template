---
name: paper-interfaces
date: 2026-10-20
source: Issue #156; the `% Interface:` markers in paper/macros.tex
scope: project
applies_to: paper/macros.tex and every paper/ source that calls an interface macro
status: active
supersedes: null
superseded_by: null
---

# Paper interface macros

## Decision

Paper-facing names, notation and reported values reach the text only through
the macros below. Each is defined in `paper/macros.tex` under an
`% Interface: <Name>` marker and has one row here. The control cue says who may
change it, with the meanings of `PAPER.md`: `locked` (only the Human),
`bounded` (an agent may change it within the stated limit), `free` and
`unresolved`.

| Interface | Meaning | Control | Source of the value |
| --- | --- | --- | --- |
| `\PaperTODO{...}` | A visible placeholder that keeps the paper compilable. | free; `make release-check` rejects any use. | authoring helper |
| `\PaperNote{...}` | A note between authors, shown only in the main build. | free; `make release-check` rejects any use. | authoring helper |
| `\PaperIdentity{...}` | Declares, in `paper/authors.tex`, a string the blind build must not contain; typesets nothing. | locked | authoring helper |
| `\PaperTitle{}` | The title of every build. | bounded wording; a change of positioning needs the Human. | `PAPER.md` |
| `\MethodName{}` | The approved name of the proposed method or system. | locked meaning; a rename needs a review of every consumer. | not set |
| `\CoreTerm{}` | The preferred term for the paper's central concept. | bounded wording; a new meaning needs the Human. | not set |
| `\StateSymbol{}` | The main state or representation symbol of the method. | bounded notation; a new symbol needs a collision and consumer review. | not set |
| `\MainResult{}` | The main result under the approved primary protocol. | bounded value; a change of metric, split, aggregation or checkpoint needs the Human. | not set |
| `\MainResultUncertainty{}` | The uncertainty paired with `\MainResult{}` under the same protocol. | bounded value; a change of uncertainty type or aggregation needs the Human. | not set |

## Why

A name, a symbol or a number written out in several sections drifts: one
section keeps the old method name, the abstract reports last week's number.
With one definition per interface, a change is one line in `paper/macros.tex`,
every build shows the same value, and the control cue makes the change
reviewable. The source column ties each reported value to the evidence behind
it (see [`../shared/results-through-interface-macros.md`](../shared/results-through-interface-macros.md)).

## Apply

- `make check` runs `.agents/scripts/check-paper-interfaces.py`. It fails when
  a marked interface has no definition or no row here, when an interface other
  than the three authoring helpers is used nowhere in `paper/`, when a macro
  without arguments is called without `{}` (TeX would swallow the following
  space), and when `paper/macros.tex` defines a command without a marker.
- Add an interface with its marker and definition in `paper/macros.tex`, a row
  here and at least one use. Remove one the paper does not need by deleting all
  three. `\PaperTODO`, `\PaperNote`, `\PaperIdentity` and `\PaperTitle` are
  required.
- For a reported value, the source names the experiment record in
  [`experiments.md`](experiments.md) and the asset id in `assets/MANIFEST.yaml`
  that produced it. Update the value, the source and the record together.
- Display helpers that are not paper-facing content (formatting commands, table
  layouts) belong in `paper/style/`, not here.
