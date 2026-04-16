from datetime import datetime
from app.models.contracts import FeedbackEvent, FeedbackIngestionResultPayload, FeedbackLabelToIngestionRequest, SourceType, TrafficDataType

class FeedbackLabelIngestionLink:
    def __init__(self, storage_client):
        self._storage_client = storage_client

    async def forward_feedback_label_to_feedback_ingestion(
        self,
        request: FeedbackLabelToIngestionRequest,
    ) -> FeedbackIngestionResultPayload:
        """Flow: feedback label -> feedback ingestion."""
        # Map TrafficDataType back to the Storage service's SourceType
        data_type = request.payload.dataType
        source_type_map = {
            TrafficDataType.PHONE: SourceType.CALL,
            TrafficDataType.URL: SourceType.URL,
            TrafficDataType.SCRIPT: SourceType.SMS,
        }
        
        feedback = FeedbackEvent(
            eventId=request.payload.eventId,
            userId=request.payload.userId,
            label=request.payload.label.value,
            sourceType=source_type_map.get(data_type, SourceType.SMS),
            riskScore=request.payload.riskScore,
            timestamp=datetime.utcnow().isoformat()
        )
        
        print(f"[Async Worker] Submitting {feedback.label} feedback for Event: {feedback.eventId}")
        accepted = await self._storage_client.submit_feedback(feedback)
        print(f"[Async Worker] Feedback submission accepted: {accepted}")
        
        return FeedbackIngestionResultPayload(
            payload=request.payload,
            accepted=accepted,
            ingestionRef=None
        )

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