---
name: reference-integrity
date: 2026-10-20
source: this template's reference-integrity contract (REFERENCES.md before v0.4.0, Issues #80-#153), moved into a record by Issue #156
scope: shared
applies_to: paper repositories that cite literature from paper/refs.bib and keep a reference ledger
status: active
supersedes: null
superseded_by: null
---

# Bibliographic identity and claim support are separate obligations

## Decision

1. **Identity and support are different questions.** A work can exist with
   correct metadata and still fail to support the sentence that cites it.
   Neither a resolving DOI nor an automated verdict approves scientific
   meaning.
2. **Durable records.** `paper/refs.bib` is the bibliography LaTeX uses;
   `.agents/references/ledger.json` (`paper-reference-ledger-v2`) is the
   reviewable ledger of `references`, `citation_usages`,
   `citation_occurrences` and `claim_evidence`, kept as arrays so that
   duplicates cannot hide; `.agents/references/policy.json` holds the
   enforcement switch and the `bibliography_origin`. Online reports, caches and
   support packets are rebuildable output under `.project/build/`.
3. **Reference identity has three states:** `verified` (external metadata
   positively matches), `problematic` (positive evidence of a mismatch or
   defect) and `unverified` (no available source could decide; never
   "fabricated"). Network failures, rate limits and bot-challenge pages are
   infrastructure outcomes in the reports, never states in the ledger. An
   agent may record an unambiguous verified identity as `agent-resolved`;
   `human-confirmed` is reserved for a choice the Human made. When the online
   audit matches a reference's OpenReview record and differs from the cited
   entry only in its year or venue name, a ledger identity verified from
   OpenReview and resolved or confirmed is reported, not failed: the locked
   checker cannot read the year or the venue abbreviation of some OpenReview
   venues (COLM), and the review already decided them.
4. **Claim support is bound to citation occurrences.** Every TeX citation
   occurrence is inventoried with its claim text and a fingerprint. Each claim
   evidence record carries the source identity and version, a verbatim passage
   with locator and hash, and a verdict: `supported`, `partially-supported`,
   `unsupported`, `contradicted` or `source-unavailable`. Two claims citing one
   key need separate evidence. Only a Human marks claim evidence
   `human-confirmed`.
5. **Evidence goes stale** when the claim fingerprint, the citation set, the
   source version, the passage hash or the protocol version changes. Draft
   warns; Release fails.
6. **Profiles.** Draft blocks malformed ledgers, duplicate or uncovered keys
   and `problematic` references and keeps the rest visible as warnings. Release
   fails closed on every unresolved reference or claim review, every missing or
   stale occurrence and every substantive claim without Human-confirmed
   support.
7. **A supplied fixed bibliography** (`bibliography_origin: supplied-fixed`)
   is read-only: a key's presence is enough to cite it at Draft strength,
   recorded as provisional. Release still requires Human-confirmed support.
8. **Activation.** The marker
   `% REFERENCE_INTEGRITY_REQUIRED: .agents/references/ledger.json` in
   `paper/refs.bib` and `"enforcement": "enforced"` in the policy go together;
   removing either while the other remains is an error, never a bypass.
9. **Tools never rewrite the bibliography or the prose.** Correction tools
   write candidates under `.project/build/`; the agent inspects the evidence
   and edits `paper/refs.bib` and the ledger. A Human decides only when several
   plausible identities or versions remain and the choice can change claim
   support.

## Why

Agents produce plausible references that do not exist, real references that do
not say what the sentence claims, and correct references attached to the wrong
version of a work. Keeping identity, use and support as separate,
occurrence-level records makes each failure visible and reviewable, and
separating infrastructure outcomes from verdicts keeps a rate limit from
looking like a fabricated citation.

## Apply

- `make check` runs the offline gate:
  `python3 .agents/scripts/check-reference-integrity.py --profile draft`;
  `make release-check` runs `--profile release` and the full online metadata
  audit of every entry, which needs `uv` and the network.
- Inventory and record support with `.agents/scripts/reference-evidence.py`
  (`inventory`, `packet`, `record`; `migrate` upgrades a v1 ledger), following
  the `citation-support-review` skill. Occurrence-level review is new in v2,
  so every occurrence `migrate` writes starts `pending` and needs a fresh
  Human confirmation before `make release-check`.
- Optional checks with the locked dependencies in
  `.agents/scripts/reference-integrity/` (needs `uv`):
  `check-bibtex-format.py` (classic BibTeX syntax and required fields),
  `check-reference-metadata.py` (online identity audit, non-generative) and
  `check-reference-corrections.py` (correction candidates). CI runs them
  keyless on pull requests and with repository secrets on protected branches;
  see the bibliographic-metadata-services knowledge record for the services
  and variables.
- **Audit tiers.** The required `references` job audits online only the
  entries new or changed against the base commit, or whose
  `verification.bibtex_fingerprint` in the ledger no longer matches
  (`--scope changed --base <commit>`); an unchanged, fingerprinted entry is
  never queried there. A pull request into `main` and a push to `main` run the
  full audit, and so does `make release-check`. The `references-full` job
  runs the full audit weekly and on `workflow_dispatch`, both audits in
  parallel with a kept cache; it reports and blocks no merge. A provider
  outage, rate limit or bot challenge is an infrastructure outcome that names
  the entries it left open, never a failed entry.
- **Fingerprints.** `check-reference-metadata.py --record` writes the
  fingerprint of each entry it verified into the ledger and drops it from an
  entry with a positive problem. Run it once after adopting the tiers, with
  the full scope, and commit the ledger; afterwards a changed entry loses its
  match and is queried again automatically.
- Repair a reference with the `reference-repair` skill. Never copy an empty
  template ledger over a populated one.
