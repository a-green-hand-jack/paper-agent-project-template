# Shared skills rules

Shared skills must avoid product names, private paths and provider-specific
assumptions. Each skill states what must be adapted in a destination project,
as slots or steps a destination can extend: destinations write their
adaptations only in a trailing `## In this repository` section (see
`template-adoption` step 5). A skill's own text never contains a line that is
exactly `## In this repository`, not even in an example.
Update the content registry when adding, renaming or retiring a shared skill.

`issue-workflow/` owns acceptance write responsibility; `agent-communication/`
owns transport, receipts, receive-time classification, recoverable terminal
summaries and message cadence. Its
`references/acceptance-scenarios.md` reviews their shared boundary without
claiming fixture review proves a real exchange.

`development-writing/` owns the common writing principles and four development
record types; `references/four-cases.md` holds transferable weak/rewrite examples.
Concrete historical cases stay outside shared packages.

`release-doc-audit/` covers release writing, rendered visual review and the
existing consistency audit; its `references/release-types.md` distinguishes
product upgrades, results, milestones/archives and concise releases. Keep
concrete project release examples outside shared packages.

<!-- registry-index:start -->
- [.gitattributes](.gitattributes) — Whitespace exceptions for vendored files that keep upstream bytes git diff --check would report; extend it when vendoring such a file.
- [academic-voice](academic-voice/SKILL.md) — Vendored, MIT, msimchowitz/writing-skills@214981f; PROVENANCE.md.
- [agent-communication](agent-communication/SKILL.md) — Resolve native addresses, reconcile backlog and record distinct delivery/receipt outcomes.
- [asset-lifecycle](asset-lifecycle/SKILL.md) — Adapt asset classes, storage roots and migration evidence.
- [better-usage](better-usage/SKILL.md) — Vendored, MIT, msimchowitz/writing-skills@214981f; PROVENANCE.md.
- [citation-support-review](citation-support-review/SKILL.md) — Occurrence-level citation support at Draft, Review and Release strength.
- [cli-first-operations](cli-first-operations/SKILL.md) — Use the project's public CLI instead of ad-hoc wrappers.
- [control-review](control-review/SKILL.md) — Review before changing anything a control cue protects.
- [credential-setup](credential-setup/SKILL.md) — Set up declared project credentials without copying logins or exposing values.
- [decision-packet](decision-packet/SKILL.md) — Prepare a Human decision and record it as a project memory record.
- [development-writing](development-writing/SKILL.md) — Write Issues, PRs, comments and commits around reader decisions and traceable evidence.
- [figure-router](figure-router/SKILL.md) — House router for figure work, harvested from downstream papers and generalized.
- [icarus-figures](icarus-figures/SKILL.md) — Vendored, MIT, TAO-QKV/Icarus-Figures@0bcaa40; front matter patched to parse, recorded in PROVENANCE.md.
- [image-to-editable-ppt](image-to-editable-ppt/SKILL.md) — Vendored, MIT, ningzimu/image-to-editable-ppt-skill@b7be494; patched to remove the fallback that read another tool's login, recorded in PROVENANCE.md.
- [issue-workflow](issue-workflow/SKILL.md) — Scope, dispatch, protect acceptance inputs, integrate and close an Issue with explicit ownership.
- [lieflat-less-ai-tone](lieflat-less-ai-tone/SKILL.md) — Vendored, MIT, larashero3-dotcom/writing-dna-skill@d5145ef; standalone since the Writing DNA suite was retired; PROVENANCE.md.
- [manuscript-consistency-review](manuscript-consistency-review/SKILL.md) — Findings-only review of a version the Human names.
- [openreview-review-collector](openreview-review-collector/SKILL.md) — House skill harvested from downstream papers; collects reviews into a dossier and a revision queue.
- [paper-brief-ingest](paper-brief-ingest/SKILL.md) — Validates a brief and fills PAPER.md; carries scripts/paper_brief.py, which refuses to ingest into the template itself.
- [paper-interface-maintenance](paper-interface-maintenance/SKILL.md) — Interface macros, the paper-interfaces record and manifest entries change together.
- [paper-orientation](paper-orientation/SKILL.md) — Session start and context recovery for a paper repository.
- [poster-build](poster-build/SKILL.md) — House skill for the optional poster/ product tree, harvested from a downstream paper and generalized.
- [project-memory-governance](project-memory-governance/SKILL.md) — Classify, register and migrate development content without losing provenance or authority.
- [proofread](proofread/SKILL.md) — Vendored, MIT, JakobThumm/proofreading@cf2f0d7; PROVENANCE.md.
- [publication-planning](publication-planning/SKILL.md) — Venue, page budget, builds and every Overleaf status, pull or push request.
- [reference-repair](reference-repair/SKILL.md) — Repair BibTeX identity, metadata, duplicates and versions.
- [release-doc-audit](release-doc-audit/SKILL.md) — Draft readable release narratives and audit rendered output, versions and upgrade paths.
- [release-review](release-review/SKILL.md) — make release-check, the release PR from dev to main and the tag.
- [scientific-english-editor](scientific-english-editor/SKILL.md) — Vendored, MIT, SailRain/scientific-english-editor-skill@2b5ed82; PROVENANCE.md.
- [scientific-figure-workflow](scientific-figure-workflow/SKILL.md) — House figure workflow, harvested from downstream papers and generalized; names no image provider.
- [scientific-writing](scientific-writing/SKILL.md) — Vendored from a-green-hand-jack/research-skills@26226c9 with the maintainer's permission (no licence file upstream); PROVENANCE.md and SOURCES.md.
- [scipilot-figure-skill](scipilot-figure-skill/SKILL.md) — Vendored, MIT, Haojae/scipilot-figure-skill@43098dd; PROVENANCE.md.
- [section-writing](section-writing/SKILL.md) — Section drafting and revision; its references hold the paper-writing guide.
- [style-alignment](style-alignment/SKILL.md) — Positioning, narrative and writing policy; its references hold the writing-style guide.
- [template-adoption](template-adoption/SKILL.md) — Adapt the target repository's rules, product paths and acceptance commands.
- [template-feedback](template-feedback/SKILL.md) — Adapt the canonical template URL, labels and upstream Issue fields.
- [template-upgrade](template-upgrade/SKILL.md) — Adapt current and target release tags, local conflicts and migration evidence.
- [thesis-figure-skill](thesis-figure-skill/SKILL.md) — Vendored, MIT, 0xE1337/thesis-figure-skill@ffe6d07; PROVENANCE.md.
- [tikz-figure-code](tikz-figure-code/SKILL.md) — Vendored, MIT, 0xE1337/thesis-figure-skill@ffe6d07; PROVENANCE.md.
- [worktree-lifecycle](worktree-lifecycle/SKILL.md) — Create, verify and retire isolated worktrees after responsibility and state handoff.
- [writing-reference-finder](writing-reference-finder/SKILL.md) — House skill harvested from downstream papers; exemplars are never citations.
- [writing-router](writing-router/SKILL.md) — House router for prose tasks, harvested from downstream papers and generalized.
<!-- registry-index:end -->

## In this repository

Vendored third-party skills: a third-party skill is vendored only under a
licence that allows it, or with its author's permission recorded in its
`PROVENANCE.md`. Its package holds:

- the upstream files needed to use the skill, byte for byte, and the upstream
  `LICENSE` unchanged;
- `PROVENANCE.md`: the upstream repository, path and full commit, the licence
  and holder, a table of every file with the SHA-256 of the upstream bytes and
  its status (`unchanged`, `unchanged above ## In this repository`, `patched`),
  each excluded upstream file with the reason, and every local change as a
  unified diff;
- this repository's notes only in the trailing `## In this repository`
  section of `SKILL.md`.

`make check` re-hashes every file against `PROVENANCE.md`. To update a vendored
skill, replace the upstream files from the new commit, update the table, keep
the trailing section, re-apply each recorded patch, and run `make check`.
Never edit upstream text in place. When an upstream file carries whitespace
that `git diff --check` reports, list that file in `.gitattributes` here
instead of changing its bytes. Upstream file names that break the naming rules
keep them through reasoned `policy.naming_exceptions` in the registry.
