from app.models.contracts import AgentSignalScore, DeepfakeSignalPayload


class DeepfakeSignalChannel:
    def receive_from_deepfake_agent(self, signals: list[AgentSignalScore]) -> DeepfakeSignalPayload:
        """Receive Deepfake Agent output and package it as signal/score payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_deepfake_signal_payload(self, payload: DeepfakeSignalPayload) -> DeepfakeSignalPayload:
        """Normalize deepfake signal/score payload before sending to Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_deepfake_signal_payload(self, payload: DeepfakeSignalPayload) -> None:
        """Validate signal/score payload required by Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}
