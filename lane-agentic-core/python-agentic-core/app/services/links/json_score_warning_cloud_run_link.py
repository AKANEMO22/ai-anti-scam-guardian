import json
from app.models.contracts import (
    JsonScoreWarningToCloudRunApiMicroservicesRequest,
    JsonScoreWarningPayload,
)


class JsonScoreWarningCloudRunLink:
    def forward_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Flow: JSON score + warning -> Cloud Run API Microservices."""
        log_entry = {
            "link": "json_score_warning_cloud_run",
            "event": "forward",
            "status": "propagated",
            "riskScore": request.payload.riskScore
        }
        print(json.dumps(log_entry))
        # This is a final sink, logic usually ends here or calls an external service
        return

    def build_cloud_run_api_microservices_request(
        self,
        payload: JsonScoreWarningPayload,
    ) -> dict[str, object]:
        """Build request for Cloud Run API from JSON score + warning payload."""
        return payload.model_dump()

    def trace_json_score_warning_to_cloud_run_api_microservices_flow(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Emit trace point for JSON score warning -> Cloud Run API flow."""
        log_entry = {
            "link": "json_score_warning_cloud_run",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
