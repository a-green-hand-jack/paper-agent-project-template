---
name: rebuild-on-coding-template
date: 2026-10-20
source: Issue #156, the maintainer's decisions D1 to D8 on it, and dev at de691d9 (v0.3.1 and #153); Issue #185 (upstream v0.1.19)
scope: project
applies_to: this template repository's v0.4.0 layout, and the downstreams that move to it from template-sync
status: active
supersedes: null
superseded_by: null
---

# v0.4.0 is rebuilt on coding-agent-project-template

## Decision

From v0.4.0 this template is a derived template of
`coding-agent-project-template`. It adopted that template's release `v0.1.13`
(`49d0009`) through the `template-adoption` skill, and its registry records
both templates:

```yaml
template:
  repository: https://github.com/a-green-hand-jack/paper-agent-project-template
  version: v0.4.0
  upstream:
    repository: https://github.com/a-green-hand-jack/coding-agent-project-template
    version: v0.1.13
```

Before anything changed, every path of `dev` at `de691d9` (448 tracked files)
and every path of the upstream release was given one class:

- **adopted**: copied from upstream unchanged. Shared skills and memory records
  get a trailing `## In this repository` section.
- **adapted**: rewritten or changed for a paper.
- **preserved**: kept, with only its paths changed.
- **rejected**: not taken from upstream, or retired from this repository.

The tables below are the map.

### Top-level paths of this repository

| Path | Class | Destination and reason |
| --- | --- | --- |
| `.agents/` | adapted | Rebuilt on the upstream development plane; see the subtrees below. |
| `.env.example` | adapted | The upstream file plus the variable names the online reference audits read (`BIBTEX_CHECK_MAILTO`, `OPENALEX_API_KEY`, `S2_API_KEY`). Names only, no values. |
| `.github/` | adapted | Adopted unchanged: `workflows/template-check.yml` and the Issue and PR templates. New: `workflows/paper-check.yml`, which runs `make check`, `make submission` and a build of `paper/` alone. Preserved: `workflows/reference-validation.yml`, with the new paths and without the personal fallback e-mail. Rejected: `pr-validation.yml` and `build-release.yml`, which tested retired variants, release instances and template-sync. |
| `.gitignore` | adapted | The upstream rules are merged in (`.project/`, the `assets/*` exceptions, `!.env.example`). The LaTeX-leftover and local-runtime rules stay. `paper/*.pdf` replaces `paper/main*.pdf` and covers a build run in place. |
| `AGENT_GUIDE.md` | rejected (folded) | Task routing went to `AGENTS.md`, starting a paper to `README.md`, and the process to `DEV.md`. |
| `AGENTS.md` | adapted | The upstream rules in English (three planes, work units, state, evidence) with `paper/` as the product tree, plus the paper's task routing, control cues and strong rules. |
| `ANATOMY.md` | rejected (folded) | The directory table went to `README.md`; each directory's rules are in its own `AGENTS.md`. |
| `BRIEF.md` | adapted (moved) | Became the starter record `.agents/memory/project/brief.md`, which `paper-brief-ingest` validates and ingests (D3). |
| `CLAUDE.md` | adopted | Now a relative symlink to `AGENTS.md`; it was a regular file. |
| `CONTRIBUTING.md` | rejected (folded) | Folded into `DEV.md`: the Issue and PR flow from `dev`, verification and releases. |
| `DECISIONS.md` | adapted (moved) | Split into typed records; see "Earlier decisions" below. |
| `EXPERIMENTS.md` | adapted (moved) | Became the starter record `.agents/memory/project/experiments.md`. Results from code repositories are registered in `assets/MANIFEST.yaml`. |
| `LATEX_TEMPLATES.md` | adapted (moved) | Became the dated knowledge record `.agents/knowledge/shared/official-latex-templates.md`. The `external-latex` build profile and the official-template smoke tests are retired. |
| `Makefile` | adapted | The public build entry: `pdf`, `blind`, `submission`, `check`, `release-check` and `clean`. It delegates to `paper/Makefile`, takes `TEXBIN` and `PAGE_BUDGET` overrides, and writes to `.project/build/`. `VARIANT=` is retired. |
| `PAPER.md` | preserved | The four cues and the headings that downstreams and `paper-brief.py` use stay. The operating-mode text names the three builds, and locked claims link to their evidence. |
| `PAPER_INTERFACES.md` | adapted (moved) | Became `.agents/memory/project/paper-interfaces.md`: each interface macro's meaning, control cue and source. `make check` reads it. |
| `PUBLICATION.md` | adapted (moved) | The generic rules went to `shared/one-source-three-builds.md` and `shared/page-budget-on-blind-build.md`. The paper's venue, budget and release plan went to `project/publication.md`, and the reference policy block to `.agents/references/policy.json`. Variants, delivery targets and release instances are retired. |
| `README.md` | adapted | Purpose, how to start a paper (replacing `paper-init.py`), the directory table, the builds and the reasons for the design. It absorbs `WHY_THIS_TEMPLATE.md` and the role of the upstream `USER.md`. |
| `REFERENCES.md` | adapted (moved) | The rules went to `shared/reference-integrity.md`, the service facts to `knowledge/shared/bibliographic-metadata-services.md`, and the ledger rules to `.agents/references/AGENTS.md`. The personal fallback e-mail is removed. |
| `WHY_THIS_TEMPLATE.md` | rejected (folded) | Became the "Why" section of `README.md`; the skill inventory is `.agents/skills/AGENTS.md`. |
| `paper/` | adapted | See "Product plane" below. |
| `references/` | adapted (moved) | `ledger.json` moved to `.agents/references/ledger.json`. |
| `releases/` | rejected | Release records are replaced by tags and `RELEASE_NOTES.md` (D2). |

