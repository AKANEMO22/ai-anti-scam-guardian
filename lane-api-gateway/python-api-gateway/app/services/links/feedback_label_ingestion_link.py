from app.models.contracts import FeedbackIngestionResultPayload, FeedbackLabelToIngestionRequest


class FeedbackLabelIngestionLink:
    def forward_feedback_label_to_feedback_ingestion(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> FeedbackIngestionResultPayload:
        """Flow: feedback label -> feedback ingestion."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_feedback_ingestion_payload(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> dict[str, object]:
        """Build feedback ingestion payload from scam/safe/not-sure label data."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_feedback_label_to_ingestion_flow(self, request: FeedbackLabelToIngestionRequest) -> None:
        """Emit trace point for feedback label -> feedback ingestion flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}