# Shared knowledge rules and index

This directory contains dated facts whose source and refresh condition can be
used across projects. Every record is a separate Markdown file with the fields
in [`../ENTRY_TEMPLATE.md`](../ENTRY_TEMPLATE.md), `scope: shared`, and a
refresh or expiry condition. A venue record starts from
[`../VENUE_TEMPLATE.md`](../VENUE_TEMPLATE.md); a value no official page states
stays `UNKNOWN`.

## Index

Inherited from `coding-agent-project-template`:

- [`gpt5-strict-backend-requests.md`](gpt5-strict-backend-requests.md) — the
  three GPT-5.x request shapes strict Responses backends reject, what to send
  instead, and that a relay can hide the rejections. Kept with the two LLM
  memory records it belongs to; no tool here sends such requests.

Papers:

- [`venue-iclr-2027.md`](venue-iclr-2027.md) — ICLR 2027: 9 pages at submission
  and 10 later, unlimited references and appendix, required AI use statement,
  review and decision dates, kit URL and SHA-256 values (checked 2026-10-20).
- [`venue-icml-2026.md`](venue-icml-2026.md) — ICML 2026: 8 pages (9
  camera-ready), impact statement, layout and file-size rules, kit URL and
  SHA-256 values; ICML 2027 still unpublished (checked 2026-10-20).
- [`venue-neurips-2026-poster.md`](venue-neurips-2026-poster.md) — NeurIPS
  2026 posters: 140 x 90 cm landscape, workshops 61 x 85 cm portrait, print
  order deadlines (checked 2026-10-20).
- [`official-latex-templates.md`](official-latex-templates.md) — official
  publisher and venue kits and their authorities, as compiled by this
  template's retired smoke tests (2026-08-27).
- [`bibliographic-metadata-services.md`](bibliographic-metadata-services.md) —
  the locked reference-audit tools, the services they query, their variables,
  CI secrets and rate-limit outcomes, and tools assessed and not adopted.
