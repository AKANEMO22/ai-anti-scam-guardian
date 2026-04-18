import json
from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)


class CloudRunUpdateDatabaseLink:
    def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Flow: Cloud Run -> update-database."""
        log_entry = {
            "link": "gateway_cloud_run_update",
            "event": "forward",
            "microservice": request.result.microservice
        }
        print(json.dumps(log_entry))
        
        return self.build_update_database_payload_from_cloud_run(request)

    def build_update_database_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Build Update Database payload from Cloud Run stage results."""
        return UpdateDatabaseToVectorDatabaseVertexAiRequest(
            updateKey=request.updateKey or f"key_{request.result.dataType}",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata
        )

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run -> update-database internal flow."""
        log_entry = {
            "link": "gateway_cloud_run_update",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
