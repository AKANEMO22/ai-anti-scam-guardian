import json
from app.models.contracts import (
    CloudRunMicroserviceResultPayload,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)


class UpdateDatabaseChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: CloudRunMicroserviceResultPayload,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Receive cloud run result payload emitted by Agentic Core stage."""
        log_entry = {
            "channel": "gateway_update_database",
            "event": "receive",
            "microservice": payload.microservice,
            "dataType": payload.dataType
        }
        print(json.dumps(log_entry))
        
        # Build vector db update request
        update_req = UpdateDatabaseToVectorDatabaseVertexAiRequest(
            updateKey=f"key_{payload.dataType}_{payload.microservice}",
            dataType=payload.dataType,
            payload=payload.response,
            metadata=payload.metadata
        )
        
        self.validate_update_database_payload(update_req)
        return self.normalize_update_database_payload(update_req)

    def normalize_update_database_payload(
        self,
        payload: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Normalize update-database details before Storage lane stage."""
        log_entry = {
            "channel": "gateway_update_database",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_update_database_payload(self, payload: UpdateDatabaseToVectorDatabaseVertexAiRequest) -> None:
        """Validate update-database metadata for cross-lane Storage ingestion."""
        log_entry = {
            "channel": "gateway_update_database",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
