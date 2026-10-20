# Developing the paper

## Boundaries

`paper/` is the product plane, `.agents/` the agent development plane, and the
root documents (`README.md`, `PAPER.md`, this file, `RELEASE_NOTES.md`) the
Human plane. Each topic is written out in one authoritative place, and other
places link to it. Run state, logs, screenshots and build output go to the
current worktree's `.project/`, never into tracked files or an unknown global
directory.

`paper/` is self-contained: a copy of `paper/` alone builds, it reads nothing
under `.agents/`, and a build writes to `.project/build/` (or, in a copy of
`paper/` alone, to its `build/`), never back into `paper/` or the root.

## Issues, branches and PRs

A larger unit of work starts with an Issue that settles the problem, scope,
acceptance and risks before anything changes: drafting or rewriting a section,
changing a claim, result, interface macro, venue or build, anything a control
cue in `PAPER.md` protects, and tooling or CI changes. Small fixes are made
directly in the `dev` checkout, without an Issue, worktree or PR: typos,
wording inside one paragraph that changes no claim, comments, memory or index
updates, a single-file fix without a design decision, and running existing
commands for acceptance. When unsure, treat the work as larger, and stop to
open an Issue when a small change grows or raises a design question. Small
changes are not committed or pushed automatically either; run the applicable
checks and report the evidence.

An Issue's branch starts from `dev` and is named `fix/issue-<N>-<slug>`,
`feat/issue-<N>-<slug>`, `docs/issue-<N>-<slug>` or `chore/issue-<N>-<slug>`.
It returns to `dev` through a PR; `main` holds only released states. Overleaf
edits arrive on a `sync/overleaf-<commit>` branch made by
`overleaf-sync.sh pull`.

The PR description says what changed and why, gives the command and result of
every check the acceptance and CI require, and lists the related defects fixed
on the way. A step only the maintainer can take is written as a concrete
blocker that says what the maintainer must do. Build and release evidence goes
into the Issue or PR; an agent's own summary does not replace it.

Start an Issue with Herdr's native worktree command, from `dev`, and a
separate agent session in a new pane; never switch branches in the current
agent window. The new session first runs setup. The parent session can
generate the first prompt, with the Issue link, branch, reading scope and
acceptance:

```bash
bash .agents/scripts/new-agent-prompt.sh 123 feat/issue-123-example
```

If Herdr is unavailable, report the blocker instead of implementing in the
current window. The `issue-workflow` skill covers start, merge and close-out.

## Worktree lifecycle

Each worktree is a separate unit of work with its own state. After creating
one, run in it:

```bash
bash .agents/scripts/setup-worktree.sh
```

Setup writes `.project/home` and `.project/worktree.env`, creates the local
state directories, checks tools and the asset manifest, and runs
`.agents/scripts/setup-project.sh`, which creates `.project/build/` and
reports the TeX tools. Never reuse another worktree's `.project/`.

After the PR merges, do not delete the directory directly. First run:

```bash
bash .agents/scripts/teardown-worktree.sh --migrate-to <canonical checkout>
```

It checks ignored state, copies what should be kept and writes a migration
record; it never deletes the worktree. `.agents/scripts/migrate-project.rules`
says that `.project/build/` is dropped, because `make` rebuilds it. Destroy the
worktree and branch with the worktree manager only after the assets are
migrated and no unique copy remains in it.

## Builds and checks

The root `Makefile` is the only build entry; `README.md` lists its targets.
Two variables adjust it:

- `TEXBIN=<TeX Live bin directory>` puts that directory first on `PATH`, for a
  machine where another `latexmk` comes first. Never write a machine path into
  a tracked file.
- `PAGE_BUDGET=<pages>` is the venue's main-text limit, measured on `blind`
  up to `\label{PaperMainTextEnd}`. Set it in the `Makefile` once the venue is
  known; `PAGE_BUDGET=none` declares a release with no page limit, such as an
  arXiv version. `make check` reports the count, and `make release-check`
  fails without a budget or over it.

`make check` runs, in order: the `main` and `blind` builds and their log
checks (undefined references or citations, missing files, multiply defined
labels), the page count of `blind`, the PDF text-layer check that underscores
survive (T1 encoding), the offline reference gate, the interface-macro check,
the skill, memory and knowledge structure check, and the unit tests. Build
logs are in `.project/build/logs/<build>.log`.

