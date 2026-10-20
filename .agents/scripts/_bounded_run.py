#!/usr/bin/env python3
"""Run a locked reference tool under a deadline that covers its whole process
tree, keep its caches free of credentials, and spare it a keyless OpenAlex."""
from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import time
from pathlib import Path

CREDENTIAL_VARIABLES = ("OPENALEX_API_KEY", "S2_API_KEY")
CIRCUIT_KEY = "__bibtex_updater_circuit_open_until__"
GRACE_SECONDS = 3.0


class BoundedResult:
    def __init__(self, returncode: int | None, stdout: str, stderr: str) -> None:
        self.returncode = returncode  # None when the deadline ended the run
        self.stdout = stdout
        self.stderr = stderr

    @property
    def timed_out(self) -> bool:
        return self.returncode is None


def _signal_group(group: int, sig: int) -> None:
    try:
        os.killpg(group, sig)
    except (ProcessLookupError, PermissionError):
        pass


def run_bounded(command: list[str], *, cwd: Path, env: dict[str, str], timeout: float) -> BoundedResult:
    """Run command in a new process group. At the deadline the whole group is
    stopped: `uv run` leaves its child in that group, and killing uv alone
    leaves the checker running and writing its report and cache."""
    process = subprocess.Popen(
        command, cwd=cwd, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=max(1.0, timeout))
        return BoundedResult(process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        _signal_group(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            pass
        _signal_group(process.pid, signal.SIGKILL)
        try:
            stdout, stderr = process.communicate(timeout=GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            # A descendant that left the group still holds the pipes.
            process.kill()
            stdout = stderr = ""
        return BoundedResult(None, stdout or "", stderr or "")
    finally:
        if process.poll() is None:
            _signal_group(process.pid, signal.SIGKILL)
            process.wait()


def skip_keyless_openalex(cache_file: Path, env: dict[str, str], seconds: float) -> bool:
    """Open the locked tool's own OpenAlex circuit for a run without a key, and
    close it for a run with one. Keyless OpenAlex allows about 100 searches a
    day per address; once they are spent it answers 429 with a Retry-After of
    hours, which bibtex-updater 1.6.1 waits out (bibtex-check) or retries for
    minutes per request (bibtex-update). Returns True when OpenAlex is skipped."""
    keyless = not env.get("OPENALEX_API_KEY", "").strip()
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(cache_file)
    try:
        # The table and key of bibtex-updater's SqliteCache and HttpClient circuit state.
        connection.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT NOT NULL, timestamp REAL NOT NULL)")
        row = connection.execute("SELECT value FROM cache WHERE key = ?", (CIRCUIT_KEY,)).fetchone()
        try:
            state = json.loads(row[0]) if row else {}
        except json.JSONDecodeError:
            state = {}
        state = state if isinstance(state, dict) else {}
        if keyless:
            state["openalex"] = time.time() + seconds
        else:
            state.pop("openalex", None)
        connection.execute("INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
                           (CIRCUIT_KEY, json.dumps(state), time.time()))
        connection.commit()
    finally:
        connection.close()
    return keyless


def credential_values(env: dict[str, str]) -> list[str]:
    return [value for name in CREDENTIAL_VARIABLES if (value := env.get(name, "").strip())]


def scrub_cache(directory: Path, secrets: list[str]) -> list[str]:
    """Remove every cached row whose request or response holds a credential, so
    the cache can be kept between CI runs. A request URL can carry an API key
    (OpenAlex takes it as a query parameter). Returns the files changed."""
    changed: list[str] = []
    if not secrets or not directory.is_dir():
        return changed
    for path in sorted(directory.glob("*.db")):
        connection = sqlite3.connect(path)
        try:
            tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
            removed = 0
            for table in tables:
                columns = [row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')]
                condition = " OR ".join(f'instr(CAST("{column}" AS TEXT), ?) > 0' for column in columns)
                for secret in secrets:
                    removed += connection.execute(
                        f'DELETE FROM "{table}" WHERE {condition}', [secret] * len(columns)
                    ).rowcount
            connection.commit()
            if removed:
                connection.execute("VACUUM")  # deleted rows must not survive in free pages
                changed.append(path.name)
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        finally:
            connection.close()
    # Whatever still holds a credential (another file, a write-ahead log) goes.
    for path in sorted(directory.iterdir()):
        if path.is_file() and any(secret.encode() in path.read_bytes() for secret in secrets):
            path.unlink()
            changed.append(path.name)
    return changed
