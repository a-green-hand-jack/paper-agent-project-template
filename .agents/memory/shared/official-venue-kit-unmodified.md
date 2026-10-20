---
name: official-venue-kit-unmodified
date: 2026-10-20
source: Issue #156 §7; venue-template migrations in downstream paper repositories, including a running header lost with a newer system fancyhdr and false review banners
scope: shared
applies_to: paper repositories that move a paper onto a venue's official LaTeX kit
status: active
supersedes: null
superseded_by: null
---

# Use the venue's official kit unmodified, and change typesetting only

## Decision

1. **Use the official kit for the exact venue and year**, never a hand-written
   imitation when a kit exists. Record its URL and the SHA-256 of the files used
   in the paper's publication record.
2. **Keep the kit unmodified, including the helper packages it bundles.** A kit
   that ships its own `fancyhdr.sty` or `natbib.sty` depends on that version.
3. **A migration changes typesetting only.** Text, claims, figures and
   references stay as they were; a migration PR shows no content change.
4. **Build both the named and the anonymous forms**, and check the anonymous
   PDF's text and metadata (the Author field is empty) for identity.
5. **Keep running headers truthful.** No "Under review" on a preprint, no
   "Published as" before acceptance.
6. **When the target venue changes, update every line that names it** in the
   same change: records, entry-file comments, the page budget and the knowledge
   record used.

## Why

A venue's running header disappeared when the system's newer `fancyhdr`
replaced the version bundled with the kit, so removing a kit's helper packages
is a typesetting change in disguise. Local imitation styles drifted from the
official geometry. Builds carried false review banners after a migration, and
papers kept stale venue names in records and comments after the target
changed.

## Apply

- Put the kit's class and style files into `paper/` (or `paper/style/`), keep
  them byte-identical to the download, and load them from `paper/main.tex`;
  `paper/style/compat.sty` keeps the template's display macros working under a
  venue kit.
- Build `make submission` and `make blind`, then run `make release-check`: it
  searches the anonymous PDF text, its metadata and its sources, the kit's
  files included, for every `\PaperIdentity` string. Replace the template's
  placeholder identity in `paper/authors.tex` first: `identity` fails on the
  placeholder until then. The placeholder is a synthetic token, so a kit's
  own text about authors does not match it. The search matches substrings, so declare specific strings (a full
  name, not a lone common word); a declared string that the kit's text
  contains still fails.
- Look up the venue's dated facts in `.agents/knowledge/shared/` and refresh
  them when their `refresh_after` condition is met.
