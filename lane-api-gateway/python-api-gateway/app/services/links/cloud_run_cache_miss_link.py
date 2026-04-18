import json
from app.models.contracts import (
    CacheLookupResultPayload,
    CloudRunApiMicroservicesToCacheMissRequest,
)

class CloudRunCacheMissLink:
    def forward_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Flow: Cloud Run -> cache-miss."""
        log_entry = {
            "link": "gateway_cloud_run_cache_miss",
            "event": "forward",
            "microservice": request.result.microservice
        }
        print(json.dumps(log_entry))
        
        # In a real scenario, this would create a CacheLookupResultPayload (cacheHit=False)
        return CacheLookupResultPayload(
            dataType=request.result.dataType,
            cacheKey=request.cacheKey or "unknown",
            cacheHit=False,
            metadata=request.result.metadata
        )

    def build_cache_miss_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Build cache-miss payload from Cloud Run stage results."""
        return CacheLookupResultPayload(
            dataType=request.result.dataType,
            cacheKey=request.cacheKey or "unknown",
            cacheHit=False,
            metadata=request.result.metadata
        )

    def trace_cloud_run_api_microservices_to_cache_miss_flow(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> None:
        """Emit trace point for Cloud Run -> cache-miss internal flow."""
        log_entry = {
            "link": "gateway_cloud_run_cache_miss",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
