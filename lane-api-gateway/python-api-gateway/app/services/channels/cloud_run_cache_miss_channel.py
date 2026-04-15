from app.models.contracts import (
    CacheLayerType,
    CacheLookupResultPayload,
    CloudRunApiMicroservicesToCacheMissRequest,
)


class CloudRunCacheMissChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Receive Cloud Run API Microservices payload and expose cache-miss stage input."""
        return self.build_cache_miss_lookup_payload(request)

    def build_cache_miss_lookup_payload(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Build cache-miss lookup payload from Cloud Run result and signal context."""
        return CacheLookupResultPayload(
            dataType=request.result.dataType,
            cacheLayer=CacheLayerType.REDIS,
            cacheKey=request.cacheKey or request.signal.callSessionId or "unknown_from_cloud",
            metadata=request.result.metadata
        )

    def normalize_cloud_run_cache_miss_payload(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Normalize cloud-run cache-miss payload for phone/url/script channels."""
        if payload.cacheKey:
            payload.cacheKey = payload.cacheKey.strip().lower()
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        return payload

    def validate_cloud_run_cache_miss_payload(self, payload: CacheLookupResultPayload) -> None:
        """Validate cloud-run cache-miss payload required by orchestrator-router stage."""
        if not payload.cacheKey:
            raise ValueError("Cloud run cache miss payload must contain a cacheKey.")
