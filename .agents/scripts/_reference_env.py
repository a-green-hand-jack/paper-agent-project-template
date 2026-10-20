#!/usr/bin/env python3
"""Load the allowlisted local reference-service configuration without shell evaluation."""
from __future__ import annotations

import os
from pathlib import Path

ALLOWED_KEYS = {"BIBTEX_CHECK_MAILTO", "OPENALEX_API_KEY", "S2_API_KEY"}
# The device's shared credential file, reached through the canonical checkout's link
# and, in a worktree, through the .project/credentials link (llm-credentials).
SHARED_FILE = ".project/credentials/.env"


def load_reference_env(root: Path) -> list[str]:
    """Export the allowlisted keys; the process environment wins, then .env, then the shared file."""
    return _load(root / ".env", ".env", strict=True) + _load(root / SHARED_FILE, SHARED_FILE, strict=False)


def _load(path: Path, label: str, strict: bool) -> list[str]:
    # The root .env belongs to this project and rejects every other line. The shared file
    # holds other consumers' keys: those lines are skipped unparsed and never exported.
    if not path.is_file():
        return []
    loaded: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not strict and line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            if strict:
                raise ValueError(f"{label}:{number} must be KEY=VALUE")
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key not in ALLOWED_KEYS:
            if strict:
                raise ValueError(f"{label}:{number} unsupported key: {key}")
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif value.startswith(("\"", "'")) or value.endswith(("\"", "'")):
            raise ValueError(f"{label}:{number} has unmatched quotes")
        if value and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)
    return loaded
