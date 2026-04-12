# Python Backend Lane Architecture

Tai lieu nay map 3 lane backend Python theo dung luong trong so do:
- API Gateway
- Agentic AI Core
- Storage

Lane End User (Android) duoc giu nguyen.

## 1) Runtime links giua 3 lane

1. End User goi `POST /v1/signals/analyze` vao API Gateway lane.
2. API Gateway lane:
- Validate bearer token.
- Check cache layer (in-memory, tuong duong cache Redis trong demo).
- Cache miss -> goi Agentic Core lane (`/v1/agentic/score`).
- Sau khi co ket qua, API Gateway index signal sang Storage lane (`/v1/storage/index`).
3. Agentic Core lane:
- Orchestrator route signal den Deepfake/STT/Threat/Entity.
- Query Storage lane (`/v1/storage/search`) de lay scam pattern (RAG-like).
- Decision engine tong hop score va explanation.
4. Feedback flow:
- End User goi API Gateway `/v1/feedback`.
- API Gateway forward xuong Storage `/v1/storage/feedback`.

## 2) Port mapping

- API Gateway: `http://localhost:8100`
- Agentic Core: `http://localhost:8101`
- Storage: `http://localhost:8102`

## 3) Folder mapping theo lane

- API Gateway lane:
  - `lane-api-gateway/python-api-gateway/app/routes/analyze.py`
  - `lane-api-gateway/python-api-gateway/app/routes/feedback.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_auth_flow.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_cache_flow.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_cache_miss_flow.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_cloud_run_cache_miss_flow.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_cloud_run_update_database_flow.py`
  - `lane-api-gateway/python-api-gateway/app/routes/internal_feedback_flow.py`
  - `lane-api-gateway/python-api-gateway/app/services/auth_service.py`
  - `lane-api-gateway/python-api-gateway/app/services/cache_service.py`
  - `lane-api-gateway/python-api-gateway/app/services/internal_link_orchestrator.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/authenticated_data_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/cloud_run_result_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/cache_miss_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/cloud_run_cache_miss_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/update_database_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/feedback_label_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/channels/feedback_ingestion_channel.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/firebase_auth_authenticated_data_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/authenticated_data_cloud_run_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/cloud_run_cache_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/cache_miss_orchestrator_langgraph_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/cloud_run_cache_miss_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/cloud_run_update_database_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/update_database_vector_database_vertex_ai_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/feedback_label_ingestion_link.py`
  - `lane-api-gateway/python-api-gateway/app/services/links/feedback_ingestion_cache_link.py`

## 3.3) API Gateway internal links (theo so do)

1. `Firebase Auth -> Authenticated Data`
2. `Authenticated Data -> Cloud Run API Microservices`
3. `Cloud Run API Microservices -> Cache Layer (redis)` cho `phone / url / script`
4. `User feedback (scam/safe/not sure) -> feedback label -> feedback ingestion -> Cache Layer (redis)` cho `phone / url / script`
5. `Cache Layer (redis) phone/url/script -> cache miss -> Orchestrator Agent LangGraph Router`
6. `Cloud Run API Microservices -> cache miss -> Orchestrator Agent LangGraph Router`
7. `Cloud Run API Microservices -> Update database -> Vector Database Vertex AI`

## 3.5) Naming convention cho flow Cache Layer -> cache miss -> Orchestrator Router

- Stage name: `CacheLayer` -> `CacheMiss` -> `OrchestratorAgentLangGraphRouter`
- Payload model: `CacheLookupResultPayload`
- Request model 1: `CacheLayerToCacheMissRequest`
- Request model 2: `CacheMissToOrchestratorAgentLangGraphRouterRequest`
- Route 1: `/v1/gateway/internal/cache-layer-to-cache-miss`
- Route 2: `/v1/gateway/internal/cache-miss-to-orchestrator-agent-langgraph-router`
- Channel class: `CacheMissChannel`
- Link class: `CacheMissOrchestratorLangGraphLink`

## 3.6) Naming convention cho flow Cloud Run -> cache miss -> Orchestrator Router

