from app.models.contracts import FeedbackIngestionToCacheRequest


class FeedbackIngestionCacheLink:
    def forward_feedback_ingestion_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Flow: feedback ingestion -> Cache Layer (redis) for phone/url/script."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_feedback_cache_write_request(self, request: FeedbackIngestionToCacheRequest) -> dict[str, object]:
        """Build redis-cache write request from feedback ingestion result payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_feedback_ingestion_to_cache_flow(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Emit trace point for feedback ingestion -> cache-layer flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}