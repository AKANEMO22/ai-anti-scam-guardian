import json
from app.models.contracts import SearchQueryPayload

class SearchQueryThreatAgentLink:
    def forward_search_query_to_threat_agent(
        self,
        payload: SearchQueryPayload,
    ) -> SearchQueryPayload:
        """Flow: search-query -> Threat Agent."""
        log_entry = {
            "link": "search_query_threat_agent",
            "event": "forward",
            "query_len": len(payload.query)
        }
        print(json.dumps(log_entry))
        return payload

    def build_threat_agent_request_from_search_query(
        self,
        payload: SearchQueryPayload,
    ) -> dict[str, object]:
        """Build Threat Agent request from search query payload."""
        return payload.model_dump()

    def trace_search_query_to_threat_agent_flow(self, payload: SearchQueryPayload) -> None:
        """Emit trace point for search-query -> Threat Agent internal flow."""
        log_entry = {
            "link": "search_query_threat_agent",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))