import json
from app.models.contracts import (
    FeedbackIngestionToCacheRequest,
    FeedbackIngestionResultPayload,
)


class FeedbackIngestionCacheLink:
    def forward_feedback_ingestion_to_cache_layer(
        self,
        request: FeedbackIngestionToCacheRequest,
    ) -> FeedbackIngestionResultPayload:
        """Flow: feedback-ingestion -> Cache Layer."""
        log_entry = {
            "link": "gateway_feedback_cache",
            "event": "forward",
            "eventId": request.result.payload.eventId,
            "cacheLayer": request.cacheLayer
        }
        print(json.dumps(log_entry))
        return request.result

    def build_cache_write_request(self, request: FeedbackIngestionToCacheRequest) -> dict[str, object]:
        """Build cache-layer write request from feedback ingestion results."""
        return request.model_dump()

    def trace_feedback_ingestion_to_cache_layer_flow(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Emit trace point for feedback-ingestion -> Cache Layer internal flow."""
        log_entry = {
            "link": "gateway_feedback_cache",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))