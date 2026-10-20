---
name: venue-icml-2026
date: 2026-10-20
source: https://icml.cc/Conferences/2026/AuthorInstructions and https://icml.cc/Conferences/2026/CallForPapers, read 2026-10-20; the official style archive, downloaded and hashed 2026-10-20
scope: shared
applies_to: papers that target ICML 2026, or plan for ICML 2027 until its own pages are published
status: active
refresh_after: when https://icml.cc/Conferences/2027/CallForPapers stops returning 404; write venue-icml-2027 then
supersedes: null
superseded_by: null
---

# ICML 2026: submission facts (and ICML 2027 unknowns)

## Fact

Checked on 2026-10-20 against the official pages under Evidence. Every ICML
2026 deadline has passed; the facts below are the latest official ICML rules
and are only a planning stand-in for ICML 2027, whose pages are not published.

### Identity

- Venue, year and track: ICML 2026, main track.
- Review model: double-blind; the `[preprint]` option gives a named draft and
  `[accepted]` the camera-ready.

### Timeline

- Abstract deadline: 2026-01-23, AoE (passed).
- Paper deadline: 2026-01-28, AoE (passed).
- ICML 2027: every date UNKNOWN.

### Page limits

- Main text at submission: 8 pages; a paper over the limit is rejected
  automatically.
- Main text at camera-ready: 9 pages.
- Not counted: the impact statement, references and appendices, all in the
  same PDF.

### Submission rules

- Impact statement: required for the main track, in its own section before the
  references.
- Abstract: one paragraph, ideally 4-6 sentences.
- Layout: US letter, two columns, 6.75 in text width, 9 in height, 0.25 in
  column gap, 10 pt Times on 11 pt leading; table captions above, figure
  captions below; do not change margins or spacing.
- File size: at most 50 MB at submission and 20 MB at camera-ready; the page
  states no Type 3 font check. The kit's own text says at most 10 MB and Type 1
  fonts only; the web page is the later source.
- Format checker: https://papercheck.icml.cc/papercheck.html

### Kit

- Official kit URL: https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip
  (228368 bytes, SHA-256 `8b29290f5828e176debb57ea9cc00252502973d55ea561a2f18a7f0a326bfc6c`).
- SHA-256 of the files a paper uses:
  - `icml2026.sty`: `7cdcf90f6a59c5219e7f15c88f7ed09fcaf598dad91e6cdddc4dc3cb0e397a95`
  - `icml2026.bst`: `0ec3d5eb9b02efb7e0b44a32f3775882f42a743d0bdc618f34e6936309b98764`
  - bundled `fancyhdr.sty`: `9130c52f91087abc6d223164ffa587e207e3257fcbcd069ef09ecb5391043f14`
  - bundled `algorithm.sty`: `93fd0eb31c112eb405833db8f1d7f5d238c7e691b1c05680d7276e68f36d564a`
  - bundled `algorithmic.sty`: `48d18794a5d97c0479a588cc2eac0917992feb9da83acc4631b8f55757d80f9b`
- The archive hash equals the one downstream papers recorded in September 2026.
- `icml2026.sty` contains the words "author names" (line 340, a comment) and
  "author name" (line 474, an error message). `make release-check` matches
  each `\PaperIdentity` string against every line the blind build reads, so an
  identity made of those words matches the unmodified kit. The template's
  placeholder identity does not; it fails `identity` on its own until the
  paper declares its authors (#170, checked 2026-10-20 against the archive
  above).

### Unknowns and conflicts

- ICML 2027: the call for papers, dates, page limits and kit are UNKNOWN; the
  2027 pages (`/Conferences/2027`, `/CallForPapers`, `/Dates`,
  `/AuthorInstructions`) returned 404 on 2026-10-20.
- The file-size and font rules of the kit text against the web page (above).

## Evidence

- https://icml.cc/Conferences/2026/AuthorInstructions, read 2026-10-20.
- https://icml.cc/Conferences/2026/CallForPapers (deadlines, statements).
- The kit: `curl -fsSL -o icml2026.zip <kit URL>`, then `sha256sum` on the
  archive and on the extracted files, 2026-10-20.

## Refresh

When the ICML 2027 call for papers is published, write `venue-icml-2027.md`
from `VENUE_TEMPLATE.md` and mark this record superseded for 2027 planning.
