from app.models.contracts import (
    GoogleSttApiToTranscribedTextRequest,
    TranscribedTextPayload,
)


class GoogleSttTranscribedTextLink:
    def forward_google_stt_api_to_transcribed_text(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> TranscribedTextPayload:
        """Flow: Google STT API -> Transcribed Text."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_transcribed_text_payload_from_google_stt_api(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> TranscribedTextPayload:
        """Build Transcribed Text payload from Google STT API stage request."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_google_stt_api_to_transcribed_text_flow(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> None:
        """Emit trace point for Google STT API -> Transcribed Text flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}