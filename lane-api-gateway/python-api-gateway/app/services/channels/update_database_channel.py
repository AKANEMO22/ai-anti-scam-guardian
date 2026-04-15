from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)


class UpdateDatabaseChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Receive Cloud Run API Microservices payload and expose update-database stage input."""
        return UpdateDatabaseToVectorDatabaseVertexAiRequest(
            updateKey=request.updateKey or request.signal.callSessionId or "unknown_update_key",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata
        )

    def normalize_update_database_payload(
        self,
        payload: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Normalize update-database payload before Vector Database Vertex AI stage."""
        payload.updateKey = payload.updateKey.strip()
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        return payload

    def validate_update_database_payload(
        self,
        payload: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Validate update-database payload structure for Vector Database Vertex AI write flow."""
        if not payload.updateKey:
            raise ValueError("Update database payload must contain an updateKey.")
