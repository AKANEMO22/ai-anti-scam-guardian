from app.models.contracts import FeedbackIngestionResultPayload, FeedbackLabelToIngestionRequest


class FeedbackLabelIngestionLink:
    def forward_feedback_label_to_feedback_ingestion(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> FeedbackIngestionResultPayload:
        """Flow: feedback label -> feedback ingestion."""
        pass

    def build_feedback_ingestion_payload(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> dict[str, object]:
        """Build feedback ingestion payload from scam/safe/not-sure label data."""
        pass

    def trace_feedback_label_to_ingestion_flow(self, request: FeedbackLabelToIngestionRequest) -> None:
        """Emit trace point for feedback label -> feedback ingestion flow."""
        pass