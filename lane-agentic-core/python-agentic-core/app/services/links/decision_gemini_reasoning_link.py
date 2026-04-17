from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload


class DecisionGeminiReasoningLink:
    def forward_reasoning_context_to_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Flow: Decision & Reasoning Engine -> Gemini API Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_gemini_reasoning_input(self, bundle: DecisionSignalBundle) -> dict[str, object]:
        """Build Gemini reasoning request payload from Decision signal bundle."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_decision_to_gemini_reasoning_flow(self, bundle: DecisionSignalBundle) -> None:
        """Emit trace point for Decision->Gemini reasoning/explanation internal flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}