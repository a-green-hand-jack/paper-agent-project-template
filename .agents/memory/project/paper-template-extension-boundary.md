---
name: paper-template-extension-boundary
date: 2026-11-05
source: Issues #195 and #197; v0.4.7 and dev commit 80bfd1d
applies_to: maintenance and upgrades of this derived paper template
---

# Maintain the paper template as an extension

## Decision

The coding template owns the generic development foundation. This repository
follows its released version and adds paper capabilities; its own release and
upstream version are separate registry identities. The paper is the product:
`paper/` builds on its own and Overleaf receives only the paper tree.

Paper workflows are discoverable through six focused skills. Their scripts and
tests are grouped by responsibility, while inherited generic tooling stays in
its upstream layout. Existing citation ledger and policy paths remain stable;
writing, figure and poster exemplars are development support, not evidence for
a manuscript claim unless independently reviewed as citations.

## Why

The former flat skill and script inventories mixed upstream governance, paper
workflows and third-party tools. Overlapping entrypoints made their authority
and upgrade ownership hard to see. Paper-specific grouping restores those
boundaries without discarding unique tools, sources or licenses. A document's
use as a presentation example does not establish its identity or support for a
scientific claim.

## Apply

Use the registry as the identity and migration authority; preserve stable IDs,
local adaptations, optional rejection and user-owned records. A path move must
cover the callers, test discovery and real old-version upgrade, including
conflict preflight and repeat-upgrade behavior. Keep necessary local upstream
fixes explicit and review them when following another upstream release. The
operational rules and current commands live in the skills, `DEV.md` and the
reference governance, not in this decision record.