New top-level paths: `DEV.md`, `RELEASE_NOTES.md` (this template's own release
history, `scope: template`), `assets/README.md` and `assets/MANIFEST.yaml`.

### Upstream top-level paths (v0.1.13)

| Upstream path | Class | Reason |
| --- | --- | --- |
| `AGENTS.md`, `README.md`, `DEV.md` | adapted | Rewritten in English for a paper. |
| `CLAUDE.md` | adopted | A symlink to `AGENTS.md`. |
| `USER.md` | rejected | A paper has no installed product. The reader-facing role belongs to `README.md` and the paper itself. |
| `RELEASE_NOTES.md` | rejected | It is the coding template's own history; this template keeps its own. |
| `.env.example`, `.gitignore` | adapted | See above. |
| `.github/` | adopted | See above; `paper-check.yml` is added beside it. |
| `assets/` | adapted | `README.md` and `MANIFEST.yaml` describe a paper's evidence: result tables, figure data and reported numbers from code repositories. |
| `src/`, `pyproject.toml`, `Dockerfile`, `.dockerignore`, `install.sh` | rejected | The product tree is `paper/`, and a paper has no package, container or installer. `DEV.md` says so, and `diagnose-environment.sh` reports these files as optional ones that are absent. |

### `.agents/` subtrees of this repository

| Path | Class | Destination and reason |
| --- | --- | --- |
| `.agents/AGENTS.md` | adapted | The upstream development-plane rules plus an index that includes `references/`. |
| `.agents/ANATOMY.md` | rejected | Replaced by the index in each directory's `AGENTS.md`. |
| `.agents/dependencies/reference-integrity/` | preserved (moved) | Moved to `.agents/scripts/reference-integrity/`, next to the scripts whose dependencies it locks. The licence inventory stays in `THIRD_PARTY.md`. |
| `.agents/documentation-consistency.json` | rejected | Its checker guarded the retired documents. The inherited `release-doc-audit` replaces it. |
| `.agents/knowledge/` | adapted | The upstream layout (`AGENTS.md`, `ENTRY_TEMPLATE.md`, `shared/`, `project/`) plus `VENUE_TEMPLATE.md`; `README.md` became `AGENTS.md`. `scientific-writing.md` and `writing-style.md` are guidance, not dated facts, so they moved into the `section-writing` and `style-alignment` packages as references. `venues/` became `VENUE_TEMPLATE.md` (the old `_template.md` fields on the upstream front matter) and dated `shared/venue-*.md` records. The old rule that a concrete venue file belongs only downstream is superseded by #156 §7. `writing/`, the Writing DNA workflow, is retired with its suite (D1). |
| `.agents/overleaf-sync.json` | rejected | The remote now comes from local Git configuration (`overleaf-sync.sh`). The tracked file named this template's own Overleaf project, which therefore leaves the public tree. |
| `.agents/paper-build.json` | rejected | Build profiles are retired with the variants; `paper/Makefile` is the build. |
| `.agents/runtime/` | rejected | Local state lives in `.project/`. |
| `.agents/skills/` | adapted | The upstream `skills/shared/` plus this template's skills; see "Skills" below. |
| `.agents/template-inheritance.json`, `.agents/template-sync.json` | rejected | Retired by #156; the registry and `template-upgrade` replace them. |
| `.agents/tests/` | adapted | The upstream `AGENTS.md` plus a paper paragraph. Tests remain only for kept scripts (below). |
| `.agents/tools/` | adapted | Kept tools moved to `.agents/scripts/`; the rest are retired (below). |
| `.agents/vendor/` | rejected | CCFA-Skills and writing-dna-skill are dropped as a whole (D1). `lieflat-less-ai-tone` is vendored again as a standalone skill. |

