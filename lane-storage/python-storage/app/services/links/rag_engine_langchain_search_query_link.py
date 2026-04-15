from app.models.contracts import (
    RagEngineLangChainToSearchQueryRequest,
    SearchQueryPayload,
)


class RagEngineLangChainSearchQueryLink:
    def forward_rag_engine_langchain_to_search_query(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Flow: RAG Engine LangChain -> Search Query."""
        # Build the search query payload
        payload = self.build_search_query_payload_from_rag_engine_langchain(request)
        # Emit trace for the flow
        self.trace_rag_engine_langchain_to_search_query_flow(request)
        return payload

    def build_search_query_payload_from_rag_engine_langchain(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Build Search Query payload from LangChain RAG request context."""
        return SearchQueryPayload(
            query=request.query.query,
            sourceType=request.query.sourceType,
            topK=request.query.topK,
            metadata={
                "traceId": request.traceId or "",
            }
        )

    def trace_rag_engine_langchain_to_search_query_flow(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> None:
        """Emit trace point for RAG Engine LangChain -> Search Query flow."""
        # Simple logging - in a real implementation this might send to a tracing system
        trace_id = request.traceId or "no-trace"
        print(f"[TRACE] RAG Engine LangChain -> Search Query: {request.query.query[:50]}... (trace: {trace_id})")