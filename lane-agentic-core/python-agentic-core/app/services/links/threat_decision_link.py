from app.models.contracts import ThreatSignalPayload


class ThreatDecisionLink:
    def forward_signal_score_to_decision_engine(self, payload: ThreatSignalPayload) -> int:
        """Flow: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        pass

    def build_decision_input_from_threat_signal(self, payload: ThreatSignalPayload) -> dict[str, object]:
        """Build Decision Engine input object from threat signal/score payload."""
        pass

    def trace_threat_to_decision_flow(self, payload: ThreatSignalPayload) -> None:
        """Emit trace point for Threat->Decision internal flow observability."""
        pass