New `.agents/` paths: `content-registry.yaml`, `memory/`, `references/` and
`scripts/`.

### Upstream `.agents/` content (v0.1.13)

| Upstream path | Class | Reason |
| --- | --- | --- |
| `scripts/*.sh` | adopted | Byte-identical to the release. Project setup is in `setup-project.sh` and `migrate-project.rules`. |
| `scripts/AGENTS.md`, `tests/AGENTS.md` | adapted | Index of this repository's scripts; the paper's test commands. |
| `skills/shared/asset-lifecycle/` | adopted | Its section covers result tables, figure data and numbers from code repositories. |
| `skills/shared/cli-first-operations/`, `skills/shared/project-memory-governance/` | adopted | `shared`. |
| `skills/shared/issue-workflow/` | adopted | Its section fills the slots: `dev`, this repository, `make check`, CI on. |
| `skills/shared/release-doc-audit/` | adopted | Its section sets `RELEASE_HEADING` and the paper release tags. |
| `skills/shared/template-adoption/` | adopted | Its section names the paper product tree, the build output and the acceptance commands. It replaces this repository's own `template-adoption` skill and tool. |
| `skills/shared/template-feedback/` | adopted | Its section sends feedback to this template first and inherited defects upstream. |
| `skills/shared/template-upgrade/` | adopted | Its section names the followed template and adds `make check`. It replaces `template-sync`. |
| `skills/shared/worktree-lifecycle/` | adopted | Its section says `.project/build/` is rebuildable and is dropped at teardown. |
| `skills/shared/long-running-supervision/` | rejected | A paper repository has no long product runs; experiments run in code repositories. |
| `skills/template-harvest/` | rejected | The coding template's own maintainer procedure (`scope: template` there). |
| `memory/shared/issue-close-out.md`, `issue-dispatch-by-difficulty.md`, `issue-in-herdr-worktree.md`, `resolve-real-paths-before-moving.md` | adopted | `shared`. |
| `memory/shared/product-state-root.md` | adopted | Its section: `paper/Makefile` finds `BUILD_DIR` from an argument, the `.project/home` marker, then `paper/build/` for a copy of `paper/` alone. |
| `memory/shared/llm-credentials.md`, `third-party-llm-compat-patches.md`, `knowledge/shared/gpt5-strict-backend-requests.md` | adopted | Template-adoption step 3 maps them together when a repository runs a tool that calls an LLM provider. Here that is only the optional CLI fallback of `image-to-editable-ppt`, which takes an API key. The sections fill `CREDENTIAL_DIR` and `PATCH_DIR`. |
| `memory/shared/docker-objects-prefixed-and-removed.md` | rejected | A paper starts no containers. |
| `memory/shared/run-settings-from-config.md` | rejected | A paper has no product runs. |
| `memory/project/harvest-*.md` | rejected | The coding template's own records. |
| `memory/ENTRY_TEMPLATE.md`, `knowledge/ENTRY_TEMPLATE.md` | adopted | Unchanged. |
| `memory/**/AGENTS.md`, `knowledge/**/AGENTS.md` | adapted | Same rules, indexes rewritten for this repository. |

### Upstream v0.1.19 (Issue #185)

The upgrade from `v0.1.13` to `v0.1.19` crossed six releases. The command
applied the shared files; these are the decisions it left to this repository.

