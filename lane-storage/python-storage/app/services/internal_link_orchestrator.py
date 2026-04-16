from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    EmbeddingLinkRequest,
    PatternMatch,
    PatternResolutionRequest,
    PatternSyncRequest,
    RagEngineLangChainToSearchQueryRequest,
    SearchRequest,
    SearchQueryPayload,
    SearchQueryToThreatAgentRequest,
    UpdateDatabasePayload,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)
from app.services.rag_engine import LangChainRagEngine
from app.services.scam_pattern_service import ScamPatternService
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService


class StorageInternalLinkOrchestrator:
    def __init__(
        self,
        rag_engine: LangChainRagEngine,
        vector_db_service: VectorDbVertexAiService,
        scam_pattern_service: ScamPatternService,
    ) -> None:
        self._rag_engine = rag_engine
        self._vector_db_service = vector_db_service
        self._scam_pattern_service = scam_pattern_service

    def link_embeddings_rag_engine_to_vector_db(self, request: EmbeddingLinkRequest) -> None:
        """Arrow: RAG Engine -> Vector DB Vertex AI (embeddings write path)."""
        # Mock logic
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_semantic_matches_vector_db_to_rag_engine(self, request: SearchRequest) -> list[PatternMatch]:
        """Arrow: Vector DB Vertex AI -> RAG Engine (semantic retrieval path)."""
        # Mock response to satisfy the schema without cost
        return [
            PatternMatch(pattern_id="mock-1", pattern_text="Mock scam pattern text", score=0.9),
            PatternMatch(pattern_id="mock-2", pattern_text="Mock another scam pattern", score=0.85)
        ]

    def link_rag_engine_langchain_to_search_query(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Arrow: RAG Engine LangChain -> Search Query."""
        return SearchQueryPayload(
            query=request.query.query,
            sourceType=request.query.sourceType,
            topK=request.query.topK,
            metadata={"traceId": request.traceId} if request.traceId else {}
        )

    def link_search_query_to_threat_agent(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent."""
        return request.payload

    def link_scam_pattern_to_vector_db(self, request: PatternSyncRequest) -> None:
        """Arrow: Scam Pattern -> Vector DB Vertex AI (pattern metadata sync path)."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_vector_db_to_scam_pattern(self, request: PatternResolutionRequest) -> list[str]:
        """Arrow: Vector DB Vertex AI -> Scam Pattern (pattern resolution path)."""
        return ["scam-pattern-id-1", "scam-pattern-id-2"]

    def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Arrow: Cloud Run API Microservices -> Update database."""
        return UpdateDatabasePayload(
            updateKey=request.updateKey or "default_key",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata
        )

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Arrow: Update database -> Vector Database Vertex AI."""
        print("mocked")
        return locals().get("mock_data", None) or {}
