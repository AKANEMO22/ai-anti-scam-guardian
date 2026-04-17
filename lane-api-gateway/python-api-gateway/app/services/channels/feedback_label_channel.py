from app.models.contracts import UserFeedbackLabelPayload, UserFeedbackToFeedbackLabelRequest


class FeedbackLabelChannel:
    def receive_user_feedback(self, request: UserFeedbackToFeedbackLabelRequest) -> UserFeedbackLabelPayload:
        """Receive user feedback and map it into feedback-label payload stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_feedback_label_payload(self, payload: UserFeedbackLabelPayload) -> UserFeedbackLabelPayload:
        """Normalize feedback label payload before feedback ingestion stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_feedback_label_payload(self, payload: UserFeedbackLabelPayload) -> None:
        """Validate feedback label payload for scam/safe/not-sure ingestion contract."""
        print("mocked")
        return locals().get("mock_data", None) or {}