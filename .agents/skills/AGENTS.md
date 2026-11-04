# Skills directory rules

Shared procedures belong in `shared/`; repository-owned procedures belong in
`project/`. Physical grouping does not imply reuse permission: the registry
keeps `scope: template` packages out of downstream projects. Each package uses
`SKILL.md`; nested AGENTS are only added when a distinct governance boundary
needs them. Generated group indexes come from the registry; do not maintain a
second list of summaries here.

## In this repository

- `shared/` holds the procedures every paper made from this template reuses;
  the generated index in [`shared/AGENTS.md`](shared/AGENTS.md) lists them. A
  paper's own skills go in `project/<name>/` and state their commands,
  evidence and failure boundaries.
- Skills give process, not permission: `PAPER.md` and the records take
  precedence over any skill text.
- Load the one owner skill for the task (the root `AGENTS.md` routes tasks to
  them), and a second skill only when the owner skill or the Human names it.
  Never load the whole family.
