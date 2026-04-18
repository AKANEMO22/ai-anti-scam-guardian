import json
from app.models.contracts import SearchQueryPayload, SearchRequest

class RagEngineLangChainSearchQueryLink:
    def forward_rag_engine_langchain_to_search_query(
        self,
        payload: SearchQueryPayload,
    ) -> SearchQueryPayload:
        """Flow: RAG Engine -> search-query."""
        log_entry = {
            "link": "rag_search_query",
            "event": "forward",
            "query": payload.query[:30]
        }
        print(json.dumps(log_entry))
        return payload

    def build_search_query_payload_from_rag_engine_langchain(
        self,
        request: SearchRequest,
    ) -> SearchQueryPayload:
        """Build Search Query payload from RAG engine stage output."""
        return SearchQueryPayload(
            query=request.query,
            sourceType=request.sourceType,
            topK=request.topK
        )

    def trace_rag_engine_langchain_to_search_query_flow(self, payload: SearchQueryPayload) -> None:
        """Emit trace point for RAG Engine -> search-query internal flow."""
        log_entry = {
            "link": "rag_search_query",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))