from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload, JsonScoreWarningPayload, RiskResponse

class DecisionEngine:
    def ingest_deepfake_signal_scores(self, signals: list[float]) -> int:
        """Consume Deepfake Agent signal/score input as one contributor to decision result."""
        if not signals:
            return 0
        return int(max(signals))

    def ingest_threat_signal_scores(self, signals: list[float]) -> int:
        """Consume Threat Agent signal/score input as one contributor to decision result."""
        if not signals:
            return 0
        return int(max(signals))

    def ingest_entity_signal_scores(self, signals: list[float]) -> int:
        """Consume Entity Agent signal/score input as one contributor to decision result."""
        if not signals:
            return 0
        return int(max(signals))

    def aggregate_signal_scores(self, bundle: DecisionSignalBundle) -> dict:
        """Receive signal/score from Deepfake, Threat, Entity and compute decision score."""
        voice_scores = [s.score for s in bundle.deepfake_signals] if bundle.deepfake_signals else [0.0]
        text_scores = [s.score for s in bundle.threat_signals] if bundle.threat_signals else [0.0]
        entity_scores = [s.score for s in bundle.entity_signals] if bundle.entity_signals else [0.0]
        
        voice_score = self.ingest_deepfake_signal_scores(voice_scores)
        text_score = self.ingest_threat_signal_scores(text_scores)
        entity_score = self.ingest_entity_signal_scores(entity_scores)

        # Trọng số: Text 40%, Entity 30%, Voice (nếu có) 30%
        # Nếu không có voice (sourceType = SMS/URL), chia đều cho 2 cái kia: Text 60%, Entity 40%
        if sum(voice_scores) > 0:
            total_score = int(voice_score * 0.3 + text_score * 0.4 + entity_score * 0.3)
        else:
            total_score = int(text_score * 0.6 + entity_score * 0.4)

        return {
            "total_score": total_score,
            "voice_score": voice_score,
            "text_score": text_score,
            "entity_score": entity_score
        }

    def merge_reasoning_explanation(self, reasoning: GeminiReasoningPayload) -> str:
        """Merge Gemini reasoning output into final explanation for client response."""
        return reasoning.explanation

    def build_risk_response(self, score_dict: dict, explanation: str, cacheHit: bool = False, matched_patterns: list = None) -> RiskResponse:
        """Build final risk response object returned by Agentic Core external API."""
        return RiskResponse(
            riskScore=score_dict.get("total_score", 0),
            explanation=explanation,
            voiceScore=score_dict.get("voice_score", 0),
            textScore=score_dict.get("text_score", 0),
            entityScore=score_dict.get("entity_score", 0),
            cacheHit=cacheHit,
            matchedPatterns=matched_patterns or []
        )

    def build_json_score_warning_payload(
        self,
        score: int,
        warning: str,
        explanation: str,
    ) -> JsonScoreWarningPayload:
        return JsonScoreWarningPayload(riskScore=score, warning=warning, explanation=explanation)

    def forward_json_score_warning_to_cloud_run_api_microservices(
        self,
        payload: JsonScoreWarningPayload,
    ) -> None:
        pass
