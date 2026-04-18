import json
from app.models.contracts import UpdateDatabasePayload

class UpdateDatabaseChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        payload: UpdateDatabasePayload,
    ) -> UpdateDatabasePayload:
        """Receive data for database update from microservices stage."""
        log_entry = {
            "channel": "storage_update_database",
            "event": "receive",
            "dataType": payload.dataType
        }
        print(json.dumps(log_entry))
        
        self.validate_update_database_payload(payload)
        return self.normalize_update_database_payload(payload)

    def normalize_update_database_payload(
        self,
        payload: UpdateDatabasePayload,
    ) -> UpdateDatabasePayload:
        """Normalize database update payload details before Vertex AI stage."""
        payload.dataType = payload.dataType.upper()
        
        log_entry = {
            "channel": "storage_update_database",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_update_database_payload(self, payload: UpdateDatabasePayload) -> None:
        """Validate database update payload for Vertex AI ingestion."""
        if not payload.updateKey:
            log_entry = {
                "channel": "storage_update_database",
                "event": "validate",
                "warning": "missing_updateKey",
                "action": "ignore_per_user_request"
            }
            print(json.dumps(log_entry))
            
        log_entry = {
            "channel": "storage_update_database",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
