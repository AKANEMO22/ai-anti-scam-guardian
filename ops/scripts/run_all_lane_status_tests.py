from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run project-wide logic checks across all code files")
    parser.add_argument("--strict-exit", action="store_true", help="Return code 1 when logic checks fail")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    runner = repo_root / "ops" / "scripts" / "project_logic_test_runner.py"
    report_dir = repo_root / "ops" / "scripts" / "reports"

    cmd = [
        sys.executable,
        str(runner),
        "--repo-root",
        str(repo_root),
        "--report-dir",
        str(report_dir),
        "--report-name",
        "project_latest_report.json",
    ]

    if args.strict_exit:
        cmd.append("--strict-exit")

    print("\n=== Running project-wide logic checks (all files) ===")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
