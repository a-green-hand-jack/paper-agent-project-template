---
name: asset-lifecycle
description: Keep large external assets visible, linked and migratable from a repository.
---

# Asset lifecycle

Use this skill for datasets, model checkpoints, caches or other large assets that
should not be committed to Git.

1. Create a stable repository-visible entry under `assets/`, normally a symlink to
   managed external storage.
2. Register its id, purpose, source, version, checksum and rebuildability in
   `assets/MANIFEST.yaml`.
3. Keep machine-specific targets out of product code. Setup and diagnosis must
   report a missing or broken link clearly.
4. Before retiring a worktree, migrate the manifest, link and any durable records
   using the repository teardown procedure. Check that no unique copy remains in
   the old worktree.
   Before moving, replacing or re-linking an asset's storage, or deleting a copy,
   follow [`resolve-real-paths-before-moving`](../../../memory/shared/resolve-real-paths-before-moving.md):
   a link can make source and destination the same directory.
5. Never put credentials, raw auth files or unregistered personal data in the
   asset directory.

The link and manifest are the project control plane; the external storage is only
the payload location.

## In this repository

The assets of a paper are the results it reports. Register every result table,
figure data file and reported number taken from a code repository in
`assets/MANIFEST.yaml` with the source repository, commit, run or config
identifier, checksum and regeneration command (the entry format is in the
manifest header). A small table or figure file the paper includes is committed
under `paper/tables/` or `paper/figures/`; its manifest entry names that path
as `paper_path`. Large payloads (raw logs, checkpoints) stay in their code
repository or managed storage and are linked under `assets/` as above.

- Step 2 (Register its id): also record `paper_path` and, for a number, the
  interface macro in `paper/macros.tex` that carries it
  ([`results-through-interface-macros`](../../../memory/shared/results-through-interface-macros.md)).
