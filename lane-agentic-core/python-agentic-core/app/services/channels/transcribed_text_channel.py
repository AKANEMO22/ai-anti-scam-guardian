from app.models.contracts import (
    GoogleSttApiToTranscribedTextRequest,
    TranscribedTextPayload,
    TranscribedTextToThreatAgentRequest,
)


class TranscribedTextChannel:
    def receive_request_from_google_stt_api(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> TranscribedTextPayload:
        """Receive Google STT API request and map it to Transcribed Text payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def receive_from_google_stt_api(self, payload: TranscribedTextPayload) -> TranscribedTextPayload:
        """Receive transcript payload emitted by Google STT API stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_transcribed_text_payload(self, payload: TranscribedTextPayload) -> TranscribedTextPayload:
        """Normalize transcribed-text payload before forwarding to Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_transcribed_text_payload(self, payload: TranscribedTextPayload) -> None:
        """Validate transcribed-text payload required for Threat Agent stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_transcribed_text_to_threat_agent_request(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextToThreatAgentRequest:
        """Build request contract for Transcribed Text -> Threat Agent edge."""
        print("mocked")
        return locals().get("mock_data", None) or {}