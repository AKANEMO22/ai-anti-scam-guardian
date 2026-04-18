import json
import logging
import time
from typing import Dict, Optional
import redis
from dataclasses import dataclass

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
    def __init__(self, ttl_seconds: int = 180, redis_url: str = "redis://localhost:6379/0") -> None:
        self._ttl_seconds = ttl_seconds
        self._redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

    def ingest_cloud_run_api_microservice_result(self, payload: CloudRunMicroserviceResultPayload) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), receive upstream result payload."""
        pass

    def build_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for phone/url/script channels."""
        return f"risk_cache:{data_type.lower()}:{cache_key.lower()}"

    def write_cloud_run_result_to_cache_layer(self, request: CloudRunToCacheRequest) -> None:
        """Arrow: Cloud Run API Microservices -> Cache Layer (redis), write payload to cache."""
        key = self.build_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        try:
            self._redis_client.setex(key, self._ttl_seconds, json.dumps(request.payload))
            log_entry = {
                "event": "cache_write",
                "key": key,
                "dataType": request.dataType,
                "status": "success"
            }
            print(json.dumps(log_entry))
        except Exception as e:
            logger.warning(f"Redis write failed: {e}")

    def read_cloud_run_result_from_cache_layer(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for cached Cloud Run result by phone/url/script channel key."""
        key = self.build_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        try:
            val = self._redis_client.get(key)
            if val:
                log_entry = {
                    "event": "cache_hit",
                    "key": key,
                    "dataType": request.dataType
                }
                print(json.dumps(log_entry))
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis read failed: {e}")
        return None

    def ingest_feedback_ingestion_result(self, payload: FeedbackIngestionResultPayload) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), receive ingestion result payload."""
        pass

    def build_feedback_redis_key_for_phone_url_script(self, data_type: str, cache_key: str) -> str:
        """Build redis-style cache key for feedback ingestion phone/url/script channels."""
        return self.build_redis_key_for_phone_url_script(data_type, cache_key)

    def write_feedback_ingestion_result_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Arrow: Feedback ingestion -> Cache Layer (redis), write feedback ingestion result."""
        key = self.build_feedback_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        try:
            self._redis_client.setex(key, self._ttl_seconds, json.dumps(request.result.model_dump()))
        except Exception as e:
            logger.warning(f"Redis feedback write failed: {e}")

    def read_feedback_ingestion_result_from_cache_layer(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Lookup helper for feedback-ingestion cache keys in phone/url/script channels."""
        key = self.build_feedback_redis_key_for_phone_url_script(request.dataType, request.cacheKey)
        try:
            val = self._redis_client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis feedback read failed: {e}")
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
        try:
            val = self._redis_client.get(key)
            if not val:
                return None
            parsed = json.loads(val)
            return RiskResponse(**parsed)
        except Exception as e:
            logger.warning(f"Redis get risk response failed: {e}")
            return None

    def set(self, key: str, value: RiskResponse) -> None:
        try:
            self._redis_client.setex(key, self._ttl_seconds, json.dumps(value.model_dump()))
        except Exception as e:
            logger.warning(f"Redis set risk response failed: {e}")
