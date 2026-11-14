---
name: paper-writing
description: Draft, revise or proofread scientific prose while preserving claims, evidence and the author's decisions.
---

# Paper writing

Identify whether the task concerns argument and section structure, narrative and style, sentence-level language, or final proofreading. Read `PAPER.md`, the active section and only the evidence and interfaces the task needs. Preserve the strength and meaning of claims; report uncertain scientific changes rather than silently making them. Draft structure before polishing language. Use exemplars to study expression, never as automatic claim support or bibliography entries.

Use the following detailed guidance only when applicable; do not run every pass by default:

- [Section drafting](sources/section-writing/reference.md) and [scientific writing](sources/scientific-writing/reference.md)
- [Narrative and style](sources/style-alignment/reference.md)
- [English editing](sources/scientific-english-editor/reference.md), [word usage](sources/better-usage/reference.md) and [academic voice](sources/academic-voice/reference.md)
- [AI-tone rules](sources/lieflat-less-ai-tone/reference.md) and [proofreading](sources/proofread/reference.md)
- [Finding writing exemplars](sources/writing-reference-finder/reference.md)

When the task is the argument rather than the prose, read the matching record
under [`.agents/memory/shared/paper-writing/`](../../../memory/shared/paper-writing/):
claims fix their experiment and expected result, claims are stated without
hedging, the evaluation is organised claim by claim, notation is a cost, and
undecided content lives in author comments. Collaborator text stays byte for
byte ([`collaborator-content-byte-for-byte`](../../../memory/shared/collaborator-content-byte-for-byte.md)).

For changed paper source, run the project's build checks and inspect affected pages when layout can change.
