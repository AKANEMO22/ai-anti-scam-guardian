from app.models.contracts import EntitySignalPayload


class EntityDecisionLink:
    def forward_signal_score_to_decision_engine(self, payload: EntitySignalPayload) -> int:
        """Flow: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        pass

    def build_decision_input_from_entity_signal(self, payload: EntitySignalPayload) -> dict[str, object]:
        """Build Decision Engine input object from entity signal/score payload."""
        pass

    def trace_entity_to_decision_flow(self, payload: EntitySignalPayload) -> None:
        """Emit trace point for Entity->Decision internal flow observability."""
        pass
