from app.models.contracts import PatternMatch, RagEmbeddingPayload, SearchRequest, VectorRetrievalRequest

class LangChainRagEngine:
    def __init__(self, embedding_service, scam_pattern_repository):
        self.embedding_service = embedding_service
        self.scam_pattern_repository = scam_pattern_repository

    def prepare_langchain_context(self, request: SearchRequest) -> list[str]:
        """Prepare LangChain context blocks before embedding and retrieval.
        Actually, in traditional RAG, this might just mean fetching all available patterns to embed them.
        We will return the full list of active patterns for initial indexing.
        """
        patterns = self.scam_pattern_repository.get_all_patterns()
        return [p["sample_text"] for p in patterns]

    def create_embeddings_for_vector_db(self, request: SearchRequest) -> list[RagEmbeddingPayload]:
        """Generate embeddings payload to write to Vector DB (FAISS)."""
        patterns = self.scam_pattern_repository.get_all_patterns()
        
        # We need to map request -> embeddings. Usually we just embed ALL patterns on startup
        # But if request is for seeding:
        if not patterns:
            return []
            
        texts = [p["sample_text"] for p in patterns]
        vectors = self.embedding_service.build_embeddings_for_rag_documents(texts)
        
        payloads = []
        for i, pattern in enumerate(patterns):
            meta = {
                "category": pattern.get("category", ""),
                "risk_level": pattern.get("risk_level", "UNKNOWN")
            }
            payload = RagEmbeddingPayload(
                source_id=pattern["id"],
                source_text=pattern["sample_text"],
                metadata=meta
            )
            # Attach vector directly to the object temporarily or zip it later 
            # (In vector_repository._upsert_with_vectors we zip them)
            payloads.append((payload, vectors[i]))
            
        return payloads

    def build_vector_retrieval_query(self, request: SearchRequest) -> list[float]:
        """Build semantic retrieval request sent from LangChain RAG Engine to Vector DB.
        Returns the embedded vector of the SearchRequest.query.
        """
        return self.embedding_service.build_embedding_for_search_query(request.query)

    def map_vector_matches_back_to_langchain(self, retrieval_matches: list[PatternMatch]) -> list[PatternMatch]:
        """Arrow: Vector DB FAISS -> embeddings matches -> LangChain RAG Engine.
        Here we can enrich matches with additional pattern data if needed.
        For now, pass-through.
        """
        return retrieval_matches
