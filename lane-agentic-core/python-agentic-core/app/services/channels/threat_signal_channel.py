from app.models.contracts import AgentSignalScore, ThreatSignalPayload


class ThreatSignalChannel:
    def receive_from_threat_agent(self, signals: list[AgentSignalScore]) -> ThreatSignalPayload:
        """Receive Threat Agent output and package it as signal/score payload."""
        pass

    def normalize_threat_signal_payload(self, payload: ThreatSignalPayload) -> ThreatSignalPayload:
        """Normalize threat signal/score payload before sending to Decision Engine."""
        pass

    def validate_threat_signal_payload(self, payload: ThreatSignalPayload) -> None:
        """Validate signal/score payload required by Decision & Reasoning Engine."""
        pass
