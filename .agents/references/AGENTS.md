# Reference records rules

Two uses of external papers have distinct authority:

- Manuscript citations support claims. The product bibliography is
  `paper/refs.bib`; this directory's ledger and policy hold the development
  evidence for the cited identities and individual claim occurrences.
- Writing and design exemplars teach presentation. They are not citations or
  evidence merely because they are useful examples. Keep durable, sourced
  exemplar cards in `exemplars/` and downloaded material in
  `.project/artifacts/writing-exemplars/`; use `paper-writing`.
  A work used for both purposes still needs independent citation review.

- `ledger.json` — the reference ledger (`paper-reference-ledger-v2`): the
  identity of every entry of `paper/refs.bib`, how each cited key is used,
  every citation occurrence and the claim evidence bound to it.
- `policy.json` — `enforcement` (`enforced` or `disabled`, together with the
  activation marker at the top of `paper/refs.bib`), the ledger and
  bibliography paths, and `bibliography_origin` (`agent-curated`, or
  `supplied-fixed` for a read-only bibliography supplied with the task).

The rules are in
[`../memory/shared/reference-integrity.md`](../memory/shared/reference-integrity.md).
Change the ledger through `.agents/scripts/shared/paper-references/reference_evidence.py` and the
`paper-references` skill, never by copying an
empty ledger over a populated one. `check_reference_metadata.py --record`
writes only `verification.bibtex_fingerprint`, the fingerprint of the entry it
verified online. Online reports, caches and support packets
are rebuildable and go under `.project/build/`, not here.
