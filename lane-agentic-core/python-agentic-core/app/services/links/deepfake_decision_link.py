import json
from app.models.contracts import DeepfakeSignalPayload, AgentSignalScore


class DeepfakeDecisionLink:
    def forward_signal_score_to_decision_engine(
        self,
        payload: DeepfakeSignalPayload,
    ) -> list[AgentSignalScore]:
        """Flow: Deepfake Agent -> Decision Engine."""
        log_entry = {
            "link": "deepfake_decision",
            "event": "forward",
            "signal_count": len(payload.signals)
        }
        print(json.dumps(log_entry))
        return payload.signals

    def build_decision_input_from_deepfake_signal(
        self,
        payload: DeepfakeSignalPayload,
    ) -> list[AgentSignalScore]:
        """Build decision input list from Deepfake Agent output signals."""
        return payload.signals

    def trace_deepfake_to_decision_flow(self, payload: DeepfakeSignalPayload) -> None:
        """Emit trace point for Deepfake Agent -> Decision Engine internal flow."""
        log_entry = {
            "link": "deepfake_decision",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
