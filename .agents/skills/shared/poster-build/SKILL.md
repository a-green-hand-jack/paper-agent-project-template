---
name: poster-build
description: Build, refresh or redesign the conference poster as an optional second product tree `poster/` made from the paper, following a reference poster's layout, or bring the poster in line after the paper's results change.
---

# Poster Build

A poster is an optional second product tree, `poster/`, beside `paper/`. Like
`paper/` it is self-contained (it compiles with no file outside `poster/`),
it builds into `.project/build/poster/`, and it has its own Overleaf project,
never the paper's. Its content comes only from the paper.

## Minimum context

- `PAPER.md`: locked and bounded items bind the poster too;
- `.agents/memory/project/publication.md` for the venue and the poster's
  record, and the venue's poster facts in `.agents/knowledge/shared/` (for
  example `venue-neurips-2026-poster.md`), rechecked on the official page
  before a print is ordered;
- the reference poster's source and render;
- the paper sections that supply content: abstract, introduction, method,
  experiments, conclusion and limitations.

## Layout of `poster/`

- `poster.tex` and the class or style files it needs;
- `figures/`: byte-identical copies of the paper figures the poster uses;
- `macros.tex`: a byte-identical copy of `paper/macros.tex`, so names and
  reported numbers come through the same interface macros;
- `Makefile`: builds `poster.pdf` into `$(BUILD_DIR)`, which defaults to
  `../.project/build/poster` when the worktree marker `../.project/home`
  exists and to `build/` otherwise, the same rule as `paper/Makefile`;
- `README.md`: the file table, the content sources and the verification
  record.

`tikzposter` and `beamerposter` are part of TeX Live. `baposter` is not, and
its class file carries no licence statement: take `baposter.cls` from the
reference poster's source package or from its author's distribution, note
the source in `poster/README.md`, and ask the Human before committing a file
without a licence statement.

## Procedure

### 1. Identify the reference

- Stage reference packages under `.project/artifacts/poster-references/`.
  Open each archive before trusting its name; only packages with both source
  and render count.
- Read the reference `.tex` for class options, colours, box options and the
  header layout, and its render for density and reading order.

### 2. Map paper content to boxes

- Keep the reference's visual language: class options, colours, header
  shape, table style, callout boxes. Take content only from the paper.
- Fix the reading path across the columns; the method box may span columns.
- Copy figures from `paper/figures/` byte for byte and check each with `cmp`.
  Never crop or edit a figure the paper treats as locked.
- Transcribe tables from the `.tex` sources under `paper/`, not from the PDF.
  Keep bold or underline marks only when the full set of rows is shown; on a
  subset they can mislead.
- The title comes from `\PaperTitle{}`; authors, marks and affiliations come
  from `paper/authors.tex`.
- Numbers come through the interface macros of `poster/macros.tex`, called
  with braces as in `\MainResult{}`, never as typed digits.

### 3. Build and fit

Build with the output redirected to a log, then render the whole page after
every change (`v1`, `v2`, ...) and look at it:

```bash
mkdir -p .project/build/logs .project/build/inspect/poster
make -C poster > .project/build/logs/poster.log 2>&1
pdftoppm -png -r 40 -singlefile .project/build/poster/poster.pdf .project/build/inspect/poster/v1
```

To fix overflow, in this order: tighten the wording, fold a small box into a
neighbour, rebalance the figure and text of the spanning box, and change the
font scale last.

### 4. Verify

- **Margins.** The lowest text must sit above the page height minus the
  class margin; take both from `pdfinfo` and the class options. Find the
  lowest word with
  `pdftotext -bbox .project/build/poster/poster.pdf - | grep '<word' | awk -F'"' '{print $8}' | sort -n | tail -1`,
  and look at the header area in a close-up crop as well.
- **Numbers.** Every number in the poster body occurs in the paper sources
  (layout parameters aside), every transcribed table row matches its paper row
  cell by cell, including deviations, and `cmp poster/macros.tex paper/macros.tex`
  passes.
- **Claim wording.** Re-read every sentence against the paper. Compression
  must not turn "outperforms every baseline of one kind" into "best",
  "similar" into "the same", or a bounded claim into an unbounded one, and
  every caveat the paper attaches to a locked claim must survive.
- **Build health.** No overfull or underfull boxes, all fonts embedded
  (`pdffonts`), exactly one page at the intended size (`pdfinfo`), and a clean
  `git diff --check`.

### 5. Clean up and record

- Remove from `poster/` every file the layout no longer uses; the tree holds
  only what compiles.
- Update `poster/README.md`: files, sources and the verification record.
- Record the Human's layout and policy choices through `decision-packet`.

### 6. Sync, only when the Human asks

- Commit and push through the usual Issue and PR flow.
- Overleaf sync requests belong to `publication-planning`. The poster has its
  own Overleaf project on a second remote, never the paper's:

  ```bash
  bash .agents/scripts/overleaf-sync.sh status --remote overleaf-poster --tree poster
  bash .agents/scripts/overleaf-sync.sh push --remote overleaf-poster --tree poster
  ```

  Never push over Overleaf edits that `poster/` lacks: import them first with
  `pull` and the same options. After the push the Overleaf tree must equal
  `HEAD:poster`. `.agents/memory/shared/overleaf-paper-tree-only.md` gives the
  rules.

## baposter notes

- `fontscale` is the ratio of the base page to the final page: the printed
  font size is the base size divided by `fontscale`. With a 10 pt base,
  `\normalsize` prints at 40 pt at 0.25 and at about 33 pt at 0.3.
  Figures scale with the column, so smaller text does not shorten a box whose
  height a figure sets.
- Text that TikZ draws inside header boxes (QR labels, wordmarks) is silently
  set in `nullfont` unless the box body is wrapped in `pgfinterruptpicture`;
  the symptom is `Missing character ... in font nullfont`.
- After that fix, the remaining `nullfont` messages for `;` characters, three
  per box, come from the class and are harmless.
- `above=bottom` on the last box of each column makes the columns end flush.
  `textborder=faded` hides spare space at the foot of a box, but not overflow.

## Human decisions

The Human chooses the reference poster, the page size and orientation within
the venue's limits, departures from the paper's figure policy, institutional
logos, and every push to GitHub or Overleaf.
