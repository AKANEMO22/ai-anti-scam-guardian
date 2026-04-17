from typing import Optional
import httpx
import os
from app.models.contracts import PatternMatch, SourceType

class StorageClient:
    def __init__(self):
        self.base_url = os.environ.get("STORAGE_BASE_URL", "http://localhost:8102")

    async def fetch_pattern_matches_for_threat_agent(self, query: str, source_type: SourceType, top_k: int = 5) -> list[PatternMatch]:
        """Fetch scam-pattern matches from Storage lane for Threat Agent stage."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/storage/search",
                    json={
                        "query": query,
                        "sourceType": source_type.value,
                        "topK": top_k
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    return [PatternMatch(**m) for m in matches]
        except Exception as e:
            print(f"Error fetching from storage: {e}")
        return []

    def build_search_query_request_for_storage(self, query: str, source_type: SourceType, top_k: int = 5) -> dict[str, object]:
        return {"query": query, "sourceType": source_type.value, "topK": top_k}

    async def forward_search_query_to_storage_for_threat_agent(
        self,
        query: str,
        source_type: SourceType,
        top_k: int = 5,
    ) -> list[PatternMatch]:
        """Forward Search Query stage to Storage lane and return matches for Threat Agent."""
        return await self.fetch_pattern_matches_for_threat_agent(query, source_type, top_k)

    def sync_agentic_metadata_to_storage(self, call_session_id: Optional[str], metadata: dict[str, str]) -> None:
        """Push agentic metadata snapshots to Storage lane (Fire and forget)."""
        print("mocked")
        return locals().get("mock_data", None) or {}
