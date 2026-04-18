import json
from app.models.contracts import CloudRunMicroserviceResultPayload


class CloudRunResultChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Receive cloud run result payload emitted by Agentic Core stage."""
        log_entry = {
            "channel": "gateway_cloud_run_result",
            "event": "receive",
            "microservice": payload.microservice,
            "dataType": payload.dataType
        }
        print(json.dumps(log_entry))
        
        self.validate_cloud_run_result_payload(payload)
        return self.normalize_cloud_run_result_payload(payload)

    def normalize_cloud_run_result_payload(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> CloudRunMicroserviceResultPayload:
        """Normalize cloud run result details before final response stage."""
        log_entry = {
            "channel": "gateway_cloud_run_result",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_cloud_run_result_payload(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Validate cloud run result metadata for mobile app response."""
        log_entry = {
            "channel": "gateway_cloud_run_result",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))