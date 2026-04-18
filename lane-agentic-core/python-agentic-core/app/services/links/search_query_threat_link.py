import json
from app.models.contracts import SearchQueryPayload


class SearchQueryThreatLink:
    def forward_search_query_to_threat_agent(
        self,
        payload: SearchQueryPayload,
    ) -> SearchQueryPayload:
        """Flow: Search Query -> Threat Agent."""
        log_entry = {
            "link": "search_query_threat",
            "event": "forward",
            "query_snippet": payload.query[:20]
        }
        print(json.dumps(log_entry))
        return payload

    def build_threat_agent_search_query_input(
        self,
        payload: SearchQueryPayload,
    ) -> dict[str, object]:
        """Build Threat Agent input from Search Query payload."""
        return payload.model_dump()

    def trace_search_query_to_threat_agent_flow(self, payload: SearchQueryPayload) -> None:
        """Emit trace point for Search Query -> Threat Agent internal flow."""
        log_entry = {
            "link": "search_query_threat",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))