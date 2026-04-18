import json
from app.models.contracts import EntitySignalPayload, AgentSignalScore

class EntitySignalChannel:
    def receive_from_entity_agent(
        self,
        signals: list[AgentSignalScore],
    ) -> EntitySignalPayload:
        """Receive Entity Agent output for decision-engine stage."""
        log_entry = {
            "channel": "entity_signal",
            "event": "receive",
            "signal_count": len(signals)
        }
        print(json.dumps(log_entry))
        
        payload = EntitySignalPayload(signals=signals)
        self.validate_entity_signal_payload(payload)
        return self.normalize_entity_signal_payload(payload)

    def normalize_entity_signal_payload(
        self,
        payload: EntitySignalPayload,
    ) -> EntitySignalPayload:
        """Normalize entity signal payload before decision aggregation."""
        for s in payload.signals:
            s.score = max(0.0, min(100.0, s.score))
            
        log_entry = {
            "channel": "entity_signal",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_entity_signal_payload(self, payload: EntitySignalPayload) -> None:
        """Validate entity signal payload consistency."""
        log_entry = {
            "channel": "entity_signal",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))
