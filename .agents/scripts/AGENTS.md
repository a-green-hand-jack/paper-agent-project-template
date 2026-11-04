# Script directory rules

Scripts may prepare environments, inspect state, migrate assets and invoke the
project's public CLI. They must not create a second runtime layer, global command,
or hidden state store. Destructive operations require an explicit, inspectable
precondition and should be delegated to the approved worktree or asset manager.

## In this repository

`shared/` holds the scripts inherited from `coding-agent-project-template`,
replaced whole by `template-upgrade` (never edit them here), and this
template's own scripts that a paper inherits: `paper-check.sh`
(`make check`) and `release-check.sh` (`make release-check`), which write only
under `.project/build/`; `overleaf-sync.sh`; the build, interface and
content checks; the offline reference gate and citation-support records; and
the optional reference audits with their locked dependencies in
`shared/reference-integrity/`. The generated index in
[`shared/AGENTS.md`](shared/AGENTS.md) describes each one.

`project/` holds the setup hooks a paper adapts: `setup-project.sh`, run by
`setup-worktree.sh`, creates `.project/build/` and reports the TeX tools;
`migrate-project.rules` says that `.project/build/` is dropped at teardown
because `make` rebuilds it.
