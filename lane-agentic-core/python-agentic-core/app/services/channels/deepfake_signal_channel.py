from app.models.contracts import AgentSignalScore, DeepfakeSignalPayload


class DeepfakeSignalChannel:
    def receive_from_deepfake_agent(self, signals: list[AgentSignalScore]) -> DeepfakeSignalPayload:
        """Receive Deepfake Agent output and package it as signal/score payload."""
        pass

    def normalize_deepfake_signal_payload(self, payload: DeepfakeSignalPayload) -> DeepfakeSignalPayload:
        """Normalize deepfake signal/score payload before sending to Decision Engine."""
        pass

    def validate_deepfake_signal_payload(self, payload: DeepfakeSignalPayload) -> None:
        """Validate signal/score payload required by Decision & Reasoning Engine."""
        pass
