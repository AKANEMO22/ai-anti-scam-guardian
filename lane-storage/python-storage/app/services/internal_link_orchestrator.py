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
    VectorRetrievalRequest,
)
from app.services.rag_engine import LangChainRagEngine
from app.services.scam_pattern_service import ScamPatternService
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService

# Import Links
from app.services.links.cloud_run_update_database_link import CloudRunUpdateDatabaseLink
from app.services.links.rag_engine_langchain_search_query_link import RagEngineLangChainSearchQueryLink
from app.services.links.rag_vector_embedding_link import RagVectorEmbeddingLink
from app.services.links.scam_pattern_vector_link import ScamPatternVectorLink
from app.services.links.search_query_threat_agent_link import SearchQueryThreatAgentLink
from app.services.links.update_database_vector_database_vertex_ai_link import UpdateDatabaseVectorDatabaseVertexAiLink

# Import Channels
from app.services.channels.search_query_channel import SearchQueryChannel
from app.services.channels.update_database_channel import UpdateDatabaseChannel


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
        
        # Links
        self.cloud_run_update_link = CloudRunUpdateDatabaseLink()
        self.rag_search_query_link = RagEngineLangChainSearchQueryLink()
        self.rag_vector_link = RagVectorEmbeddingLink()
        self.scam_vector_link = ScamPatternVectorLink()
        self.search_threat_link = SearchQueryThreatAgentLink()
        self.update_vertex_link = UpdateDatabaseVectorDatabaseVertexAiLink()

        # Channels
        self.search_query_channel = SearchQueryChannel()
        self.update_database_channel = UpdateDatabaseChannel()

    def link_embeddings_rag_engine_to_vector_db(self, request: EmbeddingLinkRequest) -> None:
        """Arrow: RAG Engine -> Vector DB Vertex AI (embeddings write path)."""
        import json
        log_entry = {
            "link": "storage_rag_to_vector",
            "event": "write_embeddings",
            "item_count": len(request.items)
        }
        print(json.dumps(log_entry))
        self._vector_db_service.push_embeddings_from_rag_engine(request)

    def link_semantic_matches_vector_db_to_rag_engine(self, request: SearchRequest) -> list[PatternMatch]:
        """Arrow: Vector DB Vertex AI -> RAG Engine (semantic retrieval path)."""
        query_vector = self._rag_engine.build_vector_retrieval_query(request)
        retrieval_req = VectorRetrievalRequest(query_text=request.query, topK=request.topK)
        
        self.rag_vector_link.forward_rag_engine_langchain_to_vector_database_vertex_ai(retrieval_req)
        
        return self._vector_db_service.pull_matches_for_rag_engine(query_vector, request.topK)

    def link_rag_engine_langchain_to_search_query(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Arrow: RAG Engine LangChain -> Search Query."""
        payload = self.rag_search_query_link.build_search_query_payload_from_rag_engine_langchain(request.query)
        return self.search_query_channel.receive_from_rag_engine_langchain(payload)

    def link_search_query_to_threat_agent(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent."""
        return self.search_threat_link.forward_search_query_to_threat_agent(request.payload)

    def link_scam_pattern_to_vector_db(self, request: PatternSyncRequest) -> None:
        """Arrow: Scam Pattern -> Vector DB Vertex AI (pattern metadata sync path)."""
        self.scam_vector_link.forward_scam_pattern_service_to_vector_database_vertex_ai(request)
        self._vector_db_service.link_scam_patterns_into_vector_index(request.pattern_ids)

    def link_vector_db_to_scam_pattern(self, request: PatternResolutionRequest) -> list[str]:
        """Arrow: Vector DB Vertex AI -> Scam Pattern (pattern resolution path)."""
        return self._vector_db_service.resolve_pattern_ids_from_matches(request.embedding_ids)

    def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Arrow: Cloud Run API Microservices -> Update database."""
        payload = self.cloud_run_update_link.forward_cloud_run_api_microservices_to_update_database(request)
        return self.update_database_channel.receive_from_cloud_run_api_microservices(payload)

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Arrow: Update database -> Vector Database Vertex AI."""
        payload = self.update_vertex_link.forward_update_database_to_vector_database_vertex_ai(request.payload)
        # Final sink for storage flow
        import json
        log_entry = {
            "link": "storage_update_to_vertex",
            "event": "finalize",
            "status": "success"
        }
        print(json.dumps(log_entry))
