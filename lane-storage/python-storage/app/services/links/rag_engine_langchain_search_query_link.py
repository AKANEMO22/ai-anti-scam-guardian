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
        pass

    def build_search_query_payload_from_rag_engine_langchain(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Build Search Query payload from LangChain RAG request context."""
        pass

    def trace_rag_engine_langchain_to_search_query_flow(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> None:
        """Emit trace point for RAG Engine LangChain -> Search Query flow."""
        pass