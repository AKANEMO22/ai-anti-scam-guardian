from app.models.contracts import AgentSignalScore, EntitySignalPayload


class EntitySignalChannel:
    def receive_from_entity_agent(self, signals: list[AgentSignalScore]) -> EntitySignalPayload:
        """Receive Entity Agent output and package it as signal/score payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_entity_signal_payload(self, payload: EntitySignalPayload) -> EntitySignalPayload:
        """Normalize signal/score payload before sending to Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_entity_signal_payload(self, payload: EntitySignalPayload) -> None:
        """Validate signal/score payload required by Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}
