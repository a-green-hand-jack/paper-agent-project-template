---
name: venue-<venue>-<year>
date: YYYY-MM-DD
source: the official pages read, with their URLs
scope: shared | project
applies_to: papers that target <venue> <year>
status: active | superseded
refresh_after: the next official date or announcement that can change these facts
supersedes: null
superseded_by: null
---

# <Venue> <year>: submission facts

Copy this file to `shared/venue-<venue>-<year>.md` (facts any paper can use) or
`project/venue-<venue>-<year>.md` (facts only this paper needs), replace the
placeholders, and link it from that directory's `AGENTS.md`. A value no
official page states stays `UNKNOWN`; never turn a missing fact into an
assumption, and never take a fact from memory or from an earlier year.

## Fact

Checked on YYYY-MM-DD against the official pages under Evidence.

### Identity

- Venue, year and track: UNKNOWN
- Review model (double-blind, single-blind, open): UNKNOWN

### Timeline

- Abstract deadline: UNKNOWN
- Paper deadline: UNKNOWN
- Supplementary material deadline: UNKNOWN
- Reviews released / author discussion: UNKNOWN
- Decisions: UNKNOWN
- Camera-ready: UNKNOWN
- Conference: UNKNOWN

### Page limits

- Main text at submission: UNKNOWN
- Main text at camera-ready: UNKNOWN
- Not counted (references, appendix, required statements): UNKNOWN
- What happens over the limit: UNKNOWN

### Submission rules

- Anonymity rules: UNKNOWN
- Required or recommended statements: UNKNOWN
- Supplementary material: UNKNOWN
- File size and font rules: UNKNOWN
- Policies on prior publication, preprints and AI use: UNKNOWN

### Kit

- Official kit URL: UNKNOWN
- SHA-256 of the kit archive and of each file the paper uses: UNKNOWN
- Options for the review, preprint and camera-ready forms: UNKNOWN

### Unknowns and conflicts

- Every field that is still `UNKNOWN`, and every place where two official
  sources disagree (quote both).

## Evidence

- The official URL of each page read, the date it was read, and the command
  used to hash the kit (for example `sha256sum` on the downloaded archive and
  on the extracted files).

## Refresh

- Recheck before deadline-sensitive planning and before a release, and when
  `refresh_after` is reached. When an official fact changes, update the value,
  the check date and `refresh_after` together; when the paper changes venue,
  supersede the record instead of editing the old year.
