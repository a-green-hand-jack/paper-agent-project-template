# Provenance

- Upstream: https://github.com/TAO-QKV/Icarus-Figures, paths `.claude/skills/icarus-figures/` (`SKILL.md`, `references/`) and the repository root (`paperfig/`, `scripts/`, `examples/hero_tikz/`, `pyproject.toml`, `requirements.txt`, `LICENSE`), flattened into this directory
- Commit: 0bcaa40c07ef0dc6ea1506ab147ce0a4f5a542fd (2026-06-30)
- Licence: MIT; `LICENSE` is the upstream file, unchanged. Holder: TAO-QKV.
- Vendored: 2026-10-20 for paper-agent-project-template (#156)

## Files

| File | Upstream path | SHA-256 of the upstream bytes | Status |
| --- | --- | --- | --- |
| `SKILL.md` | `.claude/skills/icarus-figures/SKILL.md` | 7c4f04d9ab9c504d4ccf5bcb7315e9b292d9ec8c5b6a510dc664a27d5d91c143 | patched |
| `examples/hero_tikz/framework_hero.png` | `examples/hero_tikz/framework_hero.png` | e239657e49bf9f0591c65848b7b25467832de712039dc7027702ca3ed65dd2f1 | unchanged |
| `examples/hero_tikz/framework_hero.tex` | `examples/hero_tikz/framework_hero.tex` | 019176a549306b2c2bad194134f92745b464c64c5f4cd7a42b0665bea5917231 | unchanged |
| `examples/hero_tikz/graphical_model_hero.png` | `examples/hero_tikz/graphical_model_hero.png` | c680b700da08e5e2cfe3161457736178aa3ddccab93344e9aaef3d0e44fb259d | unchanged |
| `examples/hero_tikz/graphical_model_hero.tex` | `examples/hero_tikz/graphical_model_hero.tex` | e3ee2d10a7df32359bc8e2025d1249c7cbff50f748fd1249003b8d18b2d68e87 | unchanged |
| `examples/hero_tikz/matrix_layout_hero.png` | `examples/hero_tikz/matrix_layout_hero.png` | 11eadf7a9ed53f5b92fd19b6a706157f307d9907ebda28eb9ab99cb72fb41419 | unchanged |
| `examples/hero_tikz/matrix_layout_hero.tex` | `examples/hero_tikz/matrix_layout_hero.tex` | 64bac7e6c0e4914d7cba6ded5f9f0e4c4136e379dd4886b620fcacc7612f0dcf | unchanged |
| `examples/hero_tikz/pipeline_hero.tex` | `examples/hero_tikz/pipeline_hero.tex` | ef210017ebbda7a56c898fcc6ad578e8eacaa7f240c51279b3ece5c511f75242 | unchanged |
| `examples/hero_tikz/tensor_framework_hero.png` | `examples/hero_tikz/tensor_framework_hero.png` | 201488a46647ad54bca9fec56291fa7c490baa022966d38a63c9a9dc09788262 | unchanged |
| `examples/hero_tikz/tensor_framework_hero.tex` | `examples/hero_tikz/tensor_framework_hero.tex` | 91b8013f3f45e47684997eed209386f298b571d0ae523e4225f9b10df83e4f50 | unchanged |
| `paperfig/__init__.py` | `paperfig/__init__.py` | 89ff4b2d2914a8e6907d74fdb5e890fb91ec480011162b50e4a0875b4772ded7 | unchanged |
| `paperfig/archetypes.py` | `paperfig/archetypes.py` | 9d5272094b7df5f8999a09cbe67f6c431f847b801e28909eb05292e8d9b9c958 | unchanged |
| `paperfig/paperfig.mplstyle` | `paperfig/paperfig.mplstyle` | 5a58f106d56bbd5b948ad4fa83ffd34c4cc5f9cd0d87fe2af5897b2f8a629402 | unchanged |
| `paperfig/scientific.py` | `paperfig/scientific.py` | 04509ff65d35e9d6e813fd40aca81db39ecc3ea45bf998043ba7ebb47be62dc6 | unchanged |
| `paperfig/style.py` | `paperfig/style.py` | 638cb15cef61a012d4d372d718815b62b4dda9d9f83f51f10404066a394c937a | unchanged |
| `pyproject.toml` | `pyproject.toml` | 3342c656798181660ecc4a84c68bbf77acd7856dc26194aff13e933d37b97c1a | unchanged |
| `references/caption-and-quality.md` | `.claude/skills/icarus-figures/references/caption-and-quality.md` | d1f184f264ba53b834d115b76a78419a99706ee264f7edbed9955c75af2557ef | unchanged |
| `references/figure-cookbook.md` | `.claude/skills/icarus-figures/references/figure-cookbook.md` | b4a15b5fbe3d59a5345f39c5778b76ba7d90e97546e4711b2a0885c95a34156d | unchanged |
| `references/figure-critique.md` | `.claude/skills/icarus-figures/references/figure-critique.md` | 447db77c5a16ec381b097c095117181ee7307ef7450993fe85b5fb1a8d00e692 | unchanged |
| `references/framework-figures.md` | `.claude/skills/icarus-figures/references/framework-figures.md` | 575972cccf58c228a8dd72b8ee64c68e9068315baed23dd24e692290cd3dc171 | unchanged |
| `requirements.txt` | `requirements.txt` | d3820e46038bc3670becfb91280dd14ccbf30be2c507c6381d7194f45e3adb13 | unchanged |
| `scripts/_smoke_test.py` | `scripts/_smoke_test.py` | 6bbb4e5add4f4d8bbc3a57d18a909321120c8d0df62b358f36988706fc0979fb | unchanged |
| `scripts/_style.py` | `scripts/_style.py` | 10e7de3d49a8544039649efeca22a782e02b1b0e22d3c2c5040a1cb2a0324683 | unchanged |
| `scripts/critique.py` | `scripts/critique.py` | b6e95be4371e908cd0b8b2e874866ed859321da827a60fe9bf129d351e017af6 | unchanged |
| `LICENSE` | `LICENSE` | 3862df88e809bc59fab222a5688f44fedbe8fca9a718c3727097bfdd59a5f958 | unchanged |

## Excluded

- `.claude/skills/icarus-figures/evals/` (`README.md`, `trigger-eval.json`) — trigger evaluations for the upstream skill; not needed to use it.
- `examples/` except `examples/hero_tikz/` — 12 demonstration scripts that render the `paperfig` archetypes, and their 17 PNGs (about 13 MB); nothing in `SKILL.md` or `references/` points to them.
- `tests/`, `.github/` — upstream unit tests and CI.
- `README.md`, `CITATION.cff`, `CLAUDE.md` — repository overview, citation metadata and the auto-loaded agent role for the upstream repository; `SKILL.md` carries the skill itself.
- `.gitattributes`, `.gitignore`, `data/processed/.gitkeep`, `outputs/figures/.gitkeep`, `outputs/figures/figure_manifest.csv` (a header line only) — housekeeping and empty placeholders for the upstream output layout, which the trailing section of `SKILL.md` maps to this repository.

## Local changes

- `SKILL.md` front matter: the upstream `description:` is a plain scalar that contains `: `, so YAML parsers reject it ("mapping values are not allowed here"). It is folded with `>-`; the description text is unchanged.

````diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -1,6 +1,7 @@
 ---
 name: icarus-figures
-description: Icarus Figures produces publication-grade figures for scientific papers — reproducible matplotlib/seaborn data figures and original TikZ method/framework/architecture figures, held to a four-axis quality bar (depth · elegance · unimpeachable · visible-gap) and exported as editable PDF+PNG+SVG with a runnable critique gate. Use this whenever a figure is destined for a paper, journal, conference submission, thesis, or report — making a plot/chart publication- or journal-ready, building a method/architecture/framework diagram or 技术路线图 (the hero figure a paper opens with), a schematic or workflow figure, or cleaning up a matplotlib/seaborn/TikZ figure that currently looks like a homework plot. Trigger even when the user never says "publication": if the figure goes into a written scientific document, this skill applies.
+description: >-
+  Icarus Figures produces publication-grade figures for scientific papers — reproducible matplotlib/seaborn data figures and original TikZ method/framework/architecture figures, held to a four-axis quality bar (depth · elegance · unimpeachable · visible-gap) and exported as editable PDF+PNG+SVG with a runnable critique gate. Use this whenever a figure is destined for a paper, journal, conference submission, thesis, or report — making a plot/chart publication- or journal-ready, building a method/architecture/framework diagram or 技术路线图 (the hero figure a paper opens with), a schematic or workflow figure, or cleaning up a matplotlib/seaborn/TikZ figure that currently looks like a homework plot. Trigger even when the user never says "publication": if the figure goes into a written scientific document, this skill applies.
 ---

 # Icarus Figures
````
