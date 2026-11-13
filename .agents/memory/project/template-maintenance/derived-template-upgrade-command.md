---
name: derived-template-upgrade-command
date: 2026-11-13
source: Issue #218 and coding-agent-project-template #155 (v0.1.33); replaces the decision of Issue #213
applies_to: maintenance and upgrades of this derived paper template
---

# A derived template follows its upstream with the target release's command

## Decision

When this template follows a newer `coding-agent-project-template` release, run
the **target release's** complete `.agents/scripts/shared/` command directory, as
`template-upgrade` describes, and afterwards keep the inherited scripts
byte-identical to that release. This repository carries no local change in
`upgrade-template.sh` or `content_registry.py`.

## Why

Until v0.1.32 the coding template's command dropped every `scope: template`
entry from the resulting registry. This repository is itself a template and
keeps its own template-only records, so following v0.1.32 with the followed
template's command lost all 28 of them, and this repository upgraded with its
own adapted copy instead (Issue #213). The copy grew to about 140 differing
lines: every upstream release then needed a manual re-merge of the migration
and identity logic, and upstream's regression tests never ran on the merged
result.

Upstream v0.1.33 absorbed those changes (coding template #155). Its command
keeps local `scope: template` entries when the registry has `template.upstream`,
merges local `policy.root_files`, relocates project-owned records with their
links, and records content that is not adopted only as `omitted:` records. The
follow from v0.1.32 to v0.1.33 was run with the v0.1.33 command directory: the
29 `scope: template` entries and the `references` root entry survived, and the
inherited scripts compare equal to v0.1.33 with `cmp`. A paper-level test of
that follow then found that the command kept two omission records for one
identity when the target itself had `omitted:` records; v0.1.34 fixed it
(coding template #159), and this template follows v0.1.34.

## Apply

- Fetch the target tag's command directory and run it (`--check` first).
- Confirm the registry still lists its `scope: template` entries and its extra
  `policy.root_files`.
- Compare each inherited script with the followed release using `cmp`, and each
  inherited record above its `## In this repository` section. Record a
  difference that must stay in `DEV.md` ("与模板的关系") with its reason, and
  report a generic fix to the coding template instead of keeping it here.
- Upstream's upgrade regression tests can be run on this repository's command
  copy from a checkout of the followed release:
  `TEMPLATE_COMMAND_DIR=<this repository>/.agents/scripts/shared python3 -m unittest discover -s .agents/tests/project -p 'test_template_upgrade*.py'`.
