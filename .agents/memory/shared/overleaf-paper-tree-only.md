---
name: overleaf-paper-tree-only
date: 2026-10-20
source: Issue #156 §4; Overleaf synchronization in every downstream paper repository examined, including a rejected subtree push and a rewrapped Overleaf tip
scope: shared
applies_to: repositories whose product tree is mirrored to an Overleaf project through Overleaf's Git remote
status: active
supersedes: null
superseded_by: null
---

# Overleaf receives the paper tree only, as a fast-forward checked by tree

## Decision

1. **Only the product tree goes to Overleaf, never the repository root.** The
   Overleaf project holds the contents of `paper/` (a second product, such as
   a poster, has its own Overleaf project and remote). `.agents/`, `.github/`,
   records and build output never reach Overleaf.
2. **A push projects a tree onto the Overleaf tip.** Fetch the Overleaf branch,
   commit the tree `HEAD:paper` with the fetched tip as its only parent, and
   push that commit as a fast-forward. Never force-push.
3. **Compare trees, not commits.** Overleaf rewrites the commits it receives,
   so its tip never has a local commit id. Overleaf and Git agree when
   `git rev-parse HEAD:paper` equals `git rev-parse overleaf/<branch>^{tree}`.
4. **A push is done only when a fresh fetch shows equal trees.** The push
   command's own success message is not the evidence.
5. **Overleaf edits come back on a branch.** Import the Overleaf tip tree into
   `paper/` on a `sync/overleaf-*` branch based on the last state both sides
   had, and merge it through a PR. A push refuses while Overleaf holds edits
   that Git does not have.
6. **The remote URL carries no token.** The Overleaf Git token stays in a Git
   credential helper, never in the remote URL, a tracked file or a command
   argument.

## Why

Pushing the root exposes the development plane to collaborators and makes
Overleaf compile a tree that is not the paper. A `git subtree` push was
rejected as non-fast-forward with no remote edits at all, because the Overleaf
tip is a server-side rewrap that no local split descends from; projecting the
tree onto the fetched tip worked. A tool that printed success right after
`git push` gave no evidence that Overleaf held the intended tree. Comparing
commit ids after a sync reports a false difference every time.

## Apply

- Use `.agents/scripts/overleaf-sync.sh status|push|pull`; it implements every
  point above, verifies tree equality after each push and pull, and refuses a
  remote URL with a password or token. `--remote` and `--tree` select a second
  product (`--remote overleaf-poster --tree poster`).
- Add the remote once per clone:
  `git remote add overleaf https://git.overleaf.com/<project-id>`, and let a
  credential helper store the token.
- Before claiming a sync, report the Overleaf tip tree, `HEAD:paper` and that
  they are equal, as `overleaf-sync.sh status` prints them.
- A real Overleaf run is a maintainer step: the template's tests use a local
  bare repository standing in for Overleaf.
