from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload, JsonScoreWarningPayload, RiskResponse


class DecisionEngine:
    def ingest_deepfake_signal_scores(self, signals: list[float]) -> int:
        """Consume Deepfake Agent signal/score input as one contributor to decision result."""
        pass

    def ingest_threat_signal_scores(self, signals: list[float]) -> int:
        """Consume Threat Agent signal/score input as one contributor to decision result."""
        pass

    def ingest_entity_signal_scores(self, signals: list[float]) -> int:
        """Consume Entity Agent signal/score input as one contributor to decision result."""
        pass

    def aggregate_signal_scores(self, bundle: DecisionSignalBundle) -> int:
        """Receive signal/score from Deepfake, Threat, Entity and compute decision score."""
        pass

    def merge_reasoning_explanation(self, reasoning: GeminiReasoningPayload) -> str:
        """Merge Gemini reasoning output into final explanation for client response."""
        pass

    def build_risk_response(self, score: int, explanation: str) -> RiskResponse:
        """Build final risk response object returned by Agentic Core external API."""
        pass

    def build_json_score_warning_payload(
        self,
        score: int,
        warning: str,
        explanation: str,
    ) -> JsonScoreWarningPayload:
        """Arrow: Decision & Reasoning Engine -> JSON score + warning payload."""
        pass

    def forward_json_score_warning_to_cloud_run_api_microservices(
        self,
        payload: JsonScoreWarningPayload,
    ) -> None:
        """Arrow: JSON score + warning -> Cloud Run API Microservices."""
        pass
