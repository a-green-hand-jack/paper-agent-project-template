# Agent rules

## What to read first

Before working, read this file, `.agents/AGENTS.md`, the Issue, and only the
records and skills under `.agents/memory/`, `.agents/knowledge/` and
`.agents/skills/` that the task needs. For paper work, start with `PAPER.md`
(see "Paper work" below). Understand the existing text and boundaries before
deciding to change anything.

`CLAUDE.md` is a symlink to this file, so that Claude Code finds the same rules
from the repository root. Change only `AGENTS.md`; never let the two diverge.

## Three planes

- The product is the paper in `paper/`. It is self-contained: a copy of
  `paper/` alone builds, it never reads `.agents/`, and builds write to the
  worktree's `.project/build/`, never into `paper/` or the repository root.
- Agent rules, records, skills, scripts and checks live in `.agents/`.
- The Human documents are in the root: `README.md`, `PAPER.md` (the Human
  contract), `DEV.md` and `RELEASE_NOTES.md`.

Do not copy development material into `paper/`, and do not keep the paper's
behavior only in development material.

## How to work

- Work directly in the existing `dev` checkout unless the Human specifies
  otherwise. Check and preserve unrelated changes and running tasks; choose
  Issues, review and PRs according to the task and its risks. Run applicable
  checks; committing or pushing still requires explicit authorization.
- Before dispatching a Herdr worktree, ask the Human whether to dispatch and
  confirm the coding agent, concrete model and thinking level. Do not dispatch
  or silently change those choices without confirmation. Use Herdr's native
  worktree command if dispatch is authorized; do not replace it with raw Git.
- The coordinator handles integration in `dev`. Related work may reuse an
  existing session and worktree with explicit scope and ownership.
- Continue authorized work through implementation and verification; investigate
  and resolve related issues instead of stopping at known unfinished work.
  Report concrete blockers and continue independent work when possible.
- Remove unnecessary rules before adding new ones.
- Write no special cases for a particular role, task or benchmark.
- Do not add explanatory code comments by default. Record durable decisions,
  sourced facts and repeatable procedures in memory, knowledge and skills;
  keep required language/tool directives and licence notices. Do not remove
  existing comments solely for this rule.
- Do not replace project memory with an agent's private memory.
- Check `.agents/content-registry.yaml` first to tell shared content from
  project content.
- Do not hide state, logs, receipts or assets in unknown directories outside
  the project.
- Operate through the project's own `make` targets and `.agents/scripts/`;
  create no global commands.
- Preserve unrelated changes; never reset, overwrite or commit someone else's
  work.
- Do not commit or push unless the user explicitly asks.
- Before writing a visible Issue, PR, push or release, check the repository's
  visibility. Public or private, never write credentials, private data,
  machine-local absolute paths or unredacted logs.
- Write Issues, PRs, comments and the Human documents in the working language
  declared by `writing.language` in `.agents/content-registry.yaml`, and open an
  Issue body with the sections of `writing.issue_sections`; with no declaration
  keep each file's own language. Shared template text (above a
  `## In this repository` section) keeps the template's language; do not
  translate it.

## Context and state

Every worktree first runs `.agents/scripts/shared/setup-worktree.sh`. All local state
goes in that worktree's `.project/`. An external asset has an `assets/` link
and an entry in `assets/MANIFEST.yaml`. Credentials are injected only by path
or runtime environment, and never written into Git, logs or the manifest; a
project that calls LLM providers lists the credentials it needs, by name only,
in a root `credentials.yaml` (`llm-credentials`).

## Evidence

Report tests, builds, real runs and releases separately. A passing test does
not mean the product is done, and an agent's final message is not delivery
evidence. When a defect related to the task turns up, keep the failing
evidence first, then fix it in the current unit of work and verify again.

For the paper, the evidence is the build: `make check` passes, and the
rendered pages have been looked at
([`post-build-visual-inspection`](.agents/memory/shared/post-build-visual-inspection.md)).
A release also passes `make release-check`.

## Paper work

### Orientation

1. Read `PAPER.md`.
2. Read `.agents/memory/project/experiments.md` only for experiment, evidence,
   claim-support or result-interpretation work.
3. Read `.agents/memory/project/paper-interfaces.md` only for recurring
   identity, terminology, notation, results, claims, figures, tables or macros.
4. Read `.agents/memory/project/publication.md` only for the venue, the builds,
   Overleaf or releases.
