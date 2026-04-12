from app.models.contracts import (
    CacheLookupResultPayload,
    CloudRunApiMicroservicesToCacheMissRequest,
)


class CloudRunCacheMissChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Receive Cloud Run API Microservices payload and expose cache-miss stage input."""
        pass

    def build_cache_miss_lookup_payload(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Build cache-miss lookup payload from Cloud Run result and signal context."""
        pass

    def normalize_cloud_run_cache_miss_payload(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Normalize cloud-run cache-miss payload for phone/url/script channels."""
        pass

    def validate_cloud_run_cache_miss_payload(self, payload: CacheLookupResultPayload) -> None:
        """Validate cloud-run cache-miss payload required by orchestrator-router stage."""
        pass
