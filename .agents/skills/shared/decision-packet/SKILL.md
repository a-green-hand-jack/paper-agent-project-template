---
name: decision-packet
description: Use when a Human must choose among high-impact alternatives or approve a change outside a bounded area, and to record the decision afterwards.
---

# Decision Packet

## Trigger

Use when a Human must choose among high-impact alternatives or approve a change
outside a bounded area.

## Minimum context

- the current contract entry in `PAPER.md` or the project record it lives in
  (`.agents/memory/project/experiments.md`, `paper-interfaces.md`,
  `publication.md`);
- the latest applicable decision record in `.agents/memory/project/`;
- directly affected paper sections, experiments and interfaces;
- concrete evidence or constraints needed for this decision.

Do not include exhaustive search logs or unrelated history.

## Procedure

Prepare one focused packet:

- **Question** — the single decision needed now.
- **Why now** — the blocker or opportunity.
- **Current state** — what is presently approved or unresolved.
- **Options** — genuinely different choices and their consequences.
- **Affected surfaces** — claims, sections, experiments, interfaces,
  limitations, builds, release.
- **Recommendation** — a neutral recommendation grounded in stated criteria,
  evidence and tradeoffs; do not present Agent preference as approval.
- **Unchanged scope** — what this decision will not alter.

Do not bundle independent semantic choices into one approval gate. Prepare a
separate focused packet and use a separate Human approval gate for each.

## Recording the decision

After the Human answers, record it in the repository; a decision left only in
chat or in `.project/` notes is not recorded.

1. Update the contract it changes: `PAPER.md` or the project record.
2. Write the decision as its own record `.agents/memory/project/<topic>.md`
   from `.agents/memory/ENTRY_TEMPLATE.md`: front matter (`name`, `date`,
   `source`, `scope: project`, `applies_to`, `status: active`, `supersedes`,
   `superseded_by`) and the sections Decision, Why and Apply. State what was
   chosen, the paper objects it affects, rejected alternatives when relevant,
   and which future change needs review again.
3. Add the record to the index `.agents/memory/project/AGENTS.md`, and link it
   from `PAPER.md` when it changes a cue.
4. When it replaces an earlier decision, set the earlier record's
   `status: superseded` and `superseded_by`, and the new record's
   `supersedes`; do not rewrite the earlier decision's text.

Record durable, high-impact choices only, not every sentence edit or passing
discussion.

## Human decision

The Human decides scientific commitments, story direction, experiment
fairness, result interpretation, claim degradation and release acceptance.
