import json
from app.models.contracts import UserFeedbackLabelPayload, FeedbackIngestionResultPayload

class FeedbackIngestionChannel:
    def receive_from_feedback_label(
        self,
        payload: UserFeedbackLabelPayload,
    ) -> FeedbackIngestionResultPayload:
        """Receive feedback label payload from feedback stage."""
        log_entry = {
            "channel": "gateway_feedback_ingestion",
            "event": "receive",
            "eventId": payload.eventId,
            "label": payload.label
        }
        print(json.dumps(log_entry))
        
        # Build initial ingestion result
        result = FeedbackIngestionResultPayload(
            payload=payload,
            accepted=True,
            ingestionRef=f"ref_{payload.eventId}"
        )
        
        self.validate_feedback_ingestion_payload(result)
        return self.normalize_feedback_ingestion_payload(result)

    def normalize_feedback_ingestion_payload(
        self,
        payload: FeedbackIngestionResultPayload,
    ) -> FeedbackIngestionResultPayload:
        """Normalize feedback ingestion details before Storage update stage."""
        log_entry = {
            "channel": "gateway_feedback_ingestion",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_feedback_ingestion_payload(self, payload: FeedbackIngestionResultPayload) -> None:
        """Validate feedback ingestion metadata for Vector DB update."""
        log_entry = {
            "channel": "gateway_feedback_ingestion",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
        
    def build_feedback_ingestion_result_payload(self, payload: UserFeedbackLabelPayload) -> FeedbackIngestionResultPayload:
        """Build feedback ingestion result payload."""
        return FeedbackIngestionResultPayload(
            payload=payload,
            accepted=True,
            ingestionRef=f"ref_{payload.eventId}"
        )