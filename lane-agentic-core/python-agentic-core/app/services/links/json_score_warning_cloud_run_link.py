from app.models.contracts import JsonScoreWarningToCloudRunApiMicroservicesRequest


class JsonScoreWarningCloudRunLink:
    def forward_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Flow: JSON score + warning -> Cloud Run API Microservices."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_cloud_run_api_microservices_request(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> dict[str, object]:
        """Build Cloud Run API Microservices request body from JSON score + warning payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_json_score_warning_to_cloud_run_api_microservices_flow(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Emit trace point for JSON score + warning -> Cloud Run API Microservices flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}
