# Shared knowledge rules and index

This directory contains dated facts whose source and refresh condition can be
used across projects. Every record is a separate Markdown file with the fields
in [`../entry-template.md`](../entry-template.md), a registry-owned refresh condition.

<!-- registry-index:start -->
- [agent-session-messaging.md](agent-session-messaging.md) — Dated native messaging, naming, bootstrap and caller-context observations.
- [bibliographic-metadata-services.md](bibliographic-metadata-services.md) — Services, variables and secrets of the online reference audits.
- [credential-inventory.md](credential-inventory.md) — Credential inventory formats and value-free validation/probe behavior.
- [gpt5-strict-backend-requests.md](gpt5-strict-backend-requests.md) — Dated request shapes rejected by strict backends; refresh when clients or providers change.
- [official-latex-templates.md](official-latex-templates.md) — Official publisher and venue kits and their authorities as last compiled by the retired smoke tests.
- [venue-iclr-2027.md](venue-iclr-2027.md) — Dated ICLR 2027 facts and kit hashes; refresh at the decisions and the camera-ready instructions.
- [venue-icml-2026.md](venue-icml-2026.md) — Dated ICML 2026 facts and kit hashes; ICML 2027 unknown until its call is published.
- [venue-neurips-2026-poster.md](venue-neurips-2026-poster.md) — Dated NeurIPS 2026 poster sizes and print deadlines; recheck before ordering.
- [venue-template.md](venue-template.md) — Record shape for a venue's submission facts; unknown values stay UNKNOWN.
<!-- registry-index:end -->

## In this repository

A venue record starts from [`venue-template.md`](venue-template.md); a value no
official page states stays `UNKNOWN`.
