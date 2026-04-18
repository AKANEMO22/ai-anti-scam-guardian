import json
from app.models.contracts import GeminiReasoningPayload


class GeminiDecisionReasoningLink:
    def forward_reasoning_explanation_to_decision(
        self,
        payload: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Flow: Gemini API Reasoning Engine -> Decision Engine."""
        log_entry = {
            "link": "gemini_decision_reasoning",
            "event": "forward",
            "summary": payload.summary
        }
        print(json.dumps(log_entry))
        return payload

    def build_decision_reasoning_input(
        self,
        payload: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Build decision input from Gemini reasoning output."""
        return payload

    def trace_gemini_to_decision_reasoning_flow(self, payload: GeminiReasoningPayload) -> None:
        """Emit trace point for Gemini API Reasoning Engine -> Decision Engine internal flow."""
        log_entry = {
            "link": "gemini_decision_reasoning",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))