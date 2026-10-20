---
name: experiments
date: 2026-10-20
source: the template's experiment contract (EXPERIMENTS.md before v0.4.0), moved into a record by Issue #156
scope: project
applies_to: this paper's experiment evidence and the code repositories that produce it
status: active
supersedes: null
superseded_by: null
---

# Experiment evidence

## Decision

This record holds what the paper needs experiments to establish and which
choices need the Human. It is not a run ledger and not a second copy of raw
results: the code repositories own their runs, and every result the paper
reports is registered in `assets/MANIFEST.yaml` with its repository, commit,
run, checksum and regeneration command. Use the control cues of `PAPER.md`:
`locked`, `bounded`, `free` and `unresolved`.

| ID | Paper question | Supports | Manifest entries | State |
| --- | --- | --- | --- | --- |
| — | No paper-facing evidence question recorded yet | — | — | unresolved |

Add one section per real paper-facing question with the structure below, and
the next free ID. Do not assume that a question is a comparison, or that a
paper needs an ablation or a fixed number of experiments.

### E<N>: question

- Paper question: TODO
- Supports: the approved claim or decision, if any
- Reader question: TODO
- Maximum paper-facing interpretation: unresolved
- Code repository, commit and runs: the manifest ids that hold them
- Locked conditions (an agent must not change them silently): dataset and
  split, primary metric, baselines needed for a fair comparison, checkpoint
  selection, evaluation protocol, exclusions that change the conclusion. TODO
- Bounded adjustments (with their range): seeds, secondary metrics, search
  budget, plot layout, order of the analyses. TODO
- Free: plotting and table formatting, file organization, wording within the
  approved interpretation.
- Unresolved: the statistical summary; whether the result supports "improves",
  "consistently improves" or a more careful statement. TODO

## Why

The Human must understand the configuration and interpretation that a claim
rests on, without searching the code repositories. Keeping the question, its
conditions and its interpretation boundary here, and the provenance of each
number in the manifest, separates what the paper may say from where the
numbers come from.

## Apply

- Prepare context and ask the Human before changing a locked condition,
  removing an agreed baseline, changing the primary metric or split,
  interpreting an observational result causally, hiding a negative or
  inconclusive result that constrains a core claim, or weakening, strengthening
  or replacing a claim this evidence supports.
- For each reported result, state in plain language what was measured, under
  which conditions, what the aggregation or uncertainty means, what it can and
  cannot support, and what would make the interpretation stale.
- A number enters the text only through an interface macro whose row in
  [`paper-interfaces.md`](paper-interfaces.md) names its manifest entry
  ([`../shared/results-through-interface-macros.md`](../shared/results-through-interface-macros.md)).
  A planned result stays planned.
