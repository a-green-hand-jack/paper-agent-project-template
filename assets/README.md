# Assets

This directory is the repository-visible entry point for the evidence behind
the paper: result tables, figure data and reported numbers produced in code
repositories, and any large external payload (raw logs, checkpoints, datasets).

Register each one in [`MANIFEST.yaml`](MANIFEST.yaml) with its source
repository, commit, run or config identifier, checksum and regeneration
command; the header of the manifest gives the entry format. A number reaches
the paper only through an interface macro in `paper/macros.tex`, whose record
in `.agents/memory/project/paper-interfaces.md` names the manifest id. A planned
result is registered with `status: planned` and is never written as an
observation.

Small files the paper includes are committed under `paper/tables/` or
`paper/figures/`. Large payloads stay in their code repository or managed
storage. Link them here locally, never in Git, because a link target exposes
an absolute path and is invalid on another machine:

```text
assets/run-logs -> /managed/storage/run-logs
```

Put local link mappings in the ignored `.project/assets.links` file, one
`name=absolute/path` entry per line, then run
`bash .agents/scripts/setup-worktree.sh` to create the links. Do not commit
large binary payloads, credentials or unregistered paths.
