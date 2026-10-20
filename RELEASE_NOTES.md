# Release notes

This file records this template's own releases, one `## <tag>` heading each.
A paper made from the template keeps its own release notes instead and does
not copy this history.

## v0.4.1

Fixes the reference tooling and the adoption order that downstream papers
reported after taking v0.4.0 (#166).

### Fixed

- `reference-evidence.py inventory` recorded `claim_text` from the citation
  command instead of the start of the sentence, so the claim was missing from
  the record and its fingerprint (#159). It now records the whole sentence;
  the part before or after the citation that is longer than 600 characters is
  cut at a word boundary and marked `claim_text_truncated`.
- When a cited sentence changed, `inventory` gave it a new occurrence and left
  its evidence pointing at the old one, which the Draft gate rejected
  (`points to unknown occurrence`). The evidence now moves to the new
  occurrence at the same location with the same keys and keeps its old
  fingerprint, so it is stale: Draft warns and Release fails, as the
  reference contract says.
- A shipped test ran the Release reference gate on the repository itself, so
  `make check` failed in any paper whose ledger was still at Draft strength
  (#160). It now tests the factory state in a temporary directory, and
  `make check` is the Draft gate again.
- `diagnose-environment.sh` cannot pass during an adoption from `main`, before
  `dev` exists (#161). The v0.4.0 notes (steps 8 and 10) and
  `template-adoption` now name the three branch-model lines that are expected
  to fail until the maintainer runs `init-branches.sh` after the merge. The
  script is inherited unchanged; the change to it is reported upstream.
- `reference-evidence.py migrate` wrote evidence that the Draft gate rejected
  (`source_identity lacks a stable identifier or source_hash`) (#162). It now
  copies the reference's identifiers and a `source_hash` into
  `source_identity`, as `record` does.
- The `references` CI job failed in a repository with a policy and no ledger,
  a state the Draft gate accepts (#163). Its `status` and `inventory` step now
  runs only when `.agents/references/ledger.json` exists.
- Title normalization read a LaTeX accent (`Caf{\'e}`) as a wording change, so
  the correction audit failed against a Unicode candidate title (#164). Accents
  are now decoded to Unicode with the locked `bibtex-updater`'s own decoder
  before NFKC.
- The online metadata audit could not verify a COLM citation (#165):
  - a DBLP `202` bot-challenge page is now an infrastructure outcome
    (`bot_challenged_services`; an `unverified` run becomes
    `provider_unavailable`), not "no hit";
  - a reference that the ledger records `verified` from `openreview` and
    `agent-resolved` or `human-confirmed` is reported, not failed, when the
    checker matched its OpenReview record and only the year or the venue name
    differs (`ledger_reviewed_openreview_keys`).

  The locked `bibtex-updater` 1.6.1 is not patched. Its later releases map
  `COLM` (1.11.0) and report DBLP's 202 as an incomplete lookup (1.12.0);
  reading an OpenReview record's year from `venueid` is reported upstream
  ([rpatrik96/bibtexupdater#82](https://github.com/rpatrik96/bibtexupdater/issues/82)).

### Upgrading a paper from v0.4.0

Take the release with `template-upgrade`, then:

1. Run `python3 .agents/scripts/reference-evidence.py inventory`. The claim
   fingerprint and the occurrence id change for every citation (#159); until
   `inventory` runs, the Draft gate fails on occurrences missing from the
   ledger. Afterwards every occurrence is `pending` and its evidence stale
   (Draft warns, Release fails). Record the support evidence again with
   `packet` and `record` (the `citation-support-review` skill), and have the
   Human confirm it again before `make release-check`.
2. A paper that migrated a v1 ledger with v0.4.0 and repaired
   `source_identity` by hand keeps working. Every occurrence that `migrate`
   writes starts `pending`, because occurrence-level review is new in v2, and
   needs a fresh Human confirmation before `make release-check` (#162).
3. Drop any local workaround for #160 (a skipped Release subtest) or #163 (a
   ledger bootstrapped only to turn the `references` job green).
4. A COLM or other OpenReview-only citation that the audit cannot verify:
   record its identity in the ledger as `verified` with `openreview` among the
   sources, an `openreview` identifier, and `agent-resolved` (or
   `human-confirmed` by the Human).

## v0.4.0 — 2026-10-20

This is a breaking release. The template is rebuilt on
[`coding-agent-project-template`](https://github.com/a-green-hand-jack/coding-agent-project-template)
`v0.1.13` and renamed `paper-agent-project-template` (#156). A paper is now
developed like code: a self-contained `paper/` product tree, Issues and PRs
from `dev`, a build that acts as the test suite, tagged releases on `main`,
and a recorded source for every reported number.
`.agents/memory/project/rebuild-on-coding-template.md` maps every earlier
path, tool, test, skill and decision to its new place.

### Changed

- **Inheritance.** The template adopted the coding template's scripts, shared
  skills (`issue-workflow`, `worktree-lifecycle`, `template-adoption`,
  `template-upgrade`, `template-feedback`, `release-doc-audit`,
  `asset-lifecycle`, `cli-first-operations`, `project-memory-governance`) and
  shared memory records, unchanged. Their adaptation is only in trailing
  `## In this repository` sections. The registry names this template in
  `template` and the coding template in `template.upstream`.
- **Branches.** `dev` is the default and integration branch; `main` is the
  release branch. `template-dev` is retired, and its last commit is kept as
  the tag `archive/template-dev`.
- **Product plane.** `paper/` holds `main.tex`, `submission.tex`, `blind.tex`,
  `authors.tex`, `macros.tex`, `refs.bib`, `sections/`, `figures/`, `tables/`,
  `algorithms/`, `style/` and a `Makefile`, and builds with no file outside
  `paper/`. One source gives three builds in a fixed order, each removing a
  layer: `main` (named, with notes), `submission` (notes removed) and `blind`
  (identity and acknowledgements removed as well).
- **Builds.** The root `Makefile` has the targets `pdf`, `blind`,
  `submission`, `check`, `release-check` and `clean`. TeX comes from `PATH` or
  `TEXBIN`, and all output goes to the worktree's `.project/build/`.
  - `make check` fails on undefined references or citations, missing files,
    multiply defined labels, lost underscores in the PDF text, reference
    ledger errors, interface-macro errors, invalid skill or record structure
    and failing tests. It reports the main-text pages of `blind` against
    `PAGE_BUDGET`.
  - `make release-check` fails on author identity in the anonymous PDF, its
    metadata or its sources, on leftover notes or TODOs in `submission`, on a
    missing or exceeded page budget, and on references below release
    strength.
- **Human plane.** The root holds `README.md`, `PAPER.md`, `DEV.md`,
  `RELEASE_NOTES.md` and `AGENTS.md`, with `CLAUDE.md` as a symlink to it.
  `EXPERIMENTS.md`, `PAPER_INTERFACES.md`, `PUBLICATION.md`, `BRIEF.md` and
  `DECISIONS.md` became typed records under `.agents/memory/`, and
  `REFERENCES.md` and `LATEX_TEMPLATES.md` became memory and knowledge
  records.
- **Evidence.** `assets/MANIFEST.yaml` registers every result table, figure
  data file and reported number with its source repository, commit, run,
  checksum and regeneration command. Numbers reach the text only through
  interface macros, each with a `% Interface:` marker in `paper/macros.tex`
  and an entry in `.agents/memory/project/paper-interfaces.md`.
- **Overleaf.** `.agents/scripts/overleaf-sync.sh` has `status`, `push` and
  `pull`. `push` puts `HEAD:paper` on the Overleaf tip as a fast-forward;
  `pull` brings Overleaf edits onto a `sync/overleaf-<commit>` branch for a PR.
  Both check that the trees are equal, and the repository root never reaches
  Overleaf. The remote comes from local Git configuration, and credentials
  stay in Git's credential channel.
- **Releases.** A release is a PR from `dev` to `main`, a tag such as
  `submit-<venue>-<yyyy>`, `arxiv-v1` or `camera-ready`, and an entry in the
  paper's `RELEASE_NOTES.md`.
- **CI.** `template-check` (inherited: `structure`), `paper-check` (`check`,
  `paper-only`) and `reference-validation` (`references`). Required checks on
  `main` become `structure`, `check`, `paper-only` and `references`.
- **Skills.** All skills are under `.agents/skills/shared/`. Harvested from the
  downstream papers and generalized: `writing-router`,
  `writing-reference-finder`, `openreview-review-collector`, `figure-router`,
  `scientific-figure-workflow` and `poster-build`. Vendored at pinned commits,
  each with its licence and a hashed `PROVENANCE.md`: `scientific-writing`,
  `scientific-english-editor`, `better-usage`, `academic-voice`, `proofread`,
  `lieflat-less-ai-tone`, `scipilot-figure-skill`, `icarus-figures`,
  `thesis-figure-skill`, `tikz-figure-code` and `image-to-editable-ppt` (the
  last patched so that it never reads another tool's login).
- **Records.** New shared memory records hold the lessons the downstream
  papers share: one source and three builds, Overleaf receiving the paper tree
  only, syncing Overleaf before editing, post-build visual inspection, valid
  skill front matter, the page budget on the blind build, unmodified official
  venue kits, TeX from `TEXBIN`, results through interface macros, and
  reference integrity. New shared knowledge records hold dated facts on ICLR
  2027, ICML 2026, NeurIPS 2026 posters, official LaTeX kits and the
  bibliographic metadata services, each with a refresh condition.
- **Repository.** The description is "Paper template built on
  coding-agent-project-template: develop a paper like code".

### Fixed

- `paper-brief.py ingest` split a multi-line bullet into several bullets,
  including in the locked section of `PAPER.md` (#154). It now keeps the
  continuation lines of every list item.
- `reference-evidence.py inventory --location` deleted the occurrence records
  of every other location. It now keeps them.
- `reference-evidence.py record --origin` silently recorded an unknown origin
  as `agent-pdf`. It now refuses an unknown origin.
- `check-reference-integrity.py` now validates `bibliography_origin` in
  `.agents/references/policy.json`.
- Eight `SKILL.md` files (seven `ccf-*` wrappers and `writing-dna-skill`)
  had front matter that did not parse. They are retired, and `make check`
  now parses every `SKILL.md`.
- The reference-validation workflow no longer falls back to a personal
  e-mail address; it reads the `BIBTEX_CHECK_MAILTO` repository variable.
- The tracked Overleaf configuration that named this template's own Overleaf
  project is removed.

### Retired

`template-sync`, `paper-init.py`, `template-inheritance.json`,
`template-sync.json`, the old `template-adoption` tool and skill,
`paper/variants/`, `paper/generated/`, build profiles (`paper-build.json`,
`external-latex`), release instances and release records (`release.py`,
`releases/`, `build-release.yml`), the documentation-consistency checker,
`verify.sh` and the checks of the old layout, the CCFA-Skills suite and
writing-dna-skill with their wrappers, and the root documents `AGENT_GUIDE.md`,
`ANATOMY.md`, `CONTRIBUTING.md`, `WHY_THIS_TEMPLATE.md`, `LATEX_TEMPLATES.md`
and `REFERENCES.md`. #155 (an `external-latex` adoption blocked by
canonical-variant fixtures) is obsolete with them.

### Moving a paper that uses `template-sync`

`template-sync` cannot carry a paper across this release, because the release
changes the layout that `template-sync` itself depends on. Move once, as an
adoption, and use `template-upgrade` for every later release.

1. **Open an Issue** in the paper repository and do the move on its branch in
   a separate worktree, like any larger change. `.agents/template-sync.json`
   names the last template commit the paper reviewed; its downstream-local
   paths are the paper's own additions and must survive the move.
2. **Read the release** without changing your checkout, for example with
   `git clone --branch v0.4.0 --depth 1 https://github.com/a-green-hand-jack/paper-agent-project-template.git`
   into the worktree's `.project/`. Follow its `template-adoption` skill and
   write the migration map before changing anything.
   `.agents/memory/project/rebuild-on-coding-template.md` in the release says
   where each old path went.
3. **Take the development plane** from the release: `AGENTS.md` and the
   `CLAUDE.md` symlink, `.agents/` (scripts, skills, records, tests, registry),
   `.github/`, the root `Makefile`, `assets/`, `.env.example` and the
   `.gitignore` rules. Then remove what belongs only to the template and fill
   the slots it leaves to the paper, as `README.md` ("Start a paper", steps 4
   and 5) describes. Keep `template.repository` and set
   `template.version: v0.4.0`, without an `upstream` block.
4. **Move the paper into the new `paper/` layout:**
   - Keep `sections/`, `figures/`, `tables/`, `refs.bib`, `macros.tex` and
     `style/`, and use the release's `main.tex`, `submission.tex`,
     `blind.tex`, `authors.tex` and `Makefile` as the frame.
   - Map the variants onto the three builds: `draft` is `main`,
     `camera-ready` and `arxiv` are `submission`, and `anonymous` is `blind`.
   - Put the author block in `paper/authors.tex`, with one
     `\PaperIdentity{...}` for each name, e-mail address, affiliation or URL
     that the anonymous build must not contain.
   - Write author notes as `\PaperNote{...}`. Keep acknowledgements in the
     part of `main.tex` that `blind` leaves out.
   - A variant difference that does more than remove a layer, such as a
     camera-ready style option, is a Human decision: record it in
     `.agents/memory/project/publication.md`.
   - Move `paper/venue_preamble.tex` into `main.tex`. Move each number from
     `paper/generated/` into an interface macro in `macros.tex`, with an
     `assets/MANIFEST.yaml` entry.
   - Add a `% Interface: <Name>` marker above each interface macro.
5. **Move the root contracts into records:**
   - `EXPERIMENTS.md` becomes `.agents/memory/project/experiments.md`.
   - `PAPER_INTERFACES.md` becomes `paper-interfaces.md`.
   - `PUBLICATION.md` becomes `publication.md`, and its reference policy block
     becomes `.agents/references/policy.json`.
   - `BRIEF.md` becomes `brief.md`, and each active entry of `DECISIONS.md`
     becomes its own project record.
   - `PAPER.md` stays; replace its mentions of variants.
   - Move `references/ledger.json` to `.agents/references/ledger.json`, and
     change the marker line at the top of `paper/refs.bib` to that path.
6. **Delete what this release retires:**
   - under `.agents/`: `template-sync.json`, `template-inheritance.json`,
     `paper-build.json`, `documentation-consistency.json`, `init-state.json`,
     `template-origin.json`, `ANATOMY.md`, `runtime/`, `tools/`,
     `dependencies/` and `vendor/`, and the `ccf-*` and `writing-dna-skill`
     wrappers;
   - `releases/`;
   - at the root: `AGENT_GUIDE.md`, `ANATOMY.md`, `CONTRIBUTING.md`,
     `LATEX_TEMPLATES.md`, `REFERENCES.md` and `WHY_THIS_TEMPLATE.md`;
   - `.github/workflows/pr-validation.yml` and `build-release.yml`.

   Before deleting `.agents/overleaf-sync.json`, add its project URL as a
   local remote, without a token in it:
   `git remote add overleaf https://git.overleaf.com/<project-id>`.
7. **Carry the release history.** Each record in `releases/records/` becomes a
   `## <tag>` entry in the paper's own `RELEASE_NOTES.md`; tag the released
   commits when they are known.
8. **Verify** with `bash .agents/scripts/setup-worktree.sh`,
   `bash .agents/scripts/diagnose-environment.sh`, `make pdf`, `make blind`,
   `make submission` and `make check`, and confirm that `git status --short`
   is empty afterwards. Until step 10 creates `dev`, `diagnose-environment.sh`
   exits 1 on its three branch-model lines, and only on them:
   `FAIL local dev branch`, `FAIL origin/dev branch` and
   `FAIL GitHub default branch: main` (a `skip` where `gh` is not
   authenticated). This is expected; every other line must pass. Compare `blind` and `submission` with the last
   anonymous and camera-ready PDFs, by page count and by their `pdftotext`
   text: the move changes how the paper is built, not the paper.
9. **Overleaf.** `bash .agents/scripts/overleaf-sync.sh status` reports
   `overleaf-behind` (Overleaf holds an earlier state of `paper/`) or
   `in-sync`; if it reports Overleaf edits, `pull` them first. After the PR
   merges into `dev`, run `push`.
10. **On GitHub**, after the merge, the maintainer makes `dev` the default
    branch if it is not (`bash .agents/scripts/init-branches.sh`), and moves
    the required checks on `main` to `structure`, `check`, `paper-only` and
    `references`. `diagnose-environment.sh` then passes its three
    branch-model lines as well.

## Earlier releases

Before v0.4.0 the template was `agent-writing-harness` (v0.3.x) and, before
that, `ccfa-writing-paper-template`. Each tag's GitHub release or commit has
the details.

- **v0.3.1 — 2026-09-02**: a supplied, read-only bibliography can be cited
  offline at Draft strength (#153).
- **v0.3.0 — 2026-08-28**: the repository is renamed `agent-writing-harness`
  (#151).
- **v0.2.1 — 2026-08-25**: template repository test fixtures are isolated.
- **v0.2.0 — 2026-08-24**: the template development surface moves to
  `template-dev`, and the CCFA-Skills suite and writing-dna-skill are bundled.
- **v0.1.0 — 2026-08-09**: template lifecycle validation is hardened (#91).
- **v0.0.5 — 2026-07-17**: the first tagged release, with display macros,
  numbered file names, a flattened arXiv export, Overleaf publishing and
  venue-kit verification gates.
