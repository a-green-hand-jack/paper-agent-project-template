---
name: undecided-content-in-author-comments
date: 2026-11-14
source: RSI_light_paper `undecided-content-in-author-comments` record; both downstream papers keep open decisions and placeholders inside paper/ comments
applies_to: paper repositories that build several forms from one source
---

# Undecided content lives in author comments, never in the article

## Decision

Work still to be decided is written as an author comment in the manuscript, next
to the text it concerns, using the macros `paper/style/author-comments.sty`
declares. The article text contains only content the authors have decided. Open
questions are not parked in the development plane, a README or a notes file.

## Why

A decision recorded away from its sentence drifts from the text and is invisible
to whoever reads the built paper; a decision recorded as an author comment
survives the next rewrite because it moves with the paragraph. The build then
tells the truth: `main` shows the comments, `submission` and `blind` do not, and
a release gate fails while any comment remains.

## Apply

- Put the question, the options and who decides in the comment, not just a
  marker such as "TODO".
- Use the command declared for the author who raised it; a custom comment
  command must call `\AuthorComment` or be declared in
  `paper/style/author-comments.sty`, otherwise the leftover check misses it.
- Check the working draft after a rewrite: a comment that no longer applies is
  deleted, not left as history.
- Before a release, `make release-check` must report no surviving author
  comment; deleting the comment means the decision was made or the text left
  out.
