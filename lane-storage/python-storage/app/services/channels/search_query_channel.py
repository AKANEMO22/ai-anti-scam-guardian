from app.models.contracts import (
    RagEngineLangChainToSearchQueryRequest,
    SearchQueryPayload,
)


class SearchQueryChannel:
    def receive_from_rag_engine_langchain(
        self,
        request: RagEngineLangChainToSearchQueryRequest,
    ) -> SearchQueryPayload:
        """Receive RAG Engine LangChain output and expose Search Query stage payload."""
        pass

    def normalize_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Normalize search-query payload before forwarding to Threat Agent."""
        pass

    def validate_search_query_payload(self, payload: SearchQueryPayload) -> None:
        """Validate Search Query payload required by Threat Agent flow."""
        pass