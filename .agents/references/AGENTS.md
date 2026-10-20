# Reference records rules

- `ledger.json` — the reference ledger (`paper-reference-ledger-v2`): the
  identity of every entry of `paper/refs.bib`, how each cited key is used,
  every citation occurrence and the claim evidence bound to it.
- `policy.json` — `enforcement` (`enforced` or `disabled`, together with the
  activation marker at the top of `paper/refs.bib`), the ledger and
  bibliography paths, and `bibliography_origin` (`agent-curated`, or
  `supplied-fixed` for a read-only bibliography supplied with the task).

The rules are in
[`../memory/shared/reference-integrity.md`](../memory/shared/reference-integrity.md).
Change the ledger through `.agents/scripts/reference-evidence.py` and the
`citation-support-review` and `reference-repair` skills, never by copying an
empty ledger over a populated one. `check-reference-metadata.py --record`
writes only `verification.bibtex_fingerprint`, the fingerprint of the entry it
verified online. Online reports, caches and support packets
are rebuildable and go under `.project/build/`, not here.
