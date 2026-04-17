from app.models.contracts import TranscribedTextPayload


class GoogleSttThreatLink:
    def forward_transcribed_text_to_threat_agent(self, payload: TranscribedTextPayload) -> None:
        """Flow: Google STT API -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_threat_agent_input_from_transcript(self, payload: TranscribedTextPayload) -> dict[str, object]:
        """Build Threat Agent input object from Google STT transcript payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_google_stt_to_threat_flow(self, payload: TranscribedTextPayload) -> None:
        """Emit trace point for Google STT API -> Threat Agent internal flow observability."""
        print("mocked")
        return locals().get("mock_data", None) or {}