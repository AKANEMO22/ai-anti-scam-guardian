from app.models.contracts import CloudRunMicroserviceResultPayload


class CloudRunResultChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Receive Cloud Run API Microservices output for cache-layer stage."""
        pass

    def normalize_cloud_run_result_payload(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Normalize Cloud Run result payload before Redis cache write stage."""
        pass

    def validate_cloud_run_result_payload(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Validate Cloud Run result payload for phone/url/script cache channels."""
        pass