- Stage name: `CloudRunApiMicroservices` -> `CacheMiss` -> `OrchestratorAgentLangGraphRouter`
- Request model 1: `CloudRunApiMicroservicesToCacheMissRequest`
- Request model 2: `CacheMissToOrchestratorAgentLangGraphRouterRequest`
- Route 1: `/v1/gateway/internal/cloud-run-api-microservices-to-cache-miss`
- Route 2: `/v1/gateway/internal/cloud-run-api-microservices-cache-miss-to-orchestrator-agent-langgraph-router`
- Channel class: `CloudRunCacheMissChannel`
- Link class: `CloudRunCacheMissLink`

## 3.7) Naming convention cho flow Cloud Run -> Update Database -> Vector DB Vertex AI

- Stage name: `CloudRunApiMicroservices` -> `UpdateDatabase` -> `VectorDatabaseVertexAi`
- Request model 1: `CloudRunApiMicroservicesToUpdateDatabaseRequest`
- Request model 2: `UpdateDatabaseToVectorDatabaseVertexAiRequest`
- Route 1: `/v1/gateway/internal/cloud-run-api-microservices-to-update-database`
- Route 2: `/v1/gateway/internal/update-database-to-vector-database-vertex-ai`
- Channel class: `UpdateDatabaseChannel`
- Link class 1: `CloudRunUpdateDatabaseLink`
- Link class 2: `UpdateDatabaseVectorDatabaseVertexAiLink`

- Agentic Core lane:
  - `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
  - `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
  - `lane-agentic-core/python-agentic-core/app/clients/storage_client.py`
  - `lane-agentic-core/python-agentic-core/app/services/agents/*.py`
  - `lane-agentic-core/python-agentic-core/app/services/decision_engine.py`
  - `lane-agentic-core/python-agentic-core/app/services/channels/transcribed_text_channel.py`
  - `lane-agentic-core/python-agentic-core/app/services/channels/search_query_channel.py`
  - `lane-agentic-core/python-agentic-core/app/services/channels/json_score_warning_channel.py`
  - `lane-agentic-core/python-agentic-core/app/services/links/google_stt_transcribed_text_link.py`
  - `lane-agentic-core/python-agentic-core/app/services/links/transcribed_text_threat_agent_link.py`
  - `lane-agentic-core/python-agentic-core/app/services/links/search_query_threat_link.py`
  - `lane-agentic-core/python-agentic-core/app/services/links/decision_json_score_warning_link.py`
  - `lane-agentic-core/python-agentic-core/app/services/links/json_score_warning_cloud_run_link.py`

- Storage lane:
  - `lane-storage/python-storage/app/services/rag_engine.py`
  - `lane-storage/python-storage/app/services/vector_db_vertex_ai_service.py`
  - `lane-storage/python-storage/app/services/scam_pattern_service.py`
  - `lane-storage/python-storage/app/services/internal_link_orchestrator.py`
  - `lane-storage/python-storage/app/services/channels/update_database_channel.py`
  - `lane-storage/python-storage/app/services/channels/search_query_channel.py`
  - `lane-storage/python-storage/app/services/links/cloud_run_update_database_link.py`
  - `lane-storage/python-storage/app/services/links/rag_engine_langchain_search_query_link.py`
  - `lane-storage/python-storage/app/services/links/search_query_threat_agent_link.py`
  - `lane-storage/python-storage/app/services/links/update_database_vector_database_vertex_ai_link.py`
  - `lane-storage/python-storage/app/repositories/vector_repository.py`
  - `lane-storage/python-storage/app/repositories/scam_pattern_repository.py`
  - `lane-storage/python-storage/app/repositories/feedback_repository.py`

## 3.1) Storage internal links (theo so do)

