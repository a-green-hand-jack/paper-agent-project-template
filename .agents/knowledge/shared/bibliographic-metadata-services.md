---
name: bibliographic-metadata-services
date: 2026-10-20
source: this template's reference-integrity contract (REFERENCES.md, last changed 2026-09-02 by #153) and the locked dependencies in .agents/scripts/reference-integrity/, moved into a record by Issue #156; DBLP and OpenReview behavior observed 2026-10-20 (#165)
scope: shared
applies_to: paper repositories that run the online reference audits in .agents/scripts/
status: active
refresh_after: when bibtex-updater or pybtex changes version in uv.lock, or when a service changes its API, rate limits or key requirements
supersedes: null
superseded_by: null
---

# Bibliographic metadata services used by the reference audits

## Fact

- **Tools.** The online audits use `bibtex-updater==1.6.1` (MIT, marked Beta
  upstream; core dependencies only): `bibtex-check` in non-generative mode for
  identity and `bibtex-update` for correction candidates. `pybtex==0.26.1`
  (MIT) parses classic BibTeX for the format gate. The complete dependency
  graph is locked in `.agents/scripts/reference-integrity/uv.lock`; nothing is
  vendored or read by `paper/`. They need Python 3.10+ and `uv`.
- **Services.** The identity audit queries Crossref, OpenAlex, DBLP, OpenReview
  and Semantic Scholar. Google Books and Zotero are not used (the audit passes
  `--no-google-books`; the locked core excludes Zotero), nor are the optional
  Scholar, organizer, embedding or LLM extras.
- **Variables.** Trusted local runs read the ignored root `.env` with a strict
  parser that accepts only these names; already exported values win:
  - `BIBTEX_CHECK_MAILTO`: a monitored contact address for the Crossref and
    OpenAlex polite pool; not a secret.
  - `OPENALEX_API_KEY`, `S2_API_KEY`: optional API keys; secrets.
- **CI.** The contact is a repository variable and each key a repository
  secret (`gh variable set BIBTEX_CHECK_MAILTO`, `gh secret set OPENALEX_API_KEY`,
  `gh secret set S2_API_KEY`). Pull-request jobs run keyless because they
  execute contributor-controlled code; pushes to protected branches and manual
  runs (which check out `main`) use the secrets at step scope only. Uploaded
  artifacts are an explicit list of reports; environments and HTTP/SQLite
  caches are excluded because request URLs can contain keys. Missing keys
  degrade to keyless access.
- **Rate limits.** The wrapper uses one worker and a conservative request rate,
  runs at most 12 minutes, and reuses its SQLite cache. HTTP 429 or the
  checker's circuit breaker is recorded as `rate_limited`; network failures and
  timeouts without a status as `provider_unavailable`. Neither blocks CI or
  classifies a reference as false.
- **DBLP bot challenge.** DBLP answers automated search requests, locally and
  on GitHub-hosted runners, with HTTP 202 and an HTML challenge page, which
  `bibtex-check` 1.6.1 reads as "no hits" without an error. The wrapper runs
  the checker with `--verbose`, finds the 202 in its HTTP log (and keeps that
  log, which holds request URLs, out of the console and the reports), records
  `bot_challenged_services`, and treats an `unverified` result in that run as
  `provider_unavailable`. A positive problem still fails.
- **OpenReview-only venues.** `bibtex-check` 1.6.1 takes an OpenReview
  record's year from `content.year` or a year inside `content.venue`; COLM
  records have neither (`venue` is `COLM`, the year is only in `venueid`), and
  `COLM` does not match `First Conference on Language Modeling`. A COLM entry
  therefore ends `venue_mismatch` (full name) or `strict_warn_cnv` with the
  year unconfirmed (abbreviation). The wrapper reports instead of failing such
  a record when the checker matched the OpenReview record, only `year` or
  `venue` differ, and the ledger records the reference `verified` from
  `openreview` and `agent-resolved` or `human-confirmed`
  (`ledger_reviewed_openreview_keys`). It does not patch the locked package.
- **Upstream state.** Later `bibtex-updater` releases map `COLM` to its full
  name (1.11.0) and report DBLP's 202 as a lookup that did not complete
  (1.12.0), so a lock upgrade, which is a separate change, takes both. 1.12.0
  still reads no year from an OpenReview `venueid` or `pdate`; that is
  reported upstream ([rpatrik96/bibtexupdater#82](https://github.com/rpatrik96/bibtexupdater/issues/82)).
- **Assessed and not adopted:**
  - `color4-alt/CiteCheck`, default branch at
    `fae7888bf7c1ce92bbafad15faf61cf55b7e2bd7`, reviewed 2026-08-08: MIT, but no
    tag or release, an unlocked Alpha package, Markdown-only output, no failing
    exit status, first-result title matching, and it reads an inherited
    `OPENAI_API_KEY` and may send manuscript context to an LLM.
  - Paper-BibChecker: no declared software licence or tagged release, and it
    follows arbitrary URLs from contributor-controlled BibTeX.

## Evidence

- `REFERENCES.md` of this template at v0.3.1 and #153; `uv.lock` and
  `THIRD_PARTY.md` in `.agents/scripts/reference-integrity/`.
- 2026-10-20 (#165): a DBLP search request answered `202 Accepted` with
  `text/html`, and keyless `bibtex-check` runs with the wrapper's options on a
  public COLM 2024 entry gave `venue_mismatch` (`mismatched_fields: [venue]`)
  and, with `booktitle={{COLM}}`, `strict_warn_cnv` (`[year]`), each with
  OpenReview among the sources and no error recorded.

## Refresh

When `uv.lock` changes: change the exact version in the dependency project,
regenerate the lock, read the diff and the third-party licences, run the
fixture tests, and try a small known-good and known-bad bibliography before
merging. Reconsider an assessed tool only when it has tagged releases, locked
dependencies, non-generative fail-closed operation, stable JSON output and exit
codes, provider-failure classification and field-level matching.
