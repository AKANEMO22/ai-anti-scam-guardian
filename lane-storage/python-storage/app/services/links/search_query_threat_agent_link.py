from app.models.contracts import SearchQueryPayload, SearchQueryToThreatAgentRequest


class SearchQueryThreatAgentLink:
    def forward_search_query_to_threat_agent(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> SearchQueryPayload:
        """Flow: Search Query -> Threat Agent."""
        # Build the threat agent request and return the search query payload
        threat_request = self.build_threat_agent_search_query_request(request)
        self.trace_search_query_to_threat_agent_flow(request)
        return request.payload

    def build_threat_agent_search_query_request(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> dict[str, object]:
        """Build Threat Agent handoff request from Search Query payload."""
        return {
            "query": request.payload.query,
            "sourceType": request.payload.sourceType,
            "topK": request.payload.topK,
            "metadata": request.payload.metadata,
        }

    def trace_search_query_to_threat_agent_flow(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> None:
        """Emit trace point for Search Query -> Threat Agent flow."""
        # TODO: Implement proper tracing with logging or monitoring
        print(f"Tracing search query to threat agent flow: {request.payload.query}")