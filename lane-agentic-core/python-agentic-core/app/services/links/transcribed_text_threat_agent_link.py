import json
from app.models.contracts import TranscribedTextPayload

class TranscribedTextThreatAgentLink:
    def forward_transcribed_text_to_threat_agent(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Flow: Transcribed Text -> Threat Agent."""
        log_entry = {
            "link": "transcribed_text_threat",
            "event": "forward",
            "callSessionId": payload.callSessionId or "unknown"
        }
        print(json.dumps(log_entry))
        return payload

    def build_threat_agent_request_from_transcribed_text(
        self,
        payload: TranscribedTextPayload,
    ) -> dict[str, object]:
        """Build Threat Agent request from transcribed text payload."""
        return payload.model_dump()

    def trace_transcribed_text_to_threat_agent_flow(self, payload: TranscribedTextPayload) -> None:
        """Emit trace point for Transcribed Text -> Threat Agent internal flow."""
        log_entry = {
            "link": "transcribed_text_threat",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))