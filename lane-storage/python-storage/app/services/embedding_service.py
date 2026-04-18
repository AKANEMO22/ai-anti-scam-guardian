import os
import google.generativeai as genai
import math

class EmbeddingService:
    def __init__(self):
        # Configure Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = "models/embedding-001"

    def build_embeddings_for_rag_documents(self, documents: list[str]) -> list[list[float]]:
        """Create embeddings from RAG documents before writing to FAISS."""
        if not documents:
            return []
        
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=documents,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error calling Gemini Embedding API: {e}")
            # Fallback mock for testing if API fails
            return [[0.1] * 768 for _ in documents]

    def build_embedding_for_search_query(self, query_text: str) -> list[float]:
        """Create one embedding vector from a user query for semantic retrieval."""
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query_text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error calling Gemini Embedding API: {e}")
            return [0.1] * 768

    def score_embedding_similarity(self, left: list[float], right: list[float]) -> float:
        """Return cosine similarity score between two vectors."""
        dot_product = sum(a * b for a, b in zip(left, right))
        norm_left = math.sqrt(sum(a * a for a in left))
        norm_right = math.sqrt(sum(b * b for b in right))
        if norm_left == 0 or norm_right == 0:
            return 0.0
        return dot_product / (norm_left * norm_right)
