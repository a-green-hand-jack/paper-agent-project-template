# Skills directory rules

Use `shared/` for procedures that every paper made from this template reuses,
and register each one in `.agents/content-registry.yaml`. A paper's own skills
(procedures only that paper needs) go in another directory such as
`project/<name>/` and must state their commands, evidence and failure
boundaries. Skills give process, not permission: `PAPER.md` and the records
take precedence over any skill text.

Load the one owner skill for the task (the root `AGENTS.md` routes tasks to
them), and a second skill only when the owner skill or the Human names it.
Never load the whole family.

Inherited from `coding-agent-project-template`:

- `shared/agent-communication/` — route a handoff or follow-up between Herdr
  panes and agent sessions through native capabilities; distinguish receipts,
  reconcile covered events and preserve pending duties without ACK loops.
- `shared/asset-lifecycle/` — keep external assets, including result tables
  and figure data from code repositories, linked and in the manifest.
- `shared/cli-first-operations/` — operate through the public entry points
  (`make`, `.agents/scripts/`), never through ad hoc wrappers.
- `shared/credential-setup/` — the steps that apply `llm-credentials`: link
  the device's shared file, log in once per canonical checkout, keep values out
  of every output.
- `shared/development-writing/` — reader decisions and current evidence for
  Issues, PRs, comments and commits, with neutral examples in references.
- `shared/issue-workflow/` — Issue worktrees, dispatch by difficulty, merge
  and close-out; task identity, declared targets, protected acceptance inputs
  and coordinator reconciliation.
- `shared/project-memory-governance/` — classify, register and clean memory,
  knowledge and skills.
- `shared/release-doc-audit/` — prepare and visually review release narratives,
  then audit documentation, version references and upgrade instructions.
- `shared/template-adoption/` — bring an existing paper repository onto this
  template, establishing its concepts and directory contracts before migration.
- `shared/template-feedback/` — report a template defect to this template or
  upstream.
- `shared/template-upgrade/` — upgrade a paper to a newer template release.
- `shared/worktree-lifecycle/` — create, set up, migrate and retire a
  worktree after its acceptance and outstanding responsibilities are settled.

Paper workflow (this template's own):

- `shared/paper-orientation/` — recover the context a session needs.
- `shared/paper-brief-ingest/` — validate a brief and fill `PAPER.md` from it.
- `shared/control-review/` — before changing anything a control cue protects.
- `shared/decision-packet/` — prepare a Human decision and record it.
- `shared/section-writing/` — draft or revise a section from the contracts and
  evidence.
- `shared/style-alignment/` — positioning, narrative and writing policy.
- `shared/paper-interface-maintenance/` — interface macros, their record and
  their manifest entries.
- `shared/manuscript-consistency-review/` — findings-only review of a finished
  version.
- `shared/citation-support-review/` — whether a cited work supports the text.
- `shared/reference-repair/` — repair BibTeX identity and metadata.
- `shared/publication-planning/` — venue, page budget, builds and Overleaf.
- `shared/release-review/` — prepare a tagged release for Human approval.

Writing:

- `shared/writing-router/` — entry point for prose tasks; routes to one of the
  skills below.
- `shared/scientific-writing/` — structure, drafting and revision of a
  scientific manuscript (vendored).
- `shared/scientific-english-editor/` — language editing for non-native
  writers (vendored).
- `shared/better-usage/` — repair mismatched word combinations (vendored).
- `shared/academic-voice/` — careful academic register (vendored).
- `shared/lieflat-less-ai-tone/` — remove AI writing tells by an explicit rule
  list (vendored).
- `shared/proofread/` — checklist proofreading, report or interactive
  (vendored).
- `shared/writing-reference-finder/` — find and record writing exemplars,
  never citations.
- `shared/openreview-review-collector/` — collect reviews into a dossier and a
  revision queue.

Figures and posters:

- `shared/figure-router/` — entry point for figure work; routes to one of the
  skills below.
- `shared/scientific-figure-workflow/` — plan and evaluate a figure, from data
  plots to schematic drafts.
- `shared/scipilot-figure-skill/` — data-figure advice and production
  (vendored).
- `shared/icarus-figures/` — reproducible data figures and TikZ method figures
  (vendored).
- `shared/thesis-figure-skill/` — TikZ and draw.io diagrams for papers
  (vendored).
- `shared/tikz-figure-code/` — robust TikZ code, with a lint entry point
  (vendored).
- `shared/image-to-editable-ppt/` — rebuild slide images as editable
  PowerPoint (vendored, patched).
- `shared/poster-build/` — the optional `poster/` product tree.

Add a new skill to this list and to `.agents/content-registry.yaml` in the same
change; `make check` fails otherwise.
