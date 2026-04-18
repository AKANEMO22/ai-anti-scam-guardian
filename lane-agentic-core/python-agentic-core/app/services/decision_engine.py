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
        
        # Extract specific signals from threat agent
        threat_signals = bundle.threat_signals
        text_score = 0.0
        pii_score = 0.0
        engagement_score = 0.0
        pii_types = []

        for s in threat_signals:
            if s.signal_name == "scam_risk":
                text_score = max(text_score, s.score)
            elif s.signal_name == "pii_risk":
                pii_score = max(pii_score, s.score)
                if s.reason and s.reason != "none":
                    pii_types.extend(s.reason.split(","))
            elif s.signal_name == "engagement":
                engagement_score = max(engagement_score, s.score)

        entity_scores = [s.score for s in bundle.entity_signals] if bundle.entity_signals else [0.0]
        entity_score = self.ingest_entity_signal_scores(entity_scores)

        # Trọng số: Text 40%, Entity 30%, Voice (nếu có) 30%
        if sum(voice_scores) > 0:
            voice_score = self.ingest_deepfake_signal_scores(voice_scores)
            total_score = int(voice_score * 0.3 + text_score * 0.4 + entity_score * 0.3)
        else:
            voice_score = 0
            total_score = int(text_score * 0.6 + entity_score * 0.4)

        return {
            "total_score": total_score,
            "voice_score": voice_score,
            "text_score": int(text_score),
            "entity_score": entity_score,
            "pii_score": int(pii_score),
            "engagement_score": int(engagement_score),
            "pii_types": list(set(pii_types))
        }

    def merge_reasoning_explanation(self, reasoning: GeminiReasoningPayload) -> str:
        """Merge Gemini reasoning output into final explanation for client response."""
        return reasoning.explanation

    def build_risk_response(self, score_dict: dict, reasoning: GeminiReasoningPayload, cacheHit: bool = False, matched_patterns: list = None) -> RiskResponse:
        """Build final risk response object returned by Agentic Core external API."""
        return RiskResponse(
            riskScore=score_dict.get("total_score", 0),
            explanation=reasoning.explanation,
            voiceScore=score_dict.get("voice_score", 0),
            textScore=score_dict.get("text_score", 0),
            entityScore=score_dict.get("entity_score", 0),
            piiScore=score_dict.get("pii_score", 0),
            engagementScore=score_dict.get("engagement_score", 0),
            piiTypes=score_dict.get("pii_types", []),
            baiterResponse=reasoning.baiter_response,
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
        """Official Arrow: Final propagation of decision to infrastructure monitoring."""
        # In a real environment, this might call a logging service or trigger a 
        # Cloud Pub/Sub event for upstream consumers.
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"ALARM: High risk score {payload.riskScore} detected. Warning: {payload.warning}")
