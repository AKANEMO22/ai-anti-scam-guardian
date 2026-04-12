from app.models.contracts import PatternMatch, RagEmbeddingPayload, SearchRequest, VectorRetrievalRequest


class LangChainRagEngine:
    def prepare_langchain_context(self, request: SearchRequest) -> list[str]:
        """Prepare LangChain context blocks before embedding and retrieval."""
        pass

    def create_embeddings_for_vector_db(self, request: SearchRequest) -> list[RagEmbeddingPayload]:
        """Arrow: LangChain RAG Engine -> embeddings payload -> Vector DB Vertex AI."""
        pass

    def build_vector_retrieval_query(self, request: SearchRequest) -> VectorRetrievalRequest:
        """Build semantic retrieval request sent from LangChain RAG Engine to Vector DB."""
        pass

    def map_vector_matches_back_to_langchain(self, retrieval_matches: list[PatternMatch]) -> list[PatternMatch]:
        """Arrow: Vector DB Vertex AI -> embeddings matches -> LangChain RAG Engine."""
        pass
