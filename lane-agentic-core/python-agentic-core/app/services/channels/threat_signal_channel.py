import json
from app.models.contracts import ThreatSignalPayload, AgentSignalScore

class ThreatSignalChannel:
    def receive_from_threat_agent(
        self,
        signals: list[AgentSignalScore],
    ) -> ThreatSignalPayload:
        """Receive Threat Agent output for decision-engine stage."""
        log_entry = {
            "channel": "threat_signal",
            "event": "receive",
            "signal_count": len(signals)
        }
        print(json.dumps(log_entry))
        
        payload = ThreatSignalPayload(signals=signals)
        self.validate_threat_signal_payload(payload)
        return self.normalize_threat_signal_payload(payload)

    def normalize_threat_signal_payload(
        self,
        payload: ThreatSignalPayload,
    ) -> ThreatSignalPayload:
        """Normalize threat signal payload before decision aggregation."""
        # Ensure scores are within 0-100 range and signal names are clean
        for s in payload.signals:
            s.score = max(0.0, min(100.0, s.score))
            s.signal_name = s.signal_name.strip().lower()
            
        log_entry = {
            "channel": "threat_signal",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_threat_signal_payload(self, payload: ThreatSignalPayload) -> None:
        """Validate threat signal payload consistency."""
        if not payload.signals:
            log_entry = {
                "channel": "threat_signal",
                "event": "validate",
                "warning": "empty_signals",
                "action": "fallback_to_default"
            }
            print(json.dumps(log_entry))
            # Fallback happens by using empty list in Pydantic model usually,
            # but we log it here as requested.
        
        log_entry = {
            "channel": "threat_signal",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
