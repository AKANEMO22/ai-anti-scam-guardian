from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run logic checks for lane-end-user scope")
    parser.add_argument("--strict-exit", action="store_true", help="Return code 1 when logic checks fail")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    repo_root = here.parents[1]
    runner = repo_root / "ops" / "scripts" / "project_logic_test_runner.py"
    report_dir = here / "reports"

    cmd = [
        sys.executable,
        str(runner),
        "--repo-root",
        str(repo_root),
        "--scope",
        "lane-end-user",
        "--report-dir",
        str(report_dir),
        "--report-name",
        "latest_report.json",
    ]

    if args.strict_exit:
        cmd.append("--strict-exit")

    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
