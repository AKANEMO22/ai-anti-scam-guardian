from app.models.contracts import PatternMatch, RagEmbeddingPayload, SearchRequest, VectorRetrievalRequest
from app.services.rag_engine import LangChainRagEngine
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService


class RagVectorEmbeddingLink:
    def __init__(
        self,
        rag_engine: LangChainRagEngine,
        vector_db_service: VectorDbVertexAiService,
    ) -> None:
        self._rag_engine = rag_engine
        self._vector_db_service = vector_db_service

    def forward_rag_engine_langchain_to_vector_database_vertex_ai(
        self,
        payload: VectorRetrievalRequest,
    ) -> VectorRetrievalRequest:
        """Flow: RAG Engine -> Vector Database Vertex AI."""
        log_entry = {
            "link": "rag_vector_embedding",
            "event": "forward",
            "query_text": payload.query_text[:30]
        }
        print(json.dumps(log_entry))
        return payload

    def build_vector_database_vertex_ai_request_from_rag(
        self,
        payload: VectorRetrievalRequest,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI request from RAG task output."""
        return payload.model_dump()

    def trace_rag_engine_langchain_to_vector_database_vertex_ai_flow(self, payload: VectorRetrievalRequest) -> None:
        """Emit trace point for RAG Engine -> Vector Database Vertex AI internal flow."""
        log_entry = {
            "link": "rag_vector_embedding",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))

    def map_matches_back_to_rag(self, matches: list[PatternMatch]) -> list[PatternMatch]:
        """Flow: normalize vector matches for LangChain RAG output stage."""
        print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
        return locals().get("mock_data", None) or {}
