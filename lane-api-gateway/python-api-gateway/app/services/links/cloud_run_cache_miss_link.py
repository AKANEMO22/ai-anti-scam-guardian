from app.models.contracts import (
    CacheLookupResultPayload,
    CloudRunApiMicroservicesToCacheMissRequest,
)


class CloudRunCacheMissLink:
    def forward_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Flow: Cloud Run API Microservices -> cache miss."""
        pass

    def build_cache_miss_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Build cache-miss payload from Cloud Run API Microservices result context."""
        pass

    def trace_cloud_run_api_microservices_to_cache_miss_flow(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> cache miss flow."""
        pass
