---
name: writing-router
description: Route a manuscript-prose task (drafting, structure, grammar, word choice, register, AI-tone cleanup, proofreading) to the one skill that owns it, and run cross-check passes only when the Human or the task asks for them.
---

# Writing Router

Use this skill to choose the owner of a prose task in `paper/` before loading
any writing skill. Then load only the chosen skill's `SKILL.md` and the files
it points to.

## Boundary

- Writing skills change language and organisation, never facts. No pass adds,
  removes, strengthens or weakens a claim, number, citation, equation or
  result.
- Structure comes before language: do not polish text that may still be cut
  or moved.
- If a language edit would change meaning, stop and report it instead of
  making it.
- Precedence: the Human's current request and decisions; then the cues in
  `PAPER.md` (`locked`, `bounded`, `free`, `unresolved`); then the paper's
  records in `.agents/memory/project/` (experiments, paper interfaces,
  publication); then the owner skill; then this router.
- A language pass never edits text that `PAPER.md` marks `locked`; it reports
  the issue and the change goes through `control-review`.
- Out of scope: citations and the bibliography (`citation-support-review`),
  writing exemplars (`writing-reference-finder`), figures (`figure-router`),
  venue, builds and submission logistics (`publication-planning`).

## Route the task

| Job | Owner |
| --- | --- |
| Drafting a section, substantive revision, reorganising an argument | `section-writing` |
| Positioning, narrative, terminology policy, the paper's writing policy | `style-alignment` |
| Structure diagnosis: section roles, the abstract as an argument, claims against evidence | `scientific-writing` (a reference for the two owners above) |
| Consistency of terms, numbers and claims across the manuscript | `manuscript-consistency-review` |
| Grammar, non-native phrasing, sentence clarity and concision | `scientific-english-editor` |
| Word choice: a verb that does not fit its subject or object, a hidden actor, a vague relation | `better-usage` |
| Register and scholarly voice; no corporate, social-media or changelog tone | `academic-voice` |
| AI writing tells, by an explicit whitelist of patterns (final pass) | `lieflat-less-ai-tone` |
| Pre-submission proofreading: notation, abbreviations, figures and tables, statistics reporting | `proofread` |

When a task spans several rows, start with the earliest row in the table:
structure before language.

## Cross-check passes (opt-in)

A cross-check runs only when the Human asks for it or the task names it, for
example "proofread before the submission build". It is then an independent
pass from a different row of the table, reported separately; a skill never
both edits and certifies the same text. Sequences that work well:

- after a section rewrite: `better-usage`, then `academic-voice`, then
  `proofread`;
- after a sentence-level fix: `better-usage`, then `lieflat-less-ai-tone`;
- before a submission build: `lieflat-less-ai-tone`, then `proofread`, then
  `scientific-writing` again if the argument moved.

Each pass works on the result of the previous one and never silently undoes
an earlier meaning-preserving edit.

## Conflicts

- Meaning and evidence win over style. When two passes disagree, for example
  voice against AI tone, keep the meaning-preserving text and report the
  conflict instead of forcing either side.
- The whitelist skills (`lieflat-less-ai-tone`, and `proofread` in report
  mode) touch only their listed patterns.
- `section-writing` and `style-alignment` decide organisation; language
  passes never restructure.

## Report

State which skill owned the edit, what changed, which cross-checks ran (or
that none were requested), and any conflict or open question. Keep a
`file:line` ledger with the reason for each change, not the full rewritten
text. When `paper/` changed, run `make check` and report its result; when the
change can move the layout (line or page breaks, floats), inspect the rendered
pages as `.agents/memory/shared/post-build-visual-inspection.md` describes.
