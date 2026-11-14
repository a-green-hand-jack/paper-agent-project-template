---
name: paper-publication
description: Plan paper submission and publication, operate Overleaf synchronization or build a paper-derived poster.
---

# Paper publication

Respect the Human's venue, anonymity, page-budget and release choices. The three paper builds share one source; Overleaf receives only `HEAD:paper` through the project's sync command. A release or external publication requires the Human's approval.

Release order is fixed: prepare on `dev`, pass `make check` and `make release-check`, open the `dev` -> `main` pull request, merge it, and only then create the release tag on `main` and publish the release notes. Never tag a `dev` commit, and never release from a branch other than `main`.

- [Publication commands](../../../scripts/shared/paper-publication/)
- [Publication planning and Overleaf](sources/publication-planning/reference.md)
- [Paper release review](sources/release-review/reference.md)
- [Poster build](sources/poster-build/reference.md)

Overleaf edits are taken in by tree, byte for byte
([`overleaf-tree-is-authoritative`](../../../memory/shared/paper-publication/overleaf-tree-is-authoritative.md)).
