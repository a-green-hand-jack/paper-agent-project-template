# Development plane rules

This directory belongs to agent development of the paper. It never reaches
`paper/`, the Overleaf project or a release: `paper/` builds without anything
here.

Read `.agents/content-registry.yaml` before adding or reusing a memory,
knowledge entry, skill or script. Keep the registry and its index files updated
in the same change as the content decision.

## Directory guidance convention

Every managed subdirectory directly under `.agents/` has an `AGENTS.md` with
its local rules. Grouping directories such as `skills/shared/` also have one.
Individual skill packages use `SKILL.md` as their entry point and do not add a
duplicate `AGENTS.md`. Keep this convention uniform when adding directories.

The `AGENTS.md` files are the indexes for this development plane. Do not add
README files under `.agents/`; update the relevant `AGENTS.md` when registering
memory, knowledge or skills.

- [`skills/`](skills/AGENTS.md) — repeatable procedures, one package per skill.
- [`memory/`](memory/AGENTS.md) — durable decisions and lessons, including the
  paper's own records (brief, experiments, interfaces, publication).
- [`knowledge/`](knowledge/AGENTS.md) — dated, sourced facts such as venue
  rules.
- [`references/`](references/AGENTS.md) — the reference ledger and its policy.
- [`scripts/`](scripts/AGENTS.md) — setup, checks, Overleaf sync and reference
  tools.
- [`tests/`](tests/AGENTS.md) — unit tests of the scripts.

## Where information goes

- A durable decision, correction or project lesson goes in `memory/` and its
  index before it counts as recorded.
- A changing environment or external fact goes in `knowledge/`, with date and
  source.
- A repeatable operation goes in `skills/`.
- Paper content belongs in `paper/`, and the Human contract in `PAPER.md`; not
  here.
- Session progress may remain private; project knowledge may not.

Never store credentials, raw authentication files, private sessions or personal
data here.
