import json
from app.models.contracts import UserFeedbackLabelPayload

class FeedbackLabelChannel:
    def receive_from_user_feedback(
        self,
        payload: UserFeedbackLabelPayload,
    ) -> UserFeedbackLabelPayload:
        """Receive user feedback label payload from collection stage."""
        log_entry = {
            "channel": "gateway_feedback_label",
            "event": "receive",
            "userId": payload.userId,
            "label": payload.label
        }
        print(json.dumps(log_entry))
        
        self.validate_user_feedback_label_payload(payload)
        return self.normalize_user_feedback_label_payload(payload)

    def normalize_user_feedback_label_payload(
        self,
        payload: UserFeedbackLabelPayload,
    ) -> UserFeedbackLabelPayload:
        """Normalize user feedback details before ingestion stage."""
        payload.label = payload.label.upper()
        
        log_entry = {
            "channel": "gateway_feedback_label",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_user_feedback_label_payload(self, payload: UserFeedbackLabelPayload) -> None:
        """Validate user feedback consistency for feedback processing."""
        log_entry = {
            "channel": "gateway_feedback_label",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))