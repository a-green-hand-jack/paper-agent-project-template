---
name: venue-iclr-2027
date: 2026-10-20
source: https://iclr.cc/Conferences/2027/AuthorGuidelines and https://iclr.cc/Conferences/2027/Dates, read 2026-10-20; the official style-file archive, downloaded and hashed 2026-10-20
scope: shared
applies_to: papers that target ICLR 2027
status: active
refresh_after: 2026-12-16 (final decisions), and when the camera-ready instructions arrive (announced for mid-February 2027)
supersedes: null
superseded_by: null
---

# ICLR 2027: submission facts

## Fact

Checked on 2026-10-20 against the official pages under Evidence.

### Identity

- Venue, year and track: ICLR 2027, main conference.
- Review model: double-blind. Revealing identity in the main text or the
  supplementary material leads to desk rejection; abstracts must be genuine.
- A paper is desk-rejected when none of its authors is registered as a
  reviewer.

### Timeline

- Abstract deadline: 2026-09-18, AoE (passed).
- Paper deadline: 2026-09-25, AoE (passed); supplementary material has the
  same deadline.
- Reviews released: 2026-11-05; author-reviewer discussion 2026-11-05 to
  2026-11-18; reviewer-AC discussion 2026-11-19 to 2026-12-16.
- Final decisions: 2026-12-16.
- Camera-ready: instructions by e-mail in mid-February 2027; no date listed.
- Conference: main conference April 26-28, workshops April 29-30 (the Dates
  page shows no year on these lines and also says "location and dates to be
  announced").

### Page limits

- Main text at submission: at most 9 pages, strictly enforced; over the limit
  is a desk rejection.
- Main text during the discussion and at camera-ready: 10 pages.
- Not counted: references and appendices (both unlimited), the AI use
  statement, the ethics statement, the reproducibility statement and the
  acknowledgements.
- The camera-ready and rebuttal FAQ also says, verbatim, "Page limit is
  identical with the submission version (10 pages)", which conflicts with the
  9-page submission limit above.

### Submission rules

- AI use statement: required, not counted.
- Ethics statement: optional, at most one page, not counted.
- Reproducibility statement: recommended, not counted.

### Kit

- Official kit URL: https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip
  (39348 bytes, SHA-256 `0d940dfa9398ae99a18f24a85a8a683f367204b6af6d17d2899e60a67102529e`).
- SHA-256 of the files a paper uses:
  - `iclr2027_conference.sty`: `797deef41724e93761426ac0cbcca46279a91cc650dd1f0ce76a4f08d2098ea6`
  - `iclr2027_conference.bst`: `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5`
  - bundled `fancyhdr.sty`: `b56ec4434b9f4607529a4b23dc68ad8d4b94f1f631c8cddaf7da78140d53a5ea`
  - bundled `natbib.sty`: `88bc70c0e48461934cab5b2accef06b74a8b3ac45ad03ccd3f2a6b7e0d6d530d`
- The same `.sty`, `.bst`, `fancyhdr.sty` and `natbib.sty` hashes were recorded
  by downstream papers in September 2026, so the kit has not changed since.
- Options: the review form is the default; `\iclrfinalcopy` gives the
  camera-ready. Single column, 5.5 x 9 in text block, Times, author-year
  citations.
- Keep the bundled `fancyhdr.sty`: with the newer system `fancyhdr` of TeX Live
  2026 the review running header disappears.

### Unknowns and conflicts

- Camera-ready deadline and supplementary rules for the camera-ready: UNKNOWN.
- The 9-page against "identical ... (10 pages)" wording above.
- The conference year and location on the Dates page.

## Evidence

- https://iclr.cc/Conferences/2027/AuthorGuidelines, read 2026-10-20 (page
  limits, statements, anonymity, reviewer registration, deadlines, kit URL).
  The older path `/Conferences/2027/AuthorGuide` returns 404.
- https://iclr.cc/Conferences/2027/Dates, read 2026-10-20.
- The kit: `curl -fsSL -o iclr-2027-style-files.zip <kit URL>`, then
  `sha256sum` on the archive and on the extracted files, 2026-10-20.

## Refresh

Recheck at the final decisions (2026-12-16) and when the camera-ready
instructions arrive, before any camera-ready work; re-hash the kit before
building a camera-ready from it.
