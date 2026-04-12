from app.models.contracts import JsonScoreWarningPayload


class JsonScoreWarningChannel:
    def receive_from_decision_and_reasoning_engine(
        self,
        payload: JsonScoreWarningPayload,
    ) -> JsonScoreWarningPayload:
        """Receive JSON score + warning payload emitted by Decision & Reasoning Engine."""
        pass

    def normalize_json_score_warning_payload(
        self,
        payload: JsonScoreWarningPayload,
    ) -> JsonScoreWarningPayload:
        """Normalize JSON score + warning payload before Cloud Run forwarding stage."""
        pass

    def validate_json_score_warning_payload(self, payload: JsonScoreWarningPayload) -> None:
        """Validate JSON score + warning payload structure for internal routing."""
        pass
