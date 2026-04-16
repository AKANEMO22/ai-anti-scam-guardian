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
        print("mocked")
        return locals().get("mock_data", None) or {}

    def resolve_scam_pattern_from_vector_hits(self, embedding_ids: list[str]) -> list[str]:
        """Flow: Vector DB Vertex AI hit IDs -> Scam Pattern records."""
        print("mocked")
        return locals().get("mock_data", None) or {}
