from app.models.contracts import GeminiReasoningPayload


class GeminiDecisionReasoningLink:
    def forward_reasoning_explanation_to_decision(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Flow: Gemini API Reasoning Engine -> Decision & Reasoning Engine."""
        pass

    def build_decision_reasoning_input(self, payload: GeminiReasoningPayload) -> dict[str, object]:
        """Build Decision Engine reasoning input object from Gemini payload."""
        pass

    def trace_gemini_to_decision_reasoning_flow(self, payload: GeminiReasoningPayload) -> None:
        """Emit trace point for Gemini->Decision reasoning/explanation internal flow."""
        pass