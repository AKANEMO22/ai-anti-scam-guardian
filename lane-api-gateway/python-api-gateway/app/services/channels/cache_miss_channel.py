from app.models.contracts import CacheLayerToCacheMissRequest, CacheLookupResultPayload


class CacheMissChannel:
    def receive_from_cache_layer(self, request: CacheLayerToCacheMissRequest) -> CacheLookupResultPayload:
        """Receive cache-layer lookup payload and expose cache-miss stage input."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_cache_miss_lookup_payload(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Normalize cache-miss lookup payload for phone/url/script branches."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_cache_miss_lookup_payload(self, payload: CacheLookupResultPayload) -> None:
        """Validate cache-miss lookup payload required by orchestrator-router stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def route_phone_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build phone-channel cache-miss stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def route_url_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build url-channel cache-miss stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def route_script_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build script-channel cache-miss stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}
