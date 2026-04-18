# Implementation Priority Report (4 Lane)

Generated: 2026-04-12

## 1) File Count Summary

Measurement notes:
- `ALL_INCL_GIT`: all files on disk including `.git`
- `ALL_EXCL_GIT`: all files on disk excluding `.git`
- `WORKING_TOTAL`: actionable files excluding generated/system folders (`.git`, `.gradle`, `build`, `apk-output`, `.idea`, `.venv`, `__pycache__`)

Counts:
- ALL_INCL_GIT = 3244
- ALL_EXCL_GIT = 2876
- WORKING_TOTAL = 253

Actionable files by lane:
- lane-end-user = 125
- lane-api-gateway = 37
- lane-agentic-core = 47
- lane-storage = 23

Actionable files by top-level area:
- lane-end-user = 125
- lane-agentic-core = 47
- lane-api-gateway = 37
- lane-storage = 23
- docs = 4
- shared = 4
- gradle = 3
- ops = 2
- root files (README/build/gradle wrappers/properties) = 8

Main file-type distribution (actionable scope):
- .py = 91
- .kt = 64
- .xml = 30
- .kts = 19
- .dart = 16
- .md = 10

## 2) Incomplete Scaffold Density (placeholder markers)

Marker patterns: `NotImplementedError`, `UnimplementedError`, `pass`, `TODO:`

Counts by lane:
- lane-end-user = 290
- lane-agentic-core = 164
- lane-api-gateway = 91
- lane-storage = 66

Interpretation:
- End User lane has highest unfinished surface (UI/bridge/worker/orchestrator stubs).
- Agentic Core is the highest backend logic surface.
- API Gateway and Storage are narrower and should be completed first for backend runtime stability.

## 3) Runtime Dependency Order (what must run first)

Based on `ops/scripts/docker-compose.python-lanes.yml`:
1. `storage-lane` (no service dependency)
2. `agentic-core-lane` (depends on storage)
3. `api-gateway-lane` (depends on storage + agentic-core)
4. `lane-end-user` app/Flutter consume API gateway output

Therefore, for end-to-end runnable pipeline, implementation order should be:
1. Lane 4 Storage
2. Lane 3 Agentic Core
3. Lane 2 API Gateway
4. Lane 1 End User

## 4) Critical-First File Plan by Lane

### Lane 4: Storage (do first)

Goal: make retrieval/index/feedback interfaces stable for upstream lanes.

Priority A (must do first):
- `lane-storage/python-storage/app/models/contracts.py`
- `lane-storage/python-storage/app/routes/storage.py`
- `lane-storage/python-storage/app/services/internal_link_orchestrator.py`
- `lane-storage/python-storage/app/main.py`
- `lane-storage/python-storage/app/dependencies.py`

Role map Priority A:
- `lane-storage/python-storage/app/models/contracts.py`: dinh nghia request/response schema cho search/index/feedback va internal edges; day la diem dong bo contract cho lane tren.
- `lane-storage/python-storage/app/routes/storage.py`: expose endpoint runtime (external + internal); route la cua vao de lane khac goi duoc.
- `lane-storage/python-storage/app/services/internal_link_orchestrator.py`: truc dieu phoi noi bo giua RAG, Vector DB, Scam Pattern, Update Database.
- `lane-storage/python-storage/app/main.py`: khoi tao FastAPI app va include router; khong co file nay service khong boot duoc.
- `lane-storage/python-storage/app/dependencies.py`: wiring dependency graph (services/repositories) de route chay duoc.

Why first:
- Defines request/response contracts consumed by Agentic Core and API Gateway.
- Stabilizes endpoint signatures (`/v1/storage/search`, `/v1/storage/index`, `/v1/storage/feedback`, internal routes).

Priority B:
- `lane-storage/python-storage/app/services/rag_engine.py`
- `lane-storage/python-storage/app/services/vector_db_vertex_ai_service.py`
- `lane-storage/python-storage/app/services/scam_pattern_service.py`
- `lane-storage/python-storage/app/services/embedding_service.py`

