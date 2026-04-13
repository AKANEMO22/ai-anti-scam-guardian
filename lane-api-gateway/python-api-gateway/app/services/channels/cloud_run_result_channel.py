from app.models.contracts import CloudRunMicroserviceResultPayload


class CloudRunResultChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Receive Cloud Run API Microservices output for cache-layer stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_cloud_run_result_payload(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Normalize Cloud Run result payload before Redis cache write stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_cloud_run_result_payload(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Validate Cloud Run result payload for phone/url/script cache channels."""
        print("mocked")
        return locals().get("mock_data", None) or {}