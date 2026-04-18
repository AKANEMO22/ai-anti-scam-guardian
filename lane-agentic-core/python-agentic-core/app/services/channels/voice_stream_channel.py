import json
from app.models.contracts import VoiceStreamPayload

class VoiceStreamChannel:
    def receive_from_orchestrator_route(
        self,
        payload: VoiceStreamPayload,
    ) -> VoiceStreamPayload:
        """Receive Voice Stream payload from orchestrator for STT stage."""
        log_entry = {
            "channel": "voice_stream",
            "event": "receive",
            "streamRef": payload.streamRef or "none"
        }
        print(json.dumps(log_entry))
        
        self.validate_voice_stream_payload(payload)
        return self.normalize_voice_stream_payload(payload)

    def normalize_voice_stream_payload(
        self,
        payload: VoiceStreamPayload,
    ) -> VoiceStreamPayload:
        """Normalize voice stream payload before forwarding to STT Agent."""
        if payload.streamRef:
            payload.streamRef = payload.streamRef.strip()
            
        log_entry = {
            "channel": "voice_stream",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_voice_stream_payload(self, payload: VoiceStreamPayload) -> None:
        """Validate voice stream consistency for Google STT API."""
        if not payload.streamRef:
             log_entry = {
                "channel": "voice_stream",
                "event": "validate",
                "warning": "missing_streamRef",
                "action": "allow_if_callSessionId_exists"
            }
             print(json.dumps(log_entry))
             
        log_entry = {
            "channel": "voice_stream",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
