---
name: publication
date: 2026-10-20
source: the template's publication contract (PUBLICATION.md before v0.4.0), moved into a record by Issue #156
scope: project
applies_to: this paper's venue, builds, Overleaf project and releases
status: active
supersedes: null
superseded_by: null
---

# Publication plan

## Decision

| Item | Value |
| --- | --- |
| Target venue, year and track | unresolved |
| Venue facts used | a dated record in `.agents/knowledge/shared/` or `project/`, or unresolved |
| Official kit | unresolved (URL and SHA-256 of the files used) |
| Page budget | `PAGE_BUDGET` unresolved; measured on the blind build |
| Builds | `main`, `submission` and `blind` from one source |
| Overleaf | none yet (remote `overleaf`, branch `main`, tree `paper/`) |
| Release authority | Human |

Releases are tags on `main`, recorded in `RELEASE_NOTES.md`:

| Tag | Form | Date | Commit | Notes |
| --- | --- | --- | --- | --- |
| — | none yet | — | — | — |

Use tag names that say what was delivered, such as `submit-<venue>-<yyyy>`,
`arxiv-v1` or `camera-ready-<venue>-<yyyy>`. A tag is never moved or reused; a
new delivery gets a new tag.

## Why

The three builds differ only by removal
([`../shared/one-source-three-builds.md`](../shared/one-source-three-builds.md)),
so the publication plan is a short list of facts and decisions rather than a
set of variant files: which venue rules apply, which kit typesets the paper,
which budget binds and which tag holds each delivered version.

## Apply

- Before deadline-sensitive work, check the venue's knowledge record and its
  `refresh_after` condition; official dates are hard constraints, internal
  milestones are not.
- Human review is needed before adding a build, changing what a build shows
  (identity, acknowledgements, appendix), accepting a difference between two
  delivered versions, and creating a release tag.
- Overleaf mirrors `paper/` on `dev`: `.agents/scripts/overleaf-sync.sh`
  (`status` before the first edit of a session, `pull` onto a branch for a PR,
  `push` after a merge). Record the Overleaf project here by its remote name
  only; the project URL and the token stay in the local Git configuration and
  credential helper.
- A release: `make release-check` on `dev`, a PR from `dev` to `main`, the
  Human's approval, the merge, the tag on the merge commit, and a
  `RELEASE_NOTES.md` entry naming the tag, the form and the PDF's SHA-256. A
  local build does not prove that a venue, Overleaf or arXiv accepted the
  upload; record that separately.
- Per-paper layout preferences (float placement, last-line targets) are
  recorded here, as the slots of
  [`../shared/post-build-visual-inspection.md`](../shared/post-build-visual-inspection.md).
