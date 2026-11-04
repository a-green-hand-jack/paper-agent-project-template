---
name: paper-interface-maintenance
description: Use when adding or changing a recurring paper-facing name, term, symbol, result, claim form, figure, table, or LaTeX interface macro.
---

# Paper Interface Maintenance

## Trigger

Use when adding or changing a recurring paper-facing name, term, symbol,
result, claim form, figure, table or LaTeX interface macro.

## Minimum context

- the entry in `.agents/memory/project/paper-interfaces.md` (each interface
  macro's meaning, control cue and source);
- `paper/macros.tex` and its active consumers;
- for a value taken from a code repository, its entry in
  `assets/MANIFEST.yaml` (source repository, commit, run or config, checksum,
  regeneration command);
- the related claim or experiment record only when meaning or result
  interpretation is involved.

## Procedure

1. State the current interface meaning and control boundary.
2. Search active paper surfaces for every consumer.
3. Distinguish a presentation or value update from a semantic change.
4. A reported number reaches the text only through its macro
   (`.agents/memory/shared/results-through-interface-macros.md`). A new value
   from a code repository changes together with its manifest entry; never
   type a number that has no recorded source, and never write a planned result
   as an observation. An unknown value stays `\PaperTODO{}`.
5. Keep low-risk implementation changes local and consistent.
6. For a semantic change, show the Human the old meaning, proposed meaning,
   affected claims and experiments, and the migration impact.
7. Update the macro, its interface record and all active consumers together.
8. Run `make check`; its interface check fails on a macro that is defined but
   unused, used but undefined, or called without its `{}`.
9. Report stale aliases, literal duplicates, placeholders and unresolved uses.

## Human decision

Request Human review before changing metric, split, aggregation, uncertainty
meaning, claim strength, stable terminology meaning or an artifact's narrative
responsibility.
