import json
import os
from typing import Optional

from app.models.contracts import (
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    SignalRequest,
)

class CacheMissOrchestratorLangGraphLink:
    def __init__(self, project_id: Optional[str] = None):
        self._topic_id = os.getenv("PUBSUB_LANGGRAPH_ROUTER_TOPIC", "agentic-core-input-topic")

    async def forward_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Flow: cache miss -> Orchestrator Agent LangGraph Router."""
        signal_request = self.build_orchestrator_agent_langgraph_router_signal_request(request)
        
        self.trace_cache_miss_to_orchestrator_agent_langgraph_router_flow(request)

        # Convert Pydantic model to dict, then to JSON string
        payload_json = json.dumps(signal_request.model_dump())
        
        # Step back: Instead of triggering a real GCP Pub/Sub publisher,
        # we log the event as a simulated message drop.
        print(f"[Mock Publisher] Simulating dropping message into topic: {self._topic_id}")
        print(f"[Mock Publisher] Payload: {payload_json}")

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
