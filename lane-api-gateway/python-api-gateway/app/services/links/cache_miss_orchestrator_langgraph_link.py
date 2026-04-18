import json
from app.models.contracts import (
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    SignalRequest,
)


class CacheMissOrchestratorLangGraphLink:
    def forward_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> SignalRequest:
        """Flow: cache-miss -> Orchestrator Agent LangGraph Router."""
        log_entry = {
            "link": "gateway_cache_orchestrator",
            "event": "forward",
            "cacheKey": request.lookup.cacheKey,
            "sourceType": request.signal.sourceType
        }
        print(json.dumps(log_entry))
        
        return self.build_orchestrator_agent_langgraph_router_input(request)

    def build_orchestrator_agent_langgraph_router_input(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> SignalRequest:
        """Build LangGraph router input from cache-miss and original signal."""
        return request.signal

    def trace_cache_miss_to_orchestrator_agent_langgraph_router_flow(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Emit trace point for cache-miss -> Orchestrator Agent LangGraph Router internal flow."""
        log_entry = {
            "link": "gateway_cache_orchestrator",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
