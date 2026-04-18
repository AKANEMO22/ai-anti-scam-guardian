import json
from app.models.contracts import RawAudioPayload

class RawAudioChannel:
    def receive_from_orchestrator_route(
        self,
        payload: RawAudioPayload,
    ) -> RawAudioPayload:
        """Receive Raw Audio reference from orchestrator for deepfake-agent stage."""
        log_entry = {
            "channel": "raw_audio",
            "event": "receive",
            "callSessionId": payload.callSessionId or "unknown"
        }
        print(json.dumps(log_entry))
        
        self.validate_raw_audio_payload(payload)
        return self.normalize_raw_audio_reference(payload)

    def normalize_raw_audio_reference(
        self,
        payload: RawAudioPayload,
    ) -> RawAudioPayload:
        """Normalize raw audio reference details before deepfake analysis."""
        # Simple normalization: ensure path is stripped
        if payload.rawAudioRef:
            payload.rawAudioRef = payload.rawAudioRef.strip()
            
        log_entry = {
            "channel": "raw_audio",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_raw_audio_payload(self, payload: RawAudioPayload) -> None:
        """Validate raw audio payload for deepfake detection stage."""
        if not payload.callSessionId:
            log_entry = {
                "channel": "raw_audio",
                "event": "validate",
                "warning": "missing_callSessionId",
                "action": "use_default_unknown"
            }
            print(json.dumps(log_entry))
            
        log_entry = {
            "channel": "raw_audio",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
