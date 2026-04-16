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
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Normalize search-query payload before forwarding to Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_search_query_payload(self, payload: SearchQueryPayload) -> None:
        """Validate Search Query payload required by Threat Agent flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}