1. `RAG Engine -> Vector DB Vertex AI`:
- embeddings write path
2. `Vector DB Vertex AI -> RAG Engine`:
- semantic retrieval path
3. `Scam Pattern -> Vector DB Vertex AI`:
- pattern metadata sync path
4. `Vector DB Vertex AI -> Scam Pattern`:
- pattern resolution path
5. `Cloud Run API Microservices -> Update database`:
- database update staging path
6. `Update database -> Vector Database Vertex AI`:
- vector write path from updated database payload
7. `RAG Engine LangChain -> Search Query`:
- search-query staging path from LangChain RAG output
8. `Search Query -> Threat Agent`:
- handoff path from Search Query stage to Threat Agent scoring

## 3.2) Agentic Core internal links (theo so do)

1. `Orchestrator Agent LangGraph Route -> Raw Audio`
2. `Orchestrator Agent LangGraph Route -> Text/Metadata`
3. `Orchestrator Agent LangGraph Route -> Voice Stream`
4. `Raw Audio -> Deepfake Agent`
5. `Voice Stream -> Google STT API`
6. `Google STT API -> Transcribed Text`
7. `Transcribed Text -> Threat Agent`
8. `Text/Metadata -> Entity Agent`
9. `Deepfake Agent -> signal/score -> Decision & Reasoning Engine`
10. `Threat Agent -> signal/score -> Decision & Reasoning Engine`
11. `Entity Agent -> signal/score -> Decision & Reasoning Engine`
12. `Decision & Reasoning Engine -> Gemini API Reasoning Engine` (Reasoning/Explanation context)
13. `Gemini API Reasoning Engine -> Decision & Reasoning Engine` (Reasoning/Explanation payload)
14. `Decision & Reasoning Engine -> JSON score + warning`
15. `JSON score + warning -> Cloud Run API Microservices`
16. `Search Query -> Threat Agent` (RAG retrieval context handoff)

## 3.4) Naming convention cho flow Decision -> JSON -> Cloud Run

- Stage name: `DecisionAndReasoningEngine` -> `JsonScoreWarning` -> `CloudRunApiMicroservices`
- Payload model: `JsonScoreWarningPayload`
- Request model 1: `DecisionAndReasoningEngineToJsonScoreWarningRequest`
- Request model 2: `JsonScoreWarningToCloudRunApiMicroservicesRequest`
- Route 1: `/v1/agentic/internal/decision-and-reasoning-engine-to-json-score-warning`
- Route 2: `/v1/agentic/internal/json-score-warning-to-cloud-run-api-microservices`
- Channel class: `JsonScoreWarningChannel`
- Link class 1: `DecisionJsonScoreWarningLink`
- Link class 2: `JsonScoreWarningCloudRunLink`

## 3.8) Naming convention cho flow RAG Engine LangChain -> Search Query -> Threat Agent

- Stage name: `RagEngineLangChain` -> `SearchQuery` -> `ThreatAgent`
- Payload model: `SearchQueryPayload`
- Request model 1 (Storage): `RagEngineLangChainToSearchQueryRequest`
- Request model 2 (Storage): `SearchQueryToThreatAgentRequest`
- Request model 3 (Agentic): `SearchQueryToThreatAgentRequest`
- Route 1 (Storage): `/v1/storage/internal/rag-engine-langchain-to-search-query`
- Route 2 (Storage): `/v1/storage/internal/search-query-to-threat-agent`
- Route 3 (Agentic): `/v1/agentic/internal/search-query-to-threat-agent`
- Channel class (Storage): `SearchQueryChannel`
- Channel class (Agentic): `SearchQueryChannel`
- Link class (Storage 1): `RagEngineLangChainSearchQueryLink`
- Link class (Storage 2): `SearchQueryThreatAgentLink`
- Link class (Agentic): `SearchQueryThreatLink`

## 3.9) Naming convention cho flow Google STT API -> Transcribed Text -> Threat Agent

- Stage name: `GoogleSttApi` -> `TranscribedText` -> `ThreatAgent`
- Payload model: `TranscribedTextPayload`
- Request model 1: `GoogleSttApiToTranscribedTextRequest`
- Request model 2: `TranscribedTextToThreatAgentRequest`
- Route 1: `/v1/agentic/internal/google-stt-api-to-transcribed-text`
- Route 2: `/v1/agentic/internal/transcribed-text-to-threat-agent`
- Channel class: `TranscribedTextChannel`
- Link class 1: `GoogleSttTranscribedTextLink`
- Link class 2: `TranscribedTextThreatAgentLink`

