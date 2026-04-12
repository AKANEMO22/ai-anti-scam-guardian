from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload


class GeminiApiReasoningEngine:
    def request_reasoning_from_decision_signals(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Arrow: Decision Engine -> Gemini API Reasoning Engine."""
        pass

    def return_reasoning_to_decision_engine(self, reasoning: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Arrow: Gemini API Reasoning Engine -> Decision Engine."""
        pass
