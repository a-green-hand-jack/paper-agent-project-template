---
name: openreview-review-collector
description: Collect the OpenReview reviews, meta-review, discussion and decision of this paper and normalise them into a review dossier with a triaged revision queue; use for reviewer-feedback triage, rebuttal planning and post-review revision tracking.
---

# OpenReview Review Collector

Collect the OpenReview feedback on this paper once and turn it into a
structured dossier that writing and review work can use without scraping or
rereading the forum again.

## When to use

- to collect, download or summarise the OpenReview reviews of this paper;
- to structure reviewer comments for later work;
- to triage concerns, weaknesses, questions, requested experiments or
  rebuttal items;
- to update the revision plan from reviews, the meta-review, the discussion
  or the decision.

For writing exemplars found on OpenReview use `writing-reference-finder`; for
literature search use `citation-support-review`.

## Context to read first

1. `PAPER.md`: the paper's identity, locked and bounded claims, current
   evidence state and unresolved decisions.
2. `.agents/memory/project/experiments.md` when feedback touches results,
   baselines, protocols, ablations or claim support.
3. `.agents/memory/project/paper-interfaces.md` when feedback touches names,
   terms, notation, result macros, figures, tables or claim forms.
4. `.agents/memory/project/publication.md` when feedback affects the
   submission, a release, the Overleaf project, the venue or a camera-ready or
   revision package.

## Inputs

In order of preference:

1. the OpenReview forum URL or forum id of the submission;
2. an OpenReview JSON export, PDF or copied review text that the Human
   provides;
3. a raw capture already under `.project/artifacts/openreview/<forum-id>/raw/`.

Never ask for, print or store passwords, cookies, API tokens or browser
profile databases. If the forum is not public, use a browser session the
Human logs into themselves (below), or ask for an export.

## Browser-assisted collection

Use this path when direct API requests return a challenge such as
`ChallengeRequiredError`, when reviews are visible only after login, or when
the Human asks for it. It needs Chrome or Chromium and Node.js 22 or later.

1. Start a visible browser with a throwaway profile outside the repository
   and a debugging port bound to the local machine:

   ```bash
   forum=<forum-id>
   raw=.project/artifacts/openreview/$forum/raw
   profile=$(mktemp -d)
   mkdir -p "$raw"
   google-chrome --user-data-dir="$profile" --remote-debugging-port=9222 \
     --no-first-run --new-window "https://openreview.net/forum?id=$forum"
   ```

   On macOS start the browser with
   `open -na "Google Chrome" --args <the same flags>`. The debugging port gives
   full control of that browser to local processes: keep it on `127.0.0.1`
   and close the browser when the capture is done.
2. The Human completes OpenReview's challenge or login in that window.
3. Extract the forum from inside the page, so no cookie or token leaves the
   browser:

   ```bash
   node .agents/skills/shared/openreview-review-collector/scripts/openreview-cdp-extract.mjs \
     --forum "$forum" --out "$raw"
   ```

   It writes `openreview-cdp-capture.json` (page URL, title, page text and the
   status of each API read), `note_by_id.json`, `forum_notes.json`,
   `forum_references.json` (`.txt` when a response is not JSON) and
   `page-body.txt`, and prints a JSON status summary. Pass
   `--cdp http://127.0.0.1:<port>` when the browser listens on another port,
   for example one forwarded over SSH from the machine that shows the browser.
4. If an API read still reports HTTP 403, ask the Human to repeat the
   challenge in the open window and rerun only the extractor. If the page
   cannot be reached, ask for an export instead.
5. Close the browser and delete the throwaway profile (`rm -r "$profile"`);
   it holds the login session.

Before writing new automation, look at existing public clients:
`openreview/openreview-py` (the official Python client, still subject to the
challenge), `tamnd/openreview-cli` (a terminal client for public forums) and
`AutoTrustAI/autotrust-skills` (browser automation with temporary profiles).

## Collection procedure

1. **Establish the forum's identity.** Record venue, track, submission or
   forum id, the title as OpenReview shows it, and the collection date. If the
   title or id conflicts with `PAPER.md`, stop and ask.
2. **Capture raw material.** Keep review text, ratings, confidence, questions,
   official comments, meta-review, decision and author responses separate.
3. **Label roles.** Each item is one of `review`, `official_comment`,
   `author_response`, `meta_review`, `decision`, `ethics_review`,
   `area_chair_comment`, `public_comment` or `unknown`.
4. **Anonymise consistently.** Use stable labels such as `R1`, `R2`, `AC`,
   `SAC`, `Decision`. Never infer anyone's identity.
5. **Extract actionable content.** For each reviewer item separate the summary
   and perceived contribution, strengths, weaknesses, questions, requested
   experiments or analyses, requested citations or related-work changes,
   clarity and organisation requests, reproducibility or artifact concerns,
   and score, confidence and recommendation when present.
6. **Map to the manuscript.** Link each point to `abstract`, `introduction`,
   `preliminaries`, `method`, `experiments`, `related_work`, `limitations`,
   `appendix`, `figures`, `tables`, `references`, `code_or_artifacts` or
   `global`.
