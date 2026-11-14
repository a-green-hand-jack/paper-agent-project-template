---
name: writing-exemplar-archive
date: 2026-11-14
source: ResearchWorld_paper Issue #21, which moved its exemplar archive out of .agents/references/ and then committed 1,261 files (262 MB); writing-reference-finder's playbook
applies_to: paper repositories that keep example papers to study structure and expression
---

# Study exemplars outside Git

## Decision

Example papers are read from `.project/artifacts/writing-exemplars/`, which is
ignored, or from an external asset declared in `assets/MANIFEST.yaml`. What a
cohort taught goes to a knowledge record as a card; the papers, PDFs, source
bundles and screenshots themselves never enter Git.

## Why

An exemplar is read once, quoted in a card and rarely reopened; keeping the
payload in Git makes every clone, worktree and upgrade carry hundreds of
megabytes of third-party PDFs, mixes other authors' copyright into the
repository, and pushes the tracked tree past the size where `git diff` and
review stay useful. The card is what the paper actually cites.

## Apply

- Download and extract under `.project/artifacts/writing-exemplars/<cohort>/`;
  keep the reading log next to the download, not in the repository.
- Write one knowledge card per cohort: what the exemplar does, the sentence or
  figure worth imitating, and the claim it does *not* support.
- When material must be retained, move it to managed storage and register it in
  `assets/MANIFEST.yaml` with source, checksum and the command that produced it.
- An exemplar is a writing model, never a citation: a factual claim taken from
  one is verified in the original before it enters the manuscript.
