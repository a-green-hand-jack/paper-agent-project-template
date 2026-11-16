---
name: experiments-argue-for-claims
date: 2026-11-14
source: RSI_light_paper `experiments-argue-for-claims` record, written while restructuring its Experiments section; Issue #261, a paper whose author keeps claims out of the evaluation text
applies_to: paper repositories that report several claims in one evaluation section
---

# Experiments argue for claims, not archive results

## Decision

The evaluation section is organised claim by claim. Each subsection carries the
evidence for one claim: the one table or the one figure (or the two) that holds
it, and the one conclusion the reader should draw. A measurement that supports
no claim either moves to an appendix as support material or is dropped.

Whether a subsection names the claim it supports is the author's choice,
`CLAIM_NAMING`: `named` (the subsection opens with the claim) or `implicit`
(the subsection states what was done, how and what resulted, and the claims
stay in the introduction for the reader to match).

## Why

A results section that walks through every run makes the reader do the
argument: the ordering follows the implementation rather than the claims, and
an inconclusive run looks as important as a decisive one. One claim, one
exhibit, one conclusion keeps the evidence traceable and makes a missing claim
visible as a gap in the section. Naming the claim makes the mapping explicit;
some authors find that it reads as if the claim were already granted, and
prefer the reader to make the match.

## Apply

Each project fills one parameter in the `## In this repository` section at the
end of this record (see `template-adoption` step 5):

- `CLAIM_NAMING`: `named` or `implicit`. Without a value, `named`.

Then:

- Order the subsections by the claims in the introduction, one claim each.
- With `named`, open each subsection with the claim and close it with what the
  exhibit shows. With `implicit`, write the setup and the result as facts and
  never write that an experiment tests or supports a claim; the order of the
  subsections still follows the claims.
- Do not let a paragraph describe numbers without saying what they show.
- Keep one exhibit per claim where possible; if two are needed, say what each
  adds.
- Keep negative or inconclusive results visible where they constrain a claim.
- Register every exhibit's data through the asset manifest and the interface
  macros, so a number in the text is traceable to the run.
