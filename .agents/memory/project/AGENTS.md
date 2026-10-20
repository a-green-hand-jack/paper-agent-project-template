# Project memory rules and index

This directory contains decisions owned by this repository. Every record is a
separate Markdown file with the fields in
[`../ENTRY_TEMPLATE.md`](../ENTRY_TEMPLATE.md), `scope: project`, and an active
or superseded status. A paper records its own decisions here, one topic per
file; a decision replaced later is marked superseded and names its successor.

## Index

The paper's records (starters that a paper made from this template fills):

- [`brief.md`](brief.md) — the Human-authored brief the paper starts from.
- [`experiments.md`](experiments.md) — the evidence questions, their
  conditions and interpretation boundaries, linked to manifest entries.
- [`paper-interfaces.md`](paper-interfaces.md) — each interface macro's
  meaning, control cue and source.
- [`publication.md`](publication.md) — venue, kit, page budget, builds,
  Overleaf and release tags.

This template's own records (`scope: template` in the registry; a paper made
from the template deletes them):

- [`rebuild-on-coding-template.md`](rebuild-on-coding-template.md) — the
  v0.4.0 rebuild on coding-agent-project-template: the per-path migration map
  and where each earlier decision went.
- [`protected-case-branches.md`](protected-case-branches.md) — the case
  branches, case Issues and verification trackers are protected evidence.
- [`repository-identity.md`](repository-identity.md) — the repository's name,
  description, positioning and branches.
- [`paper-run-boundary.md`](paper-run-boundary.md) — the template is a
  versioned foundation; paper-run owns the runtime.
