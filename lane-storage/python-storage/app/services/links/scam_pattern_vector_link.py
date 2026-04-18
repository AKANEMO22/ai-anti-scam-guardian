import json
from app.models.contracts import PatternSyncRequest
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

    def forward_scam_pattern_service_to_vector_database_vertex_ai(
        self,
        request: PatternSyncRequest,
    ) -> PatternSyncRequest:
        """Flow: Scam Pattern Service -> Vector Database Vertex AI."""
        log_entry = {
            "link": "scam_pattern_vector",
            "event": "forward",
            "pattern_ids": request.pattern_ids
        }
        print(json.dumps(log_entry))
        return request

    def build_vector_database_vertex_ai_sync_request(
        self,
        request: PatternSyncRequest,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI sync request from Scam Pattern Service task."""
        return request.model_dump()

    def trace_scam_pattern_service_to_vector_database_vertex_ai_flow(self, request: PatternSyncRequest) -> None:
        """Emit trace point for Scam Pattern Service -> Vector Database Vertex AI internal flow."""
        log_entry = {
            "link": "scam_pattern_vector",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
