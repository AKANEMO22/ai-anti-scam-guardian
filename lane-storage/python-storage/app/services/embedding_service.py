import math
from typing import List

class EmbeddingService:
    def _text_to_vector(self, text: str) -> List[float]:
        text_lower = text.lower()
        counts = [float(text_lower.count(chr(ord("a") + i))) for i in range(26)]
        magnitude = math.sqrt(sum(c * c for c in counts)) or 1.0
        return [c / magnitude for c in counts]
    
    def build_embeddings_for_rag_documents(self, documents: list[str]) -> list[list[float]]:
        """Create embeddings from RAG documents before writing to Vector DB Vertex AI."""
        return [self._text_to_vector(doc) for doc in documents]

    def build_embedding_for_search_query(self, query_text: str) -> list[float]:
        """Create one embedding vector from a user query for semantic retrieval."""
        return self._text_to_vector(query_text)

    def score_embedding_similarity(self, left: list[float], right: list[float]) -> float:
        """Return similarity score between two vectors for ranking retrieval results."""
        if len(left) != len(right):
            return 0.0
        dot_product = sum(a * b for a, b in zip(left, right))
        return round(dot_product, 4)
