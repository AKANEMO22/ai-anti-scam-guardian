import json
from app.models.contracts import VoiceStreamPayload, TranscribedTextPayload

class GoogleSttApiTranscribedTextLink:
    def forward_google_stt_api_to_transcribed_text(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Flow: Google STT API -> Transcribed Text."""
        log_entry = {
            "link": "google_stt_transcribed_text",
            "event": "forward",
            "callSessionId": payload.callSessionId or "unknown"
        }
        print(json.dumps(log_entry))
        return payload

    def build_transcribed_text_payload_from_google_stt_api(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Build Transcribed Text payload from Google STT API output."""
        # Simple passthrough in this stage, but could include filtering
        return payload

    def trace_google_stt_api_to_transcribed_text_flow(self, payload: TranscribedTextPayload) -> None:
        """Emit trace point for Google STT API -> Transcribed Text internal flow observability."""
        log_entry = {
            "link": "google_stt_transcribed_text",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))