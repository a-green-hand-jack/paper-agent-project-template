---
name: section-writing
description: Use when drafting or substantially revising a specific paper section from the current paper contracts and available evidence.
---

# Section Writing

## Trigger

Use when drafting or substantially revising a title, abstract, introduction,
related-work section, method, experiment section, limitation section,
conclusion, appendix, caption or other named paper section.

Do not use this skill for a manuscript-wide review after a version is complete
(`manuscript-consistency-review`).

## Minimum context

- the paper identity, thesis, contributions, story, section responsibility and
  writing choices relevant to the active section in `PAPER.md`;
- the active section and only the neighboring text needed for continuity;
- the matching surface in [`references/paper-writing-guide.md`](references/paper-writing-guide.md);
- `.agents/memory/project/experiments.md` only for experiment, result,
  evidence or interpretation text;
- `.agents/memory/project/paper-interfaces.md` only for recurring terminology,
  notation, claims, results, figures, tables or macros;
- `.agents/memory/shared/reference-integrity.md` and the relevant records in
  `.agents/references/ledger.json` only when citations or external claim
  support are involved.

Do not load the complete manuscript, all references, release material or venue
knowledge unless the active section actually requires them.

## Procedure

1. Identify the active section and its reader task from `PAPER.md`.
2. State the one point the reader should retain and the inputs that support it.
3. Select only the applicable section guidance and rhetorical moves from
   `references/paper-writing-guide.md`.
4. Separate scientific content from presentation. Preserve locked and bounded
   meaning while handling free wording directly.
5. If the prompt introduces, fabricates, removes or materially changes a
   citation or claim-support request, inspect the reference-integrity record
   and the relevant ledger records before drafting; do not invent support.
6. When the draft adds or checks a citation, run the Draft profile of
   `citation-support-review`: inventory the active occurrence, resolve or
   discover the source, retrieve a bounded passage set, compare once in the
   current writing context, and record a passing result as `provisional`.
   Never insert a citation from title relevance or metadata existence alone,
   and never upgrade provisional support to `human-confirmed`.
7. Draft from available claims, evidence, results, interfaces and references.
   A reported number enters the text only through its interface macro in
   `paper/macros.tex` (`.agents/memory/shared/results-through-interface-macros.md`);
   a planned or expected result is never written as an observation. Keep
   missing material visible with `\PaperTODO{}` rather than filling it
   plausibly; an author note for co-authors goes in `\PaperNote{}`, which only
   the `main` build shows.
8. Check the active section locally for defined terms, claim strength,
   citation placement, figure and table references, and continuity with
   immediate neighbors.
9. Build with `make pdf` and fix the undefined references, citations or
   missing files the draft introduced; run `make check` before handing the
   section over.
10. Report any unresolved input or proposed wording that would change a claim,
    experiment interpretation, consequential limitation or interface meaning.

## Language passes and exemplars

After the content is drafted, `writing-router` can run one or more language
passes (grammar, word usage, academic voice, AI-tone cleanup, proofreading)
when the Human asks for them or `PAPER.md` writing style calls for them. A
language pass changes wording only; it never adds, removes, weakens or
strengthens a claim, number, citation or result, and its edits are reported
separately from the draft.

Use writing exemplars (`writing-reference-finder`) only for transferable
rhetorical moves. Never copy wording, claims, examples, technical content or
distinctive phrasing from a reference paper.

## Drafting boundary

Do not invoke a reviewer persona, launch parallel reviewer passes, audit the
complete manuscript or emit a manuscript review report while drafting. A local
coherence check is part of writing; a version-level consistency review is a
separate Human-requested task. The Draft citation-support flow stays bounded to
the active claim, uses at most three passages and one semantic comparison, and
never launches a reviewer subagent or persona.

## Human decision

The Human decides the central story, contribution and claim identity,
important result interpretation, and any section responsibility that changes
what the paper promises. The Agent may draft and revise inside the current
boundary.
