import json
from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabasePayload,
)


class CloudRunUpdateDatabaseLink:
    def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Flow: Cloud Run API Microservices -> update-database."""
        log_entry = {
            "link": "cloud_run_update_database",
            "event": "forward",
            "microservice": request.result.microservice
        }
        print(json.dumps(log_entry))
        
        return self.build_update_database_payload_from_cloud_run_api_microservices(request)

    def build_update_database_payload_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Build Update Database payload from Cloud Run API output."""
        return UpdateDatabasePayload(
            updateKey=request.updateKey or "default_key",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata
        )

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run API -> update-database internal flow."""
        log_entry = {
            "link": "cloud_run_update_database",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
