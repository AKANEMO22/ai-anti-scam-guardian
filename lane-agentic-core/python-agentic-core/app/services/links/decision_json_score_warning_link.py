from app.models.contracts import (
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    JsonScoreWarningPayload,
)


class DecisionJsonScoreWarningLink:
    def forward_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Flow: Decision & Reasoning Engine -> JSON score + warning."""
        pass

    def build_json_score_warning_payload(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Build JSON score + warning payload from decision output fields."""
        pass

    def trace_decision_and_reasoning_engine_to_json_score_warning_flow(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> None:
        """Emit trace point for Decision & Reasoning Engine -> JSON score + warning flow."""
        pass
