---
name: bibliographic-metadata-services
date: 2026-10-20
source: this template's reference-integrity contract (REFERENCES.md, last changed 2026-09-02 by #153) and the locked dependencies in .agents/scripts/reference-integrity/, moved into a record by Issue #156; DBLP and OpenReview behavior observed 2026-10-20 (#165); keyless OpenAlex and Semantic Scholar responses and the tools' backoff code read 2026-10-20 (#171); shared credential file as the preferred key source (#176)
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
- **Variables.** Trusted local runs read only these names, never by shell
  evaluation. The preferred source is the device's shared credential file,
  reached through `.project/credentials/.env` (the canonical checkout's link,
  and in a worktree its `.project/credentials` link; `llm-credentials`): every
  other key in it is skipped and never exported. The fallback is the ignored
  root `.env`, which belongs to the project alone and fails on any other name.
  Exported values win over the root `.env`, and the root `.env` over the
  shared file:
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
- **Rate limits.** The wrappers use a conservative request rate per service.
  HTTP 429 or the checker's circuit breaker is recorded as `rate_limited`;
  network failures and timeouts without a status as `provider_unavailable`.
  Neither blocks CI or classifies a reference as false.
- **Keyless budgets (observed 2026-10-20, #171).** Keyless OpenAlex charges 10
  credits per search against 1000 a day per address (its `x-ratelimit-*`
  headers), so about 100 searches; once they are spent it answers 429 with a
  `Retry-After` of hours. The adaptive limiter of `bibtex-check` 1.6.1 (and of
  1.12.0) sleeps for that whole `Retry-After`; `bibtex-update` caps each retry
  at 60 s but retries six times per request. Without `OPENALEX_API_KEY` both
  audits therefore skip OpenAlex by opening the tool's own circuit for it in
  their cache (`skipped_services`). Keyless Semantic Scholar shares one global
  pool and answers 429 to a large share of requests; each costs retries of
  seconds to a minute. Only `200` responses are cached, so a request that
  ended in 429 is sent again by the next run.
- **Caps, workers and cache.** Each audit runs the tool in its own process
  group and ends the group at `--timeout` (default 3600 s; CI: 600 s in the
  changed tier, 1800 s on the release path, 5400 s in the weekly full audit).
  A capped metadata run reports `checked_keys` and `unfinished_keys`. Four
  workers share each service's rate limit; on 20 public entries without keys
  they finished a cold audit in 201 s against 519 s for one (2026-10-20). The
  HTTP caches are in `.project/build/reference-integrity/cache/`, one CI cache
  per audit; CI restores and saves them on every run, after the audits removed
  each row that holds an API key.
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
