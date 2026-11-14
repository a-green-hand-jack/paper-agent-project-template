# Scripts project rules

Follow the category rules and the content registry.
Keep repository-owned content here; reuse scope is recorded independently in the registry.

<!-- registry-index:start -->
- [check-development-paths.allow](check-development-paths.allow) — Explicit exemptions for check-development-paths.py, each with its reason; printed when the check runs.
- [check_development_paths.py](check_development_paths.py) — Check that development-plane documents name existing paths and that CLAUDE.md, .claude and .pi are the expected symlinks.
- [migrate-project.rules](migrate-project.rules) — Teardown rules for the .project/ entries setup-project.sh creates (build is dropped); a paper adds a line for each entry it creates.
- [setup-project.sh](setup-project.sh) — This template's setup hook (creates .project/build/, reports the TeX tools); a paper adds its own setup lines.
<!-- registry-index:end -->
