---
name: claims-set-expected-results
date: 2026-11-14
source: RSI_light_paper `claims-set-expected-results` record and its `expected-results-for-claims` skill, used to write experiment-side Issues before any run
applies_to: paper repositories whose experiments run outside the paper repository
---

# Each claim sets its experiment and its expected result before the runs

## Decision

For every claim the paper makes, write down before running anything: the
experiment that would support it, the comparison or condition it needs, and the
result shape that would count as support or as refutation. That record belongs
to the claim, not to a results file. A claim whose experiment or expected result
is still open is marked planned everywhere it appears.

## Why

A claim written after the numbers exist turns whatever was measured into the
claim's evidence, and an experiment designed after the claim is drafted tests
the implementation rather than the idea. Writing the expected result first makes
a failed expectation visible instead of letting it be re-described as a result,
and it lets an experiment repository work from a fixed specification.

## Apply

- Keep the claim, its experiment and its expected result in one place in the
  paper's experiment record, with the experiment repository and Issue that run
  it.
- Register the result as planned in the asset manifest until a run produces it;
  a planned result is never written as an observation.
- When an expectation fails, record the failure next to the claim and decide
  with the Human whether the claim weakens; do not silently replace the
  expected result with the observed one.
- Reported numbers reach the text only through the interface macros.
