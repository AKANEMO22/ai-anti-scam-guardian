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
        # Create embeddings from the search request using RAG engine
        embeddings = self._rag_engine.create_embeddings_for_vector_db(request)
        # Push the embeddings to Vector DB Vertex AI
        self._vector_db_service.push_embeddings_from_rag_engine(embeddings)

    def build_vector_retrieval_from_rag_query(self, request: SearchRequest) -> VectorRetrievalRequest:
        """Flow: RAG query -> Vector DB retrieval request."""
        # Delegate to RAG engine to build the retrieval request
        return self._rag_engine.build_vector_retrieval_query(request)

    def pull_embedding_matches_from_vector_db(self, request: VectorRetrievalRequest) -> list[PatternMatch]:
        """Flow: Vector DB Vertex AI -> embedding matches -> LangChain RAG Engine."""
        # Delegate to vector DB service to retrieve matches
        return self._vector_db_service.pull_matches_for_rag_engine(request)

    def map_matches_back_to_rag(self, matches: list[PatternMatch]) -> list[PatternMatch]:
        """Flow: normalize vector matches for LangChain RAG output stage."""
        # Delegate to RAG engine to map matches back
        return self._rag_engine.map_vector_matches_back_to_langchain(matches)
