---
name: writing-exemplar-archive
date: 2026-11-14
source: ResearchWorld_paper Issue #21, which moved its exemplar archive out of .agents/references/ and then committed 1,261 files (262 MB); writing-reference-finder's playbook; Issue #261, a paper whose author keeps its exemplars in Git
applies_to: paper repositories that keep example papers to study structure and expression
---

# Study exemplars as writing models, stored where the project decides

## Decision

Example papers are writing models: they teach structure and expression, and
what a cohort taught goes to a knowledge record as a card. They are never a
citation.

Where the papers, PDFs and source bundles live is `EXEMPLAR_STORE`: by default
the ignored `.project/artifacts/writing-exemplars/` or managed storage outside
the repository; a project may instead keep them in Git under a path it
registers in `policy.root_files` of the content registry. They never enter
`paper/`.

## Why

An exemplar is read once, quoted in a card and rarely reopened; keeping the
payload in Git makes every clone, worktree and upgrade carry hundreds of
megabytes of third-party PDFs, mixes other authors' copyright into the
repository, and pushes the tracked tree past the size where `git diff` and
review stay useful. That is why the default store is ignored. An author who
wants a fixed reference set beside the paper for every agent may accept those
costs; the store is then a declared root, not an unregistered directory. The
card is what the paper actually uses.

## Apply

Each project fills one parameter in the `## In this repository` section at the
end of this record (see `template-adoption` step 5):

- `EXEMPLAR_STORE`: `.project/artifacts/writing-exemplars/` (ignored), managed
  storage, or a tracked path also listed in `policy.root_files`. Without a
  value, the ignored default.

Then:

- Download and extract under `<EXEMPLAR_STORE>/<cohort>/`; keep the reading log
  next to the download.
- Write one knowledge card per cohort: what the exemplar does, the sentence or
  figure worth imitating, and the claim it does *not* support.
- In managed storage, record the location, checksum and the command that
  produced it in the reading log.
- A factual claim taken from an exemplar is verified in the original before it
  enters the manuscript.
