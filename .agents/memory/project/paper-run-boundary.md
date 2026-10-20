---
name: paper-run-boundary
date: 2026-10-20
source: Issue #152, the standing collaboration contract with paper-run, carried over by Issue #156
scope: project
applies_to: this template repository and the paper-run project that consumes its releases
status: active
supersedes: null
superseded_by: null
---

# The template is a versioned foundation; paper-run owns the runtime

## Decision

1. **This template provides** the paper repository layout (`paper/`, the
   records in `.agents/memory/`, `PAPER.md`), the builds and their checks, the
   reference-integrity tools, the paper skills, and the release and upgrade
   conventions. Its principle: never invent facts, results, contributions,
   citations or Human approval, and keep unresolved and negative evidence
   visible.
2. **This template does not provide** a globally installed paper CLI, agent
   launchers or session controllers, a replacement for an agent's own user
   interface, stage scheduling, pause and resume or Human attachment for an
   end-to-end run, a runtime database of agent traces, or automated idea
   discovery, experiment design, experiment execution or resource scheduling.
   Static template checks are never presented as evidence that a paper is ready
   for publication.
3. **paper-run** (`a-green-hand-jack/paper-run`) is the layer above. It may
   read, initialize and call this template's records, skills, scripts and paper
   layout. It must not silently redefine their meaning, bypass a Human
   decision, or keep a second scientific source.
4. **Releases are the interface.** paper-run and every paper depend on a
   release tag of this template, never on the moving `dev` branch.

## Why

Two repositories that both grow runtime control and paper contracts duplicate
each other and drift. Keeping the runtime in paper-run and the paper
foundation here lets both release and verify independently, while a paper
built with both still compiles without any agent runtime and stays traceable
to a template version and a paper commit.

## Apply

- A change to the template's paths, records, check outputs, skill routing or
  release conventions that paper-run may consume is a cross-repository change:
  name the affected tag, path and behavior in this repository's Issue and link
  the paper-run Issue. A breaking change gets a migration note in
  `RELEASE_NOTES.md`.
- Requests for a global CLI, agent integration, an end-to-end stage controller
  or Human interaction belong to paper-run; record only the template interface
  they need here.
- Real paper content, author decisions, experiment results and publication
  approval are never written into the template as project facts.
- A paper made from the template removes this record (`scope: template`).
