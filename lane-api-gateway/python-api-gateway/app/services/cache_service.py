from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class CacheEntry:
    value: RiskResponse
    expires_at: float


class InMemoryRiskCache:
    def __init__(self, ttl_seconds: int = 180) -> None:
        self._ttl_seconds = ttl_seconds
        self._entries: Dict[str, CacheEntry] = {}

    def ingest_cloud_run_api_microservice_result(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), receive upstream result payload."""
        pass

    def build_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for phone/url/script channels."""
        pass

    def write_cloud_run_result_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), write payload to cache."""
        pass

    def read_cloud_run_result_from_cache_layer(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for cached Cloud Run result by phone/url/script channel key."""
        pass

    def ingest_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), receive ingestion result payload."""
        pass

    def build_feedback_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for feedback ingestion phone/url/script channels."""
        pass

    def write_feedback_ingestion_result_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), write feedback ingestion result."""
        pass

    def read_feedback_ingestion_result_from_cache_layer(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for feedback-ingestion cache keys in phone/url/script channels."""
        pass

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

        return entry.value

    def set(self, key: str, value: RiskResponse) -> None:
        expires_at = time.time() + self._ttl_seconds
        self._entries[key] = CacheEntry(value=value, expires_at=expires_at)
