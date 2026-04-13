from app.models.contracts import CloudRunToCacheRequest


class CloudRunCacheLink:
    def forward_cloud_run_api_microservices_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Flow: Cloud Run API Microservices -> Cache Layer (redis)."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_cache_write_request_from_cloud_run(self, request: CloudRunToCacheRequest) -> dict[str, object]:
        """Build cache-layer write request object from Cloud Run output payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_cloud_run_to_cache_flow(self, request: CloudRunToCacheRequest) -> None:
        """Emit trace point for Cloud Run API Microservices -> Cache Layer flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}