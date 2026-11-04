# Scripts shared rules

Follow the category rules and the content registry.
Shared may be empty; do not generalize project implementations just to fill it.

<!-- registry-index:start -->
- [bib_identity.py](bib_identity.py) — Shared BibTeX identity normalization for the reference checks.
- [bounded_run.py](bounded_run.py) — Bounded subprocess runner for the online reference audits.
- [check-development.sh](check-development.sh) — Public development-plane registry and layout check.
- [check-shells.sh](check-shells.sh) — Check every nested development Shell script without missing glob arguments.
- [check_agent_content.py](check_agent_content.py) — Check skill front matter, record structure and vendored-file hashes against the registry.
- [check_bibtex_format.py](check_bibtex_format.py) — Optional BibTeX format audit in the locked reference environment.
- [check_paper_build.py](check_paper_build.py) — Read one build: log problems, main-text pages, PDF underscores, blind identity and leftovers.
- [check_paper_interfaces.py](check_paper_interfaces.py) — Check the interface macros of paper/macros.tex against their record.
- [check_reference_corrections.py](check_reference_corrections.py) — Optional validation of proposed BibTeX corrections.
- [check_reference_integrity.py](check_reference_integrity.py) — Offline reference gate at draft, review and release strength.
- [check_reference_metadata.py](check_reference_metadata.py) — Optional online metadata audit in the locked reference environment.
- [citation_occurrences.py](citation_occurrences.py) — Citation occurrence scanner shared by the reference gate and evidence tool.
- [content_registry.py](content_registry.py) — Validate development identities, naming, provenance, lifecycle and generated indexes.
- [diagnose-environment.sh](diagnose-environment.sh) — Check environment, branch model, adaptation sections and asset visibility.
- [init-branches.sh](init-branches.sh) — Initialize the declared dev/main branch model.
- [inspect-state.sh](inspect-state.sh) — Inspect local state and containers mounting this worktree.
- [migrate-assets.sh](migrate-assets.sh) — Migrate and verify owned state and asset links before worktree retirement.
- [new-agent-prompt.sh](new-agent-prompt.sh) — Generate a scoped Issue handoff from the current registry and workflow.
- [overleaf-sync.sh](overleaf-sync.sh) — status, push and pull between HEAD:paper and an Overleaf project, fast-forward only.
- [paper-check.sh](paper-check.sh) — make check: build main and blind, run the build, reference, interface and content checks and the unit tests.
- [probe-credentials.sh](probe-credentials.sh) — Report only the status of explicitly declared credential requirements.
- [reference-integrity](reference-integrity) — Locked dependencies of the optional reference checks (bibtex-updater, pybtex) and their licence inventory.
- [reference_env.py](reference_env.py) — Load the reference-audit variables from the shared credential link.
- [reference_evidence.py](reference_evidence.py) — Record and migrate occurrence-level citation-support evidence.
- [release-check.sh](release-check.sh) — make release-check: release gates of the blind and submission builds.
- [setup-worktree.sh](setup-worktree.sh) — Initialize worktree-local state, asset links and project setup.
- [teardown-worktree.sh](teardown-worktree.sh) — Check retirement preconditions and migrate local state.
- [upgrade-template.sh](upgrade-template.sh) — Apply reviewed template upgrades with schema and identity-aware path migration.
- [validate_bibtex_correction.py](validate_bibtex_correction.py) — pybtex validator of one proposed BibTeX correction.
- [validate_bibtex_with_pybtex.py](validate_bibtex_with_pybtex.py) — pybtex validator of a bibliography's format.
<!-- registry-index:end -->
