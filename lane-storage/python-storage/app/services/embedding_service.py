class EmbeddingService:
    def build_embeddings_for_rag_documents(self, documents: list[str]) -> list[list[float]]:
        """Create embeddings from RAG documents before writing to Vector DB Vertex AI."""
        pass

    def build_embedding_for_search_query(self, query_text: str) -> list[float]:
        """Create one embedding vector from a user query for semantic retrieval."""
        pass

    def score_embedding_similarity(self, left: list[float], right: list[float]) -> float:
        """Return similarity score between two vectors for ranking retrieval results."""
        pass
