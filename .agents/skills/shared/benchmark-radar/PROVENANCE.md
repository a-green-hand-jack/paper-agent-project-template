# Provenance

- Upstream: https://github.com/ktwu01/benchmark-radar, path `skills/benchmark-radar/`
  and the repository-root `LICENSE`
- Commit: 21f3018c460cda0eec74f303569524288dd22bbc (2026-11-10)
- Licence: MIT; `LICENSE` is the upstream file, unchanged. Holder: ktwu01.
- Vendored: 2026-11-11 for paper-agent-project-template (#199)

## Files

| File | Upstream path | SHA-256 of the upstream bytes | Status |
| --- | --- | --- | --- |
| `SKILL.md` | `skills/benchmark-radar/SKILL.md` | 71e3311f0e415652b096cbf704500f1fa22ce8c7718f9d4102d855fe27265184 | unchanged |
| `agents/openai.yaml` | `skills/benchmark-radar/agents/openai.yaml` | 8718b9fb489c0fb47bea0e8ae0fc13fe93fe0bb587d63448214d2e05ad3b9ec5 | unchanged |
| `LICENSE` | `LICENSE` | 764cee39e340ab4813a8dd9881642bfffbd2f01bedeacfbba5746bb3fec5bf7a | unchanged |

## Excluded

- `skills/benchmark-radar-reply/`, `skills/maintainer-local-clean/` and
  `skills/say-it-once/` — the other upstream skills, outside this package.
- `README.md` and `README.zh-CN.md` — installation and service overview; this
  package keeps only the skill's own CLI steps.
- `CITATION.md`, `CITATION.cff` and `LICENSE-CONTENT.md` — citation and
  content-licence notices for the upstream service and its data, which this
  package does not vendor.
- `src/`, `scripts/`, `tests/`, `data/`, `config/`, `config.yml`, `docs/`,
  `site/`, `assets/`, `evaluation/`, `traction/`, `pyproject.toml`, `uv.lock`,
  `.github/`, `.gitmodules`, `.gitignore`, `.env.example`, `AGENTS.md`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `design.md`,
  `principle.md` and `maintainer-review.md` — the upstream service
  implementation, data, CI and repository housekeeping; the CLI installs from
  upstream on demand.

## Local changes

None.
