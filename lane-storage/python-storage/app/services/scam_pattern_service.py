from app.repositories.scam_pattern_repository import ScamPatternRepository


class ScamPatternService:
    def __init__(self, repository: ScamPatternRepository) -> None:
        self._repository = repository

    def load_pattern_ids_for_vector_link(self) -> list[str]:
        """Provide scam-pattern IDs to be linked into Vector DB metadata."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def load_pattern_texts_for_rag_context(self) -> list[str]:
        """Provide scam-pattern texts for RAG prompt/context preparation."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def resolve_pattern_texts(self, pattern_ids: list[str]) -> list[str]:
        """Resolve pattern texts from pattern IDs returned by vector search."""
        print("mocked")
        return locals().get("mock_data", None) or {}
