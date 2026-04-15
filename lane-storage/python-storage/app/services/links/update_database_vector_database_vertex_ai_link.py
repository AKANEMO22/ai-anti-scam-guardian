from app.models.contracts import RagEmbeddingPayload, UpdateDatabaseToVectorDatabaseVertexAiRequest
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService
import uuid


class UpdateDatabaseVectorDatabaseVertexAiLink:
    def __init__(self, vector_db_service: VectorDbVertexAiService) -> None:
        self._vector_db_service = vector_db_service

    def forward_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Flow: Update database -> Vector Database Vertex AI."""
        # Build the write request
        write_request = self.build_vector_database_vertex_ai_write_request(request)
        # Process the write request (create embeddings and store them)
        self._process_write_request(write_request)
        # Emit trace for the flow
        self.trace_update_database_to_vector_database_vertex_ai_flow(request)

    def build_vector_database_vertex_ai_write_request(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> dict[str, object]:
        """Build Vector Database Vertex AI write request from update-database stage payload."""
        payload = request.payload

        # Extract text content from the payload
        # This is a simplified extraction - in practice, this would depend on the payload structure
        text_content = self._extract_text_from_payload(payload.payload)

        return {
            "update_key": payload.updateKey,
            "data_type": payload.dataType,
            "text_content": text_content,
            "metadata": payload.metadata,
        }

    def trace_update_database_to_vector_database_vertex_ai_flow(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Emit trace point for Update database -> Vector Database Vertex AI flow."""
        # Simple logging - in a real implementation this might send to a tracing system
        print(f"[TRACE] Update Database -> Vector Database Vertex AI: {request.payload.updateKey}")

    def _extract_text_from_payload(self, payload: dict[str, object]) -> str:
        """Extract text content from the update payload."""
        # Simple extraction logic - look for common text fields
        text_fields = ["text", "content", "message", "description", "script"]

        for field in text_fields:
            if field in payload and isinstance(payload[field], str):
                return payload[field]

        # If no specific text field found, convert the entire payload to string
        return str(payload)

    def _process_write_request(self, write_request: dict[str, object]) -> None:
        """Process the write request by creating embeddings and storing them."""
        text_content = write_request.get("text_content", "")
        if not text_content:
            return

        # Create a simple embedding payload
        # In a real implementation, this would use the embedding service
        embedding_payload = RagEmbeddingPayload(
            source_id=f"update-{write_request['update_key']}-{uuid.uuid4().hex[:8]}",
            source_text=text_content,
            metadata={
                "data_type": write_request["data_type"],
                "update_key": write_request["update_key"],
                **write_request["metadata"]
            },
            # Note: vector would be computed by embedding service in real implementation
            # For now, we'll store without vector since the repository handles it
        )

        # Store the embedding in the vector database
        self._vector_db_service.push_embeddings_from_rag_engine([embedding_payload])
