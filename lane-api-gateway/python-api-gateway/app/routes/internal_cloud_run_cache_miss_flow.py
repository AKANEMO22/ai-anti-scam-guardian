from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    CloudRunApiMicroservicesToCacheMissRequest,
)
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/cloud-run-api-microservices-to-cache-miss")
def internal_cloud_run_api_microservices_to_cache_miss(
    request: CloudRunApiMicroservicesToCacheMissRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Cloud Run API Microservices -> cache miss."""
    pass


@router.post("/v1/gateway/internal/cloud-run-api-microservices-cache-miss-to-orchestrator-agent-langgraph-router")
def internal_cloud_run_api_microservices_cache_miss_to_orchestrator_agent_langgraph_router(
    request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: cache miss (from Cloud Run API Microservices) -> Orchestrator Agent LangGraph Router."""
    pass
