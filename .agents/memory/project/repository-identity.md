---
name: repository-identity
date: 2026-10-20
source: DEC-0018 and DEC-0019 of this template's decision log, Issues #148, #151 and #156
scope: project
applies_to: this template repository's name, description and positioning
status: active
supersedes: null
superseded_by: null
---

# The repository is paper-agent-project-template

## Decision

1. **Name.** The repository is
   `a-green-hand-jack/paper-agent-project-template`. It was renamed from
   `ccfa-writing-paper-template` to `agent-writing-harness` (#148, #151) and
   then to `paper-agent-project-template` (#156). GitHub redirects the old
   names; never create a repository under an old name, because that breaks the
   redirect.
2. **Positioning.** It is a paper template built on
   `coding-agent-project-template`: a paper is developed like code, with a
   self-contained `paper/` product tree, Issues and PRs from `dev`, a build that
   acts as the test suite, tagged releases and recorded provenance. It serves
   papers in any field; it is not tied to one venue family or one bundled skill
   suite.
3. **Description.** "Paper template built on coding-agent-project-template:
   develop a paper like code".
4. **Branches.** `dev` is the default and integration branch, `main` the
   release branch. `template-dev` is retired; its last commit is kept as the
   tag `archive/template-dev`.

## Why

The first name tied the template to one venue family and the bundled CCFA
suite (DEC-0018 kept the name only to avoid breaking references); the second
described an agent harness rather than a template. The current name places the
repository next to the coding template it is built on. Keeping the redirect
chain intact keeps old template references and clones working.

## Apply

- Write the current name in new text. Old names appear only where a tool must
  recognize them (the brief tool refuses to ingest into any of the template's
  names) or in history.
- Renaming again, or changing the default or release branch, needs the
  maintainer and a migration note in `RELEASE_NOTES.md`.
- A paper made from the template removes this record (`scope: template`).
