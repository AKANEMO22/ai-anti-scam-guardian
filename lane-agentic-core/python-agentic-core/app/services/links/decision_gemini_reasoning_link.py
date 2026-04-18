import json
from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload


class DecisionGeminiReasoningLink:
    def forward_reasoning_context_to_gemini(
        self,
        bundle: DecisionSignalBundle,
    ) -> DecisionSignalBundle:
        """Flow: Decision Engine -> Gemini API Reasoning Engine."""
        log_entry = {
            "link": "decision_gemini_reasoning",
            "event": "forward",
            "signals": {
                "threat": len(bundle.threat_signals),
                "entity": len(bundle.entity_signals),
                "deepfake": len(bundle.deepfake_signals)
            }
        }
        print(json.dumps(log_entry))
        return bundle

    def build_gemini_reasoning_input(
        self,
        bundle: DecisionSignalBundle,
    ) -> DecisionSignalBundle:
        """Build reasoning context input for Gemini based on signal bundle."""
        return bundle

    def trace_decision_to_gemini_reasoning_flow(self, bundle: DecisionSignalBundle) -> None:
        """Emit trace point for Decision Engine -> Gemini API Reasoning Engine internal flow."""
        log_entry = {
            "link": "decision_gemini_reasoning",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))