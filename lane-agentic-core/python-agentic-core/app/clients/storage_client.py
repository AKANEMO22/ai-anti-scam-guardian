from app.models.contracts import PatternMatch, SourceType


class StorageClient:
    def fetch_pattern_matches_for_threat_agent(self, query: str, source_type: SourceType) -> list[PatternMatch]:
        """Fetch scam-pattern matches from Storage lane for Threat Agent stage."""
        pass

    def build_search_query_request_for_storage(self, query: str, source_type: SourceType, top_k: int = 5) -> dict[str, object]:
        """Build Search Query request body for Storage lane semantic retrieval endpoint."""
        pass

    def forward_search_query_to_storage_for_threat_agent(
        self,
        query: str,
        source_type: SourceType,
        top_k: int = 5,
    ) -> list[PatternMatch]:
        """Forward Search Query stage to Storage lane and return matches for Threat Agent."""
        pass

    def sync_agentic_metadata_to_storage(self, call_session_id: str | None, metadata: dict[str, str]) -> None:
        """Push agentic metadata snapshots to Storage lane for observability and replay."""
        pass
