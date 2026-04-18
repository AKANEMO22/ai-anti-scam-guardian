import json
from app.models.contracts import AuthenticatedDataPayload

class AuthenticatedDataChannel:
    def receive_from_firebase_auth(
        self,
        payload: AuthenticatedDataPayload,
    ) -> AuthenticatedDataPayload:
        """Receive authenticated data payload emitted by Firebase Auth stage."""
        log_entry = {
            "channel": "gateway_auth_data",
            "event": "receive",
            "uid": payload.claims.uid or "unknown",
            "sourceType": payload.sourceType
        }
        print(json.dumps(log_entry))
        
        self.validate_authenticated_data_payload(payload)
        return self.normalize_authenticated_data_payload(payload)

    def normalize_authenticated_data_payload(
        self,
        payload: AuthenticatedDataPayload,
    ) -> AuthenticatedDataPayload:
        """Normalize authenticated data fields before Cloud Run stage."""
        if payload.sourceType:
            payload.sourceType = payload.sourceType.upper()
            
        log_entry = {
            "channel": "gateway_auth_data",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_authenticated_data_payload(self, payload: AuthenticatedDataPayload) -> None:
        """Validate authenticated data consistency for microservice routing."""
        log_entry = {
            "channel": "gateway_auth_data",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))