| Upstream content | Class | Reason |
| --- | --- | --- |
| `scripts/upgrade-template.sh` | adopted | Byte-identical to the release; the local copy's differences (state under `.project/build/`, any `.md` file as a sectioned file) are gone, and its clone and proposals now live in `.project/state/template-upgrade/`. |
| `scripts/probe-credentials.sh`, `skills/shared/credential-setup/`, `knowledge/shared/credential-inventory.md` | adopted | They go with `llm-credentials`. This repository keeps no root `credentials.yaml`, because nothing it ships calls an LLM provider; the probe skips. |
| `memory/shared/host-files-owned-by-running-user.md`, `look-at-the-artifact-before-concluding.md`, `provider-cost-routing.md`, `screen-with-scriptable-fakes.md`, `speed-and-parallelism-by-measurement.md`, `skills/shared/agent-communication/` | adopted | `shared`. |
| `memory/shared/serve-the-coding-agent.md` | rejected | Optional. A paper keeps no run records or usage accounting to name in its five slots. |
| `memory/shared/docker-objects-prefixed-and-removed.md`, `skills/shared/long-running-supervision/` and the product release skeleton (`pyproject.toml`, `Dockerfile`, `install.sh`, `.dockerignore`) | rejected | Unchanged from v0.1.13; the command keeps a rejected `optional: true` path out. |
| `.github/workflows/template-check.yml` | adopted | `issue-workflow` `<CI>` is `yes`; `<LOCAL_CHECK>` is `make check` plus the steps the workflow adds. |
| `writing:` registry block | left out | The block is the repository's own; none is declared, so each file keeps its language. |
| `memory/project/harvest-*.md`, `template-work-runs-on-pi-deepseek.md`, `skills/template-harvest/`, `tests/test_template_*.py`, `RELEASE_NOTES.md` | rejected | The coding template's own records, tests and history (`scope: template` or project-owned there). |

### Product plane: `paper/`

| Path | Class | Destination and reason |
| --- | --- | --- |
| `paper/main.tex` | adapted | One source. `\PaperBlindBuild` (no identity, acknowledgements or notes) and `\PaperSubmissionBuild` (no notes) set the build switches `\ifPaperBlind` and `\ifPaperNotes`, and `\label{PaperMainTextEnd}` marks the end of the main text for the page count. |
| `paper/blind.tex`, `paper/submission.tex` | adapted (new) | One-line entry files that Overleaf can also select as the main document. |
| `paper/authors.tex` | adapted (new) | The only file with author identity. The anonymous build does not read it, and its `\PaperIdentity` strings are what the release check searches for. |
| `paper/Makefile` | adapted (new) | latexmk builds `main`, `blind` and `submission`. It takes `TEXBIN`, and `BUILD_DIR` from the marker or `build/`. |
| `paper/macros.tex` | preserved | The interface macros, now each with a `% Interface:` marker. `\PaperNote` is added, and the `generated/results-macros.tex` hook is removed. |
| `paper/refs.bib` | preserved | The marker path is updated to `.agents/references/ledger.json`. |
| `paper/sections/` | preserved | Placeholder sections. |
| `paper/style/` | preserved | `paper-harness.sty` (T1 encoding) and `compat.sty`. Their `README.md` became comments in the packages. |
| `paper/figures/`, `paper/tables/` | preserved | `.gitkeep` files replace their `README.md` files. The figure-source policy moved to `DEV.md` and the figure skills. `figures/srcs/` is dropped, because editable sources are evidence assets in the manifest. |
| `paper/algorithms/` | adapted (new) | Required by #156. |
| `paper/variants/` | rejected | Retired by #156 in favour of macro-switched builds. |
| `paper/generated/` | rejected | Retired by #156. Numbers enter through `macros.tex`, each with a manifest source. |
| `paper/venue_preamble.tex` | rejected | A venue's class and style files go directly into `paper/` and `main.tex`. |
| `paper/supplementary/` | rejected | Nothing used it. Supplementary material is an appendix section or a separate build. |
| `paper/ANATOMY.md` | rejected | Folded into `README.md`. |

### Tools and tests

These were kept because they guard paper risks, and they moved to `.agents/scripts/`:

