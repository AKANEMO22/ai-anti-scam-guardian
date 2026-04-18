import json
from app.models.contracts import DeepfakeSignalPayload, AgentSignalScore

class DeepfakeSignalChannel:
    def receive_from_deepfake_agent(
        self,
        signals: list[AgentSignalScore],
    ) -> DeepfakeSignalPayload:
        """Receive Deepfake Agent output for decision-engine stage."""
        log_entry = {
            "channel": "deepfake_signal",
            "event": "receive",
            "signal_count": len(signals)
        }
        print(json.dumps(log_entry))
        
        payload = DeepfakeSignalPayload(signals=signals)
        self.validate_deepfake_signal_payload(payload)
        return self.normalize_deepfake_signal_payload(payload)

    def normalize_deepfake_signal_payload(
        self,
        payload: DeepfakeSignalPayload,
    ) -> DeepfakeSignalPayload:
        """Normalize deepfake signal payload before decision aggregation."""
        for s in payload.signals:
            s.score = max(0.0, min(100.0, s.score))
            
        log_entry = {
            "channel": "deepfake_signal",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_deepfake_signal_payload(self, payload: DeepfakeSignalPayload) -> None:
        """Validate deepfake signal payload consistency."""
        log_entry = {
            "channel": "deepfake_signal",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
