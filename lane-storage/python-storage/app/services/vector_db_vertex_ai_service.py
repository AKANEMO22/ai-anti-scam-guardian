from app.models.contracts import PatternMatch, RagEmbeddingPayload, VectorRetrievalRequest
from app.repositories.vector_repository import VectorDbVertexAiRepository


class VectorDbVertexAiService:
    def __init__(self, repository: VectorDbVertexAiRepository) -> None:
        self._repository = repository

    def push_embeddings_from_rag_engine(self, payloads: list[RagEmbeddingPayload]) -> None:
        """Internal link: RAG Engine -> Vector DB Vertex AI via embeddings."""
        for payload in payloads:
            self._repository.upsert_embedding(payload)

    def pull_matches_for_rag_engine(self, request: VectorRetrievalRequest) -> list[PatternMatch]:
        """Internal link: Vector DB Vertex AI -> RAG Engine via semantic matches."""
        return self._repository.search_nearest_neighbors(request)

    def link_scam_patterns_into_vector_index(self, pattern_ids: list[str]) -> None:
        """Internal link: Scam Pattern catalog -> Vector DB metadata mapping."""
        self._repository.attach_pattern_ids_to_embeddings(pattern_ids)

    def resolve_pattern_ids_from_matches(self, embedding_ids: list[str]) -> list[str]:
        """Internal link: Vector DB matches -> Scam Pattern IDs for final context."""
        return self._repository.resolve_pattern_ids_from_embedding_hits(embedding_ids)
