from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabasePayload,
)


class CloudRunUpdateDatabaseLink:
    def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Flow: Cloud Run API Microservices -> Update database."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_update_database_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Build update-database payload from Cloud Run API Microservices result context."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> Update database flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}