Priority C:
- `lane-storage/python-storage/app/services/channels/search_query_channel.py`
- `lane-storage/python-storage/app/services/channels/update_database_channel.py`
- `lane-storage/python-storage/app/services/links/*.py`
- `lane-storage/python-storage/app/repositories/*.py`

Completion gate for next lane:
- `/v1/storage/search` returns deterministic schema.
- `/v1/storage/index` and `/v1/storage/feedback` accept payload and return stable ack.

### Lane 3: Agentic Core (do second)

Goal: produce stable scoring pipeline and consume storage retrieval.

Priority A (must do first):
- `lane-agentic-core/python-agentic-core/app/models/contracts.py`
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/routes/score.py`
- `lane-agentic-core/python-agentic-core/app/clients/storage_client.py`

Role map Priority A:
- `lane-agentic-core/python-agentic-core/app/models/contracts.py`: schema trung tam cho signal payload, stage payload, va output score.
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`: orchestration backbone cho fan-out/fan-in (Deepfake/STT/Threat/Entity/Decision).
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`: gom cac moc noi noi bo thanh API callables theo flow edge.
- `lane-agentic-core/python-agentic-core/app/routes/score.py`: expose endpoint external/internal cua Agentic Core; lane API Gateway phu thuoc truc tiep file nay.
- `lane-agentic-core/python-agentic-core/app/clients/storage_client.py`: client goi storage retrieval/index metadata; mat xich de Threat/RAG phoi hop.

Why first:
- This is the execution spine for all internal edges and route exposure.
- API Gateway depends on `/v1/agentic/score` behavior.

Priority B:
- `lane-agentic-core/python-agentic-core/app/services/agents/stt_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/threat_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/deepfake_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/entity_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/reasoning_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/decision_engine.py`

Priority C:
- `lane-agentic-core/python-agentic-core/app/services/channels/*.py`
- `lane-agentic-core/python-agentic-core/app/services/links/*.py`

Completion gate for next lane:
- `/v1/agentic/score` returns stable `riskScore/explanation/sub-scores` schema.
- Internal edges for STT/transcribed-text/threat and search-query/threat are callable.

### Lane 2: API Gateway (do third)

Goal: authenticate, cache, dispatch to agentic/storage, return stable API for clients.

Priority A (must do first):
- `lane-api-gateway/python-api-gateway/app/models/contracts.py`
- `lane-api-gateway/python-api-gateway/app/routes/analyze.py`
- `lane-api-gateway/python-api-gateway/app/routes/feedback.py`
- `lane-api-gateway/python-api-gateway/app/clients/agentic_core_client.py`
- `lane-api-gateway/python-api-gateway/app/clients/storage_client.py`
- `lane-api-gateway/python-api-gateway/app/services/auth_service.py`
- `lane-api-gateway/python-api-gateway/app/services/cache_service.py`

Role map Priority A:
- `lane-api-gateway/python-api-gateway/app/models/contracts.py`: contract public API va contract handoff toi Agentic/Storage.
- `lane-api-gateway/python-api-gateway/app/routes/analyze.py`: entrypoint phan tich signal; gate chinh cua luong runtime end-user -> backend.
- `lane-api-gateway/python-api-gateway/app/routes/feedback.py`: entrypoint feedback loop; mo duong update tri-thuc scam pattern.
- `lane-api-gateway/python-api-gateway/app/clients/agentic_core_client.py`: adapter goi score service lane Agentic.
- `lane-api-gateway/python-api-gateway/app/clients/storage_client.py`: adapter goi index/search/feedback service lane Storage.
- `lane-api-gateway/python-api-gateway/app/services/auth_service.py`: auth gate giua external traffic va backend lane.
- `lane-api-gateway/python-api-gateway/app/services/cache_service.py`: quyet dinh cache-hit/cache-miss va khong che do tre response.

Why first:
- This is the external entrypoint for mobile/web clients.
- Must be stable before End User integration testing.

Priority B:
- `lane-api-gateway/python-api-gateway/app/services/internal_link_orchestrator.py`
- `lane-api-gateway/python-api-gateway/app/routes/internal_*.py`

Priority C:
- `lane-api-gateway/python-api-gateway/app/services/channels/*.py`
- `lane-api-gateway/python-api-gateway/app/services/links/*.py`

Completion gate for next lane:
- `/v1/signals/analyze` and `/v1/feedback` work end-to-end with lane-agentic-core and lane-storage.
- Cache hit/miss behavior is deterministic.

### Lane 1: End User (do fourth for full integration)

Goal: connect UI/background/realtime/feedback to stable backend APIs.

Priority A (must do first in mobile lane):
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/GuardianApp.kt`
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/MainActivity.kt`
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/navigation/AppNavGraph.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/BackgroundMonitorWorker.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/EndUserBackgroundFlowOrchestrator.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningFlowOrchestrator.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowOrchestrator.kt`

Role map Priority A:
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/GuardianApp.kt`: app bootstrap, init dependency/app scope.
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/MainActivity.kt`: host UI runtime va route den feature screens.
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/navigation/AppNavGraph.kt`: dinh nghia navigation graph giua dashboard/scan/warning/history.
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/BackgroundMonitorWorker.kt`: worker thu signal nen (SMS/CALL/URL) va kick pipeline.
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/EndUserBackgroundFlowOrchestrator.kt`: dieu phoi luong Mobile -> Background -> On-device Filter.
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningFlowOrchestrator.kt`: dieu phoi warning explanation va branch theo signal type.
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowOrchestrator.kt`: dieu phoi feedback label -> ingestion -> cache loop.

Priority B:
- Bridges (`MobileAppBackgroundServiceBridge.kt`, `OnDeviceWarningUiBridge.kt`, `WarningUserFeedbackBridge.kt`)
- Flutter flow orchestrators/channels/bridges in `lane-end-user/flutter-mobile-app/lib/**`

Priority C:
- UI polish assets, drawables, styles, and extended feature contracts.

Completion gate:
- Mobile app can send signal, receive warning, submit feedback.
- Background and feedback workers are stable under repeated runs.

## 5) Cross-Lane Milestone Plan (recommended)

Milestone 0: Contract freeze
- Freeze `contracts.py` in Storage, Agentic, API Gateway.
- Freeze openapi/event schema touchpoints in `shared/contracts/*`.

Milestone 1: Service backbone
- Implement `main.py`, `dependencies.py`, core `routes/*.py` in 3 Python lanes.
- Health checks + basic acks first.

Milestone 2: Core pipeline path
- Implement: API Gateway `/v1/signals/analyze` -> Agentic `/v1/agentic/score` -> Storage `/v1/storage/search`.
- Add deterministic fallback handling and timeout behavior.

Milestone 3: Cache + feedback loop
- Implement cache read/write path and feedback path end-to-end.

Milestone 4: Extended internal edges
- Implement update-database/vector path.
- Implement STT -> transcribed-text -> threat path.
- Implement RAG-search-query -> threat handoff path.

Milestone 5: End User integration
- Wire Android/Flutter lane to stable gateway APIs and worker loops.

## 6) Immediate Do-First Checklist (next practical steps)

1. Complete Storage Priority A files first.
2. Complete Agentic Core Priority A files next.
3. Complete API Gateway Priority A files next.
4. Run compose stack and verify 3-lane backend runtime.
5. Then wire End User lane orchestrators/workers/bridges to real endpoints.

## 7) Validation Checklist per sprint

- Python: `python -m compileall app` in all 3 backend lanes.
- Kotlin: compile app/service/feature/core/domain/data modules.
- Workspace diagnostics: zero new errors.
- Pipeline docs updated when adding new edges/contracts.
