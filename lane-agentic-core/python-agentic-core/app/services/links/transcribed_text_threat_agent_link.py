from app.models.contracts import (
    TranscribedTextPayload,
    TranscribedTextToThreatAgentRequest,
)


class TranscribedTextThreatAgentLink:
    def forward_transcribed_text_to_threat_agent(
        self,
        request: TranscribedTextToThreatAgentRequest,
    ) -> None:
        """Flow: Transcribed Text -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_threat_agent_request_from_transcribed_text(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextToThreatAgentRequest:
        """Build Threat Agent request contract from Transcribed Text payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_transcribed_text_to_threat_agent_flow(
        self,
        request: TranscribedTextToThreatAgentRequest,
    ) -> None:
        """Emit trace point for Transcribed Text -> Threat Agent flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}