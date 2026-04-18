import json
import logging
import time
from typing import Dict, Optional

from app.models.contracts import (
    CloudRunMicroserviceResultPayload,
    CloudRunToCacheLookupRequest,
    CloudRunToCacheRequest,
    FeedbackIngestionResultPayload,
    FeedbackIngestionToCacheLookupRequest,
    FeedbackIngestionToCacheRequest,
    RiskResponse,
    SignalRequest,
)

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    value: dict
    expires_at: float


class InMemoryRiskCache:
    def __init__(self, ttl_seconds: int = 180) -> None:
        self._ttl_seconds = ttl_seconds
        self._entries: Dict[str, CacheEntry] = {}

    def ingest_cloud_run_api_microservice_result(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), receive upstream result payload."""
        # This is a hook to potentially post-process results before caching
        pass

    def build_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for phone/url/script channels."""
        return f"risk_cache:{data_type.lower()}:{cache_key.lower()}"

    def write_cloud_run_result_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), write payload to cache."""
        key = self.build_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        expires_at = time.time() + self._ttl_seconds
        self._entries[key] = CacheEntry(value=request.payload, expires_at=expires_at)
        
        log_entry = {
            "event": "cache_write",
            "key": key,
            "dataType": request.dataType,
            "status": "success"
        }
        print(json.dumps(log_entry))

    def read_cloud_run_result_from_cache_layer(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for cached Cloud Run result by phone/url/script channel key."""
        key = self.build_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        now = time.time()
        entry = self._entries.get(key)
        
        if entry is None or entry.expires_at <= now:
            if key in self._entries:
                self._entries.pop(key)
            return None

        log_entry = {
            "event": "cache_hit",
            "key": key,
            "dataType": request.dataType
        }
        print(json.dumps(log_entry))
        return entry.value

    def ingest_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), receive ingestion result payload."""
        # Simple implementation: feedback ingestion might invalidate cache
        pass

    def build_feedback_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for feedback ingestion phone/url/script channels."""
        return self.build_redis_key_for_phone_url_script(data_type, cache_key)

    def write_feedback_ingestion_result_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), write feedback ingestion result."""
        # In this implementation, feedback writes directly to the same key structure
        key = self.build_feedback_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        expires_at = time.time() + self._ttl_seconds
        # Adapt result payload if necessary
        self._entries[key] = CacheEntry(value=request.result.model_dump(), expires_at=expires_at)

    def read_feedback_ingestion_result_from_cache_layer(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for feedback-ingestion cache keys in phone/url/script channels."""
        key = self.build_feedback_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        entry = self._entries.get(key)
        if entry and entry.expires_at > time.time():
            return entry.value
        return None

    def build_key(self, request: SignalRequest) -> str:
        normalized_text = (request.text or "").strip().lower()
        metadata = "|".join(f"{k}:{v}" for k, v in sorted(request.metadata.items()))
        return "::".join(
            [
                request.sourceType.value,
                request.callSessionId or "-",
                normalized_text,
                metadata,
            ]
        )

    def get(self, key: str) -> Optional[RiskResponse]:
        now = time.time()
        entry = self._entries.get(key)
        if entry is None:
            return None

        if entry.expires_at <= now:
            self._entries.pop(key, None)
            return None

        # Try to parse into RiskResponse if it's a dict
        if isinstance(entry.value, dict):
            try:
                return RiskResponse(**entry.value)
            except Exception:
                return None
        return entry.value

    def set(self, key: str, value: RiskResponse) -> None:
        expires_at = time.time() + self._ttl_seconds
        self._entries[key] = CacheEntry(value=value.model_dump(), expires_at=expires_at)
