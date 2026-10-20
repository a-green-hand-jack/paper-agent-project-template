# Shared memory rules and index

This directory contains durable decisions that are neutral enough to reuse
across projects. Every record is a separate Markdown file with the fields in
[`../ENTRY_TEMPLATE.md`](../ENTRY_TEMPLATE.md), `scope: shared`, and an active
or superseded status. A record that names parameters for the destination is
registered `shared_with_adaptation`; the destination writes their values in a
trailing `## In this repository` section (see `template-adoption` step 5), and
the record's own text never contains that heading line.

## Index

Inherited from `coding-agent-project-template`:

- [`issue-in-herdr-worktree.md`](issue-in-herdr-worktree.md) — implement each
  Issue in its own Herdr worktree and agent session, which verifies to
  completion, fixes related defects and leaves conflicts to the dev checkout.
- [`issue-close-out.md`](issue-close-out.md) — close out an Issue's worktree
  right after its PR merges; the merge approval covers the close-out.
- [`issue-dispatch-by-difficulty.md`](issue-dispatch-by-difficulty.md) — dispatch
  each Issue agent with an explicit model and effort for its difficulty tier, and
  record it in the Issue.
- [`llm-credentials.md`](llm-credentials.md) — share stable LLM credentials
  through one device file; log refreshing logins in once per canonical checkout,
  whose worktrees link to them; never pass a credential as a command-line
  argument. Here only the optional `image-to-editable-ppt` CLI uses one.
- [`product-state-root.md`](product-state-root.md) — commands find the
  worktree's state root from an argument, a variable, the setup marker, then a
  default; here the paper's build directory.
- [`resolve-real-paths-before-moving.md`](resolve-real-paths-before-moving.md)
  — before moving, replacing or symlinking a directory, resolve both paths and
  stop on overlap.
- [`third-party-llm-compat-patches.md`](third-party-llm-compat-patches.md) —
  changes to third-party LLM tools live in the repository; check one captured
  request body before a batch; no retry-without-the-parameter fallbacks.

Papers:

- [`one-source-three-builds.md`](one-source-three-builds.md) — `main`,
  `submission` and `blind` come from one source in a fixed order, each removing
  a layer; notes vanish from the later forms.
- [`results-through-interface-macros.md`](results-through-interface-macros.md)
  — reported numbers reach the text only through interface macros with a
  manifest source; planned results are never observations.
- [`reference-integrity.md`](reference-integrity.md) — bibliographic identity
  and claim support are separate, occurrence-level obligations.
- [`page-budget-on-blind-build.md`](page-budget-on-blind-build.md) — measure
  the page budget on the anonymous build, keep a margin, report an overage.
- [`post-build-visual-inspection.md`](post-build-visual-inspection.md) — look
  at the rendered pages before calling a build done.
- [`official-venue-kit-unmodified.md`](official-venue-kit-unmodified.md) — use
  the venue's official kit unmodified; a migration changes typesetting only.
- [`tex-engine-from-texbin.md`](tex-engine-from-texbin.md) — TeX binaries come
  from an overridable `TEXBIN`; build leftovers stay out of tracked trees.
- [`overleaf-paper-tree-only.md`](overleaf-paper-tree-only.md) — Overleaf
  receives `HEAD:paper` as a fast-forward, checked by tree, never the root.
- [`sync-overleaf-before-editing.md`](sync-overleaf-before-editing.md) — take
  in Overleaf edits before writing, and deliver to both sides together.
- [`skill-frontmatter-validity.md`](skill-frontmatter-validity.md) — every
  `SKILL.md` front matter parses; re-check after every skill change.
