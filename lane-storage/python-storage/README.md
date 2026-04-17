# Python Storage Lane

## Vai tro
- Define noi bo 3 khoi theo so do: RAG Engine, Vector DB Vertex AI, Scam Pattern.
- Khai bao ro cac duong noi noi bo giua 3 khoi.
- Tach tung chuc nang thanh file/module rieng.
- Cung cap skeleton function (co mo ta muc dich, chua co logic xu ly).

## Duong noi noi bo theo so do
1. `RAG Engine -> Vector DB Vertex AI` (embeddings write)
2. `Vector DB Vertex AI -> RAG Engine` (semantic retrieval)
3. `Scam Pattern -> Vector DB Vertex AI` (pattern metadata sync)
4. `Vector DB Vertex AI -> Scam Pattern` (pattern resolution)
5. `Cloud Run API Microservices -> Update database`
6. `Update database -> Vector Database Vertex AI`
7. `RAG Engine LangChain -> Search Query`
8. `Search Query -> Threat Agent`

Flow ban yeu cau da duoc set ro:
`Scam Pattern <-> Vector DB Vertex AI <- embeddings -> LangChain RAG Engine`

## File mapping theo chuc nang
- `app/services/rag_engine.py`: ham khung phia RAG Engine
- `app/services/vector_db_vertex_ai_service.py`: ham khung phia Vector DB Vertex AI
- `app/services/scam_pattern_service.py`: ham khung phia Scam Pattern
- `app/services/internal_link_orchestrator.py`: ham khung cho cac duong noi noi bo
- `app/services/links/rag_vector_embedding_link.py`: ham khung rieng cho flow embeddings giua LangChain RAG va Vector DB
- `app/services/links/scam_pattern_vector_link.py`: ham khung rieng cho flow Scam Pattern <-> Vector DB
- `app/services/channels/update_database_channel.py`: ham khung stage update database cho payload tu Cloud Run API Microservices
- `app/services/channels/search_query_channel.py`: ham khung stage Search Query tu RAG Engine LangChain
- `app/services/links/cloud_run_update_database_link.py`: ham khung rieng cho flow Cloud Run API Microservices -> Update database
- `app/services/links/update_database_vector_database_vertex_ai_link.py`: ham khung rieng cho flow Update database -> Vector Database Vertex AI
- `app/services/links/rag_engine_langchain_search_query_link.py`: ham khung rieng cho flow RAG Engine LangChain -> Search Query
- `app/services/links/search_query_threat_agent_link.py`: ham khung rieng cho flow Search Query -> Threat Agent
- `app/repositories/vector_repository.py`: contract thao tac Vector DB
- `app/repositories/scam_pattern_repository.py`: contract thao tac Scam Pattern
- `app/repositories/feedback_repository.py`: contract feedback loop
- `app/routes/storage.py`: endpoint skeleton, gom ca endpoint noi bo

## Chay local
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8102
```

## API chinh
- `POST /v1/storage/search`
- `POST /v1/storage/index`
- `POST /v1/storage/feedback`
- `POST /v1/storage/internal/embeddings-rag-to-vector`
- `POST /v1/storage/internal/vector-to-rag`
- `POST /v1/storage/internal/scam-pattern-to-vector`
- `POST /v1/storage/internal/vector-to-scam-pattern`
- `POST /v1/storage/internal/cloud-run-api-microservices-to-update-database`
- `POST /v1/storage/internal/update-database-to-vector-database-vertex-ai`
- `POST /v1/storage/internal/rag-engine-langchain-to-search-query`
- `POST /v1/storage/internal/search-query-to-threat-agent`
- `GET /health`
