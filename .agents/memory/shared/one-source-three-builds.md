---
name: one-source-three-builds
date: 2026-10-20
source: Issue #156 §2 and §7; downstream paper repositories that retired a copied-variant overlay for macro-switched builds
scope: shared
applies_to: paper repositories that build more than one publication form (working draft, named copy, anonymous review copy) from one LaTeX source
status: active
supersedes: null
superseded_by: null
---

# One source, three builds, in a fixed order

## Decision

1. **One source.** `paper/main.tex` and the files it reads are the only
   authored paper. No publication form copies a section, a figure or a macro
   file.
2. **Three builds in a fixed order, each removing a layer from the one
   before:**
   1. `main`: the working draft, with authors, acknowledgements and author
      notes.
   2. `submission`: `main` without author notes or placeholders; the named copy
      for arXiv, a camera-ready or a venue that is not anonymous.
   3. `blind`: `submission` without author identity and acknowledgements; the
      anonymous copy reviewers receive.

   A later form only removes. It never adds text, changes a claim or swaps a
   figure.
3. **A switch selects the form.** One entry file per form (`blind.tex`,
   `submission.tex`) defines a switch and reads `main.tex`, so every form builds
   with the same command and Overleaf can select it as the main document.
   Author identity lives in one file (`authors.tex`) that only the named forms
   read.
4. **Notes vanish from the later forms.** Author notes compile only in `main`
   and never count toward the page budget. A citation or a label that appears
   only inside a note disappears from `submission` and `blind`: cite it in the
   text as well.

## Why

Copied variants drift: a fix in one copy does not reach the others, and an
overlay allowed to change presentation hooks can also change content without
review. Downstream papers retired a four-variant overlay for this switch and
kept it. Building by subtraction keeps the review of a later form small: the
difference between two forms is the removed layers and nothing else. Notes
behind the same switch cannot leak into a submission, and a reference carried
only by a note has silently vanished from a submission build before.

## Apply

- `make pdf`, `make submission` and `make blind` build the three forms into
  `.project/build/`. `make check` builds `main` and `blind`;
  `make release-check` searches `blind` for identity and `submission` for notes
  and placeholders.
- Put what the anonymous form must not show behind `\ifPaperBlind`, and a note
  in `\PaperNote{...}`. Never edit a section differently per form.
- A further form (for example a camera-ready with a venue option) is another
  entry file that sets switches; record it in the paper's publication record.
- A public preprint is the `submission` form: do not re-anonymize it. A venue
  that later needs an anonymous version receives `blind`.
