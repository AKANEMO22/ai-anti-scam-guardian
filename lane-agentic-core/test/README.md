# Lane Agentic Core Logic Test

Run (debug-friendly, always exits 0):

```bash
python lane-agentic-core/test/run_lane_status.py
```

Run (strict for CI, exits 1 when logic check fails):

```bash
python lane-agentic-core/test/run_lane_status.py --strict-exit
```

Debug entrypoint:

```bash
python lane-agentic-core/test/logic_checks.py
```

Output:
- JSON report: `lane-agentic-core/test/reports/latest_report.json`
- Includes function-level implementation status and file-level DONE/NOT_DONE/SKIPPED_NON_CODE.
