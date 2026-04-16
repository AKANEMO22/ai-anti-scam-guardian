from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, BackgroundTasks

from app.dependencies import (
    get_auth_service,
    get_cache_service,
    get_api_gateway_internal_link_orchestrator,
)
from app.models.contracts import RiskResponse, SignalRequest, CacheMissToOrchestratorAgentLangGraphRouterRequest, CacheLookupResultPayload, TrafficDataType, SourceType
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["signals"])

def _map_source_type_to_traffic_data_type(source: SourceType) -> TrafficDataType:
    if source == SourceType.CALL:
        return TrafficDataType.PHONE
    
    elif source == SourceType.URL:
        return TrafficDataType.URL
    
    return TrafficDataType.SCRIPT

# The arrival - when app receives a suspicious text messages
@router.post("/v1/signals/analyze", response_model=RiskResponse)
async def analyze_signal(
    request: SignalRequest,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    auth_service: AuthService = Depends(get_auth_service),
    cache_service: InMemoryRiskCache = Depends(get_cache_service),
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(get_api_gateway_internal_link_orchestrator),
) -> RiskResponse:
    auth_service.validate_bearer_token(authorization)
    # check if it in cache -> return immediately 
    cache_key = cache_service.build_key(request).strip().lower()
    cached = cache_service.get(cache_key)
    if cached is not None:
        return cached.model_copy(update={"cacheHit": True})

    # IF data is not found in cache -> then send to background orchestrator
    lookup_payload = CacheLookupResultPayload(
        dataType=_map_source_type_to_traffic_data_type(request.sourceType),
        cacheKey=cache_key,
    )
    routing_request = CacheMissToOrchestratorAgentLangGraphRouterRequest(
        lookup=lookup_payload,
        signal=request
    )
    # TODO : Ask Huy Hoang to implement polling to update the UI warning
    background_tasks.add_task(
        internal_orchestrator.link_cache_miss_to_orchestrator_agent_langgraph_router,
        routing_request
    )

    # Return instant fallback response
    return RiskResponse(
        riskScore=0,
        explanation="Analyzing your request in the background...",
        voiceScore=0,
        textScore=0,
        entityScore=0,
        cacheHit=False
    )

# using post request here avoid revealing user data into the search bar 
# sending a post request -> compile the payload into a JSON (envelop)
# -> the mobile sent a post request to call analysis from Server