7. **Classify risk and authority.** Mark whether a point touches a locked or
   bounded claim, the interpretation of an experiment, a paper interface, the
   release state, or a decision `PAPER.md` reserves for the Human.
8. **Cluster.** Merge duplicate concerns across reviewers while recording who
   raised them; never drop a concern because only one reviewer raised it.
9. **Write the dossier** in the formats below.

## Storage

- Raw captures and exports: `.project/artifacts/openreview/<forum-id>/raw/`.
- The dossier: `.project/artifacts/openreview/<forum-id>/review-dossier.md`
  and `review-dossier.json`, plus an optional `revision-queue.md`.

Reviews are often confidential. Nothing from OpenReview goes into the tracked
tree, `paper/`, the Overleaf project or a release unless the Human decides so;
record that decision through `decision-packet`, and even then keep only the
structured dossier, never raw exports.

## Dossier outline

```markdown
# OpenReview Review Dossier: <venue-or-forum>

## Source and status
- OpenReview forum: <url-or-id>
- Venue / track: <venue>
- Paper title on OpenReview: <title>
- Collection source: <url | export | copied text | browser_cdp>
- Collected: <yyyy-mm-dd>, by an agent
- Confidentiality: <public | confidential | unknown>
- Included material: <reviews, comments, meta-review, decision, responses>

## Executive triage
- Overall review posture: <positive | mixed | negative | unclear>
- Highest-risk issues: 1. ...
- Fast rebuttal opportunities: 1. ...
- Revision themes: 1. ...

## Per-reviewer notes
### R1
- Recommendation / score: ...
- Confidence: ...
- Summary: ...
- Strengths: ...
- Weaknesses: ...
- Questions: ...
- Actionable requests: ...

## Cross-review clusters
### C1: <cluster title>
- Raised by: R1, R3
- Type: <experiment | claim | clarity | related_work | limitation | artifact>
- Manuscript area: ...
- Locked-claim impact: ...
- Suggested handling: ...

## Revision queue
| Priority | Cluster | Action | Owner skill | Needs Human? | Verification |
| --- | --- | --- | --- | --- | --- |
| P0 | ... | ... | ... | yes/no | ... |
```

## JSON schema

```json
{
  "source": {
    "forum_url": null,
    "forum_id": null,
    "venue": null,
    "track": null,
    "openreview_title": null,
    "collection_source": "url|export|copied_text|local_file|browser_cdp",
    "confidentiality": "public|confidential|unknown",
    "collected_at": null
  },
  "items": [
    {
      "item_id": "R1-review",
      "role": "review|official_comment|author_response|meta_review|decision|ethics_review|area_chair_comment|public_comment|unknown",
      "author_label": "R1",
      "date": null,
      "score": null,
      "confidence": null,
      "recommendation": null,
      "summary": [],
      "strengths": [],
      "weaknesses": [],
      "questions": [],
      "requested_experiments": [],
      "requested_citations": [],
      "clarity_requests": [],
      "artifact_or_reproducibility": [],
      "raw_pointer": null
    }
  ],
  "clusters": [
    {
      "cluster_id": "C1",
      "title": null,
      "raised_by": ["R1"],
      "type": "experiment|claim|clarity|related_work|limitation|artifact|ethics|other",
      "manuscript_areas": ["experiments"],
      "reviewer_points": [],
      "locked_boundary_impact": "none|possible|direct",
      "human_decision_needed": false,
      "priority": "P0|P1|P2|P3",
      "suggested_handling": null,
      "verification_needed": null
    }
  ],
  "revision_queue": [
    {
      "priority": "P0|P1|P2|P3",
      "cluster_id": "C1",
      "action": null,
      "owner_skill": null,
      "needs_human": false,
      "verification": null,
      "status": "open|in_progress|blocked|done|wont_do"
    }
  ]
}
```

## Triage

- `P0`: likely affects acceptance or the decision response, a locked claim,
  central validity, missing critical evidence, or a high-risk
  misunderstanding.
- `P1`: an important rebuttal or revision point that materially raises
  reviewer confidence.
- `P2`: local clarity, citation, appendix or formatting.
- `P3`: polish or information only.

Set `human_decision_needed: true` when a response would strengthen, weaken,
remove or reframe a central claim, add experiments, change a paper interface,
accept a limitation, or choose a rebuttal or revision strategy.

## Handing the queue on

The dossier feeds the paper's revision work; it does not change the paper.

- decisions the queue raises: `decision-packet`;
- locked or bounded claims: `control-review`;
- prose revisions: `writing-router`, which routes to `section-writing`;
- names, notation and result macros: `paper-interface-maintenance`;
- requested citations: `citation-support-review`;
- new experiments: recorded in `.agents/memory/project/experiments.md` and
  run in the code repository; the paper only reports their results;
- a camera-ready or revision build: `publication-planning` and
  `release-review`.

## Boundaries

- Do not invent reviewer intent beyond the text.
- Do not change the manuscript while collecting; revision is a separate task
  after the dossier exists.
- Reviewer requests are not automatically correct; keep conflicts and
  uncertainty visible for a decision or a check.
- Never expose confidential reviews in the tracked tree, `paper/`, releases,
  the Overleaf project or any public artifact.
- Never infer the identity of reviewers or deanonymise anyone.
