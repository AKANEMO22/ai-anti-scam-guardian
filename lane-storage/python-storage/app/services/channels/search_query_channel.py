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
        # Transform the RAG engine request into a search query payload
        return SearchQueryPayload(
            query=request.query.query,
            sourceType=request.query.sourceType,
            topK=request.query.topK,
            metadata={
                "traceId": request.traceId or "",
                **request.query.metadata
            }
        )

    def normalize_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Normalize search-query payload before forwarding to Threat Agent."""
        # Create normalized copies
        normalized_metadata = payload.metadata.copy() if payload.metadata else {}

        # Normalize string values
        clean_query = payload.query.strip() if payload.query else ""
        clean_source_type = payload.sourceType.strip() if payload.sourceType else ""

        # Normalize metadata strings
        for key, value in normalized_metadata.items():
            if isinstance(value, str):
                normalized_metadata[key] = value.strip()

        # Ensure topK is within valid range
        normalized_top_k = max(1, min(20, payload.topK))

        return SearchQueryPayload(
            query=clean_query,
            sourceType=clean_source_type,
            topK=normalized_top_k,
            metadata=normalized_metadata,
        )

    def validate_search_query_payload(self, payload: SearchQueryPayload) -> None:
        """Validate Search Query payload required by Threat Agent flow."""
        # Validate required fields
        if not payload.query or not payload.query.strip():
            raise ValueError("query is required and cannot be empty")

        if not payload.sourceType or not payload.sourceType.strip():
            raise ValueError("sourceType is required and cannot be empty")

        # Validate topK range
        if payload.topK < 1 or payload.topK > 20:
            raise ValueError("topK must be between 1 and 20")

        # Validate metadata is a dict
        if payload.metadata is not None and not isinstance(payload.metadata, dict):
            raise ValueError("metadata must be a dictionary")