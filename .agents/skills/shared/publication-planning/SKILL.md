---
name: publication-planning
description: Use when choosing or changing the target venue, a deadline, the page budget, anonymity or what the main, submission and blind builds remove, and for every Overleaf status, pull or push request.
---

# Publication Planning

## Trigger

Use when choosing or changing the target venue, a deadline, the page budget,
anonymity, the official venue kit, or what the `main`, `submission` and `blind`
builds remove; and for every Overleaf status, pull or push request.

Use `release-review` to prepare a tagged release.

## Minimum context

- `.agents/memory/project/publication.md` (venue, page budget, builds,
  Overleaf, release tags);
- `PAPER.md` and the decision records it links;
- `.agents/memory/shared/one-source-three-builds.md`;
- the active venue entry `.agents/knowledge/shared/venue-<venue>-<year>.md`
  when a concrete venue is active;
- `.agents/memory/project/paper-interfaces.md` only when a result, term,
  notation, claim or artifact could differ between builds;
- for Overleaf, `.agents/memory/shared/overleaf-paper-tree-only.md` and
  `sync-overleaf-before-editing.md`.

Do not load unrelated venue entries until a concrete venue is active.

## Venue and builds

1. Identify whether the request changes the one paper source, what a build
   removes, or the venue plan.
2. For an active venue, load its entry and check its sources and
   `refresh_after` before treating deadlines, page limits, anonymity or
   operational rules as current. When the entry is missing or due for refresh,
   read the official pages and write or refresh it from
   `.agents/knowledge/VENUE_TEMPLATE.md` through `project-memory-governance`,
   with its sources and a refresh condition.
3. Treat official deadlines and limits as hard constraints. Derive internal
   writing, experiment, review and approval buffers without labeling them
   official deadlines.
4. Keep scientific and narrative changes in the one source; never copy
   sections or keep a branch per build. The builds differ only by removal:
   `submission` drops author notes, and `blind` also drops identity and
   acknowledgements. A difference that would add or change content in one
   build only does not fit this layout; bring it to the Human as a decision
   packet.
5. Use the venue's official LaTeX kit unmodified
   (`.agents/memory/shared/official-venue-kit-unmodified.md`,
   `.agents/knowledge/shared/official-latex-templates.md`): adapt the paper to
   the kit, never the kit to the paper.
6. Record the venue's main-text page limit in `publication.md`, place
   `\label{PaperMainTextEnd}` in `paper/main.tex` at the end of the part the
   venue counts, and measure the blind build with `make check PAGE_BUDGET=<pages>`
   (`.agents/memory/shared/page-budget-on-blind-build.md`).
7. Build every affected form (`make pdf`, `make submission`, `make blind`), run
   `make check`, and look at the rendered pages
   (`.agents/memory/shared/post-build-visual-inspection.md`) for anonymity,
   authors, acknowledgements, appendix and interface behavior.
8. Update `publication.md`, and the venue entry when venue facts changed.
9. Report external venue or platform behavior as unverified unless actually
   exercised.

## Overleaf

Overleaf receives only the `paper/` tree, never the repository root
(`overleaf-paper-tree-only.md`). The Overleaf remote lives in local Git
configuration, without a token in its URL, and its credentials only in Git's
credential helper; never write the Overleaf URL, project id or a token into a
tracked file.

1. Start with `bash .agents/scripts/overleaf-sync.sh status`, and before the
   first edit of a session follow `sync-overleaf-before-editing.md`.
2. When Overleaf holds edits (`overleaf-ahead` or `diverged`), run
   `overleaf-sync.sh pull`: it puts them on a `sync/overleaf-<commit>` branch
   on top of the last state both sides had. Review its diff, run `make check`
   on it and open a PR to `dev`.
3. Run `overleaf-sync.sh push` only when the Human asks, only from `dev`, and
   never force-push. `push --replace` overwrites online edits and needs Human
   approval first.
4. The sync is done only when a fresh `status` reports `in-sync`; report a
   partial sync as incomplete.

A poster kept in a second Overleaf project uses
`--remote overleaf-poster --tree poster`.

## Human decision

The Human approves the venue, any difference between builds beyond the
standard removals, scientific exceptions, Overleaf pushes that would discard
online edits, and every release (`release-review`).
