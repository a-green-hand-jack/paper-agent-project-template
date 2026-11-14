---
name: collaborator-content-byte-for-byte
date: 2026-11-14
source: the collaborator-content record of both downstream papers, each written after co-authored drafts were edited in place
applies_to: paper repositories whose manuscript, figures or captions a collaborator wrote
---

# Manuscript content a collaborator wrote is theirs

## Decision

Text, equations, figures and captions supplied by a collaborator stay byte for
byte. A change the paper needs is proposed with the reason and, where it
matters, the attribution, and waits for that collaborator or the Human. Never
rewrite, reformat, translate or "tidy" collaborator content as part of another
edit.

## Why

A collaborator's wording carries their claims, their hedging and their
responsibility. Silent edits make a co-author the author of sentences they did
not write and hide which sentence is whose, and the change is invisible in a
later reading because the file is the only record they see.

## Apply

- Keep collaborator content in its own paragraph, section or float file so a
  diff attributes the change to one person.
- When a claim in collaborator text conflicts with the paper, report the
  conflict and propose a wording; do not resolve it by editing.
- Name the author in the commit message when a commit touches collaborator
  text, and keep their formatting (line breaks, macros, spelling) even when the
  rest of the file is normalised.
- Ask before a mechanical pass (renaming, macro replacement, language change)
  that would touch collaborator text.
