import json
from app.models.contracts import ThreatSignalPayload, AgentSignalScore


class ThreatDecisionLink:
    def forward_signal_score_to_decision_engine(
        self,
        payload: ThreatSignalPayload,
    ) -> list[AgentSignalScore]:
        """Flow: Threat Agent -> Decision Engine."""
        log_entry = {
            "link": "threat_decision",
            "event": "forward",
            "signal_count": len(payload.signals)
        }
        print(json.dumps(log_entry))
        return payload.signals

    def build_decision_input_from_threat_signal(
        self,
        payload: ThreatSignalPayload,
    ) -> list[AgentSignalScore]:
        """Build decision input list from Threat Agent output signals."""
        return payload.signals

    def trace_threat_to_decision_flow(self, payload: ThreatSignalPayload) -> None:
        """Emit trace point for Threat Agent -> Decision Engine internal flow."""
        log_entry = {
            "link": "threat_decision",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
