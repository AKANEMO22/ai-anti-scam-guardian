import json
from app.models.contracts import CloudRunToCacheRequest, CloudRunMicroserviceResultPayload

class CloudRunCacheLink:
    def forward_cloud_run_api_microservices_to_cache_layer(
        self,
        request: CloudRunToCacheRequest,
    ) -> CloudRunMicroserviceResultPayload:
        """Flow: Cloud Run -> Cache Layer."""
        log_entry = {
            "link": "gateway_cloud_run_cache",
            "event": "forward",
            "cacheLayer": request.cacheLayer,
            "dataType": request.result.dataType
        }
        print(json.dumps(log_entry))
        return request.result

    def build_cache_write_request(self, request: CloudRunToCacheRequest) -> dict[str, object]:
        """Build Cache write request from Cloud Run output results."""
        return request.model_dump()

    def trace_cloud_run_api_microservices_to_cache_layer_flow(self, request: CloudRunToCacheRequest) -> None:
        """Emit trace point for Cloud Run -> Cache Layer internal flow."""
        log_entry = {
            "link": "gateway_cloud_run_cache",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))