---
name: notation-cost
date: 2026-11-14
source: ResearchWorld_paper `method-section-conventions` record, written while splitting its method section between main text and appendix
applies_to: paper repositories whose method section introduces formal notation
---

# Notation is a cost the reader pays

## Decision

Introduce a symbol only where it buys precision prose cannot provide, define it
once at first use, and reuse it. A concept that appears once is named in words.
The main text carries the notation a reader needs to follow the argument; the
appendix carries the full formalism.

## Why

Every symbol is a lookup the reader performs while reading. Notation that is
introduced to look rigorous and then used once pushes the argument out of the
text, and the same symbol reused for two ideas makes the method section
unreadable.

## Apply

- Give each symbol one meaning for the whole paper; a changed meaning needs a
  different symbol.
- Test a main-text paragraph by removing each symbol in turn: if no precision
  is lost, it belongs in the appendix or in prose.
- Move proofs, derivations and full definitions to the appendix and keep a
  pointer in the main text.
- Keep the notation table consistent with the interface and caption records; a
  renamed symbol is a paper-wide change, not a local edit.
