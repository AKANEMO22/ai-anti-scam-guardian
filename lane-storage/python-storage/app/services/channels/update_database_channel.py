from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabasePayload,
)


class UpdateDatabaseChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Receive Cloud Run API Microservices payload and expose update-database stage input."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_update_database_payload(self, payload: UpdateDatabasePayload) -> UpdateDatabasePayload:
        """Normalize update-database payload before Vector Database Vertex AI stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_update_database_payload(self, payload: UpdateDatabasePayload) -> None:
        """Validate update-database payload required for Vector Database Vertex AI write flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}
