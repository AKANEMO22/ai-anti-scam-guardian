from app.models.contracts import UserFeedbackLabelPayload, UserFeedbackToFeedbackLabelRequest


class FeedbackLabelChannel:
    def receive_user_feedback(self, request: UserFeedbackToFeedbackLabelRequest) -> UserFeedbackLabelPayload:
        """Receive user feedback and map it into feedback-label payload stage."""
        return request.payload

    def normalize_feedback_label_payload(self, payload: UserFeedbackLabelPayload) -> UserFeedbackLabelPayload:
        """Normalize feedback label payload before feedback ingestion stage."""
        payload.eventId = payload.eventId.strip()
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        return payload

    def validate_feedback_label_payload(self, payload: UserFeedbackLabelPayload) -> None:
        """Validate feedback label payload for scam/safe/not-sure ingestion contract."""
        if not payload.eventId:
            raise ValueError("Feedback label payload must contain an eventId.")
        if payload.label.value not in ["SCAM", "SAFE", "NOT_SURE"]:
            raise ValueError(f"Invalid feedback label: {payload.label}")
