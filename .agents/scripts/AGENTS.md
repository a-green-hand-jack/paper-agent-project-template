# Script directory rules

Scripts may prepare environments, inspect state, migrate assets and invoke the
project's public CLI. They must not create a second runtime layer, global command,
or hidden state store. Destructive operations require an explicit, inspectable
precondition and should be delegated to the approved worktree or asset manager.

## Index

Inherited from `coding-agent-project-template`, replaced whole by
`template-upgrade`; never edit them here:

- `setup-worktree.sh`, `teardown-worktree.sh`, `migrate-assets.sh` — set up,
  migrate and retire a worktree's `.project/` state.
- `diagnose-environment.sh`, `inspect-state.sh` — read-only diagnostics.
- `init-branches.sh` — create `dev` and make it the default branch.
- `new-agent-prompt.sh` — the hand-off prompt for an Issue session.

This repository's own:

- `setup-project.sh` — run by `setup-worktree.sh`: creates `.project/build/`
  and reports the TeX tools; `migrate-project.rules` says that
  `.project/build/` is dropped at teardown because `make` rebuilds it.
- `paper-check.sh` (`make check`) and `release-check.sh`
  (`make release-check`) — the build checks; they write only under
  `.project/build/`.
- `check-paper-build.py` — reads one build: log problems (`log`), main-text
  pages (`pages`), underscores in the PDF text (`underscores`), identity in
  the blind build (`identity`) and leftover notes or placeholders
  (`leftovers`).
- `check-paper-interfaces.py` — the interface macros of `paper/macros.tex`.
- `check-agent-content.py` — skill, memory and knowledge front matter and
  structure, indexes, registry entries and vendored-file hashes.
- `overleaf-sync.sh` — `status`, `push` and `pull` between `paper/` and an
  Overleaf project.
- `check-reference-integrity.py`, `reference-evidence.py` — the offline
  reference gate and the citation-support records; `check-bibtex-format.py`,
  `check-reference-metadata.py`, `check-reference-corrections.py` — the optional
  checks that use the locked dependencies in `reference-integrity/`; the
  `_*.py` files are their shared helpers.
