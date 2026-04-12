from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)


class CloudRunUpdateDatabaseLink:
    def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Flow: Cloud Run API Microservices -> Update database."""
        pass

    def build_update_database_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Build update-database payload from Cloud Run API Microservices result context."""
        pass

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> Update database flow."""
        pass
