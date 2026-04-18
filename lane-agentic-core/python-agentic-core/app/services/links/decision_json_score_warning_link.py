import json
from app.models.contracts import (
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    JsonScoreWarningPayload,
)


class DecisionJsonScoreWarningLink:
    def forward_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Flow: Decision Engine -> JSON score + warning."""
        log_entry = {
            "link": "decision_json_score_warning",
            "event": "forward",
            "riskScore": request.score
        }
        print(json.dumps(log_entry))
        
        return self.build_json_score_warning_payload(request)

    def build_json_score_warning_payload(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Build JSON score + warning output payload."""
        return JsonScoreWarningPayload(
            riskScore=request.score,
            warning=request.warning,
            explanation=request.explanation,
            metadata=request.metadata
        )

    def trace_decision_and_reasoning_engine_to_json_score_warning_flow(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> None:
        """Emit trace point for Decision Engine -> JSON score warning flow."""
        log_entry = {
            "link": "decision_json_score_warning",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))
