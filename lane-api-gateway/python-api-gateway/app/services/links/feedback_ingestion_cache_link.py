from app.models.contracts import FeedbackIngestionToCacheRequest


class FeedbackIngestionCacheLink:
    def __init__(self, cache_service):
        self._cache_service = cache_service

    def forward_feedback_ingestion_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Flow: feedback ingestion -> Cache Layer (redis) for phone/url/script."""
        self._cache_service.write_feedback_ingestion_result_to_cache_layer(request)

    def build_feedback_cache_write_request(self, request: FeedbackIngestionToCacheRequest) -> dict[str, object]:
        """Build redis-cache write request from feedback ingestion result payload."""
        pass

    def trace_feedback_ingestion_to_cache_flow(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Emit trace point for feedback ingestion -> cache-layer flow."""
        pass