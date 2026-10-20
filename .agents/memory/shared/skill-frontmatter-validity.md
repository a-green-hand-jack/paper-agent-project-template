---
name: skill-frontmatter-validity
date: 2026-10-20
source: Issue #156 §7; downstream paper repositories that inherited eight skills whose front matter did not parse, and a vendored skill that arrived invalid
scope: shared
applies_to: repositories that keep agent skills as SKILL.md files with YAML front matter
status: active
supersedes: null
superseded_by: null
---

# Every SKILL.md front matter parses, checked after every skill change

## Decision

1. **A skill starts with YAML front matter that parses**, with a `name` equal
   to its directory and a one- or two-sentence `description` saying when to use
   it.
2. **A plain value cannot contain `: `.** Quote it, or fold it with `>-`:

   ```yaml
   description: >-
     Use when: the paper needs a figure plan.
   ```

3. **Re-parse every skill after any change under the skills tree**, including
   vendoring a third-party skill: a vendored skill can arrive invalid.

## Why

An agent runtime that cannot parse a skill's front matter reports a load
conflict and never shows the skill's instructions: the skill is silently
absent. Eight skills inherited from an earlier release of this template failed
with `mapping values are not allowed here`, because copying them dropped the
quotes around descriptions that contain `: `; every session in the downstream
papers ran without them until one repository fixed them. The parse error
points inside the front matter, not at the offending colon, so the cause is
easy to miss.

## Apply

- `make check` runs `.agents/scripts/check-agent-content.py`, which parses every
  `SKILL.md` under `.agents/skills/` recursively and checks `name` and
  `description`, together with the front matter of every memory and knowledge
  record.
- A third-party skill whose own front matter is invalid is fixed by a recorded
  patch in its `PROVENANCE.md`, not by an unrecorded edit.
