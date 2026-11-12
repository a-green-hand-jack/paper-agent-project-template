---
name: derived-template-upgrade-command
date: 2026-11-12
source: Issue #213; the follow of coding-agent-project-template from v0.1.30 to v0.1.32
applies_to: maintenance and upgrades of this derived paper template
---

# A derived template upgrades with its own command directory

## Decision

When this template follows a newer `coding-agent-project-template` release, run
**this repository's own** `.agents/scripts/shared/upgrade-template.sh` with its
sibling `content_registry.py`, not the followed template's copy of the command.

## Why

The coding template's command drops every `scope: template` entry from the
resulting registry (`if e["scope"] == "template": continue`): a project made
from it owns no template-only records, so they become `omitted` provenance.
This repository is itself a template and keeps its own template-only records
(its maintenance memories, `RELEASE_NOTES.md`, the adoption-state test and
others). Running the followed template's v0.1.32 command directory to follow
that release dropped all 28 of them; running this repository's copy preserved
them. This repository's copy is a reviewed local adaptation that replaces the
`continue` line with a block that keeps local template entries.

## Apply

Follow the coding template by running this repository's command, and confirm the
resulting registry still lists its `scope: template` entries before committing.
Keep the template-preservation block when re-checking local divergences against a
newer upstream; the rest of the command's behavior (the schema 1 to 2 boundary
fixes, identity handling) still comes from upstream.
