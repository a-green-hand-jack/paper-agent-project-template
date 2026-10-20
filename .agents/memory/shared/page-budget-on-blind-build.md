---
name: page-budget-on-blind-build
date: 2026-10-20
source: Issue #156 §6; downstream paper repositories that measured the page budget on the wrong build and cut text against it
scope: shared
applies_to: paper repositories that submit to a venue with a main-text page limit
status: active
supersedes: null
superseded_by: null
---

# Measure the page budget on the anonymous build, and report an overage

## Decision

1. **The budget binds the build reviewers receive.** Main-text length is
   measured on the anonymous review build (`blind`), with the venue's line
   numbers and options, not on the working draft or the named copy.
2. **Main-text length is the page on which the counted text ends**, as the
   venue counts it (usually the page where the references begin). Notes that
   only the working draft shows do not count.
3. **Keep a margin** of `PAGE_MARGIN` below the limit, so that the camera-ready
   or a late edit does not push the paper over.
4. **Report an overage; never cut or move content silently.** Shortening,
   moving material to the appendix or filling the limit are author decisions.

## Why

The named copy and the anonymous build of one paper differed by about a third
of a page because line numbers and the review options change pagination; text
was cut against the wrong build. A `\FloatBarrier` before the bibliography cost
a page, and a float restricted to `[t]` was pushed past it; such effects show
only on the build that is measured. Silent cuts removed content that the
authors had not agreed to remove.

## Apply

Each project fills two parameters, `PAGE_BUDGET` in the root `Makefile` and
`PAGE_MARGIN` in the `## In this repository` section at the end of this record
(see `template-adoption` step 5):

- `PAGE_BUDGET`: the venue's main-text page limit (`PAGE_BUDGET ?=` in the
  `Makefile`, or `make check PAGE_BUDGET=9` for one run); `none` declares a
  release without a page limit, such as an arXiv version.
- `PAGE_MARGIN`: the margin kept below the limit, for example two or three
  lines.

Then:

1. Keep `\label{PaperMainTextEnd}` at the end of the last part the venue counts
   in `paper/main.tex`; `make check` reports the page of that label in the
   `blind` build against `PAGE_BUDGET`, and `make release-check` fails when the
   budget is missing or exceeded.
2. Check a venue's counting rule (what counts, which statements are exempt) in
   its dated knowledge record before relying on the number.
3. When a venue has a tighter sibling (for example 8 pages against 9), draft
   for the tighter limit first; record the plan in the paper's publication
   record.