A passing `make check` does not show that the pages look right. Before calling
a build done, render the affected pages and look at them
([`post-build-visual-inspection`](.agents/memory/shared/post-build-visual-inspection.md));
renders and screenshots go to `.project/build/inspect/`.

Requirements:

- TeX Live with `latexmk`, `pdflatex` and `bibtex`, and the packages the paper
  and its venue kit load;
- `pdftotext` and `pdfinfo` (poppler-utils) for the PDF checks;
- Python 3 with PyYAML for the scripts;
- optionally `uv`, for the online reference audits that use the locked
  dependencies in `.agents/scripts/reference-integrity/`.

`bash .agents/scripts/setup-worktree.sh` reports what is missing.

A paper has no Python package, container or installer, so this template has
no `pyproject.toml`, `Dockerfile`, `.dockerignore` or `install.sh`, and
`diagnose-environment.sh` reports them as optional files that are absent. Do
not add them for the paper. A tool that needs its own environment installs it
under `.project/`.

## Evidence

Results come from code repositories. Register every result table, figure data
file and reported number in `assets/MANIFEST.yaml`: its source repository,
commit, run or config identifier, checksum and regeneration command. A number
reaches the text only through an interface macro in `paper/macros.tex`, and
`.agents/memory/project/paper-interfaces.md` gives each macro's meaning,
control cue and manifest id. A planned result is registered `planned` and is
never written as an observation. Large payloads (raw logs, checkpoints,
datasets) stay in their code repository or managed storage; link them
locally through `.project/assets.links`, never in Git.

Figure sources:

- `paper/figures/` holds the exported files LaTeX includes, preferably vector
  PDF, so the paper compiles from `paper/` alone.
- A script that plots from data lives in the code repository with its
  manifest entry, or next to its output in `paper/figures/` when it belongs to
  the manuscript.
- An editable source that cannot be rebuilt (a drawing, a slide, a selected
  generated draft) is an asset: registered in the manifest and kept in managed
  storage or `.project/artifacts/<topic>/`, not in `paper/`.
- Scratch renders and rejected drafts go to `.project/build/figures/`.

`figure-router` and `scientific-figure-workflow` apply this policy.

## Overleaf

Overleaf mirrors `paper/` on `dev`, and only `paper/`
([`overleaf-paper-tree-only`](.agents/memory/shared/overleaf-paper-tree-only.md)).
Add the remote once per checkout, with no token in its URL, and keep the token
in a Git credential helper:

```bash
git remote add overleaf https://git.overleaf.com/<project-id>
```

The branch is found from the remote's `HEAD`; `--branch`, `OVERLEAF_BRANCH` or
`git config remote.overleaf.overleafBranch` override it. Then:

```bash
bash .agents/scripts/overleaf-sync.sh status   # in-sync, overleaf-behind, overleaf-ahead, diverged or unrelated
bash .agents/scripts/overleaf-sync.sh pull     # Overleaf edits -> branch sync/overleaf-<commit>, for a PR into dev
bash .agents/scripts/overleaf-sync.sh push     # HEAD:paper -> Overleaf, as a fast-forward
```

- Before editing, run `status`
  ([`sync-overleaf-before-editing`](.agents/memory/shared/sync-overleaf-before-editing.md)).
  When Overleaf holds edits that `dev` lacks, `pull` puts them on a branch
  built from the last state both sides shared; merge it into `dev` through a
  PR, then `push`.
- `push` commits `HEAD:paper` on top of the Overleaf tip and pushes without
  force. It refuses while Overleaf holds edits that `HEAD` lacks, and after
  pushing it fetches again and checks that the trees are equal.
  `push --replace` overwrites those edits; use it only for the first
  publication to a project that shares no state with `paper/`, or when the
  Human says so.
- Trees are compared, not commits, because Overleaf rewrites the commits it
  receives.
- A real Overleaf run needs the maintainer's project and credentials; the unit
  tests use a local bare repository in its place.

## Optional second product: `poster/`

A conference poster is a second product tree, `poster/`, beside `paper/`. It
is self-contained like `paper/`, builds into `.project/build/poster/`, takes
its content and its copy of `macros.tex` only from the paper, and has its own
Overleaf project on another remote (`--remote overleaf-poster --tree poster`).
The `poster-build` skill describes it. The template ships no `poster/`.

## Memory and knowledge

