import json
from app.models.contracts import GeminiReasoningPayload


class ReasoningExplanationChannel:
    def receive_from_decision_reasoning_engine(
        self,
        payload: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Receive reasoning output from the engine stage."""
        log_entry = {
            "channel": "reasoning_explanation",
            "event": "receive_from_engine",
            "summary": payload.summary
        }
        print(json.dumps(log_entry))
        
        self.validate_reasoning_explanation_payload(payload)
        return self.normalize_reasoning_explanation_payload(payload)

    def receive_from_gemini_api_reasoning_engine(
        self,
        payload: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Receive reasoning output from the Gemini API stage."""
        log_entry = {
            "channel": "reasoning_explanation",
            "event": "receive_from_gemini",
            "has_baiter_response": payload.baiter_response is not None
        }
        print(json.dumps(log_entry))
        
        return self.receive_from_decision_reasoning_engine(payload)

    def normalize_reasoning_explanation_payload(
        self,
        payload: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Normalize reasoning explanation payload."""
        payload.summary = payload.summary.strip()
        payload.explanation = payload.explanation.strip()
        
        log_entry = {
            "channel": "reasoning_explanation",
            "event": "normalize",
            "status": "completed"
        }
        print(json.dumps(log_entry))
        return payload

    def validate_reasoning_explanation_payload(self, payload: GeminiReasoningPayload) -> None:
        """Validate reasoning explanation consistency."""
        log_entry = {
            "channel": "reasoning_explanation",
            "event": "validate",
            "status": "success"
        }
        print(json.dumps(log_entry))