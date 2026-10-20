# Paper Agent Project Template

A template for writing a research paper the way software is developed, with a
coding agent (Claude Code, Codex, OpenCode or a plain shell) doing much of the
work. It is built on
[`coding-agent-project-template`](https://github.com/a-green-hand-jack/coding-agent-project-template)
and has three planes:

- **Product**: the paper in `paper/`, a self-contained LaTeX tree. A copy of
  `paper/` alone compiles, and it is the only thing Overleaf ever sees.
- **Development**: `AGENTS.md` and `.agents/`, with the agent rules, skills,
  memory and knowledge records, the reference ledger, scripts and checks.
- **Human**: `README.md`, `PAPER.md` (the paper contract), `DEV.md` and
  `RELEASE_NOTES.md`, plus the Issues and PRs.

Every unit of work is an Issue and a PR from `dev`. The build is the test
suite: `make check` fails on undefined references or citations, missing files,
multiply defined labels and broken interface macros. Every release is a tag on
`main`, and every number the paper reports is traced to the code repository,
commit and run that produced it.

The template works in two operating modes, which a paper declares in
`PAPER.md`. In **collaborative** mode the Human takes each substantive step
with the agent. In **autonomous** mode the Human supplies a brief and
materials, and the agent drafts, reviews and builds on its own, stopping for
the Human before a locked change, a release or a submission.

## Start a paper

1. On GitHub, use **Use this template** to create the paper repository, and
   prefer **Private** until the paper is public. For a reproducible start,
   clone a release tag instead (see "Template versions" below).
2. In the new repository, run `bash .agents/scripts/init-branches.sh`. It
   creates and pushes `dev` and makes it the default branch. Work branches
   start from `dev`; releases merge to `main`.
3. In every worktree, run `bash .agents/scripts/setup-worktree.sh` first.
4. Remove what belongs only to this template:
   - In `.agents/content-registry.yaml`, keep `template.repository` and
     `template.version` (this template and the release you started from) and
     delete the `upstream` block.
   - Delete the files the registry marks `scope: template`, together with
     their registry entries and index lines:
     `.agents/memory/project/rebuild-on-coding-template.md`,
     `protected-case-branches.md`, `repository-identity.md` and
     `paper-run-boundary.md`. In `AGENTS.md`, replace the rule about this
     template's case branches with the paper's own list, or remove it.
   - Replace `RELEASE_NOTES.md` with the paper's own, which starts empty and
     gets one `## <tag>` heading per release.
   - Rewrite this README for the paper: what it is and how to build it.
5. Fill the slots this template leaves to the paper: end
   `.agents/memory/shared/page-budget-on-blind-build.md` (`PAGE_MARGIN`) and
   `.agents/memory/shared/post-build-visual-inspection.md`
   (`MIN_FIGURE_TEXT`, `LAST_LINE_FILL`) each with a `## In this repository`
   section holding a Slot/Value table. `diagnose-environment.sh` warns until
   both have one.
6. Give the agent the paper's brief. The `paper-brief-ingest` skill validates
   it and fills the decided fields of `PAPER.md`; everything undecided stays
   `unresolved`. Without a brief, fill `PAPER.md` together with the agent.
7. When the venue is known, put its official kit into `paper/` unchanged, set
   `PAGE_BUDGET` in the root `Makefile`, and record the venue in
   `.agents/memory/project/publication.md` (`publication-planning`). Put the
   authors in `paper/authors.tex`.
8. Write in `paper/`. Register every result table, figure data file and
   reported number in `assets/MANIFEST.yaml`, and put numbers into the text
   only through interface macros in `paper/macros.tex`.

The agent reads `AGENTS.md` first. It routes each task to one skill and loads
only the records that task needs.

## Builds

The root `Makefile` is the public build entry. Output and intermediate files go
to the worktree's `.project/build/`; nothing is written into `paper/` or the
repository root.

| Command | What it builds or checks |
| --- | --- |
| `make pdf` | `main`: named, with author notes (`.project/build/main.pdf`) |
| `make submission` | `submission`: named, notes removed |
| `make blind` | `blind`: anonymous; author identity, acknowledgements and notes removed |
| `make check` | builds `main` and `blind`; fails on undefined references or citations, missing files, multiply defined labels, interface-macro and reference-ledger errors, invalid skill or record front matter and failing unit tests; reports the main-text pages of `blind` against `PAGE_BUDGET` |
| `make release-check` | builds `blind` and `submission`; fails on author identity in the anonymous PDF or its sources, leftover notes or TODOs in `submission`, a page count over budget, or references below release strength |
| `make clean` | removes the build output |

The three builds come from one source: `paper/main.tex` is `main`, and the
one-line `paper/submission.tex` and `paper/blind.tex` only switch layers off.
TeX comes from `PATH`, or from `TEXBIN=<TeX Live bin directory>` when another
`latexmk` comes first. A build needs `latexmk`, `pdflatex` and `bibtex`; the
checks also need `pdftotext`, `pdfinfo` and PyYAML.

A copy of `paper/` alone builds with `make -C <copy> main` (or `blind`,
`submission`) and writes to `<copy>/build/`.

## Directory

| Path | Plane | Purpose |
| --- | --- | --- |
| `paper/` | product | The paper: `main.tex`, `submission.tex`, `blind.tex`, `authors.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/`, `tables/`, `algorithms/`, `style/` and its `Makefile` |
| `assets/` | evidence | `MANIFEST.yaml`: the source repository, commit, run, checksum and regeneration command of every reported number, table and figure data file; local links to large payloads |
| `Makefile` | build entry | The `make` targets above |
| `.project/` | worktree-local state | Build output, logs and screenshots; ignored by Git |
| `.agents/` | development | Skills, memory and knowledge records, the reference ledger, scripts and tests; see `.agents/AGENTS.md` |
| `.github/` | development | CI and the Issue and PR templates |
| `AGENTS.md`, `CLAUDE.md` | agent entry | Rules and task routing; `CLAUDE.md` is a symlink to `AGENTS.md` |
| `README.md` | Human | This page |
| `PAPER.md` | Human | The contract: what the paper claims, its story and style, what must not change silently, and what is still open |
| `DEV.md` | Human | How the paper is developed: Issues, builds, Overleaf, evidence and releases |
| `RELEASE_NOTES.md` | Human | One heading per release tag |

## Releases and Overleaf

A release (a submission, an arXiv version, a camera-ready version) is a PR
from `dev` to `main` that passes `make release-check`, then a tag on `main`
such as `submit-<venue>-<yyyy>`, `arxiv-v1` or `camera-ready`, recorded in
`RELEASE_NOTES.md`.

Overleaf mirrors `paper/` on `dev` through
`.agents/scripts/overleaf-sync.sh`: `status` compares the two sides, `push`
puts `HEAD:paper` on Overleaf as a fast-forward, and `pull` brings Overleaf
edits onto a `sync/overleaf-*` branch for a PR. Both directions check that the
trees are equal, and the repository root never reaches Overleaf. `DEV.md`
describes both.

## Why

An ordinary LaTeX repository answers where the sources are and how to compile
them. This template also answers:

- what the paper wants readers to believe, and which decisions an agent must
  not change silently;
- which experiment questions and interpretation limits support each claim,
  and where each reported number came from;
- whether each citation supports the sentence where it appears;
- which terms, results, figures and tables must stay consistent across the
  manuscript and its three builds;
- which skill should help with the current task;
- what exact source and checks produced a release.

It does not promise better science, and it does not take research decisions
away from the Human. It keeps intent, evidence, authorship and delivery
connected while the manuscript changes, and leaves evidence that the delivered
paper is the one that was reviewed.

## Template versions

**Use this template** copies the latest state of the default branch. For a
reproducible start, clone a release tag instead (replace `<TEMPLATE_TAG>` with
a tag from the Releases page):

```bash
git clone --branch <TEMPLATE_TAG> --depth 1 \
  https://github.com/a-green-hand-jack/paper-agent-project-template.git my-paper
cd my-paper
git remote remove origin
git remote add origin https://github.com/OWNER/PAPER.git
git push -u origin main
```

Read `RELEASE_NOTES.md` at that tag first. Later releases arrive through the
`template-upgrade` skill, and a defect in the template goes back through
`template-feedback`. An existing paper repository joins through
`template-adoption`; one that used `template-sync` follows the v0.4.0 notes in
`RELEASE_NOTES.md`.
