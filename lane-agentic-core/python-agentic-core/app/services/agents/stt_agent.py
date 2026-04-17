from app.models.contracts import TranscribedTextPayload


class SttAgent:
    def transcribe_voice_stream(self, call_session_id: str | None, stream_ref: str | None) -> str:
        """Arrow: Voice Stream -> Google STT API, output transcribed text."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def emit_transcribed_text_from_google_stt_api(
        self,
        call_session_id: str | None,
        transcript: str,
        metadata: dict[str, str],
    ) -> TranscribedTextPayload:
        """Arrow: Google STT API -> Transcribed Text stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def enrich_transcript_metadata(self, transcript: str) -> dict[str, str]:
        """Prepare transcript metadata that will be forwarded to Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def emit_transcribed_text_for_threat_agent(
        self,
        call_session_id: str | None,
        transcript: str,
        metadata: dict[str, str],
    ) -> TranscribedTextPayload:
        """Arrow: Google STT API -> Threat Agent, package transcript payload for Threat stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}
