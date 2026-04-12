from app.models.contracts import AuthenticatedDataToCloudRunRequest


class AuthenticatedDataCloudRunLink:
    def forward_authenticated_data_to_cloud_run_api_microservices(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> None:
        """Flow: Authenticated Data -> Cloud Run API Microservices."""
        pass

    def build_cloud_run_microservice_request(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> dict[str, object]:
        """Build Cloud Run API Microservices request object from authenticated data payload."""
        pass

    def trace_authenticated_data_to_cloud_run_flow(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> None:
        """Emit trace point for Authenticated Data -> Cloud Run API Microservices flow."""
        pass