import json
from app.models.contracts import UpdateDatabasePayload

class UpdateDatabaseVectorDatabaseVertexAiLink:
    def forward_update_database_to_vector_database_vertex_ai(
        self,
        payload: UpdateDatabasePayload,
    ) -> UpdateDatabasePayload:
        """Flow: update-database -> Vector Database Vertex AI."""
        log_entry = {
            "link": "update_database_vertex_ai",
            "event": "forward",
            "dataType": payload.dataType
        }
        print(json.dumps(log_entry))
        return payload

    def build_vector_database_vertex_ai_request(
        self,
        payload: UpdateDatabasePayload,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI request from update-database payload."""
        return payload.model_dump()

    def trace_update_database_to_vector_database_vertex_ai_flow(self, payload: UpdateDatabasePayload) -> None:
        """Emit trace point for update-database -> Vector Database Vertex AI internal flow."""
        log_entry = {
            "link": "update_database_vertex_ai",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
