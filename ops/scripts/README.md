# Scripts

- `bootstrap-local.ps1`: script setup local env (secrets, firebase config, endpoint).
- `seed-sample-data.ps1`: nap sample event de test history/dashboard.
- `run-demo-check.ps1`: smoke check cho luong quick scan + call shield.
- `docker-compose.python-lanes.yml`: chay 3 lane backend Python lien ket theo pipeline (API Gateway + Agentic Core + Storage).
- `project_logic_test_runner.py`: bo test logic cap project, scan tat ca code files (.py/.kt/.kts/.java/.dart), detect ham stub/chua lam, va phat hien ham stub dang bi file khac goi.
- `run_all_lane_status_tests.py`: chay logic check toan project trong 1 lenh (debug-friendly mac dinh, co `--strict-exit` cho CI).

Ban co the tao cac script nay o buoc implementation tiep theo.

## Chay nhanh 3 lane Python

```bash
cd ops/scripts
docker compose -f docker-compose.python-lanes.yml up --build
```

## Chay test logic theo lane

```bash
python lane-storage/test/run_lane_status.py
python lane-agentic-core/test/run_lane_status.py
python lane-api-gateway/test/run_lane_status.py
python lane-end-user/test/run_lane_status.py
```

Bao cao JSON se duoc ghi tai:
- `lane-*/test/reports/latest_report.json`

Ban co the debug truc tiep file `logic_checks.py` trong moi lane:

```bash
python lane-storage/test/logic_checks.py
python lane-agentic-core/test/logic_checks.py
python lane-api-gateway/test/logic_checks.py
python lane-end-user/test/logic_checks.py
```

## Chay logic test toan project (tat ca files)

```bash
python ops/scripts/run_all_lane_status_tests.py
```

Neu can fail exit code cho CI:

```bash
python ops/scripts/run_all_lane_status_tests.py --strict-exit
```
