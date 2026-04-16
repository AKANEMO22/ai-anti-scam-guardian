from app.models.contracts import AgentSignalScore, ThreatSignalPayload


class ThreatSignalChannel:
    def receive_from_threat_agent(self, signals: list[AgentSignalScore]) -> ThreatSignalPayload:
        """Receive Threat Agent output and package it as signal/score payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_threat_signal_payload(self, payload: ThreatSignalPayload) -> ThreatSignalPayload:
        """Normalize threat signal/score payload before sending to Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_threat_signal_payload(self, payload: ThreatSignalPayload) -> None:
        """Validate signal/score payload required by Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}
