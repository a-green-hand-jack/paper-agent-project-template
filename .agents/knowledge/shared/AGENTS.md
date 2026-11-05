# Shared knowledge rules and index

This directory contains dated facts whose source and refresh condition can be
used across projects. Every record is a separate Markdown file with the fields
in [`../entry-template.md`](../entry-template.md), a registry-owned refresh condition.

<!-- registry-index:start -->
- [agent-session-messaging.md](agent-session-messaging.md) — Dated native messaging, naming, bootstrap and caller-context observations.
- [credential-inventory.md](credential-inventory.md) — Credential inventory formats and value-free validation/probe behavior.
- [gpt5-strict-backend-requests.md](gpt5-strict-backend-requests.md) — Dated request shapes rejected by strict backends; refresh when clients or providers change.
- [paper-publication/official-latex-templates.md](paper-publication/official-latex-templates.md) — Official publisher and venue kits and their authorities as last compiled by the retired smoke tests.
- [paper-publication/venue-iclr-2027.md](paper-publication/venue-iclr-2027.md) — Dated ICLR 2027 facts and kit hashes; refresh at the decisions and the camera-ready instructions.
- [paper-publication/venue-icml-2026.md](paper-publication/venue-icml-2026.md) — Dated ICML 2026 facts and kit hashes; ICML 2027 unknown until its call is published.
- [paper-publication/venue-neurips-2026-poster.md](paper-publication/venue-neurips-2026-poster.md) — Dated NeurIPS 2026 poster sizes and print deadlines; recheck before ordering.
- [paper-publication/venue-template.md](paper-publication/venue-template.md) — Record shape for a venue's submission facts; unknown values stay UNKNOWN.
- [paper-references/bibliographic-metadata-services.md](paper-references/bibliographic-metadata-services.md) — Services, variables and secrets of the online reference audits.
<!-- registry-index:end -->

## In this repository

A venue record starts from [`venue-template.md`](paper-publication/venue-template.md); a value no
official page states stays `UNKNOWN`.
