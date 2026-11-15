---
name: undecided-content-visible-placeholder
date: 2026-11-15
source: ResearchWorld_paper Issue #61 (eight author comments that a submission build erased) and its record `pending-items-outside-the-manuscript`; replaces the earlier rule that kept undecided content in author comments
applies_to: paper repositories that build several forms from one source and keep undecided items while they write
---

# An undecided item is a visible placeholder, its detail a note

## Decision

1. **In the manuscript** an item the paper has not decided is `\PaperTODO{...}`
   at the sentence, paragraph or table it concerns. It shows in every build, so
   a reader sees that something is missing, and `make release-check` rejects it,
   so the paper cannot be released while the item is open.
2. **Outside the manuscript** the item's text, its evidence and what it waits
   for live in one working note under `.agents/notes/` and in the Issue that owns
   the work. The manuscript keeps one line about what is missing, not the
   reasoning.
3. **Author comments are a review round, not a parking place.** `\jieke{}` or
   whatever commands `paper/style/author-comments.sty` declares carry the words
   of a reviewer during one round; the comment is removed by the edit that
   answers it. A comment that waits for the experiment side or the final results
   becomes a `\PaperTODO` plus a note entry, not a comment that stays forever.
4. **A comment macro must call `\AuthorComment`** and be declared in
   `paper/style/author-comments.sty`. A box or note command that renders text
   directly is invisible to `make release-check`, which enumerates the author
   commands it can see; such a macro hides open work from the gate.

## Why

Both mechanisms make the release gate fail, but only one leaves the state
visible to a reader. In `ResearchWorld_paper`, eight author comments sat in the
sources the submission build reads: the gate went red on a source grep while the
compiled submission showed nothing, so a co-author reading the PDF could not
tell that a metric set, a per-role score and a completeness table were still
missing. The same file also mixed revision narration ("not rewritten in this
revision") with real pending data, so nobody could count what remained.

`\PaperTODO` keeps the marker where the item is, which is what the earlier rule
was right about, without hiding it in the form a reviewer receives. Moving the
reasoning to a note and the work to an Issue gives the item an owner and a
"waiting on" that a comment in the text cannot carry (see
[`issue-close-out`](../issue-close-out.md) for the work side).

## Apply

- Add `\PaperTODO{...}` where the item belongs and a line in the working note
  naming what is missing, who provides it and the Issue that tracks it.
- When the item arrives, replace the placeholder with the content in the same
  change that closes it, and update the note.
- Keep author comments only for words a reviewer wrote in one round. Answering
  one deletes it; converting one to pending work is `\PaperTODO` + note.
- Check that every comment command in `paper/style/author-comments.sty` is a
  call of `\AuthorComment`; `make release-check` lists the commands it enumerates,
  so a command missing from that list is a defect, not a quiet exemption.
- A paper may have a stronger local rule (for example author wording that must
  stay verbatim); it records that in its own record and says how a pending item
  is then marked.
