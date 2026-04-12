from app.models.contracts import FeedbackIngestionResultPayload, FeedbackLabelToIngestionRequest


class FeedbackIngestionChannel:
    def receive_feedback_label_for_ingestion(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> FeedbackIngestionResultPayload:
        """Receive feedback-label payload and map to feedback-ingestion result stage."""
        pass

    def normalize_feedback_ingestion_result(
        self,
        payload: FeedbackIngestionResultPayload,
    ) -> FeedbackIngestionResultPayload:
        """Normalize feedback ingestion result payload before cache-layer write stage."""
        pass

    def validate_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Validate feedback ingestion result payload for cache-layer contracts."""
        pass