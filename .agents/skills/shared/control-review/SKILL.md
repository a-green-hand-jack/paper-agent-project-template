---
name: control-review
description: Use before changing a central claim, story choice, experiment condition, limitation, result interpretation, or stable paper interface.
---

# Control Review

## Trigger

Use before changing a central claim, story choice, experiment condition,
limitation, result interpretation or stable paper interface.

## Minimum context

- the relevant section of `PAPER.md`;
- `.agents/memory/project/experiments.md` only for experiment or result
  changes;
- `.agents/memory/project/paper-interfaces.md` only for recurring semantic
  interfaces;
- the active text and the decision record in `.agents/memory/project/` that
  currently governs it.

Do not load unrelated venue, release, history or reference-ledger material.

## Procedure

1. Identify what meaning could change.
2. Classify the current cue as locked, bounded, free or unresolved.
3. For free, make the low-risk edit and report it.
4. For bounded, confirm the written boundary and stop if the change exceeds it.
5. For locked, prepare a proposal rather than modifying the meaning.
6. For unresolved, prefer reversible progress; ask before a high-impact or
   hard-to-reverse choice.
7. List affected sections, experiments, interfaces and limitations, and the
   builds (`main`, `submission`, `blind`) that show them.
8. When independent semantic choices are present, use a separate Human
   approval gate for each and record each decision; approval of one choice does
   not approve another.

## Human decision

Request a Human decision when scientific meaning, claim strength, fairness,
claim degradation, required negative evidence or interface meaning may change.
Record the answer through `decision-packet`.
