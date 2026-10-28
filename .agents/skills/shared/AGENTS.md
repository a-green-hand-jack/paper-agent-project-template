# Shared skills rules

Shared skills must avoid product names, private paths and provider-specific
assumptions. Each skill states what must be adapted in a destination project,
as slots or steps a destination can extend: destinations write their
adaptations only in a trailing `## In this repository` section (see
`template-adoption` step 5). A skill's own text never contains a line that is
exactly `## In this repository`, not even in an example.
Update the content registry when adding, renaming or retiring a shared skill.

`issue-workflow/` owns acceptance write responsibility; `agent-communication/`
owns transport, receipts, receive-time classification, recoverable terminal
summaries and message cadence. Its `references/acceptance-scenarios.md` reviews
their boundary; scenario review does not prove a real exchange.

`development-writing/` owns the common principles for Issues, PRs, comments
and commits, with neutral examples in `references/four-cases.md`.
`release-doc-audit/` owns release narratives, rendered review and consistency
checks, with release types in `references/release-types.md`. Concrete project
history and examples stay outside these shared packages.

## Vendored third-party skills

A third-party skill is vendored only under a licence that allows it, or with
its author's permission recorded in its `PROVENANCE.md`. Its package holds:

- the upstream files needed to use the skill, byte for byte, and the upstream
  `LICENSE` unchanged;
- `PROVENANCE.md`: the upstream repository, path and full commit, the licence
  and holder, a table of every file with the SHA-256 of the upstream bytes and
  its status (`unchanged`, `unchanged above ## In this repository`, `patched`),
  each excluded upstream file with the reason, and every local change as a
  unified diff;
- this repository's notes only in the trailing `## In this repository`
  section of `SKILL.md`.

`make check` re-hashes every file against `PROVENANCE.md`. To update a vendored
skill, replace the upstream files from the new commit, update the table, keep
the trailing section, re-apply each recorded patch, and run `make check`.
Never edit upstream text in place. When an upstream file carries whitespace
that `git diff --check` reports, list that file in `.gitattributes` here
instead of changing its bytes.
