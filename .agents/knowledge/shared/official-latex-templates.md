---
name: official-latex-templates
date: 2026-08-27
source: this template's official-template smoke tests up to v0.3.1 (LATEX_TEMPLATES.md and its download catalog, last changed 2026-08-27), moved into a record by Issue #156
scope: shared
applies_to: papers that move onto a publisher's or venue's official LaTeX kit
status: active
refresh_after: before a paper adopts one of these kits; the smoke tests that kept this list current were retired in v0.4.0
supersedes: null
superseded_by: null
---

# Official LaTeX kits and where they come from

## Fact

Up to v0.3.1 this template downloaded the following official kits from the
listed authorities and compiled each one's own sample; the matrix last changed
on 2026-08-27. The URLs are where the official kit was published then;
versioned URLs move when a new year or version is published.

| Family | Kit identity | Authority | Status at 2026-08-27 |
| --- | --- | --- | --- |
| Elsevier | `elsarticle.cls` | [Elsevier LaTeX instructions](https://www.elsevier.com/authors/policies-and-guidelines/latex-instructions), [CTAN](https://ctan.org/pkg/elsarticle) | compiled |
| IEEE journals | `IEEEtran.cls` with `journal` | [IEEE Author Center](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/use-authoring-tools-and-ieee-article-templates/ieee-article-templates/), [CTAN](https://ctan.org/pkg/ieeetran) | compiled |
| APS/AIP | `revtex4-2.cls` | [APS REVTeX](https://journals.aps.org/revtex/), [CTAN](https://ctan.org/pkg/revtex) | compiled |
| ACM | `acmart.cls` with `manuscript` | [ACM authoring documentation](https://authors.acm.org/proceedings/production-information/preparing-your-article-with-latex), [CTAN](https://ctan.org/pkg/acmart) | compiled |
| KDD | `acmart.cls` with `sigconf,anonymous,review` | [KDD 2026 research track](https://kdd2026.kdd.org/research-track-call-for-papers/), [ACM proceedings template](https://www.acm.org/publications/proceedings-template) | compiled against the installed class |
| Springer Nature | `sn-jnl.cls`, December 2024 package | [official package](https://cms-resources.apps.public.k8s.springernature.io/springer-cms/rest/v1/content/18782940/data/v12), [author support](https://www.springernature.com/gp/authors/campaigns/latex-author-support) | compiled from the official package |
| AAS | `aastex702.cls` | [AASTeX 7.0.2](https://journals.aas.org/wp-content/uploads/2026/06/aastex702.zip), [package page](https://journals.aas.org/aastex-package-for-manuscript-preparation/) | compiled from the official package |
| IOP | `iopjournal.cls` | [IOP package](https://publishingsupport.iopscience.iop.org/wp-content/uploads/2025/07/ioplatextemplate.zip), [template page](https://publishingsupport.iopscience.iop.org/questions/latex-template/) | compiled from the official package |
| JMLR | `article` plus `jmlr2e.sty` | [style repository](https://github.com/JmlrOrg/jmlr-style-file), [format instructions](https://www.jmlr.org/format/format.html) | compiled from the current branch |
| PLOS ONE | `article` with `plos2025.bst` | [PLOS package](https://journals.plos.org/plosone/s/file?id=1457/PLOS_latex_template.zip), [PLOS LaTeX page](https://journals.plos.org/plosone/s/latex) | compiled from the official package |
| ICML | `icml2026.sty` | [author instructions](https://icml.cc/Conferences/2026/AuthorInstructions), [`icml2026.zip`](https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip) | compiled from the official package |
| ICLR | `iclr2026_conference.sty` | [official repository](https://github.com/ICLR/Master-Template) | compiled from the official package |
| NeurIPS | `neurips_2026.sty` | [call for papers](https://neurips.cc/Conferences/2026/CallForPapers), [formatting package](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip) | compiled from the official package |
| ACL | `acl.sty`, rolling repository | [ACL main conference](https://2026.aclweb.org/calls/main_conference_papers/), [ARR templates](https://aclrollingreview.org/cfp#paper-submission-and-templates), [style repository](https://github.com/acl-org/acl-style-files) | compiled from the current repository archive |
| AAAI | Author Kit 2026.1, anonymous sample | [AAAI submission instructions](https://aaai.org/conference/aaai/aaai-26/submission-instructions/), [Author Kit](https://aaai.org/authorkit26-1/) | compiled from the official package |

- The CTAN `jmlr.cls` is not JMLR's current author template, whose documented
  interface is `article` plus `jmlr2e.sty`.
- ICLR 2027 and ICML 2026 kits with their hashes are in
  [`venue-iclr-2027.md`](venue-iclr-2027.md) and
  [`venue-icml-2026.md`](venue-icml-2026.md).

## Evidence

- `LATEX_TEMPLATES.md` and `.agents/tools/_official_templates.py` of this
  template at v0.3.1 (the catalog downloaded the current bytes at each URL and
  printed their SHA-256; the CI job compiled the samples with shell escape off).
- A compiled sample proves only that those downloaded bytes built in that
  environment; it does not prove acceptance by a publisher's upload processor,
  current venue rules or anonymity requirements.

## Refresh

Before a paper adopts a kit, download it from the authority, record its URL
and SHA-256 in the paper's publication record, build both the named and the
anonymous forms, and check the venue's current instructions; a newer year's
kit replaces the row's URL.
