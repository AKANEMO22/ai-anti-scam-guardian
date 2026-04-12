from app.models.contracts import UpdateDatabaseToVectorDatabaseVertexAiRequest


class UpdateDatabaseVectorDatabaseVertexAiLink:
    def forward_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Flow: Update database -> Vector Database Vertex AI."""
        pass

    def build_vector_database_vertex_ai_write_request(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI write request from update-database stage payload."""
        pass

    def trace_update_database_to_vector_database_vertex_ai_flow(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Emit trace point for Update database -> Vector Database Vertex AI flow."""
        pass
