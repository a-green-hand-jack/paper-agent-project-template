# Writing Reference Search Playbook

Use this playbook to find auxiliary writing exemplars for a paper. The
question it answers is "Which successful papers should we study for how they
are written and organised?", not "Which papers must the manuscript cite?".

## 1. Define the exemplar need

Record these before searching:

- the paper's topic in one sentence, taken from `PAPER.md`;
- the target section or writing problem;
- the venue family and the recency window;
- whether only award papers count, or strong non-award papers too;
- whether LaTeX source is needed or reading the PDF is enough.

Derive topic keywords from the paper's identity and contribution in
`PAPER.md`: the research object, the method family, the evaluation setting
and the closest neighbouring areas. Use two to five keywords per query.

## 2. Source hierarchy

Search in this order:

1. **Official venue award pages**: the strongest evidence of an award label.
2. **Official paper pages**: OpenReview, ACL Anthology, the conference's
   virtual site, proceedings pages.
3. **Author arXiv pages and source bundles**: useful for LaTeX structure.
4. **Publisher or proceedings records**: ACM, PMLR, IEEE, USENIX, AAAI, IJCAI.
5. **Secondary lists**: leads only; verify each against a primary source.

## 3. Query patterns

Use a browser, a search engine or another approved discovery tool with quoted
queries such as:

```text
"<VENUE> <YEAR>" "best paper" "<topic keyword>"
"<VENUE> <YEAR>" "outstanding paper" OpenReview
site:<venue-domain> "Best Paper" "<YEAR>"
site:openreview.net "<VENUE> <YEAR>" "Best Paper Award"
"<VENUE> <YEAR>" "outstanding paper award" "<topic keyword>"
```

When topic queries return little, retrieve the venue's full award list for
each year first, then screen titles and abstracts by hand for writing fit.

## 4. Venue defaults

For a machine-learning paper, start with:

- ICLR: best and outstanding papers; orals and spotlights only as a second
  tier;
- ICML: best and outstanding papers; test-of-time awards only as style leads;
- NeurIPS: outstanding and best papers; orals and spotlights as a second tier;
- ACL, EMNLP, NAACL: best long papers, outstanding papers, theme and area
  awards;
- AAAI, IJCAI: best or distinguished papers when the topic is broader AI;
- domain venues only when the paper's evidence or audience calls for them.

For a writing cohort, three to seven papers are usually enough: one primary
architecture exemplar, two section-specific exemplars, and a few optional
contrast examples.

## 5. Screening criteria

Judge each candidate on:

- **Award credibility**: an official award page or proceedings record exists.
- **Topic proximity**: direct conceptual overlap, the same audience, or an
  analogous framing of the research problem.
- **Writing utility**: a clear abstract and introduction, explicit
  contributions, a good formal setup, careful limitations, or a strong
  experiment narrative.
- **Evidence compatibility**: useful despite differences in empirical
  maturity; avoid exemplars that would tempt the manuscript to overclaim.
- **Source availability**: arXiv source or clean TeX when structure extraction
  matters.
- **Diversity**: avoid a cohort in which every paper teaches the same move.

Reject or downgrade a candidate when:

- its award label is unverified;
- it is scientifically relevant but a poor writing model;
- it relies on a claim or evidence style the current paper cannot honestly
  mirror;
- only a copyrighted PDF is available and the task does not need to keep it.

## 6. Retrieval and storage

Stage downloads in the worktree's ignored state:

```bash
mkdir -p .project/artifacts/writing-exemplars/<cohort>
# arXiv source, after verifying the arXiv id:
curl -L "https://arxiv.org/e-print/<arxiv-id>" \
  -o ".project/artifacts/writing-exemplars/<cohort>/<arxiv-id>.tar"
```

Write working cards next to the downloads, one Markdown file per paper. When
the Human wants a card kept with the repository, turn it into a knowledge
record under `.agents/knowledge/project/` (front matter from
`.agents/knowledge/ENTRY_TEMPLATE.md`; the award page is the source and the
check date is the date). PDFs and source bundles are never committed. Do not
change `.agents/references/ledger.json` unless `citation-support-review`
makes the paper a manuscript citation.

## 7. Candidate card

Use these fields in reports and cards:

```markdown
## <short title>

- Role: primary architecture exemplar | introduction exemplar |
  formalism exemplar | experiment exemplar | limitation exemplar |
  contrast exemplar
- Venue / year / award: <venue>, <year>, <official award label>
- Award provenance: <official URL>, checked <yyyy-mm-dd>
- Paper page: <OpenReview / ACL Anthology / PMLR / arXiv / proceedings URL>
- Source availability: arXiv source | publisher PDF only | unknown
- Topic relation: <why this helps the current paper>
- Writing moves to study: <three to five concrete moves>
- Moves not to imitate: <overclaiming, evidence-style mismatch, layout tricks>
- Citation status: writing reference only | possible manuscript citation,
  pending citation-support-review
- Local material: <path under .project/artifacts/writing-exemplars/, if any>
```

## 8. Output contract

When asked for writing references, return:

1. a short search log naming the official sources checked;
2. a ranked or grouped candidate list, unless no ranking was requested;
3. why each candidate is useful for writing;
4. what not to imitate;
5. which files were stored, and where;
6. searches that found nothing and award labels that stay unverified.

Never present an auxiliary writing reference as a citation the manuscript
needs.
