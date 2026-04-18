import json
from app.models.contracts import TranscribedTextPayload


class GoogleSttThreatLink:
    def forward_transcribed_text_to_threat_agent(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Flow: Google STT API -> Threat Agent."""
        log_entry = {
            "link": "google_stt_threat",
            "event": "forward",
            "callSessionId": payload.callSessionId or "unknown"
        }
        print(json.dumps(log_entry))
        return payload

    def build_threat_agent_input_from_transcript(
        self,
        payload: TranscribedTextPayload,
    ) -> dict[str, object]:
        """Build Threat Agent input object from Google STT transcript payload."""
        log_entry = {
            "link": "google_stt_threat",
            "event": "build_input",
            "status": "success"
        }
        print(json.dumps(log_entry))
        return payload.model_dump()

    def trace_google_stt_to_threat_flow(self, payload: TranscribedTextPayload) -> None:
        """Emit trace point for Google STT API -> Threat Agent internal flow observability."""
        log_entry = {
            "link": "google_stt_threat",
            "event": "trace",
            "status": "active"
        }
        print(json.dumps(log_entry))