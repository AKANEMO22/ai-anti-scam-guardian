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
    # PURPOSE OF cache_service.py:
    # Acts as the quick-reference memory for the API Gateway.
    # EVENTUAL GOAL:
    # Spammers send the exact same text to millions of people. If we analyze it once,
    # we store the result here. The next 999,999 times, we instantly return the cached 
    # result without waking up the expensive AI Agentic Core.
    value: RiskResponse
    expires_at: float


class InMemoryRiskCache:
    def __init__(self, ttl_seconds: int = 180) -> None:
        self._ttl_seconds = ttl_seconds
        self._entries: Dict[str, CacheEntry] = {}
        # We use a simple dictionary to simulate Redis for local development.
        # TODO: In production, this would be an actual connection to a Redis server.
        self._redis_store: Dict[str, dict] = {}

    def ingest_cloud_run_api_microservice_result(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), receive upstream result payload."""
        pass

    def build_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for phone/url/script channels."""
        # Standardizing keys: e.g. "cloud_run:script:cache_miss_12345"
        return f"cloud_run:{data_type.lower()}:{cache_key}"

    def write_cloud_run_result_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), write payload to cache."""
        # Generating the storage key
        actual_key = self.build_redis_key_for_phone_url_script(
            request.result.dataType.value,
            request.cacheKey or f"unknown_{time.time()}"
        )
        # Store it inside our dictionary like we would in Redis
        self._redis_store[actual_key] = request.result.model_dump()
        # setattr(self, f"mock_redis_{actual_key}", request.result.model_dump())
    
    def read_cloud_run_result_from_cache_layer(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for cached Cloud Run result by phone/url/script channel key."""
        actual_key = self.build_redis_key_for_phone_url_script(
            request.dataType.value,
            request.cacheKey
        )
        # Retrieve it from our dictionary like we would from Redis
        return self._redis_store.get(actual_key)
        #setattr(self, f"mock_redis_{actual_key}", request.result.model_dump())
    
    def ingest_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), receive ingestion result payload."""
        pass

    def build_feedback_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for feedback ingestion phone/url/script channels."""
        #   return getattr(self, f"mock_redis_{actual_key}", None)
        return f"feedback_ingestion:{data_type.lower()}:{cache_key}"

    def write_feedback_ingestion_result_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), write feedback ingestion result."""
        # Using string format mapping cache_key correctly for Redis set
        actual_key = self.build_feedback_redis_key_for_phone_url_script(
            request.result.dataType.value,
            request.cacheKey
        )
        self._redis_store[actual_key] = request.result.model_dump()
        #   setattr(self, f"mock_redis_{actual_key}", request.result.model_dump())

    def read_feedback_ingestion_result_from_cache_layer(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for feedback-ingestion cache keys in phone/url/script channels."""
        actual_key = self.build_feedback_redis_key_for_phone_url_script(
            request.dataType.value,
            request.cacheKey
        )
        return self._redis_store.get(actual_key)
    #   return getattr(self, f"mock_redis_{actual_key}", None)


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
