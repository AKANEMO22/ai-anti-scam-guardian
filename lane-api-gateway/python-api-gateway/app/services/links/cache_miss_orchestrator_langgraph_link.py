import json
import os
from typing import Optional

from app.clients.agentic_core_client import AgenticCoreClient
from app.services.cache_service import InMemoryRiskCache
from app.models.contracts import (
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    SignalRequest,
    CloudRunToCacheRequest,
    CloudRunMicroserviceResultPayload,
    CloudRunMicroserviceTarget
)

class CacheMissOrchestratorLangGraphLink:
    def __init__(self, core_client: AgenticCoreClient, cache_service: InMemoryRiskCache):
        self._core_client = core_client
        self._cache_service = cache_service

    async def forward_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Flow: cache miss -> Orchestrator Agent LangGraph Router."""
        signal_request = self.build_orchestrator_agent_langgraph_router_signal_request(request)
        self.trace_cache_miss_to_orchestrator_agent_langgraph_router_flow(request)

        # Direct REST AI call inside a FastAPI BackgroundTask!
        try:
            print(f"[Async Worker] Calling Agentic Core for {request.lookup.cacheKey}...")
            risk_response = await self._core_client.analyze_signal(signal_request)
            print(f"[Async Worker] AI returned Risk Score: {risk_response.riskScore}")
            
            # Immediately cache the background result so future identical requests hit the Fast Path
            self._cache_service.set(request.lookup.cacheKey, risk_response)
            
            cache_request = CloudRunToCacheRequest(
                result=CloudRunMicroserviceResultPayload(
                    microservice=CloudRunMicroserviceTarget.AGENTIC_CORE,
                    dataType=request.lookup.dataType,
                    metadata=request.lookup.metadata,
                    response=risk_response.model_dump()
                ),
                cacheLayer=request.lookup.cacheLayer,
                cacheKey=request.lookup.cacheKey
            )
            self._cache_service.write_cloud_run_result_to_cache_layer(cache_request)
            print(f"[Async Worker] Successfully cached result for {request.lookup.cacheKey}")
        
        except Exception as e:
            print(f"[Async Worker] Pipeline failed: {str(e)}")

    def build_orchestrator_agent_langgraph_router_signal_request(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> SignalRequest:
        """Build signal request payload consumed by Orchestrator Agent LangGraph Router."""
        # The Orchestrator just needs the original user signal request, we pass it forward
        return request.signal

    def trace_cache_miss_to_orchestrator_agent_langgraph_router_flow(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Emit trace point for cache miss -> Orchestrator Agent LangGraph Router flow."""
        print(f"[Trace] Cache Miss Flow Triggered for callSessionId: {request.signal.callSessionId}")
