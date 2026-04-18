import json
from app.models.contracts import UpdateDatabaseToVectorDatabaseVertexAiRequest


class UpdateDatabaseVectorDatabaseVertexAiLink:
    def forward_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Flow: update-database -> Vector Database Vertex AI."""
        log_entry = {
            "link": "gateway_update_vertex_ai",
            "event": "forward",
            "updateKey": request.updateKey,
            "dataType": request.dataType
        }
        print(json.dumps(log_entry))
        # This is typically an external API call to the Storage lane or Vertex AI directly
        return

    def build_vector_database_vertex_ai_request(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI request from update-database payload."""
        return request.model_dump()

    def trace_update_database_to_vector_database_vertex_ai_flow(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Emit trace point for update-database -> Vector Database Vertex AI internal flow."""
        log_entry = {
            "link": "gateway_update_vertex_ai",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
