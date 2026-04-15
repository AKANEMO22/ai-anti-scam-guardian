import uuid
from app.models.contracts import PatternMatch, RagEmbeddingPayload, SearchRequest, VectorRetrievalRequest
from app.services.embedding_service import EmbeddingService

class LangChainRagEngine:
    def __init__(self, embedding_service: EmbeddingService) -> None:
        self._embedding_service = embedding_service

    def prepare_langchain_context(self, request: SearchRequest) -> list[str]:
        """Prepare LangChain context blocks before embedding and retrieval."""
        return [request.query.strip()]

    def create_embeddings_for_vector_db(self, request: SearchRequest) -> list[RagEmbeddingPayload]:
        """Arrow: LangChain RAG Engine -> embeddings payload -> Vector DB Vertex AI."""
        docs = self.prepare_langchain_context(request)
        vectors = self._embedding_service.build_embeddings_for_rag_documents(docs)
        return [
            RagEmbeddingPayload(
                source_id=f"emb-{uuid.uuid4().hex[:8]}",
                source_text=doc,
                metadata={"sourceType": request.sourceType},
                vector=vec
            ) for doc, vec in zip(docs, vectors)
        ]

    def build_vector_retrieval_query(self, request: SearchRequest) -> VectorRetrievalRequest:
        """Build semantic retrieval request sent from LangChain RAG Engine to Vector DB."""
        query_vector = self._embedding_service.build_embedding_for_search_query(request.query)
        return VectorRetrievalRequest(
            query_vector=query_vector,
            topK=request.topK or 3
        )

    def map_vector_matches_back_to_langchain(self, retrieval_matches: list[PatternMatch]) -> list[PatternMatch]:
        """Arrow: Vector DB Vertex AI -> embeddings matches -> LangChain RAG Engine."""
        return sorted(retrieval_matches, key=lambda x: x.score, reverse=True)
