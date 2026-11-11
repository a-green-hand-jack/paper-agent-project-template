---
name: optional-cli-environments
date: 2026-11-11
source: Issue #202; .agents/scripts/shared/tool-environments.json
applies_to: optional CLIs declared by a paper repository
---

# Run optional CLIs from the project environment

## Decision

Optional CLIs named by a skill run from this worktree's
`.project/tools/<tool>/venv`, created by
`.agents/scripts/shared/tool-env.sh install <tool>` and launched by
`tool-env.sh run <tool> ...`. The tracked
`.agents/scripts/shared/tool-environments.json` declares each tool's source, full
revision, entrypoint and environment paths. Data, cache and configuration stay
under `.project/tools/<tool>/`.

A missing environment is an error. The launcher never falls back to a
user-level or global binary, and `paper/` and `make check` never call these
tools.

## Why

A user-level install has no repository record: two machines or two papers can
run different builds against shared data, and deleting or syncing one project
changes another. Issue #202 found a user-level CLI that was older than the
current data and failed until it was reinstalled from a fixed commit. Keeping
the environment and data in the worktree's `.project/` makes the tool version
reviewable, isolates papers, and matches the existing rule that runtime state
lives in `.project/`. Installer lock files and caches then have a local home
instead of the repository root or the user's home.

## Apply

- Add a tool by adding one manifest row with a public source and a full commit,
  then run `tool-env.sh install <tool>`, `tool-env.sh status <tool>` and
  `tool-env.sh run <tool> ...`.
- Use the CLI's own public commands and environment variables; do not add a
  second search, status or monitoring layer around it.
- Change a version by updating the manifest revision and reinstalling; do not
  edit files inside `.project/tools/`.
- Keep credentials on the `llm-credentials` path: the manifest and tracked files
  hold names and public sources only.
