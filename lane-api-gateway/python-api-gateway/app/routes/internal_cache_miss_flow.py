from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    CacheLayerToCacheMissRequest,
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
)
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])

# PURPOSE:
# This is an "Internal Flow" route. Our scam pipeline uses an event-driven architecture.
# Instead of doing everything in one giant function, steps pass data to each other via HTTP.
# EVENTUAL GOAL:
# When the cache says "I don't know this scam" (Cache Miss), it will hit this endpoint 
# to trigger the next step in the pipeline (usually routing it to the Agentic Core).

@router.post("/v1/gateway/internal/cache-layer-to-cache-miss")
def internal_cache_layer_to_cache_miss(
    request: CacheLayerToCacheMissRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Cache Layer (redis) phone/url/script -> cache miss."""
    pass


@router.post("/v1/gateway/internal/cache-miss-to-orchestrator-agent-langgraph-router")
async def internal_cache_miss_to_orchestrator_agent_langgraph_router(
    request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: cache miss -> Orchestrator Agent LangGraph Router."""
    await internal_orchestrator.link_cache_miss_to_orchestrator_agent_langgraph_router(request)
