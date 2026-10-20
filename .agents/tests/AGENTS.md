# Development checks rules

Tests here are diagnostic and seam-focused. Do not increase coverage merely to
mirror implementation, and do not treat these checks as product acceptance when
the real public entrypoint or long-running runtime has not been exercised.

For this paper the public entry points are the builds: a passing unit test does
not replace `make check` or `make release-check`, and neither replaces looking
at the rendered pages. `make check` runs every test here with
`python3 -m unittest discover -s .agents/tests -p 'test_*.py'`; run one file
with `-p test_<name>.py`. Tests write only to temporary directories. The two
BibTeX helper tests run only inside the locked reference environment
(`uv run --project .agents/scripts/reference-integrity ...`, as CI does) and
are skipped elsewhere.
