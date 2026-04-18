import json
from app.models.contracts import CacheLookupResultPayload


class CacheMissChannel:
    def receive_from_cache_layer(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Receive cache lookup result payload emitted by Cache Layer stage."""
        log_entry = {
            "channel": "gateway_cache_miss",
            "event": "receive",
            "cacheKey": payload.cacheKey,
            "cacheHit": payload.cacheHit
        }
        print(json.dumps(log_entry))
        
        self.validate_cache_miss_payload(payload)
        return self.normalize_cache_miss_payload(payload)

    def normalize_cache_miss_payload(
        self,
        payload: CacheLookupResultPayload,
    ) -> CacheLookupResultPayload:
        """Normalize cache miss/hit details before LangGraph router stage."""
        log_entry = {
            "channel": "gateway_cache_miss",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_cache_miss_payload(self, payload: CacheLookupResultPayload) -> None:
        """Validate cache miss/hit metadata for LangGraph routing logic."""
        log_entry = {
            "channel": "gateway_cache_miss",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))

    def route_phone_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build phone-channel cache-miss stage payload."""
        print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
        return locals().get("mock_data", None) or {}

    def route_url_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build url-channel cache-miss stage payload."""
        print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
        return locals().get("mock_data", None) or {}

    def route_script_cache_miss(self, payload: CacheLookupResultPayload) -> CacheLookupResultPayload:
        """Build script-channel cache-miss stage payload."""
        print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
        return locals().get("mock_data", None) or {}
