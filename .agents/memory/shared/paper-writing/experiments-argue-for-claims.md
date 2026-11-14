---
name: experiments-argue-for-claims
date: 2026-11-14
source: RSI_light_paper `experiments-argue-for-claims` record, written while restructuring its Experiments section
applies_to: paper repositories that report several claims in one evaluation section
---

# Experiments argue for claims, not archive results

## Decision

The evaluation section is organised claim by claim. Each subsection states the
claim it supports, shows the one table or the one figure (or the two) that
carries the evidence, and says what the reader should conclude. A measurement
that supports no claim either moves to an appendix as support material or is
dropped.

## Why

A results section that walks through every run makes the reader do the
argument: the ordering follows the implementation rather than the claims, and
an inconclusive run looks as important as a decisive one. One claim, one
exhibit, one conclusion keeps the evidence traceable and makes a missing claim
visible as a gap in the section.

## Apply

- Open each subsection with the claim and close it with what the exhibit shows;
  do not let a paragraph describe numbers without saying what they mean.
- Keep one exhibit per claim where possible; if two are needed, say what each
  adds.
- Keep negative or inconclusive results visible where they constrain a claim.
- Register every exhibit's data through the asset manifest and the interface
  macros, so a number in the text is traceable to the run.
