from app.models.contracts import FeedbackIngestionResultPayload, FeedbackLabelToIngestionRequest


class FeedbackIngestionChannel:
    def receive_feedback_label_for_ingestion(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> FeedbackIngestionResultPayload:
        """Receive feedback-label payload and map to feedback-ingestion result stage."""
        return FeedbackIngestionResultPayload(
            payload=request.payload,
            accepted=True
        )

    def normalize_feedback_ingestion_result(
        self,
        payload: FeedbackIngestionResultPayload,
    ) -> FeedbackIngestionResultPayload:
        """Normalize feedback ingestion result payload before cache-layer write stage."""
        if payload.payload.metadata:
            payload.payload.metadata = {k.lower(): str(v).strip() for k, v in payload.payload.metadata.items()}
        return payload

    def validate_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Validate feedback ingestion result payload for cache-layer contracts."""
        if not payload.payload.eventId:
            raise ValueError("Feedback ingestion payload must have an eventId.")
        if payload.payload.label.value not in ["SCAM", "SAFE", "NOT_SURE"]:
            raise ValueError("Feedback ingestion payload must have a valid label.")
