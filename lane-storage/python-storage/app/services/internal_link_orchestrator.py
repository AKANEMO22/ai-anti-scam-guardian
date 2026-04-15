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
from app.services.links.cloud_run_update_database_link import CloudRunUpdateDatabaseLink
from app.services.links.rag_vector_embedding_link import RagVectorEmbeddingLink
from app.services.links.scam_pattern_vector_link import ScamPatternVectorLink
from app.services.links.update_database_vector_database_vertex_ai_link import UpdateDatabaseVectorDatabaseVertexAiLink
from app.services.links.rag_engine_langchain_search_query_link import RagEngineLangChainSearchQueryLink
from app.services.links.search_query_threat_agent_link import SearchQueryThreatAgentLink
from app.services.rag_engine import LangChainRagEngine
from app.services.scam_pattern_service import ScamPatternService
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService


class StorageInternalLinkOrchestrator:
    def __init__(
        self,
        rag_engine: LangChainRagEngine,
        vector_db_service: VectorDbVertexAiService,
        scam_pattern_service: ScamPatternService,
        rag_vector_embedding_link: RagVectorEmbeddingLink,
        scam_pattern_vector_link: ScamPatternVectorLink,
        cloud_run_update_database_link: CloudRunUpdateDatabaseLink,
        update_database_vector_database_vertex_ai_link: UpdateDatabaseVectorDatabaseVertexAiLink,
        rag_engine_langchain_search_query_link: RagEngineLangChainSearchQueryLink,
        search_query_threat_agent_link: SearchQueryThreatAgentLink,
    ) -> None:
        self._rag_engine = rag_engine
        self._vector_db_service = vector_db_service
        self._scam_pattern_service = scam_pattern_service
        self._rag_vector_embedding_link = rag_vector_embedding_link
        self._scam_pattern_vector_link = scam_pattern_vector_link
        self._cloud_run_update_database_link = cloud_run_update_database_link
        self._update_database_vector_database_vertex_ai_link = update_database_vector_database_vertex_ai_link
        self._rag_engine_langchain_search_query_link = rag_engine_langchain_search_query_link
        self._search_query_threat_agent_link = search_query_threat_agent_link

    def link_embeddings_rag_engine_to_vector_db(self, request: EmbeddingLinkRequest) -> None:
        """Arrow: RAG Engine -> Vector DB Vertex AI (embeddings write path)."""
        # For each embedding payload in the request, push it to vector DB
        for payload in request.items:
            # Create a search request from the payload to use the link
            search_request = SearchRequest(
                query=payload.source_text,
                sourceType=payload.metadata.get("sourceType", "unknown")
            )
            # Use the RagVectorEmbeddingLink to push the embedding
            # But since we already have the payload, we could directly push it
            # For now, we'll use the link's method which creates embeddings
            self._rag_vector_embedding_link.push_embeddings_from_rag_to_vector_db(search_request)

    def link_semantic_matches_vector_db_to_rag_engine(self, request: SearchRequest) -> list[PatternMatch]:
        """Arrow: Vector DB Vertex AI -> RAG Engine (semantic retrieval path)."""
        # Build retrieval request from RAG query
        retrieval_request = self._rag_vector_embedding_link.build_vector_retrieval_from_rag_query(request)
        # Pull embedding matches from vector DB
        matches = self._rag_vector_embedding_link.pull_embedding_matches_from_vector_db(retrieval_request)
        # Map matches back to RAG format
        return self._rag_vector_embedding_link.map_matches_back_to_rag(matches)

    def link_rag_engine_langchain_to_search_query(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Arrow: RAG Engine LangChain -> Search Query."""
        # Forward the RAG engine request to search query link
        return self._rag_engine_langchain_search_query_link.forward_rag_engine_langchain_to_search_query(request)

    def link_search_query_to_threat_agent(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent."""
        # Forward the search query to threat agent link
        return self._search_query_threat_agent_link.forward_search_query_to_threat_agent(request)

    def link_scam_pattern_to_vector_db(self, request: PatternSyncRequest) -> None:
        """Arrow: Scam Pattern -> Vector DB Vertex AI (pattern metadata sync path)."""
        # Sync scam pattern metadata to vector DB using the link
        self._scam_pattern_vector_link.sync_scam_pattern_metadata_to_vector_db()

    def link_vector_db_to_scam_pattern(self, request: PatternResolutionRequest) -> list[str]:
        """Arrow: Vector DB Vertex AI -> Scam Pattern (pattern resolution path)."""
        # Resolve scam patterns from vector DB hits using the link
        return self._scam_pattern_vector_link.resolve_scam_pattern_from_vector_hits(request.embedding_ids)

    def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Arrow: Cloud Run API Microservices -> Update database."""
        # Forward the request through the cloud run update database link
        return self._cloud_run_update_database_link.forward_cloud_run_api_microservices_to_update_database(request)

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Arrow: Update database -> Vector Database Vertex AI."""
        # Forward the update database request to vector database vertex ai link
        self._update_database_vector_database_vertex_ai_link.forward_update_database_to_vector_database_vertex_ai(request)
