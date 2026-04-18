import json
from app.models.contracts import EntitySignalPayload, AgentSignalScore

class EntityDecisionLink:
    def forward_signal_score_to_decision_engine(
        self,
        payload: EntitySignalPayload,
    ) -> list[AgentSignalScore]:
        """Flow: Entity Agent -> Decision Engine."""
        log_entry = {
            "link": "entity_decision",
            "event": "forward",
            "signal_count": len(payload.signals)
        }
        print(json.dumps(log_entry))
        return payload.signals

    def build_decision_input_from_entity_signal(
        self,
        payload: EntitySignalPayload,
    ) -> list[AgentSignalScore]:
        """Build decision input list from Entity Agent output signals."""
        return payload.signals

    def trace_entity_to_decision_flow(self, payload: EntitySignalPayload) -> None:
        """Emit trace point for Entity Agent -> Decision Engine internal flow."""
        log_entry = {
            "link": "entity_decision",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
