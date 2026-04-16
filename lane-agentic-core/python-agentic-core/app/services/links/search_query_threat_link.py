from app.models.contracts import SearchQueryToThreatAgentRequest


class SearchQueryThreatLink:
    def forward_search_query_to_threat_agent(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> None:
        """Flow: Search Query -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_threat_agent_search_query_input(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> dict[str, object]:
        """Build Threat Agent input object from Search Query stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_search_query_to_threat_agent_flow(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> None:
        """Emit trace point for Search Query -> Threat Agent flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}