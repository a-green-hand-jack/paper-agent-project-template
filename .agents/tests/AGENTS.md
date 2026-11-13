# Development checks rules

Tests here are diagnostic and seam-focused. Do not increase coverage merely to
mirror implementation, and do not treat these checks as product acceptance when
the real public entrypoint or long-running runtime has not been exercised.

In the template repository, the `test_template_*.py` files are the template's
own tests of its scripts (`scope: template`; a project does not copy them):
`upgrade-template.sh` against a fixture template with three tags and from an
older real release to the release candidate, `probe-credentials.sh` with setup
and diagnostics against fixture credential files, `migrate-assets.sh` rules and
`new-agent-prompt.sh` against fixture repositories (including a declared parent
integration target and the default dev target), and the branch-model checks
of `diagnose-environment.sh`. They write only to temporary directories, and
CI runs them:

```bash
python3 -m unittest discover -s .agents/tests/project -p 'test_template_*.py'
```

The real-release test needs the release tags (`git fetch --tags origin`).

`test_template_codex_context.py` models missing/stale or wrong-owner caller
context, unsupported isolation, shared restart boundaries and native/fallback
receipts. These synthetic decision scenarios do not enforce the workflow or
prove live isolation; keep the authorized two-session evidence separate.

`test_template_agent_communication.py` also folds synthetic backlog into a
test-only receipt/terminal summary model. It checks action/message/user-report
counts, retained conflicts and risks, covered outcomes and restart recovery.
It is a protocol counterexample check, not a runtime consumer or proof that a
live agent obeys the rules; native transport and receiver evidence stay separate.

## In this repository

For this paper the public entry points are the builds: a passing unit test does
not replace `make check` or `make release-check`, and neither replaces looking
at the rendered pages. `make check` runs every test in both groups except the
template's own `project/test_template_*.py`:

```bash
for dir in .agents/tests/shared .agents/tests/shared/*/ .agents/tests/project; do
  [ -d "$dir" ] || continue
  for file in "$dir"/test_*.py; do
    case ${file##*/} in test_template_*) continue ;; esac
    python3 -m unittest discover -s "$dir" -p "${file##*/}" || exit
  done
done
```

Run one file with `-p test_<name>.py`. Tests write only to temporary
directories. The two BibTeX helper tests run only inside the locked reference
environment (`uv run --project .agents/scripts/shared/paper-references/reference-integrity ...`,
as CI does) and are skipped elsewhere, and so is the locked-tool contract test
(`shared/paper-references/test_reference_tool_contract.py`), which CI runs in the same
environment.

`shared/` holds the tests of the shared scripts, which a paper keeps.
The `project/test_template_*.py` files are this template's own tests
(`scope: template`; a paper deletes them). They build papers and take several
minutes, so `make check` leaves them out: the `check` job of
`paper-check.yml` runs them where TeX is installed, the inherited
`template-check.yml` step skips them because that job has no TeX, and
a template release runs them locally (`DEV.md`, "发布"):

```bash
python3 -m unittest discover -s .agents/tests/project -p 'test_template_*.py'
```

`test_template_adoption_states.py` builds each adoption state from the shipped files in a
temporary directory, runs `make check` and `make release-check` there and
compares the failures with the newest `RELEASE_NOTES.md` entry. It also
upgrades a fresh paper at v0.4.1 to the shipped files with this release's
`upgrade-template.sh` and runs `make check` there, and checks that every
release entry marks its upgrade section. `test_template_issue_195_upgrade.py`
and `test_template_issue_197_upgrade.py` upgrade papers across the releases
that moved paper content and tooling. `shared/test_upgrade_template.py`
runs the command against a fixture template repository with three tags.
