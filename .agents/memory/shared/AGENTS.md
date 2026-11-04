# Shared memory rules and index

This directory contains durable decisions that are neutral enough to reuse
across projects. Every record is a separate Markdown file with the fields in
[`../entry-template.md`](../entry-template.md), registry-owned lifecycle and scope. A record that names parameters for the destination is
registered `shared_with_adaptation`; the destination writes their values in a
trailing `## In this repository` section (see `template-adoption` step 5), and
the record's own text never contains that heading line.

<!-- registry-index:start -->
- [host-files-owned-by-running-user.md](host-files-owned-by-running-user.md) — Keep host artifacts owned by the running user and stop at foreign ownership.
- [issue-close-out.md](issue-close-out.md) — Complete or transfer outstanding duties before migrating and retiring an Issue worktree.
- [issue-dispatch-by-difficulty.md](issue-dispatch-by-difficulty.md) — Record agent, provider, model and effort selected by difficulty and cost.
- [issue-in-herdr-worktree.md](issue-in-herdr-worktree.md) — Implement each Issue in its own verified Herdr worktree and independent agent session.
- [llm-credentials.md](llm-credentials.md) — Keep stable shared credentials and project-owned refreshing logins behind local paths.
- [look-at-the-artifact-before-concluding.md](look-at-the-artifact-before-concluding.md) — Inspect referenced artifacts before concluding from automated metrics.
- [official-venue-kit-unmodified.md](official-venue-kit-unmodified.md) — Official kit for the exact venue and year, unmodified with its helper packages; a migration changes typesetting only.
- [one-source-three-builds.md](one-source-three-builds.md) — main, submission and blind from one source in a fixed order, each removing a layer.
- [overleaf-paper-tree-only.md](overleaf-paper-tree-only.md) — Overleaf receives HEAD:paper as a fast-forward checked by tree; never the root, never force.
- [page-budget-on-blind-build.md](page-budget-on-blind-build.md) — Set PAGE_BUDGET in the Makefile and fill PAGE_MARGIN in the trailing section; measured on the blind build.
- [post-build-visual-inspection.md](post-build-visual-inspection.md) — Fill MIN_FIGURE_TEXT and LAST_LINE_FILL; look at the rendered pages before calling a build done.
- [product-state-root.md](product-state-root.md) — Resolve worktree-local product state from the project marker.
- [project-positioning-before-layout.md](project-positioning-before-layout.md) — Establish users, deliverables and domain concepts before choosing paths.
- [provider-cost-routing.md](provider-cost-routing.md) — Use the cheapest capable provider/model and record why each real run is needed.
- [reference-integrity.md](reference-integrity.md) — Identity and claim support are separate, occurrence-level obligations.
- [resolve-real-paths-before-moving.md](resolve-real-paths-before-moving.md) — Prove source and destination differ before moving or replacing assets.
- [results-through-interface-macros.md](results-through-interface-macros.md) — Reported numbers only through interface macros with a manifest source; planned results are never observations.
- [screen-with-scriptable-fakes.md](screen-with-scriptable-fakes.md) — Screen boundary failures with data-driven fakes before applicable real acceptance.
- [skill-frontmatter-validity.md](skill-frontmatter-validity.md) — Every SKILL.md front matter parses; make check re-parses them.
- [speed-and-parallelism-by-measurement.md](speed-and-parallelism-by-measurement.md) — Measure concurrency, remove repeated work and retain every required check.
- [sync-overleaf-before-editing.md](sync-overleaf-before-editing.md) — Take in Overleaf edits before writing and deliver to both sides together.
- [tex-engine-from-texbin.md](tex-engine-from-texbin.md) — TeX binaries from an overridable TEXBIN; build leftovers stay out of tracked trees.
- [third-party-llm-compat-patches.md](third-party-llm-compat-patches.md) — Fill PATCH_DIR for the project's patches or wrappers of third-party LLM tools; they run on every run and state that metrics, prompts and reasoning effort are unchanged.
<!-- registry-index:end -->
