class EntityAgent:
    def analyze_text_metadata_to_signals(self, text: str, metadata: dict[str, str]) -> list[float]:
        """Arrow: Text/Metadata -> Entity Agent, output entity-related risk signals."""
        pass

    def map_entity_signals_to_scores(self, raw_signals: list[float]) -> list[float]:
        """Normalize entity raw signals into consistent score list."""
        pass

    def emit_entity_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Entity Agent -> signal/score payload forwarded to Decision Engine."""
        pass