| Tool | Risk guarded | Tests |
| --- | --- | --- |
| `check-reference-integrity.py`, `reference-evidence.py`, `_citation_occurrences.py`, `_bib_identity.py`, `check-bibtex-format.py`, `_validate-bibtex-with-pybtex.py`, `check-reference-metadata.py`, `check-reference-corrections.py`, `_validate-bibtex-correction.py`, `_reference_env.py` | bibliography identity, cited-key coverage and claim support | `test_reference_integrity.py`, `test_reference_evidence.py`, `test_reference_corrections.py`, `test_bibtex_format_helper.py`, `test_bibtex_correction_helper.py` |
| `check-paper-interfaces.py` (rewritten) | each interface macro is defined, marked, documented and used, and zero-argument macros are called with `{}` (#131) | `test_paper_interfaces.py` (rewritten) |
| `paper-brief.py` | a brief fills only decided `PAPER.md` fields; it moved into `paper-brief-ingest/scripts/`, with #154 fixed (D3) | `test_paper_brief.py`, with #154 regressions |
| T1 encoding (`paper-harness.sty`, #129) | underscores lost from the PDF text layer | `check-paper-build.py underscores` in `make check`; the placeholder appendix carries an escaped underscore, so the check stays active in this template (it previously had no guard) |
| `overleaf-sync.py` | replaced by `overleaf-sync.sh` | `test_overleaf_sync.py` (rewritten against a local bare repository) |

New scripts:

- `paper-check.sh` (`make check`) and `release-check.sh` (`make release-check`);
- `check-paper-build.py`: log, page, PDF text-layer, identity and leftover checks of one build;
- `check-agent-content.py`: skill, memory and knowledge structure, indexes, registry entries and vendored-file hashes (`test_agent_content.py`);
- `setup-project.sh` and `migrate-project.rules`.

These were retired, because each guarded only retired machinery:

| Tool | Guarded | Tests dropped |
| --- | --- | --- |
| `verify.sh` | the old aggregate check | `test_make.py`, `test_structure.py` |
| `check-structure.py` | the old directory layout | `test_structure.py` |
| `check-documentation.py` | the retired root documents | `test_documentation.py` |
| `check-paper-contracts.py` | root contract headings and skill declarations | `test_contracts.py` |
| `check-publication.py` | the variants | `test_publication.py` |
| `check-paper-profile.py`, `_paper_profile.py`, `_official_templates.py` | build profiles and the official-template smoke tests | `test_paper_profile.py` |
| `check-venue-knowledge.py` | the old venue file schema | `test_venue_knowledge.py`; `check-agent-content.py` checks the new records |
| `paper-init.py` | cleanup of a repository made from the template | `test_paper_init.py` |
| `template-adoption.py`, `_template_inheritance.py` | the old adoption | `test_template_adoption.py` |
| `template-sync.py` | the old synchronization | `test_template_sync.py` |
| `paper-fidelity.py` | arXiv reconstruction evidence for the case branches, which keep their own copies | `test_paper_fidelity.py` |
| `release.py`, `release.sh`, `_release_core.py`, `_release_approval.py`, `check-release.py`, `_check_release_core.py`, `check-release-records.py` | release instances and records (D2) | `test_release.py`, `test_release_clean.py`, `test_release_records.py` |

### Skills

This repository's own skills all moved under `.agents/skills/shared/`,
because every paper made from the template reuses them, and were rewritten
for the new layout:

| Skill | Class | Reason |
| --- | --- | --- |
| `paper-orientation`, `control-review`, `decision-packet`, `section-writing`, `style-alignment`, `manuscript-consistency-review`, `paper-interface-maintenance`, `publication-planning`, `release-review`, `citation-support-review`, `reference-repair` | shared | Paper-generic owner skills, rewritten for one source and three builds, the memory records and `.agents/references/`. `publication-planning` now also routes Overleaf work. |
| `paper-brief-ingest` | shared | It carries `scripts/paper-brief.py` (D3). |
| `lieflat-less-ai-tone` | shared (vendored) | Used by three downstreams. It is now self-contained: the upstream file from `larashero3-dotcom/writing-dna-skill@d5145ef` (MIT), with its licence and provenance. |
| `writing-dna-skill` and the 17 `ccf-*` wrappers | rejected | D1: dropped as a whole with their snapshots. No downstream used them except `lieflat-less-ai-tone`, eight wrappers failed YAML parsing, and `dev` lacked the provenance manifest its README named. |
| `template-adoption` | rejected | Replaced by the inherited `template-adoption` with a paper section. |
| `template-sync` | rejected | Retired by #156 and replaced by `template-upgrade`. |

The following were harvested from the downstream paper repositories. House
skills were generalized; third-party skills were fetched again from their
upstream at a pinned commit, never copied from a private repository.

| Skill | Origin | Licence | Class |
| --- | --- | --- | --- |
| `writing-router` | house | this repository's | shared; routes to the template's owner skills, and cross-check chains are opt-in |
| `scientific-writing` | `a-green-hand-jack/research-skills@26226c9` (maintainer) | none upstream | shared, with attribution and `SOURCES.md` (D6) |
| `scientific-english-editor` | `SailRain/scientific-english-editor-skill@2b5ed82` | MIT | shared (vendored) |
| `better-usage`, `academic-voice` | `msimchowitz/writing-skills@214981f` | MIT | shared (vendored; the agent-client metadata file is excluded) |
| `proofread` | `JakobThumm/proofreading@cf2f0d7` | MIT | shared (vendored under its declared name; the script-path note is in its section) |
| `writing-reference-finder` | house | this repository's | shared; paper-specific topics and a private service removed |
| `openreview-review-collector` | house | this repository's | shared; a forum id and a private two-device section removed; triage hands off to the revision workflow |
| `figure-router`, `scientific-figure-workflow` | house | this repository's | shared; routes only to harvested figure skills, names no image provider, and gates on `post-build-visual-inspection` |
| `scipilot-figure-skill` | `Haojae/scipilot-figure-skill@43098dd` | MIT | shared (vendored) |
| `icarus-figures` | `TAO-QKV/Icarus-Figures@0bcaa40` | MIT | shared (vendored; the upstream front matter is invalid YAML, fixed and recorded) |
| `thesis-figure-skill`, `tikz-figure-code` | `0xE1337/thesis-figure-skill@ffe6d07` | MIT | shared (vendored under the upstream directory names, so their relative links work) |
| `image-to-editable-ppt` | `ningzimu/image-to-editable-ppt-skill@b7be494` | MIT | shared (vendored), patched to remove the fallback that read another tool's login (D7) |
| `poster-build` | house | this repository's | shared; rewritten without paper specifics; `poster/` is an optional second product tree described in `DEV.md` |
| `blender-3d-figures` | a third-party skill plus house text and Apache-2.0 code | none upstream | rejected: no licence, a missing Apache notice, and private paper content |
| `figure-image-generation` | house | this repository's | rejected: every file is tied to a retired private image provider |
| `paper-repo-architecture-translator` | house | this repository's | rejected: superseded by `template-adoption`, and it names a private paper |

Every vendored package has a `PROVENANCE.md` that records the upstream, the
commit, the licence and the SHA-256 of each file. `make check` re-hashes the
unchanged files.

### Memory and knowledge records (new)

The cross-paper lessons (#156 §7) were collected read-only from the six
downstream paper repositories. Each record is written in general terms and
names no repository, paper, person or project id. The count is the number of
repositories that showed the lesson.

| Record | Registry | Content (repositories) |
| --- | --- | --- |
| `shared/one-source-three-builds.md` | shared | The fixed order of publication forms: `main` (named, with notes), then `submission` (named, notes removed), then `blind` (identity, acknowledgements and notes removed). Each later form only removes a layer of the same source and is selected by a one-line entry file. A citation or label that only a note carries vanishes from the later forms (5/6; one had retired the same variant overlay this template shipped). |
| `shared/overleaf-paper-tree-only.md` | shared | Overleaf receives only `HEAD:paper`, committed on the fetched Overleaf tip and pushed as a fast-forward; never the root, never forced. Compare trees, not commits, because Overleaf rewraps commits (6/6). |
| `shared/sync-overleaf-before-editing.md` | shared | Fetch both sides before the first edit, take in Overleaf edits before writing, and deliver to GitHub and Overleaf together; report a partial sync as incomplete (5/6). |
| `shared/post-build-visual-inspection.md` | shared_with_adaptation | Render and look at the affected pages before calling a build done; a clean log proves nothing about layout. Slots `MIN_FIGURE_TEXT` and `LAST_LINE_FILL` (6/6). |
| `shared/skill-frontmatter-validity.md` | shared | Every `SKILL.md` front matter parses; re-check after every skill change. Eight of this repository's 33 `SKILL.md` files failed to parse before the rebuild (4/6). |
| `shared/page-budget-on-blind-build.md` | shared_with_adaptation | Measure main-text pages on the build reviewers receive, keep a margin, report an overage and never cut silently. Slots `PAGE_BUDGET` and `PAGE_MARGIN` (5/6). |
| `shared/official-venue-kit-unmodified.md` | shared | The official kit for the exact venue and year, unmodified, with its URL, SHA-256 and helper packages; a migration changes typesetting only (5/6). |
| `shared/tex-engine-from-texbin.md` | shared | TeX binaries come from an overridable `TEXBIN`; build leftovers stay out of every tracked or projected tree (4/6). |
| `shared/results-through-interface-macros.md` | shared | Reported numbers reach the text only through interface macros with a manifest source; planned results are never observations (#156 §5). |
| `shared/reference-integrity.md` | shared | Bibliographic identity and claim support, from `REFERENCES.md`. |
| `project/brief.md`, `project/experiments.md`, `project/paper-interfaces.md`, `project/publication.md` | project | Starters a paper fills. |
| `project/protected-case-branches.md`, `project/repository-identity.md`, `project/paper-run-boundary.md`, this record | template | This template's own records; a paper deletes them. |
| `knowledge/VENUE_TEMPLATE.md` and `knowledge/shared/venue-*.md`, `official-latex-templates.md`, `bibliographic-metadata-services.md` | shared | Dated, sourced facts, each with a refresh condition. |

Per-paper preferences that conflict between repositories stay out of the
shared text: last-line fill targets, float placement, draft-note macro names,
standing commit and push permissions, and whitespace normalization of
collaborators' edits. One downstream recommended a bare `git stash` during a
sync; that is not carried over, because it conflicts with the inherited
worktree rules.

### Earlier decisions (DEC-0001 to DEC-0019)

`DECISIONS.md` is retired. Each decision is kept, re-expressed or superseded:

| Decision | Outcome | Where it is now |
| --- | --- | --- |
| DEC-0001 Paper-first two-layer repository | superseded | The three planes in `AGENTS.md`: `paper/` is the product, `.agents/` development, the root documents the Human plane. |
| DEC-0002 Remove the old harness and duplicate control planes | superseded | The template now adopts worktree governance, `.project/` state and an asset manifest from the coding template. There is still no duplicate Human or memory store: memory and knowledge are typed records. |
| DEC-0003 Flexible control cues | kept | `PAPER.md` and `AGENTS.md`. |
| DEC-0004 Selective Agent context | kept | `AGENTS.md` and `.agents/skills/AGENTS.md`: one owner skill per task. |
| DEC-0005 Stable paper-facing interfaces | kept | `paper/macros.tex`, `project/paper-interfaces.md` and `shared/results-through-interface-macros.md`, checked by `check-paper-interfaces.py`. |
| DEC-0006 One canonical paper with small publication overlays | superseded | `shared/one-source-three-builds.md`: macro-switched builds replace the overlays. |
| DEC-0007 Variant, target and release instance are separate | superseded | Three builds of one source, release tags and `RELEASE_NOTES.md` (D2). |
| DEC-0008 Generated releases are not committed paper copies | superseded | Build output goes to `.project/build/`, and a release is a tag on `main`. Generated files are still never committed. |
| DEC-0009 Release readiness and packaging validation are distinct | superseded | `make check` (draft gates, run by CI) and `make release-check` (release gates, run before a tag through `release-review`). |
| DEC-0010 Path-level template synchronization | superseded | The inherited `template-upgrade`, with each repository's adaptation in `## In this repository` sections. |
| DEC-0011 Initial adoption as a separate migration | superseded | The inherited `template-adoption`. |
| DEC-0012 Overleaf as a paper-only two-way working copy | re-expressed | `shared/overleaf-paper-tree-only.md`, `shared/sync-overleaf-before-editing.md` and `overleaf-sync.sh`: `push` from `dev` as a fast-forward checked by tree, and `pull` onto a `sync/overleaf-*` branch for a PR. |
| DEC-0013 Documentation consistency as a maintained contract | superseded | The inherited `release-doc-audit`; the checker and its configuration are retired. |
| DEC-0014 Protected case branches and verification trackers | kept | `project/protected-case-branches.md`, verbatim. |
| DEC-0015 Bundled third-party skill suites | superseded | D1. Vendored skills live under `.agents/skills/shared/`, each with a `PROVENANCE.md` that `make check` verifies. |
| DEC-0016 Brief-driven paper bootstrap | kept | `paper-brief-ingest` with `paper-brief.py` in the skill package. The brief is the record `project/brief.md`; a paper starts as `README.md` describes, instead of through `ccf-project-scaffolder`. |
| DEC-0017 Operating modes and the autonomous approval boundary | kept | `PAPER.md` "Operating mode" and `AGENTS.md`. |
| DEC-0018 Domain-agnostic positioning with the old name | superseded | DEC-0019, then `project/repository-identity.md`. |
| DEC-0019 Rename to agent-writing-harness | superseded | `project/repository-identity.md` (renamed again, to `paper-agent-project-template`). The legacy-name handling in `paper-init.py` is retired with that tool; `paper-brief.py` still recognizes every name the template has had, so that it refuses to ingest into the template. |

### Branches and repository settings

| Item | Class | Destination |
| --- | --- | --- |
| `dev` | kept | The default and integration branch. |
| `main` | kept | The release branch. Its required checks move from the retired jobs (`harness`, `latex (*)`, `release-package`) to `structure`, `check`, `paper-only` and `references` (D4). |
| `template-dev` | rejected | Its tip is tagged `archive/template-dev`, then the branch is deleted (D5). |
| `case/*`, `case-from-scratch-writing` | kept untouched | DEC-0014; see `project/protected-case-branches.md`. |
| Repository description | adapted | "Paper template built on coding-agent-project-template: develop a paper like code" (D4). |

### Maintainer decisions

The questions that were the maintainer's to answer were asked together, once:

- **D1**: drop CCFA-Skills (the 17 `ccf-*` wrappers and their snapshot) and
  `writing-dna-skill` (with `knowledge/writing/`) as a whole; keep
  `lieflat-less-ai-tone` as a standalone MIT skill with its licence and
  provenance.
- **D2**: replace the release-instance tooling (`release.py` and `release.sh`,
  release records, `check-release*.py`, `build-release.yml`) with tags,
  `RELEASE_NOTES.md` and `make release-check`.
- **D3**: keep `paper-brief.py` inside the `paper-brief-ingest` package, fix
  #154 with a regression test, and make `BRIEF.md` the starter record
  `project/brief.md`.
- **D4**: when the work is pushed, move `main`'s required checks to the new job
  names and set the repository description.
- **D5**: tag the `template-dev` tip `archive/template-dev`, then delete the
  branch.
- **D6**: harvest the maintainer's unlicensed `scientific-writing` skill with
  an attribution note.
- **D7**: harvest `image-to-editable-ppt` (MIT) with a recorded patch that
  removes its fallback reading another tool's login.
- **D8**: no coding-template release is newer than `v0.1.13`, so the upgrade
  dry run replays `v0.1.12` to `v0.1.13` on a scratch copy.

### Open Issues (#156 §8)

- **#152** (the standing paper-run collaboration contract): carried over as
  `project/paper-run-boundary.md`. The template stays a versioned foundation,
  and `paper-run` depends on a release tag, never on `dev`.
- **#154** (`paper-brief.py ingest` split multi-line bullets in the locked
  section): fixed. Items keep their continuation lines; regression tests
  cover a wrapped locked bullet and continuation lines in every list section,
  including the style section.
- **#155** (an `external-latex` adoption blocked by canonical-variant test
  fixtures): obsolete. Build profiles, variants, the profile-specific tests
  and `template-adoption.py verify --builds` are retired. A publisher-native
  source stays in `paper/` with its own document class and gains the two build
  switches. Every shipped test builds its own fixture in a temporary
  directory, so no test assumes this template's paper layout.

## Why

The papers built from this template had already simplified it: one canonical
`paper/` built three ways, Overleaf mirroring only `paper/`, and root contracts
moved into records. They had also kept growing shared skills by hand. The
coding template provides the rest of the machinery a paper needs to be
developed like code: Issue worktrees, `.project/` state, an asset manifest, a
content registry, and the adoption, upgrade and feedback procedures. Building
on it removes this template's heavier copies of that machinery
(`template-sync`, release instances, build profiles, variants, documentation
contracts). Upstream fixes then arrive through `template-upgrade`, and lessons
learned in one paper reach the others through this template.

## Apply

- Read this record to find where a pre-v0.4.0 file, tool, test, skill or
  decision went. `RELEASE_NOTES.md` (v0.4.0) explains how a `template-sync`
  downstream moves over.
- Inherited files stay verbatim. Adapt them only in their `## In this
  repository` sections, take upstream changes through `template-upgrade`, and
  report inherited defects upstream through `template-feedback`.
- Restoring a retired mechanism (variants, release instances, build profiles,
  `template-sync`) needs a new Issue and the maintainer's decision.
- A paper made from the template deletes this record (`scope: template`).
