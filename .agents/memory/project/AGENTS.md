# Project memory rules and index

This directory contains decisions owned by this template repository. Every
record is a separate Markdown file with the fields in
[`../entry-template.md`](../entry-template.md), registry-owned lifecycle and scope.

<!-- registry-index:start -->
- [paper-foundation/brief.md](paper-foundation/brief.md) — Starter record a paper fills from its brief.
- [paper-foundation/experiments.md](paper-foundation/experiments.md) — Starter record of the paper's evidence questions.
- [paper-foundation/paper-interfaces.md](paper-foundation/paper-interfaces.md) — Starter record of the paper's interface macros; make check reads it.
- [paper-foundation/results-ledger.md](paper-foundation/results-ledger.md) — One row per reported result: source repository, commit, run, checksum, regeneration command, macro and use.
- [paper-publication/publication.md](paper-publication/publication.md) — Starter record of the paper's venue, kit, budget, Overleaf and release tags.
- [template-maintenance/ci-tex-install-bounded.md](template-maintenance/ci-tex-install-bounded.md) — Bound the CI Ubuntu mirror preflight and TeX install, and rerun runner DNS failures instead of bypassing required checks.
- [template-maintenance/derived-template-upgrade-command.md](template-maintenance/derived-template-upgrade-command.md) — A derived template follows its upstream with the target release's command directory and keeps the inherited scripts byte-identical.
- [template-maintenance/paper-run-boundary.md](template-maintenance/paper-run-boundary.md) — The boundary between this template and paper-run (#152).
- [template-maintenance/paper-template-extension-boundary.md](template-maintenance/paper-template-extension-boundary.md) — Why the paper template keeps inherited development, paper capabilities and product evidence in distinct boundaries.
- [template-maintenance/protected-case-branches.md](template-maintenance/protected-case-branches.md) — This template's protected case branches and trackers (DEC-0014); a paper records its own.
- [template-maintenance/rebuild-on-coding-template.md](template-maintenance/rebuild-on-coding-template.md) — This template's v0.4.0 migration map; a paper made from the template deletes it.
- [template-maintenance/repository-identity.md](template-maintenance/repository-identity.md) — This template's name, description and branches.
<!-- registry-index:end -->

## In this repository

A paper records its own decisions here, one topic per file. A decision replaced
later is deleted together with its registry entry, and Git keeps its body; the
record that replaces it lists the old ID in `supersedes` as provenance. The
registry never carries `status: superseded` or `status: retired`.

This template ships four starter records (`brief`, `experiments`,
`paper-interfaces`, `publication`) for a paper to fill; a paper rewrites this
sentence to name the records it actually keeps. This template's own records are
`scope: template` in the registry; a paper made from the template deletes them.
