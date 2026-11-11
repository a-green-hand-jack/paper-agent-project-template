---
name: ci-tex-install-bounded
date: 2026-11-11
source: Issue #205; PR #204 run 43048883339 attempt 1 (2026-11-11 15:29-15:59 UTC) and the successful rerun
applies_to: .github/workflows/paper-check.yml and release-PR CI
---

# Bound the CI TeX install and rerun runner DNS failures

## Decision

The `check` and `paper-only` jobs keep a bounded Ubuntu package-mirror DNS
preflight (3 minutes) and a bounded TeX install step (18 minutes), with apt
connection timeouts and limited retries. A transient GitHub-hosted runner
DNS/network failure fails in minutes with a clear message instead of consuming
the job timeout.

A runner DNS failure is infrastructure, not a code failure. Rerun the failed
jobs after reading the install log; do not bypass the required checks. The four
required checks remain the gate for `main`, and local `make check` remains the
code gate.

## Why

On 2026-11-11 the v0.4.9 release PR's `check` and `paper-only` jobs stayed in
"Install TeX" until the 30-minute job timeout. The install log held 118
`Temporary failure resolving` errors for `azure.archive.ubuntu.com`,
`archive.ubuntu.com` and `security.ubuntu.com`, with apt retrying every 20
seconds. A later run on a healthy runner installed in about 1.5 minutes and all
checks passed. No repository code or paper content failed.

The workflow had only a job-level timeout. Without a bounded preflight and
install step, one transient runner DNS failure blocks required checks and a
release PR for the full job budget.

## Apply

When the install step fails, read its log for `Temporary failure resolving` and
rerun the failed jobs; do not wait out a job timeout and do not merge with
administrative bypass. Keep the preflight, step timeouts and apt timeout/retry
options when editing the workflow. If failures persist across healthy reruns,
open a separate Issue to evaluate another TeX source or image instead of
changing it inside a release PR.
