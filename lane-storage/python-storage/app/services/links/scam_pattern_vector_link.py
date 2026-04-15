from app.services.scam_pattern_service import ScamPatternService
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService


class ScamPatternVectorLink:
    def __init__(
        self,
        scam_pattern_service: ScamPatternService,
        vector_db_service: VectorDbVertexAiService,
    ) -> None:
        self._scam_pattern_service = scam_pattern_service
        self._vector_db_service = vector_db_service

    def sync_scam_pattern_metadata_to_vector_db(self) -> None:
        """Flow: Scam Pattern catalog -> Vector DB Vertex AI metadata mapping."""
        # Get active pattern IDs from scam pattern service
        pattern_ids = self._scam_pattern_service.load_pattern_ids_for_vector_link()
        # Attach these pattern IDs to embeddings in vector DB
        self._vector_db_service.link_scam_patterns_into_vector_index(pattern_ids)

    def resolve_scam_pattern_from_vector_hits(self, embedding_ids: list[str]) -> list[str]:
        """Flow: Vector DB Vertex AI hit IDs -> Scam Pattern records."""
        # Resolve embedding IDs to pattern IDs using vector DB service
        pattern_ids = self._vector_db_service.resolve_pattern_ids_from_matches(embedding_ids)
        # Get the actual pattern texts from scam pattern service
        return self._scam_pattern_service.resolve_pattern_texts(pattern_ids)