## 4) Chay stack 3 lane

Dung docker compose:

```bash
cd ops/scripts
docker compose -f docker-compose.python-lanes.yml up --build
```

Hoac chay rieng tung lane (3 terminal):

```bash
# Storage
cd lane-storage/python-storage
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8102

# Agentic core
cd lane-agentic-core/python-agentic-core
pip install -r requirements.txt
set STORAGE_BASE_URL=http://localhost:8102
uvicorn app.main:app --host 0.0.0.0 --port 8101

# API gateway
cd lane-api-gateway/python-api-gateway
pip install -r requirements.txt
set AGENTIC_CORE_BASE_URL=http://localhost:8101
set STORAGE_BASE_URL=http://localhost:8102
uvicorn app.main:app --host 0.0.0.0 --port 8100
```

## 5) Vai tro file uu tien can lam truoc (theo lane)

Muc nay tra loi truc tiep cau hoi: moi file quan trong dung de lam gi, va vi sao can lam som.

### 5.1) Lane Storage

- `lane-storage/python-storage/app/models/contracts.py`
  - Vai tro: nguon su that schema cho search/index/feedback/internal flow.
- `lane-storage/python-storage/app/routes/storage.py`
  - Vai tro: expose endpoint de lane khac goi den; khong co route thi lane khac khong tich hop duoc.
- `lane-storage/python-storage/app/services/internal_link_orchestrator.py`
  - Vai tro: backbone noi bo RAG <-> Vector <-> Scam Pattern <-> Update DB.
- `lane-storage/python-storage/app/dependencies.py`
  - Vai tro: dependency wiring de route va service khoi tao dung object graph.
- `lane-storage/python-storage/app/main.py`
  - Vai tro: app entrypoint cua lane storage.

### 5.2) Lane Agentic Core

- `lane-agentic-core/python-agentic-core/app/models/contracts.py`
  - Vai tro: schema fan-out/fan-in cho toan bo stage signal.
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
  - Vai tro: dieu phoi runtime edge giua Deepfake/STT/Threat/Entity/Decision.
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
  - Vai tro: expose cac moc noi noi bo thanh callable unit theo edge.
- `lane-agentic-core/python-agentic-core/app/routes/score.py`
  - Vai tro: cua vao external score + endpoint noi bo stage edges.
- `lane-agentic-core/python-agentic-core/app/clients/storage_client.py`
  - Vai tro: cau noi retrieval/index metadata voi Storage lane.

### 5.3) Lane API Gateway

- `lane-api-gateway/python-api-gateway/app/models/contracts.py`
  - Vai tro: contract API public + handoff contract sang Agentic/Storage.
- `lane-api-gateway/python-api-gateway/app/routes/analyze.py`
  - Vai tro: endpoint chinh cho luong phan tich signal.
- `lane-api-gateway/python-api-gateway/app/routes/feedback.py`
  - Vai tro: endpoint chinh cho feedback loop.
- `lane-api-gateway/python-api-gateway/app/clients/agentic_core_client.py`
  - Vai tro: adapter goi lane Agentic Core.
- `lane-api-gateway/python-api-gateway/app/clients/storage_client.py`
  - Vai tro: adapter goi lane Storage.
- `lane-api-gateway/python-api-gateway/app/services/auth_service.py`
  - Vai tro: auth gate truoc khi vao pipeline backend.
- `lane-api-gateway/python-api-gateway/app/services/cache_service.py`
  - Vai tro: xu ly cache-hit/cache-miss de giam latency.

### 5.4) Thu tu uu tien de lane khac chay duoc

1. Storage lane truoc (la dependency cua Agentic va API Gateway).
2. Agentic Core lane sau (API Gateway phu thuoc endpoint score).
3. API Gateway lane tiep theo (End User goi vao day).
4. End User lane cuoi cung cho integration runtime.