`.agents/memory/` holds durable decisions and `.agents/knowledge/` dated facts
with a source and a refresh condition. The `AGENTS.md` of each directory holds
only its rules and a short index; each record is its own Markdown file under
`shared/` or `project/` with the front matter of the directory's
`ENTRY_TEMPLATE.md`. A venue record starts from
`.agents/knowledge/VENUE_TEMPLATE.md`. When a record is added or moved, update
its index and `.agents/content-registry.yaml`. `make check` checks each
record's front matter, sections and index link, and the registry entry of
every skill.

A paper fills the starter records in `.agents/memory/project/` (`brief.md`,
`experiments.md`, `paper-interfaces.md`, `publication.md`) and adds one record
per durable decision.

## Branch model and visibility

`dev` is the integration branch and `main` the release branch. The first setup
of a new repository creates and pushes `dev` and makes it the GitHub default
branch, when the GitHub CLI is available; `bash .agents/scripts/init-branches.sh`
does the same explicitly. The diagnostics report what is missing and how to
fix it.

Prefer a **Private** paper repository until the paper is public. Before making
it public, check credentials, private data, Issues, PRs, logs and machine
paths. This template repository is public: feedback to it holds only generic,
de-identified reproduction steps and says whether the paper repository is
private or public; name a paper repository only when it is public and its
maintainer agrees.

## Verification

Tests check real risks, past defects and seams; do not add tests for
coverage. A paper change is verified by its public entry points, the builds:

```bash
bash .agents/scripts/diagnose-environment.sh
bash .agents/scripts/inspect-state.sh
make check
```

`make check` runs every unit test; run one file with
`python3 -m unittest discover -s .agents/tests -p 'test_<name>.py'`. A
passing unit test does not replace `make check`, and neither replaces looking
at the pages.

## Releases

A paper release (a venue submission, an arXiv version, a camera-ready
version):

1. On `dev`, set `PAGE_BUDGET` for the release, run `make check` and
   `make release-check`, and look at the `blind` and `submission` pages.
2. Run `release-review`, which prepares the release for the Human's approval,
   and `release-doc-audit` on the release candidate.
3. Open a PR from `dev` to `main`. After it merges, tag `main`, for example
   `submit-<venue>-<yyyy>`, `arxiv-v1` or `camera-ready`, and push the tag.
4. Add a `## <tag>` entry to `RELEASE_NOTES.md`: what was released, from which
   build, and the check results.

This template's own releases are `v<major>.<minor>.<patch>` tags on `main`,
each with a `## <tag>` heading in `RELEASE_NOTES.md`. Before a template
release, run `release-doc-audit` and `make check`; `main` requires the CI jobs
`structure`, `check`, `paper-only` and `references`.

## Relationship with the templates

This repository is a derived template of `coding-agent-project-template`: a
template built on that one, from which papers are made. Its registry,
`.agents/content-registry.yaml`, records this template in `template` and the
coding template it follows in `template.upstream`:

| Repository | `template.repository` / `template.version` | `template.upstream` |
| --- | --- | --- |
| `coding-agent-project-template` | itself, its current version | none |
| this template | itself, its release (v0.4.0) | the coding template and the tag it follows (v0.1.13) |
| a paper made from this template | this template, the adopted tag | none |

A repository follows `template.upstream` when it has that field, and
`template` otherwise.

- This template takes coding-template releases through `template-upgrade`,
  which moves `template.upstream.version`. Inherited files stay verbatim, with
  this template's adaptation only in their trailing `## In this repository`
  sections.
- A paper takes this template's releases through `template-upgrade`, reading
  `RELEASE_NOTES.md` at the target tag. It continues the
  `## In this repository` sections this template wrote.
- A defect or gap a paper finds goes to this template through
  `template-feedback`. This template forwards a defect in inherited content to
  the coding template and links the two Issues.
- The migration from the pre-v0.4.0 layout is recorded in
  `.agents/memory/project/rebuild-on-coding-template.md`, and the steps for a
  paper that used `template-sync` are in the v0.4.0 entry of
  `RELEASE_NOTES.md`.

## Operations

Setup, builds, checks, Overleaf sync and releases go through the `make`
targets and `.agents/scripts/`, never through private functions, ad hoc
wrappers or a second set of scripts (`cli-first-operations`). A paper has no
long-running product runs; experiments run, and are supervised, in their code
repositories.
