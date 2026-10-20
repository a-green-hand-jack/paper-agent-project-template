#!/usr/bin/env python3
"""Run the locked open-source bibliography metadata audit without approving claims."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any

SUMMARY_SCHEMA = "paper-reference-metadata-run-v1"
RATE_LIMIT_TOKENS = (
    "rate-limited/unavailable",
    "rate_limit",
    "http 429",
    "status 429",
    "response 429",
    "429 too many requests",
    "circuit open for service",
)
THROTTLED_SERVICE_PATTERNS = (
    re.compile(r"service ['\"]([^'\"]+)['\"] is rate-limited/unavailable", re.IGNORECASE),
    re.compile(r"circuit open for service\s+([^\s,;]+)", re.IGNORECASE),
)
# --verbose log lines: the level prefix, and an HTTP response line. The checker
# reads DBLP's 202 bot-challenge page as "no hits"; only this line shows it.
LOG_LEVEL_RE = re.compile(r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL): ")
HTTP_RESPONSE_PREFIX = "INFO: HTTP Request: "
BOT_CHALLENGE_PATTERNS = {
    "dblp": re.compile(r'^INFO: HTTP Request: [A-Z]+ https://(?:[\w-]+\.)*dblp\.org/\S* "HTTP/[\d.]+ 202\b'),
}
# A reviewed OpenReview identity may differ from the checker only in what the
# locked checker cannot read from OpenReview: a year missing from the record,
# or a venue abbreviation such as COLM.
OPENREVIEW_RESIDUAL_STATUSES = {"venue_mismatch", "unconfirmed", "strict_warn_cnv"}
OPENREVIEW_RESIDUAL_FIELDS = {"year", "venue"}


def load_integrity_module(root: Path) -> ModuleType:
    path = root / ".agents/scripts/check-reference-integrity.py"
    spec = importlib.util.spec_from_file_location("paper_reference_integrity", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load structural checker: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_script(root: Path, filename: str, name: str) -> ModuleType:
    path = root / ".agents/scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_summary(path: Path, **values: Any) -> None:
    payload = {
        "schema_version": SUMMARY_SCHEMA,
        "approves_claim_support": False,
        **values,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]] | None:
    if not path.is_file():
        return None
    records: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    return None
                records.append(value)
    except (OSError, json.JSONDecodeError):
        return None
    return records or None


def validate_records(records: list[dict[str, Any]], bibliography_keys: set[str]) -> str | None:
    keys: list[str] = []
    for record in records:
        key = record.get("key")
        status = record.get("status")
        if not isinstance(key, str) or not key.strip():
            return "metadata report record has no non-empty key"
        if not isinstance(status, str) or not status.strip():
            return f"metadata report record {key} has no non-empty status"
        if not isinstance(record.get("abstained"), bool):
            return f"metadata report record {key} has invalid abstained flag"
        if not isinstance(record.get("coverage_incomplete"), bool):
            return f"metadata report record {key} has invalid coverage_incomplete flag"
        if not isinstance(record.get("errors"), list):
            return f"metadata report record {key} has invalid errors list"
        keys.append(key)
    if len(keys) != len(set(keys)):
        return "metadata report contains duplicate citation keys"
    if set(keys) != bibliography_keys:
        missing = sorted(bibliography_keys - set(keys))
        extra = sorted(set(keys) - bibliography_keys)
        return f"metadata report key coverage mismatch; missing={missing}, extra={extra}"
    return None


def classify_records(records: list[dict[str, Any]]) -> str:
    infrastructure_error = False
    unverified = False
    problematic = False
    for record in records:
        status = str(record.get("status", "")).strip().lower()
        if record["coverage_incomplete"] is True or any(
            token in status for token in ("api_error", "timeout", "rate_limit", "infrastructure")
        ):
            infrastructure_error = True
        elif status == "verified" and record["abstained"] is False and not record["errors"]:
            continue
        elif record["abstained"] is True or any(
            token in status for token in ("not_found", "unconfirmed", "strict_warn", "could_not_verify")
        ):
            unverified = True
        else:
            problematic = True
    if problematic:
        return "reference_problem"
    if infrastructure_error:
        return "infrastructure_error"
    if unverified:
        return "unverified"
    return "passed"


def split_checker_log(stderr: str) -> tuple[str, set[str]]:
    """Drop the --verbose detail, which holds request URLs, and return the
    services that answered with a bot challenge."""
    kept: list[str] = []
    challenged: set[str] = set()
    hidden = False
    for line in stderr.splitlines(keepends=True):
        level = LOG_LEVEL_RE.match(line)
        if level:
            hidden = level.group(1) == "DEBUG" or line.startswith(HTTP_RESPONSE_PREFIX)
            challenged.update(name for name, pattern in BOT_CHALLENGE_PATTERNS.items() if pattern.match(line))
        if not hidden:
            kept.append(line)
    return "".join(kept), challenged


def reviewed_openreview_keys(integrity: ModuleType, root: Path, policy: dict[str, Any]) -> set[str]:
    """References whose verified OpenReview identity the ledger records as reviewed."""
    ledger_path = integrity.project_path(root, policy["ledger"], "ledger")
    if not ledger_path.is_file():
        return set()
    keys: set[str] = set()
    for record in integrity.load_ledger(ledger_path)["references"]:
        if (
            isinstance(record, dict)
            and record.get("status") == "verified"
            and (record.get("human_review") or {}).get("state") in {"agent-resolved", "human-confirmed"}
            and "openreview" in ((record.get("verification") or {}).get("sources") or [])
        ):
            keys.add(record["citation_key"])
    return keys


def openreview_residual(record: dict[str, Any], reviewed: set[str]) -> bool:
    fields = set(record.get("mismatched_fields") or [])
    return (
        record["key"] in reviewed
        and str(record["status"]).strip().lower() in OPENREVIEW_RESIDUAL_STATUSES
        and "openreview" in (record.get("api_sources") or [])
        and bool(fields)
        and fields <= OPENREVIEW_RESIDUAL_FIELDS
        and not record["errors"]
        and record["coverage_incomplete"] is False
    )


def rate_limited(result: subprocess.CompletedProcess[str], records: list[dict[str, Any]]) -> bool:
    diagnostics = f"{result.stdout}\n{result.stderr}".lower()
    if any(token in diagnostics for token in RATE_LIMIT_TOKENS):
        return True
    return any(
        "rate_limit" in str(record["status"]).lower()
        or any(token in str(error).lower() for token in RATE_LIMIT_TOKENS)
        for record in records
        for error in (record["errors"] or [""])
    )


def normalized_service(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def throttled_services(result: subprocess.CompletedProcess[str], records: list[dict[str, Any]]) -> set[str]:
    diagnostics = [result.stdout, result.stderr]
    diagnostics.extend(str(error) for record in records for error in record["errors"])
    services: set[str] = set()
    for text in diagnostics:
        for pattern in THROTTLED_SERVICE_PATTERNS:
            services.update(normalized_service(match) for match in pattern.findall(text))
    return services


def only_transient_provider_infrastructure(records: list[dict[str, Any]]) -> bool:
    incomplete = [
        record
        for record in records
        if record["coverage_incomplete"] is True
        or any(token in str(record["status"]).lower() for token in ("api_error", "timeout", "infrastructure"))
    ]

    def transient(record: dict[str, Any], error: Any) -> bool:
        detail = str(error).lower()
        if any(token in detail for token in RATE_LIMIT_TOKENS):
            return True
        if "network failure after retries" in detail or detail == "request timed out":
            return True
        status = str(record["status"]).lower()
        return not detail and any(token in status for token in ("rate_limit", "timeout"))

    return bool(incomplete) and all(
        transient(record, error)
        for record in incomplete
        for error in (record["errors"] or [""])
    )


def only_rate_limit_infrastructure(records: list[dict[str, Any]], services: set[str]) -> bool:
    incomplete = [record for record in records if record["coverage_incomplete"] is True]

    def rate_related(record: dict[str, Any], error: Any) -> bool:
        detail = str(error).lower()
        if any(token in detail for token in RATE_LIMIT_TOKENS):
            return True
        if "network failure after retries" in detail:
            return any(service and service in normalized_service(detail) for service in services)
        return not detail and "rate_limit" in str(record["status"]).lower()

    return bool(incomplete) and all(
        rate_related(record, error)
        for record in incomplete
        for error in (record["errors"] or [""])
    )


def record_fingerprints(
    integrity: ModuleType,
    root: Path,
    policy: dict[str, Any],
    records: list[dict[str, Any]],
    entries: dict[str, str],
    reviewed: set[str],
) -> None:
    """Write into the ledger the fingerprint of each entry this run verified,
    and drop it from each entry with a positive problem, so that the per-PR
    tier queries an entry again only once it changes."""
    ledger_path = integrity.project_path(root, policy["ledger"], "ledger")
    if not ledger_path.is_file():
        print("WARN reference metadata audit: no ledger to record fingerprints in")
        return
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    verdicts = {
        record["key"]: "passed" if openreview_residual(record, reviewed) else classify_records([record])
        for record in records
    }
    written = dropped = 0
    for reference in ledger.get("references", []):
        key = reference.get("citation_key") if isinstance(reference, dict) else None
        verification = reference.get("verification") if key in verdicts else None
        if not isinstance(verification, dict):
            continue
        fingerprint = integrity.bibtex_fingerprint(entries[key])
        if verdicts[key] == "passed" and verification.get("bibtex_fingerprint") != fingerprint:
            verification["bibtex_fingerprint"] = fingerprint
            written += 1
        elif verdicts[key] == "reference_problem" and verification.pop("bibtex_fingerprint", None):
            dropped += 1
    if written or dropped:
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK reference metadata audit recorded {written} fingerprints and dropped {dropped} in the ledger")


def finished_records(path: Path, bibliography_keys: set[str]) -> list[dict[str, Any]]:
    """The records a stopped run streamed before its cap; a line the stop cut
    short, or a record that fails validation, is left out."""
    if not path.is_file():
        return []
    records: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(record, dict)
            and record.get("key") in bibliography_keys
            and validate_records([record], {record["key"]}) is None
        ):
            records[record["key"]] = record
    return list(records.values())


def report_unfinished(
    summary: Path,
    report: Path,
    bibliography_keys: set[str],
    reviewed: set[str],
    timeout: int,
    attempt: int,
    stdout: str,
    stderr: str,
    challenged: set[str],
    skipped: list[str],
    scope: str,
) -> int:
    """A run the cap ended: report what it verified and name what it did not.
    A positive problem among the finished entries still fails as one."""
    finished = finished_records(report, bibliography_keys)
    unfinished = sorted(bibliography_keys - {record["key"] for record in finished})
    residual = [record for record in finished if openreview_residual(record, reviewed)]
    checked = classify_records([record for record in finished if record not in residual]) if finished else "none"
    outcome = "reference_problem" if checked == "reference_problem" else "incomplete"
    write_summary(
        summary,
        outcome=outcome,
        detail=f"time cap of {timeout}s reached; {len(finished)} of {len(bibliography_keys)} entries checked",
        attempts=attempt,
        checker_returncode=None,
        report=".project/build/reference-integrity/metadata.jsonl",
        checked_keys=sorted(record["key"] for record in finished),
        checked_outcome=checked,
        unfinished_keys=unfinished,
        bot_challenged_services=sorted(challenged),
        skipped_services=skipped,
        scope=scope,
        ledger_reviewed_openreview_keys=sorted(record["key"] for record in residual),
    )
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    for record in finished:
        if record not in residual and classify_records([record]) == "reference_problem":
            print(f"ERROR reference_metadata {record['key']}: {record['status']}")
    print(
        f"ERROR reference metadata audit reached its {timeout}s cap"
        f" with {len(finished)} of {len(bibliography_keys)} entries checked ({checked});"
        f" unfinished: {', '.join(unfinished) or 'none'}. The kept cache lets the next run continue."
    )
    return 1 if outcome == "reference_problem" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--uv", default="uv", help="uv executable used with the committed lock")
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=3600, help="cap of the whole run, in seconds")
    parser.add_argument("--rate-limit", type=int, default=30, help="per-service requests per minute")
    parser.add_argument("--workers", type=int, default=4, help="concurrent bibliography entries; each service keeps its own rate")
    parser.add_argument("--scope", choices=("all", "changed"), default="all",
                        help="all entries, or only those new or changed against --base or their ledger fingerprint")
    parser.add_argument("--base", help="base commit of the changed scope")
    parser.add_argument("--record", action="store_true",
                        help="write the fingerprint of each verified entry into the ledger")
    args = parser.parse_args()
    if args.scope == "changed" and not args.base:
        parser.error("--scope changed needs --base")
    root = args.root.expanduser().resolve()
    output = root / ".project/build/reference-integrity"
    report = output / "metadata.jsonl"
    summary = output / "run.json"

    try:
        integrity = load_integrity_module(root)
        policy = integrity.enforcement_policy(root)
    except Exception as exc:  # the summary must survive malformed local policy
        write_summary(summary, outcome="infrastructure_error", detail=str(exc), attempts=0)
        print(f"ERROR reference metadata audit could not load policy: {exc}")
        return 2

    if policy is None or policy["enforcement"] != "enforced":
        write_summary(summary, outcome="skipped", detail="protected publication policy not enabled", attempts=0)
        print("SKIP reference_metadata policy not enabled")
        return 0

    structural = integrity.check(root, "draft")
    if structural != 0:
        write_summary(summary, outcome="local_validation_failed", detail="offline ledger gate failed", attempts=0)
        print("ERROR reference metadata audit blocked by offline ledger validation")
        return 1
    reviewed = reviewed_openreview_keys(integrity, root, policy)

    bibliography = integrity.project_path(root, policy["bibliography"], "bibliography")
    try:
        text = bibliography.read_text(encoding="utf-8")
        entries = dict(integrity.bibtex_entries(text))
        selected = list(entries)
        if args.scope == "changed":
            selected, base_problem = integrity.changed_entries(root, policy, text, args.base)
            if base_problem:
                print(f"WARN reference metadata audit: {base_problem}")
    except Exception as exc:
        write_summary(summary, outcome="local_validation_failed", detail=str(exc), attempts=0)
        print(f"ERROR reference metadata audit could not read bibliography: {exc}")
        return 1
    if not entries:
        write_summary(summary, outcome="skipped", detail="bibliography has no entries", attempts=0, scope=args.scope)
        print("SKIP reference_metadata bibliography has no entries")
        return 0
    if not selected:
        write_summary(summary, outcome="skipped", detail="no entry is new or changed", attempts=0, scope=args.scope,
                      selected_keys=[], entries=len(entries))
        print(f"SKIP reference_metadata none of {len(entries)} entries is new or changed; no provider queried")
        return 0
    bibliography_keys = set(selected)
    audited = bibliography
    if args.scope == "changed":
        print(f"INFO reference metadata audit checks {len(selected)} of {len(entries)} entries, new or changed:"
              f" {', '.join(selected)}")
        audited = output / "selected.bib"
        audited.parent.mkdir(parents=True, exist_ok=True)
        audited.write_text("\n".join(entries[key] for key in selected) + "\n", encoding="utf-8")

    try:
        load_script(root, "_reference_env.py", "paper_reference_env").load_reference_env(root)
        bounded = load_script(root, "_bounded_run.py", "paper_bounded_run")
    except Exception as exc:
        write_summary(summary, outcome="infrastructure_error", detail=str(exc), attempts=0)
        print(f"ERROR reference metadata audit could not load .env or its helpers: {exc}")
        return 2

    uv = shutil.which(args.uv)
    if uv is None:
        write_summary(summary, outcome="infrastructure_error", detail=f"uv executable not found: {args.uv}", attempts=0)
        print(f"ERROR reference metadata audit requires uv: {args.uv}")
        return 2

    dependency_root = root / ".agents/scripts/reference-integrity"
    lock = dependency_root / "uv.lock"
    if not lock.is_file():
        write_summary(summary, outcome="infrastructure_error", detail="missing committed uv.lock", attempts=0)
        print("ERROR reference metadata audit missing dependency lock")
        return 2

    output.mkdir(parents=True, exist_ok=True)
    cache = output / "cache"
    environment = os.environ.copy()
    environment["UV_PROJECT_ENVIRONMENT"] = str(output / "venv")
    environment["UV_CACHE_DIR"] = str(output / "uv-cache")
    command = [
        uv,
        "run",
        "--project",
        str(dependency_root),
        "--frozen",
        "--no-dev",
        "bibtex-check",
        str(audited),
        "--non-generative",
        "--strict",
        "--strict-warn-cnv",
        "--rate-limit",
        str(max(1, args.rate_limit)),
        "--workers",
        str(max(1, args.workers)),
        "--cache-file",
        str(cache / "metadata.db"),
        "--no-google-books",
        "--verbose",
        "--jsonl",
        str(report),
    ]

    skipped = ["openalex"] if bounded.skip_keyless_openalex(cache / "metadata.db", environment, args.timeout + 3600) else []
    if skipped:
        print("WARN reference metadata audit skips OpenAlex without OPENALEX_API_KEY: its keyless daily budget"
              " does not cover a bibliography, and the checker then waits out a Retry-After of hours")
    # The cap bounds the whole run, retries included.
    attempts = max(1, min(args.attempts, 3))
    deadline = time.monotonic() + max(1, args.timeout)
    last_detail = "metadata checker did not run"
    for attempt in range(1, attempts + 1):
        if report.exists():
            report.unlink()
        remaining = deadline - time.monotonic()
        if remaining < 1:
            break
        bounded_result = bounded.run_bounded(command, cwd=root, env=environment, timeout=remaining)
        bounded.scrub_cache(cache, bounded.credential_values(environment))
        stderr, challenged = split_checker_log(bounded_result.stderr)
        if args.record:
            record_fingerprints(integrity, root, policy, finished_records(report, bibliography_keys), entries, reviewed)
        if bounded_result.timed_out:
            return report_unfinished(
                summary, report, bibliography_keys, reviewed, args.timeout, attempt,
                bounded_result.stdout, stderr, challenged, skipped, args.scope,
            )
        result = subprocess.CompletedProcess(command, bounded_result.returncode, bounded_result.stdout, stderr)
        records = read_jsonl(report)
        if records is not None:
            validation_error = validate_records(records, bibliography_keys)
            residual = [] if validation_error else [record for record in records if openreview_residual(record, reviewed)]
            outcome = "infrastructure_error" if validation_error else classify_records(
                [record for record in records if record not in residual]
            )
            throttled = not validation_error and rate_limited(result, records)
            services = set() if validation_error else throttled_services(result, records)
            if throttled and outcome == "unverified":
                outcome = "rate_limited"
            elif challenged and outcome == "unverified":
                outcome = "provider_unavailable"
            elif outcome == "infrastructure_error" and only_transient_provider_infrastructure(records):
                outcome = (
                    "rate_limited"
                    if throttled and only_rate_limit_infrastructure(records, services)
                    else "provider_unavailable"
                )
            # Strict mode exits 4 for the residual records reported below.
            if outcome == "passed" and result.returncode not in ({0, 4} if residual else {0}):
                outcome = "infrastructure_error"
            # Entries a provider failure left open: named, never failed.
            unfinished = [] if validation_error else sorted(
                record["key"] for record in records
                if classify_records([record]) == "infrastructure_error"
                or (outcome in {"rate_limited", "provider_unavailable"} and classify_records([record]) == "unverified")
            )
            write_summary(
                summary,
                outcome=outcome,
                detail=validation_error or "metadata identity only; claim support remains Human-reviewed",
                attempts=attempt,
                checker_returncode=result.returncode,
                report=".project/build/reference-integrity/metadata.jsonl",
                rate_limit_degraded=throttled,
                rate_limited_services=sorted(services),
                bot_challenged_services=sorted(challenged),
                skipped_services=skipped,
                scope=args.scope,
                unfinished_keys=unfinished,
                ledger_reviewed_openreview_keys=sorted(record["key"] for record in residual),
            )
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            if unfinished:
                print(f"WARN reference metadata audit could not finish {len(unfinished)} entries for provider reasons:"
                      f" {', '.join(unfinished)}")
            for service in sorted(challenged):
                print(f"WARN reference metadata service {service} answered with a bot challenge (HTTP 202); its silence is not a miss")
            for record in residual:
                print(
                    f"WARN reference_metadata {record['key']}: {record['status']} on "
                    f"{', '.join(sorted(record['mismatched_fields']))} against OpenReview; "
                    "the ledger records a reviewed OpenReview identity, so this is reported, not failed"
                )
            if outcome == "passed":
                print("OK reference_metadata identity audit passed; claim support not approved")
                return 0
            if outcome == "rate_limited":
                print("WARN reference metadata audit was rate-limited; evidence retained and CI not blocked")
                return 0
            if outcome == "provider_unavailable":
                print("WARN reference metadata provider was unavailable; evidence retained and CI not blocked")
                return 0
            if outcome == "unverified":
                print("ERROR reference metadata audit is unverified; this is not evidence of fabrication")
            elif outcome == "infrastructure_error":
                print(f"ERROR reference metadata infrastructure incomplete: {validation_error or 'checker status/output mismatch'}")
                return 2
            else:
                print("ERROR reference metadata audit found a positive problem; see generated JSONL")
            return 1
        last_detail = (
            f"metadata checker returned {result.returncode} without a valid JSONL report; "
            f"stderr={result.stderr[-1000:].strip()}"
        )

    write_summary(summary, outcome="infrastructure_error", detail=last_detail, attempts=attempts)
    print(f"ERROR reference metadata infrastructure unavailable: {last_detail}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
