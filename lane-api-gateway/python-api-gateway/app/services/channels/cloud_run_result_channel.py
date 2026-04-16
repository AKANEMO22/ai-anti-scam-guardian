from app.models.contracts import CloudRunMicroserviceResultPayload


class CloudRunResultChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Receive Cloud Run API Microservices output for cache-layer stage."""
        return payload

    def normalize_cloud_run_result_payload(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Normalize Cloud Run result payload before Redis cache write stage."""
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        return payload

    def validate_cloud_run_result_payload(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Validate Cloud Run result payload for phone/url/script cache channels."""
        if not payload.response:
            raise ValueError("Cloud run result payload must contain a response dictionary.")
        if "riskScore" not in payload.response:
            raise ValueError("Cloud run result must include a riskScore.")
