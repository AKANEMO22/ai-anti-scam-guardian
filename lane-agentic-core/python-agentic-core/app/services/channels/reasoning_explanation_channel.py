from app.models.contracts import GeminiReasoningPayload


class ReasoningExplanationChannel:
    def receive_from_decision_reasoning_engine(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Receive reasoning/explanation payload emitted by Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def receive_from_gemini_api_reasoning_engine(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Receive reasoning/explanation payload emitted by Gemini API Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_reasoning_explanation_payload(self, payload: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Normalize reasoning/explanation payload before forwarding between engines."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_reasoning_explanation_payload(self, payload: GeminiReasoningPayload) -> None:
        """Validate reasoning/explanation payload structure for internal exchange."""
        print("mocked")
        return locals().get("mock_data", None) or {}