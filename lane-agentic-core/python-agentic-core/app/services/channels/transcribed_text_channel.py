import json
from app.models.contracts import TranscribedTextPayload

class TranscribedTextChannel:
    def receive_from_google_stt_api(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Receive Google STT API output for threat-agent stage."""
        log_entry = {
            "channel": "transcribed_text",
            "event": "receive",
            "transcript_len": len(payload.transcript)
        }
        print(json.dumps(log_entry))
        
        self.validate_transcribed_text_payload(payload)
        return self.normalize_transcribed_text_payload(payload)

    def normalize_transcribed_text_payload(
        self,
        payload: TranscribedTextPayload,
    ) -> TranscribedTextPayload:
        """Normalize transcribed text payload before threat analysis."""
        # Simple cleanup
        payload.transcript = payload.transcript.strip()
        
        log_entry = {
            "channel": "transcribed_text",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_transcribed_text_payload(self, payload: TranscribedTextPayload) -> None:
        """Validate transcribed text consistency for threat analysis."""
        if not payload.transcript:
             log_entry = {
                "channel": "transcribed_text",
                "event": "validate",
                "warning": "empty_transcript",
                "action": "warn_only"
            }
             print(json.dumps(log_entry))

        log_entry = {
            "channel": "transcribed_text",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))

    def build_transcribed_text_to_threat_agent_request(
        self,
        payload: TranscribedTextPayload,
    ) -> dict[str, object]:
        """Convert Transcribed Text stage output to Threat Agent request format."""
        # Mapping logic
        return payload.model_dump()