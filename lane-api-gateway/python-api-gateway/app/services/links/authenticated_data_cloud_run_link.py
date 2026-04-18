import json
from app.models.contracts import AuthenticatedDataToCloudRunRequest


class AuthenticatedDataCloudRunLink:
    def forward_authenticated_data_to_cloud_run(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> None:
        """Flow: Authenticated data -> Cloud Run."""
        log_entry = {
            "link": "gateway_auth_cloud_run",
            "event": "forward",
            "target": request.target,
            "uid": request.authenticatedData.claims.uid
        }
        print(json.dumps(log_entry))
        # This is typically an external API call or handoff to a delivery service
        return

    def build_cloud_run_request(self, request: AuthenticatedDataToCloudRunRequest) -> dict[str, object]:
        """Build Cloud Run request payload from authenticated data context."""
        return request.model_dump()

    def trace_authenticated_data_to_cloud_run_flow(self, request: AuthenticatedDataToCloudRunRequest) -> None:
        """Emit trace point for Authenticated data -> Cloud Run internal flow."""
        log_entry = {
            "link": "gateway_auth_cloud_run",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))