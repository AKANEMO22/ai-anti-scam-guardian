from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_UNFINISHED_PATTERNS = [
    r"NotImplementedError",
    r"UnimplementedError",
    r"TODO:",
    r"^\s*pass\s*$",
]


@dataclass
class CheckResult:
    check_type: str
    name: str
    path: str
    status: str
    issues: list[str]


def find_repo_root(start: Path) -> Path:
    for current in [start, *start.parents]:
        if (current / ".git").exists() or (current / "settings.gradle.kts").exists():
            return current
    return start


def read_text(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file_path.read_text(encoding="latin-1")


def check_required_contains(text: str, required_contains: list[str]) -> list[str]:
    missing: list[str] = []
    for marker in required_contains:
        if marker not in text:
            missing.append(marker)
    return missing


def check_regex_patterns(text: str, regex_patterns: list[str]) -> list[str]:
    hits: list[str] = []
    for pattern in regex_patterns:
        if re.search(pattern, text, flags=re.MULTILINE):
            hits.append(pattern)
    return hits


def run_file_check(repo_root: Path, check: dict[str, Any]) -> CheckResult:
    rel_path = check["path"]
    abs_path = repo_root / rel_path
    name = check.get("name", rel_path)

    issues: list[str] = []
    status = "DONE"

    if not abs_path.exists():
        status = "MISSING"
        issues.append("File not found")
        return CheckResult("file", name, rel_path, status, issues)

    text = read_text(abs_path)

    missing_contains = check_required_contains(text, check.get("required_contains", []))
    if missing_contains:
        status = "NOT_DONE"
        issues.append("Missing required markers: " + " | ".join(missing_contains))

    if not check.get("allow_unfinished", False):
        unfinished_patterns = check.get("unfinished_patterns", DEFAULT_UNFINISHED_PATTERNS)
        unfinished_hits = check_regex_patterns(text, unfinished_patterns)
        if unfinished_hits:
            status = "NOT_DONE"
            issues.append("Found unfinished markers: " + " | ".join(unfinished_hits))

    return CheckResult("file", name, rel_path, status, issues)


def run_cross_lane_check(repo_root: Path, check: dict[str, Any]) -> CheckResult:
    name = check.get("name", "cross-lane-check")
    issues: list[str] = []
    status = "DONE"

    assertions = check.get("assertions", [])
    for assertion in assertions:
        rel_path = assertion["path"]
        abs_path = repo_root / rel_path

        if not abs_path.exists():
            status = "NOT_DONE"
            issues.append(f"Missing linkage file: {rel_path}")
            continue

        text = read_text(abs_path)

        missing_contains = check_required_contains(text, assertion.get("required_contains", []))
        if missing_contains:
            status = "NOT_DONE"
            issues.append(
                "Missing linkage markers in "
                + rel_path
                + ": "
                + " | ".join(missing_contains)
            )

    return CheckResult("cross-lane", name, "(multi-file)", status, issues)


def render_console_report(lane_name: str, results: list[CheckResult]) -> None:
    print(f"=== Lane Status Report: {lane_name} ===")
    print("Status values: DONE / NOT_DONE / MISSING")

    for result in results:
        print(f"[{result.status}] {result.name}")
        if result.check_type == "file":
            print(f"  file: {result.path}")
        else:
            print("  file: cross-lane assertions")
        if result.issues:
            for issue in result.issues:
                print(f"  - {issue}")

    done_count = sum(1 for result in results if result.status == "DONE")
    not_done_count = sum(1 for result in results if result.status == "NOT_DONE")
    missing_count = sum(1 for result in results if result.status == "MISSING")

    print("--- Summary ---")
    print(f"DONE={done_count}")
    print(f"NOT_DONE={not_done_count}")
    print(f"MISSING={missing_count}")


def write_json_report(report_dir: Path, lane_name: str, results: list[CheckResult]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    payload = {
        "lane": lane_name,
        "generatedAt": timestamp,
        "summary": {
            "done": sum(1 for result in results if result.status == "DONE"),
            "notDone": sum(1 for result in results if result.status == "NOT_DONE"),
            "missing": sum(1 for result in results if result.status == "MISSING"),
            "total": len(results),
        },
        "results": [
            {
                "type": result.check_type,
                "name": result.name,
                "path": result.path,
                "status": result.status,
                "issues": result.issues,
            }
            for result in results
        ],
    }

    latest_path = report_dir / "latest_report.json"
    timestamp_path = report_dir / f"status_{timestamp}.json"

    latest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    timestamp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return latest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Lane test runner: file completion + cross-lane linkage checks")
    parser.add_argument("--config", required=True, help="Path to lane status config JSON")
    parser.add_argument("--report-dir", required=True, help="Directory to write JSON reports")
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="Return exit code 0 even when NOT_DONE/MISSING exists",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    report_dir = Path(args.report_dir).resolve()

    if not config_path.exists():
        print(f"Config not found: {config_path}")
        return 2

    config = json.loads(config_path.read_text(encoding="utf-8"))
    lane_name = config.get("lane_name", "Unknown lane")

    repo_root = find_repo_root(config_path.parent)

    results: list[CheckResult] = []

    for file_check in config.get("file_checks", []):
        results.append(run_file_check(repo_root, file_check))

    for cross_check in config.get("cross_lane_checks", []):
        results.append(run_cross_lane_check(repo_root, cross_check))

    render_console_report(lane_name, results)
    report_path = write_json_report(report_dir, lane_name, results)
    print(f"Report written: {report_path}")

    has_failures = any(result.status in {"NOT_DONE", "MISSING"} for result in results)
    if has_failures and not args.allow_incomplete:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
