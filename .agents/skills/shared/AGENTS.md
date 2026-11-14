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
summaries and message cadence. Its
`references/acceptance-scenarios.md` reviews their shared boundary without
claiming fixture review proves a real exchange.

`development-writing/` owns the common writing principles and four development
record types; `references/four-cases.md` holds transferable weak/rewrite examples.
Concrete historical cases stay outside shared packages.

`release-doc-audit/` covers release writing, rendered visual review and the
existing consistency audit; its `references/release-types.md` distinguishes
product upgrades, results, milestones/archives and concise releases. Keep
concrete project release examples outside shared packages.

<!-- registry-index:start -->
- [.gitattributes](.gitattributes) — Vendored files keep their upstream bytes; per-file whitespace exceptions live here.
- [.gitattributes](.gitattributes) — Whitespace exceptions for vendored files that keep upstream bytes git diff --check would report; extend it when vendoring such a file.
>>>>>>> bb380d1 (fix: keep the upgrade tests honest after the prune (#229))
- [agent-communication](agent-communication/SKILL.md) — Resolve native addresses, reconcile backlog and record distinct delivery/receipt outcomes.
- [asset-lifecycle](asset-lifecycle/SKILL.md) — Adapt asset classes, storage roots and migration evidence.
- [benchmark-radar](benchmark-radar/SKILL.md) — Benchmark discovery, records and recent Radar evidence; vendored MIT from ktwu01/benchmark-radar@21f3018, PROVENANCE.md.
- [cli-first-operations](cli-first-operations/SKILL.md) — Use the project's public CLI instead of ad-hoc wrappers.
- [credential-setup](credential-setup/SKILL.md) — Set up declared project credentials without copying logins or exposing values.
- [development-writing](development-writing/SKILL.md) — Write Issues, PRs, comments and commits around reader decisions and traceable evidence.
- [engineering-change](engineering-change/SKILL.md) — Implement, debug and refactor code with behavior-focused evidence.
- [issue-workflow](issue-workflow/SKILL.md) — Scope, dispatch, protect acceptance inputs, integrate and close an Issue with explicit ownership.
- [paper-figures](paper-figures/SKILL.md) — Scientific data figures and editable diagrams.
- [paper-foundation](paper-foundation/SKILL.md) — Paper context, brief, control decisions and stable interfaces.
- [paper-publication](paper-publication/SKILL.md) — Paper publication, Overleaf and posters.
- [paper-references](paper-references/SKILL.md) — Manuscript citation identity and claim support.
- [paper-review](paper-review/SKILL.md) — Manuscript consistency and peer-review triage.
- [paper-writing](paper-writing/SKILL.md) — Paper writing, structure, language and proofreading.
- [project-memory-governance](project-memory-governance/SKILL.md) — Classify, register and migrate development content without losing provenance or authority.
- [release-doc-audit](release-doc-audit/SKILL.md) — Draft readable release narratives and audit rendered output, versions and upgrade paths.
- [template-adoption](template-adoption/SKILL.md) — Adapt the target repository's rules, product paths and acceptance commands.
- [template-feedback](template-feedback/SKILL.md) — Adapt the canonical template URL, labels and upstream Issue fields.
- [template-upgrade](template-upgrade/SKILL.md) — Adapt current and target release tags, local conflicts and migration evidence.
- [worktree-lifecycle](worktree-lifecycle/SKILL.md) — Create, verify and retire isolated worktrees after responsibility and state handoff.
<!-- registry-index:end -->

## In this repository

Vendored third-party resources: a third-party package is vendored only under a
licence that allows it, or with its author's permission recorded in its
`PROVENANCE.md`. Its package holds:

- the upstream files needed to use the resource, byte for byte, and the upstream
  `LICENSE` unchanged;
- `PROVENANCE.md`: the upstream repository, path and full commit, the licence
  and holder, a table of every file with the SHA-256 of the upstream bytes and
  its status (`unchanged`, `unchanged above ## In this repository`, `patched`),
  each excluded upstream file with the reason, and every local change as a
  unified diff;
- this repository's notes in the trailing `## In this repository` section of
  the source's `reference.md`, unless a patch is recorded.

`make check` re-hashes unchanged files against each nested `PROVENANCE.md`;
patched files require their recorded diffs to be reviewed. To update a vendored
resource, replace the upstream files from the new commit, update the table, keep
the trailing section, re-apply each recorded patch, and run `make check`.
Never edit upstream text in place. When an upstream file carries whitespace
that `git diff --check` reports, list that file in `.gitattributes` here
instead of changing its bytes. Upstream file names that break the naming rules
keep them through reasoned `policy.naming_exceptions` in the registry.

A third-party skill a project installs itself belongs in `project/` as its own
package with its own `PROVENANCE.md`, not directly under `.agents/skills/`; an
installer's root lock file, such as `skills-lock.json`, is local installation
state and stays out of Git.
