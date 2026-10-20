---
name: sync-overleaf-before-editing
date: 2026-10-20
source: Issue #156 §4; downstream paper repositories whose collaborators edit in Overleaf between agent turns, including a change delivered to Overleaf only
scope: shared
applies_to: repositories whose paper is edited both in Git and in an Overleaf project
status: active
supersedes: null
superseded_by: null
---

# Take in Overleaf edits before writing, and deliver to both sides together

## Decision

1. **Check Overleaf before the first edit of a session.** Run
   `overleaf-sync.sh status`. When Overleaf holds edits Git lacks, bring them in
   first (`pull`, review, merge through a PR) and rebuild before writing.
2. **The Overleaf tip is authoritative for what collaborators wrote.** Take its
   tree as it is: do not replay its intermediate commits, and do not normalize
   collaborators' whitespace or wording unless they agreed.
3. **A paper change is delivered to both sides in the same unit of work.**
   After the PR merges into the integration branch, push `paper/` to Overleaf
   and report both tips. A clone that tracks only one remote is no reason to
   update only that one.
4. **Development-plane changes go to Git only.** Records, skills, scripts and
   CI never go to Overleaf.
5. **A partial sync is reported as incomplete**, with what is missing on which
   side.

## Why

Collaborators edit in Overleaf between agent turns; an agent that starts
writing from a stale tree produces a conflict or overwrites their work. A
change once reached Overleaf only, because the clone tracked the Overleaf
remote, and Git fell behind until a person noticed. Normalizing collaborators'
whitespace on import made every later comparison noisy and was not theirs to
approve.

## Apply

- Start a paper session with `bash .agents/scripts/overleaf-sync.sh status`; act
  on its `STATE` line.
- Keep Overleaf's compiler and TeX Live version matched to the local build, so
  that both sides typeset the same pages.
- Never use a bare `git stash` to set work aside around a sync; commit work in
  progress on the Issue branch instead (the stash stack is shared between
  worktrees).
- Standing permission to commit or push for a collaborator is a per-paper
  decision recorded in that paper's records, not a default.
