import json
from app.models.contracts import UserFeedbackLabelPayload


class FeedbackLabelIngestionLink:
    def forward_feedback_label_to_feedback_ingestion(
        self,
        payload: UserFeedbackLabelPayload,
    ) -> UserFeedbackLabelPayload:
        """Flow: feedback-label -> feedback-ingestion."""
        log_entry = {
            "link": "gateway_feedback_label_ingestion",
            "event": "forward",
            "eventId": payload.eventId
        }
        print(json.dumps(log_entry))
        return payload

    def build_feedback_ingestion_request(self, payload: UserFeedbackLabelPayload) -> dict[str, object]:
        """Build feedback ingestion request from feedback label results."""
        return payload.model_dump()

    def trace_feedback_label_to_feedback_ingestion_flow(self, payload: UserFeedbackLabelPayload) -> None:
        """Emit trace point for feedback-label -> feedback-ingestion internal flow."""
        log_entry = {
            "link": "gateway_feedback_label_ingestion",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))