# Tests project rules

Follow the category rules and the content registry.
Keep repository-owned content here; reuse scope is recorded independently in the registry.

<!-- registry-index:start -->
- [test_template_adoption_states.py](test_template_adoption_states.py) — Builds the adoption states this template documents from its shipped files, checks them against the newest RELEASE_NOTES.md entry and upgrades a fresh paper from v0.4.1 to them; a paper made from the template deletes it.
- [test_template_issue_195_upgrade.py](test_template_issue_195_upgrade.py) — Exercise upgrades preserving local paper content and evidence.
- [test_template_issue_197_upgrade.py](test_template_issue_197_upgrade.py) — Verify v0.4.7 paper tooling relocation preserves local data and upgrade behavior.
- [test_template_issue_216_upgrade.py](test_template_issue_216_upgrade.py) — Upgrade a paper that left template content out and check its omissions stay single and out.
<!-- registry-index:end -->
