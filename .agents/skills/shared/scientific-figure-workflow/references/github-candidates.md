# GitHub Candidates For Scientific Figure Workflows

Snapshot from GitHub search performed 2026-09-11. Recheck repository status,
licenses, install behavior, and maintenance before adopting any dependency.

## Python / Reproducible Quantitative Figures

| Repository | Use | Notes |
|---|---|---|
| `garrettj403/SciencePlots` | Matplotlib styles for scientific papers | Mature, lightweight style layer; good first choice for improving Matplotlib defaults. |
| `Galaxy-Dawn/pubfig` | Publication-style Matplotlib plotting and export workflow | Common plot families, paper-ready defaults, export discipline, panel/Figma workflow, agent JSON CLI. Useful if local scripts become repetitive. |
| `mwaskom/seaborn` | Statistical visualization | General-purpose statistical plotting; useful base layer but not a full paper-figure workflow. |
| `nschloe/tikzplotlib` | Matplotlib to TikZ/PGFPlots | Useful when LaTeX-native editable plots are required; verify compatibility for current Matplotlib versions. |
| `bendichter/brokenaxes` | Broken-axis Matplotlib plots | Use only for specific scale-break cases; broken axes need careful captioning. |
| `jaychouchannel/PlotCraft` | Natural language -> Matplotlib code -> sandboxed SVG | Candidate for LLM-assisted editable Python plotting; generated code must be reviewed. |

## Agent Reference And Gallery Workflows

| Repository | Use | Notes |
|---|---|---|
| `Dsadd4/AgentFigureGallery` | Reference-gallery workflow for coding agents | Lets an agent query figure references, Human selects preferred examples, then exports a reference bundle for plotting. Strong fit for deciding visual style before code generation. |

## Text-To-Image / Generative Schematic Exploration

| Repository | Use | Notes |
|---|---|---|
| `hengzzzhou/FigForge` | AI-powered scientific figure generator | Candidate for concept drafting; validate factual correctness and editability. |
| `JackaZhai/SCIdrawer` | AI-powered SCI figure generation/editing toolkit | Potential schematic/illustration tool; assess maturity before relying on it. |
| `jiangnan030-del/paperfigure-agent` | Automated scientific figure generation | Very early-looking candidate; treat as exploratory. |
| `peizhou/ScholarPlot` | AI scientific figure generator / Nano Banana style claims | Low-star candidate; use only after verification. |
| `literaf/ai4scholar-plugin-codex` | Codex plugin with paper search/citation/figure generation | Broad academic plugin, not solely figure workflow; inspect privacy and scope before use. |

## Adoption Rule

- Quantitative results: final figure must be code-generated and reproducible.
- Schematics: generative image tools may create drafts, but final paper figures
  should be editable and manually checked.
- Every final figure must pass visual inspection after PDF compilation.
