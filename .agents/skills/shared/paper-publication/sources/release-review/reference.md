---
name: release-review
description: Use when preparing a tagged paper release, such as a venue submission, an arXiv version or a camera-ready version, for Human approval.
---

# Release Review

## Trigger

Use when preparing a venue submission, an arXiv version, a camera-ready
version or another release that the Human approves and that is tagged on
`main`.

## Minimum context

- `PAPER.md` and `.agents/memory/project/experiments.md`,
  `paper-interfaces.md` and `publication.md`;
- the current decision records in `.agents/memory/project/`;
- the build being released (`blind` for an anonymous submission, otherwise
  `submission`) and the changes since the last release tag;
- the active venue entry in `.agents/knowledge/shared/`, rechecked against its
  official sources.

Do not load historical alternatives unless a current conflict requires them.

## Procedure

1. Confirm with the Human the release tag (`submit-<venue>-<yyyy>`,
   `arxiv-v1`, `camera-ready`) and the build it delivers.
2. For an active venue, recheck the venue entry's official sources before
   relying on deadlines, page limits, anonymity or operational rules, and
   refresh the entry when they changed.
3. On `dev`, add a `## <tag>` entry to `RELEASE_NOTES.md` naming the build and
   what the release contains.
4. Run `make check` and `make release-check PAGE_BUDGET=<pages>`; do not
   suppress or work around a failure. The release check fails on an identity
   string in the blind PDF, its metadata or its sources; on `\PaperTODO`,
   `\PaperNote` or TODO in the submission build; on a missing or exceeded page
   budget; and on references that fail the release profile.
5. List the high-impact changes since the last release tag
   (`git log --oneline <last-tag>..dev`) or since the last Human review.
6. Check claim strength, experiment interpretation, stable interfaces,
   limitations, negative evidence, anonymity, author and acknowledgement
   behavior, appendix inclusion, claim support at Release strength
   (`citation-support-review`), figures, tables and compilation.
7. Look at every rendered page of the delivered build
   (`.agents/memory/shared/post-build-visual-inspection.md`).
8. Mark unavailable external environments, such as a submission portal or
   arXiv processing, as unverified, not successful.
9. Open the release PR from `dev` to `main`, run `release-doc-audit` with
   `TARGET_TAG` set to the tag, and put its report and a short release summary
   in the PR: the reviewed commit and build, blockers, accepted exceptions,
   residual risks and an Agent recommendation.
10. After the Human approves, merge the PR, confirm that the merge commit's
    tree equals the reviewed commit (`git diff <reviewed> <merge>` is empty),
    tag the merge commit with an annotated tag and push the tag. The file to
    deliver is the build made from that tag, `.project/build/<build>.pdf`.
11. Never move, delete or reuse a release tag. A revised release gets a new tag
    (`arxiv-v2`) and its own `RELEASE_NOTES.md` entry.

## Human decision

Only the Human approves a release and accepts explicit residual risk or
exceptions. The approval is bound to the reviewed commit and build; a change to
either after approval needs a new review.
