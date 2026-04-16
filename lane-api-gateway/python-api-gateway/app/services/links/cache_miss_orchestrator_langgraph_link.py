from app.models.contracts import (
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    SignalRequest,
)


class CacheMissOrchestratorLangGraphLink:
    def forward_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Flow: cache miss -> Orchestrator Agent LangGraph Router."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_orchestrator_agent_langgraph_router_signal_request(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> SignalRequest:
        """Build signal request payload consumed by Orchestrator Agent LangGraph Router."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_cache_miss_to_orchestrator_agent_langgraph_router_flow(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Emit trace point for cache miss -> Orchestrator Agent LangGraph Router flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}
