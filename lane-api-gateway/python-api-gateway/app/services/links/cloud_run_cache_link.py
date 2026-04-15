from app.models.contracts import CloudRunToCacheRequest


class CloudRunCacheLink:
    def __init__(self, cache_service):
        self._cache_service = cache_service

    def forward_cloud_run_api_microservices_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Flow: Cloud Run API Microservices -> Cache Layer (redis)."""
        self._cache_service.write_cloud_run_result_to_cache_layer(request)

    def build_cache_write_request_from_cloud_run(self, request: CloudRunToCacheRequest) -> dict[str, object]:
        """Build cache-layer write request object from Cloud Run output payload."""
        pass

    def trace_cloud_run_to_cache_flow(self, request: CloudRunToCacheRequest) -> None:
        """Emit trace point for Cloud Run API Microservices -> Cache Layer flow."""
        pass