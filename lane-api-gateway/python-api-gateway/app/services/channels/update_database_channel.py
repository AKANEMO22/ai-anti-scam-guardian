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
        pass

    def normalize_update_database_payload(
        self,
        payload: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Normalize update-database payload before Vector Database Vertex AI stage."""
        pass

    def validate_update_database_payload(
        self,
        payload: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Validate update-database payload structure for Vector Database Vertex AI write flow."""
        pass
