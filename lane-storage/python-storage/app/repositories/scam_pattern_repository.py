class ScamPatternRepository:
    def list_active_pattern_ids(self) -> list[str]:
        """List active scam-pattern IDs that should be linked into vector index."""
        pass

    def list_active_patterns(self) -> list[str]:
        """List active scam-pattern texts used by RAG context preparation."""
        pass

    def get_patterns_by_ids(self, pattern_ids: list[str]) -> list[str]:
        """Resolve scam-pattern texts from pattern IDs returned by internal links."""
        pass
