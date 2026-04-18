# Python API Gateway Lane

## Vai tro
- Nhan request tu mobile end-user.
- Validate auth.
- Quan ly cache layer.
- Forward cache miss sang Agentic Core lane.
- Dong bo index/feedback xuong Storage lane.

## Duong noi noi bo theo so do
1. `Firebase Auth -> Authenticated Data`
2. `Authenticated Data -> Cloud Run API Microservices`
3. `Cloud Run API Microservices -> Cache Layer (redis)` cho `phone / url / script`
4. `User feedback (scam/safe/not sure) -> feedback label -> feedback ingestion -> Cache Layer (redis)` cho `phone / url / script`
5. `Cache Layer (redis) phone/url/script -> cache miss -> Orchestrator Agent LangGraph Router`
6. `Cloud Run API Microservices -> cache miss -> Orchestrator Agent LangGraph Router`
7. `Cloud Run API Microservices -> Update database -> Vector Database Vertex AI`

## File mapping theo chuc nang
- `app/services/auth_service.py`: skeleton auth service (bao gom flow Firebase Auth -> Authenticated Data)
- `app/services/channels/authenticated_data_channel.py`: skeleton stage Authenticated Data
- `app/services/channels/cloud_run_result_channel.py`: skeleton stage output tu Cloud Run API Microservices
- `app/services/channels/feedback_label_channel.py`: skeleton stage feedback label tu user feedback
- `app/services/channels/feedback_ingestion_channel.py`: skeleton stage feedback ingestion
- `app/services/channels/cache_miss_channel.py`: skeleton stage cache miss tu cache layer (redis)
- `app/services/channels/cloud_run_cache_miss_channel.py`: skeleton stage cache miss tu Cloud Run API Microservices
- `app/services/channels/update_database_channel.py`: skeleton stage update database tu Cloud Run API Microservices
- `app/services/internal_link_orchestrator.py`: skeleton dieu phoi internal link trong lane API Gateway
- `app/services/links/firebase_auth_authenticated_data_link.py`: skeleton link rieng Firebase Auth -> Authenticated Data
- `app/services/links/authenticated_data_cloud_run_link.py`: skeleton link rieng Authenticated Data -> Cloud Run API Microservices
- `app/services/links/cloud_run_cache_link.py`: skeleton link rieng Cloud Run API Microservices -> Cache Layer (redis)
- `app/services/links/feedback_label_ingestion_link.py`: skeleton link rieng feedback label -> feedback ingestion
- `app/services/links/feedback_ingestion_cache_link.py`: skeleton link rieng feedback ingestion -> Cache Layer (redis)
- `app/services/links/cache_miss_orchestrator_langgraph_link.py`: skeleton link rieng cache miss -> Orchestrator Agent LangGraph Router
- `app/services/links/cloud_run_cache_miss_link.py`: skeleton link rieng Cloud Run API Microservices -> cache miss
- `app/services/links/cloud_run_update_database_link.py`: skeleton link rieng Cloud Run API Microservices -> Update database
- `app/services/links/update_database_vector_database_vertex_ai_link.py`: skeleton link rieng Update database -> Vector Database Vertex AI
- `app/services/cache_service.py`: skeleton cache layer service (redis key theo phone/url/script)
- `app/routes/internal_auth_flow.py`: endpoint skeleton cho internal flow
- `app/routes/internal_cache_flow.py`: endpoint skeleton cho flow Cloud Run -> Cache Layer
- `app/routes/internal_cache_miss_flow.py`: endpoint skeleton cho flow Cache Layer -> cache miss -> Orchestrator Agent LangGraph Router
- `app/routes/internal_cloud_run_cache_miss_flow.py`: endpoint skeleton cho flow Cloud Run API Microservices -> cache miss -> Orchestrator Agent LangGraph Router
- `app/routes/internal_cloud_run_update_database_flow.py`: endpoint skeleton cho flow Cloud Run API Microservices -> Update database -> Vector Database Vertex AI
- `app/routes/internal_feedback_flow.py`: endpoint skeleton cho flow feedback -> label -> ingestion -> Cache Layer

## Chay local
```bash
pip install -r requirements.txt
set AGENTIC_CORE_BASE_URL=http://localhost:8101
set STORAGE_BASE_URL=http://localhost:8102
uvicorn app.main:app --host 0.0.0.0 --port 8100
```

## API chinh
- `POST /v1/signals/analyze`
- `POST /v1/feedback`
- `POST /v1/gateway/internal/firebase-auth-to-authenticated-data`
- `POST /v1/gateway/internal/authenticated-data-to-cloud-run-api-microservices`
- `POST /v1/gateway/internal/cloud-run-api-microservices-to-cache-layer`
- `POST /v1/gateway/internal/cloud-run-api-microservices-to-cache-layer-lookup`
- `POST /v1/gateway/internal/cache-layer-to-cache-miss`
- `POST /v1/gateway/internal/cache-miss-to-orchestrator-agent-langgraph-router`
- `POST /v1/gateway/internal/cloud-run-api-microservices-to-cache-miss`
- `POST /v1/gateway/internal/cloud-run-api-microservices-cache-miss-to-orchestrator-agent-langgraph-router`
- `POST /v1/gateway/internal/cloud-run-api-microservices-to-update-database`
- `POST /v1/gateway/internal/update-database-to-vector-database-vertex-ai`
- `POST /v1/gateway/internal/user-feedback-to-feedback-label`
- `POST /v1/gateway/internal/feedback-label-to-feedback-ingestion`
- `POST /v1/gateway/internal/feedback-ingestion-to-cache-layer`
- `POST /v1/gateway/internal/feedback-ingestion-to-cache-layer-lookup`
- `GET /health`
