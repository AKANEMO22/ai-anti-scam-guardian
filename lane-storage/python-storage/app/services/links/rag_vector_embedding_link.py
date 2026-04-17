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

    def push_embeddings_from_rag_to_vector_db(self, request: SearchRequest) -> None:
        """Flow: LangChain RAG Engine -> embeddings -> Vector DB Vertex AI."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_vector_retrieval_from_rag_query(self, request: SearchRequest) -> VectorRetrievalRequest:
        """Flow: RAG query -> Vector DB retrieval request."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def pull_embedding_matches_from_vector_db(self, request: VectorRetrievalRequest) -> list[PatternMatch]:
        """Flow: Vector DB Vertex AI -> embedding matches -> LangChain RAG Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def map_matches_back_to_rag(self, matches: list[PatternMatch]) -> list[PatternMatch]:
        """Flow: normalize vector matches for LangChain RAG output stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}
