from app.models.contracts import GeminiReasoningPayload


class ReasoningExplanationChannel:
    def receive_from_decision_reasoning_engine(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Receive reasoning/explanation payload emitted by Decision & Reasoning Engine."""
        pass

    def receive_from_gemini_api_reasoning_engine(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Receive reasoning/explanation payload emitted by Gemini API Reasoning Engine."""
        pass

    def normalize_reasoning_explanation_payload(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Normalize reasoning/explanation payload before forwarding between engines."""
        pass

    def validate_reasoning_explanation_payload(self, payload: GeminiReasoningPayload) -> None:
        """Validate reasoning/explanation payload structure for internal exchange."""
        pass