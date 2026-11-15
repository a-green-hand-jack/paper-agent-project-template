---
name: revision-rounds
description: Run one round of author review on a manuscript: count the habit a reviewer marked, plan before and after, wait for approval, then edit, build, measure and report.
---

# One review round, run as a measured change

A reviewer marks two or three places. That is a sample of a habit, not the list
of edits. A round that fixes only the marked places returns for the same
complaint, so the round starts with a count and ends with a count.

## 1. Read the comments, change nothing

Take in the edited manuscript first (for an Overleaf project, the tree, not the
commits: the editor rewraps every commit it receives, so commit ids never
match). Separate the reviewer's own edits — which are content and stay — from
the comments, which are instructions. Say back what each comment asks for in one
sentence.

## 2. Count the habit, and its relatives

A reviewer who marks "sentences open with *A world … A role …*" is marking a
sentence skeleton. Before proposing anything, count it over every section:
openers, connectors, sentence length, comma series, one name per thing. Report
the counts per section — they are what shows the reviewer the habit is
understood, and they are the only way to tell whether the repair worked.

Look for the relatives too: a reporter of `, so` also tends to chain `, and`, to
hang `, which`, and to reuse an opener for half a paragraph. Fixing only the
marked form produces a different tic in the same place; if every `, so` becomes
`therefore`, the text is still monotone.

## 3. Record the rule before the edits

An instruction from a reviewer is a standing rule for the rest of the paper. Write
it into the project's style reference with its date and the commit it came from,
then plan against the rule rather than the comment. A rule that stays in a
comment is lost by the next rewrite.

## 4. Plan before and after

Put a plan in `.agents/notes/`, registered, that shows each changed sentence
before and after, with the counts from step 2. Where an edit moves line breaks,
apply it in a copy of the repository outside the working tree, build and measure
there, and record the measured result in the plan. List separately every
addition that carries content and every place a locked item is touched.

Wait for the reviewer's approval before editing `paper/`. A reviewer may waive
review for a part; then the report says which content-bearing additions were
never seen.

## 5. Edit, build, measure, report

Apply the plan, run the builds and `make check`, measure the rendered pages (see
[`post-build-visual-inspection`](../../../../../memory/shared/paper-build/post-build-visual-inspection.md)),
and repeat the measurement until nothing is listed. Report the counts from step 2
again after the edit, the files changed, the comments removed and the comments
kept, and every addition that carries content.

## What a round must not do

- Change a claim, a number or an experiment condition to satisfy a style
  comment; a revision changes structure, not findings.
- Install a new monotony while removing one.
- Drop a detail that one sentence loses without stating it elsewhere.
- Reword text a collaborator wrote, or answer a reviewer by editing the
  reviewer's own words.
