from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import CloudRunToCacheLookupRequest, CloudRunToCacheRequest
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/cloud-run-api-microservices-to-cache-layer")
async def internal_cloud_run_api_microservices_to_cache_layer(
    request: CloudRunToCacheRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Cloud Run API Microservices -> Cache Layer (redis)."""
    await internal_orchestrator.link_cloud_run_api_microservices_to_cache(request)


@router.post("/v1/gateway/internal/cloud-run-api-microservices-to-cache-layer-lookup")
def internal_cloud_run_api_microservices_to_cache_layer_lookup(
    request: CloudRunToCacheLookupRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal lookup link for phone/url/script cache keys in Cache Layer (redis)."""
    print("mocked")
    return locals().get("mock_data", None) or {}