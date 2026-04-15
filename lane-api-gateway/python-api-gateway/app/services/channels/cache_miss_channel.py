from app.models.contracts import CacheLayerToCacheMissRequest, CacheLookupResultPayload, TrafficDataType


class CacheMissChannel:
    def receive_from_cache_layer(self, request: CacheLayerToCacheMissRequest) -> CacheLookupResultPayload:
        """Receive cache-layer lookup payload and expose cache-miss stage input."""
        return request.lookup

    def normalize_cache_miss_lookup_payload(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Normalize cache-miss lookup payload for phone/url/script branches."""
        if payload.cacheKey:
            payload.cacheKey = payload.cacheKey.strip().lower()
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        return payload

    def validate_cache_miss_lookup_payload(self, payload: CacheLookupResultPayload) -> None:
        """Validate cache-miss lookup payload required by orchestrator-router stage."""
        if not payload.cacheKey:
            raise ValueError("Cache miss lookup must contain a cacheKey.")

    def route_phone_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build phone-channel cache-miss stage payload."""
        payload.dataType = TrafficDataType.PHONE
        return payload

    def route_url_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build url-channel cache-miss stage payload."""
        payload.dataType = TrafficDataType.URL
        return payload

    def route_script_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build script-channel cache-miss stage payload."""
        payload.dataType = TrafficDataType.SCRIPT
        return payload
