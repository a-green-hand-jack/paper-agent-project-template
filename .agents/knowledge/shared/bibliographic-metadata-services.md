---
name: bibliographic-metadata-services
date: 2026-09-02
source: this template's reference-integrity contract (REFERENCES.md, last changed 2026-09-02 by #153) and the locked dependencies in .agents/scripts/reference-integrity/, moved into a record by Issue #156
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

## Refresh

When `uv.lock` changes: change the exact version in the dependency project,
regenerate the lock, read the diff and the third-party licences, run the
fixture tests, and try a small known-good and known-bad bibliography before
merging. Reconsider an assessed tool only when it has tagged releases, locked
dependencies, non-generative fail-closed operation, stable JSON output and exit
codes, provider-failure classification and field-level matching.
