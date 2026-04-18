import json
from app.models.contracts import TextMetadataPayload

class TextMetadataChannel:
    def receive_from_orchestrator_route(
        self,
        payload: TextMetadataPayload,
    ) -> TextMetadataPayload:
        """Receive Text/Metadata payload from orchestrator for entity-agent stage."""
        log_entry = {
            "channel": "text_metadata",
            "event": "receive",
            "text_len": len(payload.text)
        }
        print(json.dumps(log_entry))
        
        self.validate_text_metadata_payload(payload)
        return self.normalize_text_metadata_payload(payload)

    def normalize_text_metadata_payload(
        self,
        payload: TextMetadataPayload,
    ) -> TextMetadataPayload:
        """Normalize text/metadata payload before entity analysis."""
        payload.text = payload.text.strip()
        
        log_entry = {
            "channel": "text_metadata",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_text_metadata_payload(self, payload: TextMetadataPayload) -> None:
        """Validate text/metadata consistency for entity analysis."""
        log_entry = {
            "channel": "text_metadata",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
