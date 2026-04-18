import os
import faiss
import numpy as np
import pickle
from typing import List, Dict
from app.models.contracts import PatternMatch, RagEmbeddingPayload, VectorRetrievalRequest
from app.utils.paths import get_base_data_dir

class VectorDbVertexAiRepository:
    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim
        self.index_file = os.path.join(get_base_data_dir(), "faiss_index.bin")
        self.metadata_file = os.path.join(get_base_data_dir(), "faiss_metadata.pkl")
        
        # In FAISS IndexFlatL2, we need an IndexIDMap to store arbitrary string IDs, 
        # but FAISS only supports integer IDs. So we map string IDs to integers.
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
        
        # self.id_to_metadata[int_id] = {"source_id": str, "source_text": str, "metadata": dict}
        self.id_to_metadata: Dict[int, dict] = {}
        # self.source_id_to_int_id[str_id] = int_id
        self.source_id_to_int_id: Dict[str, int] = {}
        
        self.next_int_id = 0
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, "rb") as f:
                    data = pickle.load(f)
                    self.id_to_metadata = data.get("id_to_metadata", {})
                    self.source_id_to_int_id = data.get("source_id_to_int_id", {})
                    self.next_int_id = data.get("next_int_id", 0)
                print(f"Loaded FAISS index with {self.index.ntotal} vectors.")
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Starting fresh.")
                self.index = faiss.IndexIDMap(faiss.IndexFlatL2(self.embedding_dim))
                self.id_to_metadata = {}
                self.source_id_to_int_id = {}
                self.next_int_id = 0

    def _save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "wb") as f:
            pickle.dump({
                "id_to_metadata": self.id_to_metadata,
                "source_id_to_int_id": self.source_id_to_int_id,
                "next_int_id": self.next_int_id
            }, f)

    def upsert_embeddings(self, payloads: list[RagEmbeddingPayload]) -> None:
        """Persist embeddings into FAISS. 
        Note: RagEmbeddingPayload doesn't contain vectors, 
        so we usually use _upsert_with_vectors directly from services that handle embeddings."""
        pass

    def _upsert_with_vectors(self, payloads: list[RagEmbeddingPayload], vectors: list[list[float]]) -> None:
        if not payloads or len(payloads) != len(vectors):
            return
            
        import json
        embeddings_np = np.array(vectors, dtype=np.float32)
        int_ids_np = np.zeros(len(payloads), dtype=np.int64)

        for i, payload in enumerate(payloads):
            source_id = payload.source_id
            if source_id in self.source_id_to_int_id:
                int_id = self.source_id_to_int_id[source_id]
                try:
                    self.index.remove_ids(np.array([int_id], dtype=np.int64))
                except Exception as e:
                    log_entry = {
                        "event": "vector_remove_error",
                        "error": str(e),
                        "sourceId": source_id
                    }
                    print(json.dumps(log_entry))
            else:
                int_id = self.next_int_id
                self.source_id_to_int_id[source_id] = int_id
                self.next_int_id += 1
                
            int_ids_np[i] = int_id
            self.id_to_metadata[int_id] = {
                "source_id": payload.source_id,
                "source_text": payload.source_text,
                "metadata": payload.metadata
            }

        self.index.add_with_ids(embeddings_np, int_ids_np)
        self._save_index()
        
        log_entry = {
            "event": "vector_upsert",
            "count": len(payloads),
            "status": "success"
        }
        print(json.dumps(log_entry))

    def search_embeddings_with_vector(self, query_vector: list[float], top_k: int) -> list[PatternMatch]:
        """Return semantic nearest-neighbor matches from FAISS."""
        if self.index.ntotal == 0:
            return []

        query_np = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_np, top_k)

        matches = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            meta = self.id_to_metadata.get(idx, {})
            # Convert L2 distance to similarity score (naive mapping: 1 / (1 + distance))
            score = 1.0 / (1.0 + float(dist)) if dist >= 0 else 0.0
            
            matches.append(PatternMatch(
                pattern_id=meta.get("source_id", ""),
                pattern_text=meta.get("source_text", ""),
                score=score
            ))

        return matches
        
    def search_embeddings(self, request: VectorRetrievalRequest) -> list[PatternMatch]:
        """Official wrapper for semantic search."""
        # For now, this assumes query_vector is already in request or provided elsewhere.
        # But VectorRetrievalRequest from contract usually has 'query' string, not vector.
        # So we usually use search_embeddings_with_vector.
        return []

    def attach_pattern_ids_to_embeddings(self, pattern_ids: list[str]) -> None:
        """Handled via metadata in upsert."""
        pass

    def resolve_pattern_ids_from_embedding_hits(self, embedding_ids: list[str]) -> list[str]:
        """Handled via metadata in search."""
        pass
