---
name: writing-reference-finder
description: Find, verify and record writing exemplars for the current paper, such as recent award-winning or well-written papers to learn structure and presentation from; exemplars are never manuscript citations.
---

# Writing Reference Finder

Find papers to learn writing from, not papers to cite. An exemplar informs
section architecture, claim discipline and evidence presentation. It never
adds an entry to `paper/refs.bib` and never supports a scientific claim.

## Workflow

1. **Name the need.** Ask only when it is unclear what the exemplar should
   teach: introduction framing, formal setup, method exposition, experiments,
   limitations, related-work positioning, or the architecture of a whole
   paper.
2. **Load the paper's context.** Read `PAPER.md` for the topic, the
   contribution and the claim boundaries and, when a section is the target,
   its file under `paper/sections/`. Take topic keywords from `PAPER.md`.
   Never upload unpublished manuscript text to an external service.
3. **Search official sources first**, following
   `references/search-playbook.md`: venue award pages, then official paper
   pages, then arXiv source bundles.
4. **Screen for writing fit** (playbook, section 5). A paper can be
   scientifically relevant and still a poor model for writing.
5. **Verify provenance.** Keep the award page URL, the official paper page and
   the identifier (OpenReview, ACL Anthology, PMLR, arXiv). Never call a paper
   a best, outstanding or oral paper unless an official venue page says so,
   and record the date you checked that page.
6. **Learn structure, not geometry.** Study an exemplar's moves, order and
   evidence presentation. Never copy its spacing, margin or float tricks into
   `paper/`; layout follows the venue's official kit
   (`.agents/memory/shared/official-venue-kit-unmodified.md`).
7. **Report the results as writing references** with the candidate cards and
   the output contract of the playbook (sections 7 and 8), labelled as
   auxiliary.

## Storage

- Downloads (PDFs, arXiv source bundles) and working cards go under
  `.project/artifacts/writing-exemplars/<topic-or-cohort>/`. They are not
  committed: the papers are third-party copyrighted material.
- A card the Human wants to keep with the repository becomes a dated, sourced
  knowledge record under `.agents/knowledge/project/`, with the front matter
  of `.agents/knowledge/ENTRY_TEMPLATE.md`; the award label and its source are
  facts that can change.
- Nothing goes under `paper/`. `.agents/references/ledger.json` changes only
  when `citation-support-review` decides that a manuscript claim cites the
  paper.

## Boundaries

- Prefer official conference, OpenReview, ACL Anthology, arXiv, ACM, IEEE or
  publisher pages; blogs and curated lists are leads to verify, not sources.
- An empty search is not evidence that no exemplar exists.
- Use a paid or credentialed discovery service only with permission for the
  current task and under the project record that governs it (billing, key
  handling); never run a command that prints a key.
