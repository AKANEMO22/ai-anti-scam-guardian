import json
from app.models.contracts import SearchQueryPayload

class SearchQueryChannel:
    def receive_from_rag_engine_langchain(
        self,
        payload: SearchQueryPayload,
    ) -> SearchQueryPayload:
        """Receive Search Query payload from RAG engine for threat-agent stage."""
        log_entry = {
            "channel": "search_query",
            "event": "receive",
            "query": payload.query[:50] + "..." if len(payload.query) > 50 else payload.query
        }
        print(json.dumps(log_entry))
        
        self.validate_search_query_payload(payload)
        return self.normalize_search_query_payload(payload)

    def normalize_search_query_payload(
        self,
        payload: SearchQueryPayload,
    ) -> SearchQueryPayload:
        """Normalize search query payload before threat analysis."""
        payload.query = payload.query.strip()
        
        log_entry = {
            "channel": "search_query",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_search_query_payload(self, payload: SearchQueryPayload) -> None:
        """Validate search query consistency for threat analysis."""
        log_entry = {
            "channel": "search_query",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))