from app.models.contracts import SearchQueryPayload, SearchQueryToThreatAgentRequest


class SearchQueryChannel:
    def receive_from_rag_engine_langchain(
        self,
        request: SearchQueryToThreatAgentRequest,
    ) -> SearchQueryPayload:
        """Receive Search Query payload produced from LangChain RAG stage."""
        pass

    def normalize_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Normalize Search Query payload before Threat Agent stage."""
        pass

    def validate_search_query_payload(self, payload: SearchQueryPayload) -> None:
        """Validate Search Query payload required by Threat Agent."""
        pass