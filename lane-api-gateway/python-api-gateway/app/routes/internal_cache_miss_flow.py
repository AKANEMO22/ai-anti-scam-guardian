from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    CacheLayerToCacheMissRequest,
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
)
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/cache-layer-to-cache-miss")
def internal_cache_layer_to_cache_miss(
    request: CacheLayerToCacheMissRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Cache Layer (redis) phone/url/script -> cache miss."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/gateway/internal/cache-miss-to-orchestrator-agent-langgraph-router")
def internal_cache_miss_to_orchestrator_agent_langgraph_router(
    request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: cache miss -> Orchestrator Agent LangGraph Router."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}