5. Read only the decision records under `.agents/memory/project/` that the
   task touches.
6. Inspect the active section in `paper/` and the current diff.
7. Load one owner skill from the table below, and a second skill only when the
   owner skill or the Human names it; never load the whole family.

### Task routing

Skills are at `.agents/skills/shared/<name>/SKILL.md`.

| Task | Owner skill |
| --- | --- |
| paper context, brief, control decisions and stable interfaces | `paper-foundation` |
| scientific writing, editing, proofreading and writing exemplars | `paper-writing` |
| citation discovery, claim support and bibliographic repair | `paper-references` |
| scientific data figures, diagrams and editable figure reconstruction | `paper-figures` |
| manuscript consistency and peer-review triage | `paper-review` |
| venue, builds, Overleaf, release preparation and posters | `paper-publication` |
| result tables, figure data and numbers from code repositories | `asset-lifecycle` |
| Issue start, merge and close-out | `issue-workflow` |
| worktree setup, migration and teardown | `worktree-lifecycle` |
| bring an existing paper repository onto this template | `template-adoption` |
| upgrade to a newer template release | `template-upgrade` |
| report a defect in this template | `template-feedback` |
| scripts, build or CI | no skill; `DEV.md` and `.agents/scripts/AGENTS.md` |

Do not load skills for an ordinary local edit. Do not run manuscript-wide
review passes while drafting a section: a version-level consistency review is
explicit, starts only after the Human marks a version ready, and reports
findings only, unless the Human asks for changes.

### Collaboration cues

- **locked**: analyze or propose; do not silently change the meaning.
- **bounded**: adjust inside the written boundary.
- **free**: handle the implementation or wording while respecting
  higher-level decisions.
- **unresolved**: keep the uncertainty visible, prefer reversible progress,
  and ask before a high-impact or hard-to-reverse choice.

The Human decides the central claims, whether a claim may weaken, the main
story, experiment fairness, important result interpretation, citation
identity or version choices that affect meaning, the meaning of stable
interfaces, what the builds may differ in, release approval and external
publication.

The Agent retrieves, repairs BibTeX and the ledger from evidence, analyzes
impact, offers alternatives, keeps the paper consistent, drafts, makes
low-risk revisions, runs the builds and checks, prepares releases, maps
template adoption and upgrades, and validates. In autonomous mode
(`Mode: autonomous` in `PAPER.md`), the Agent also drafts, self-reviews,
polishes and builds without step-by-step confirmation. It still stops for the
Human before changing a locked item, approving a release or submitting.

### Strong rules

- Do not invent contributions, facts, results, citations, identity, approval
  or success on an external platform.
- Do not promote expected or unresolved results to evidence; a planned result
  is never written as an observation.
- A reported number reaches the text only through an interface macro in
  `paper/macros.tex` whose source is an entry in `assets/MANIFEST.yaml`
  ([`results-through-interface-macros`](.agents/memory/shared/results-through-interface-macros.md)).
- Do not turn correlation into causal language without support.
- Do not silently change a locked claim, story decision, experiment
  condition, limitation or interface meaning.
- The three builds come from one source: `submission` and `blind` only remove
  layers of `main`
  ([`one-source-three-builds`](.agents/memory/shared/one-source-three-builds.md)).
  Never copy scientific content into a build-specific file.
- Keep negative or inconclusive evidence visible when it constrains a central
  claim.
- `paper/` depends on nothing outside `paper/`.
- Overleaf receives only `HEAD:paper`, through `.agents/scripts/shared/overleaf-sync.sh`,
  never the repository root and never a forced push
  ([`overleaf-paper-tree-only`](.agents/memory/shared/overleaf-paper-tree-only.md)).
- Build output, screenshots and logs go to `.project/`, never into `paper/` or
  the root.
- Never draft a real paper in this template repository.
- This template repository protects the case branches `case/arxiv-2505-22954`,
  `case/arxiv-2604-01658` and `case/arxiv-2605-03042`, their case Issues (#23,
  #24, #30) and the verification trackers (#21, #31): never propose, plan or
  perform their deletion, and leave them out of cleanup reports
  ([`protected-case-branches`](.agents/memory/project/protected-case-branches.md)).
  A paper made from the template keeps its own list instead.

### Handoff

Report the changed files, the scientific or narrative meaning affected, the
decisions made or still open, the interfaces, builds and experiment records
affected, and the checks run with their output (`make check`, and
`make release-check` for a release).
