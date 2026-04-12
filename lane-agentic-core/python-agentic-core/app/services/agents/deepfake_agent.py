class DeepfakeAgent:
    def analyze_raw_audio_to_signals(self, call_session_id: str | None, raw_audio_ref: str | None) -> list[float]:
        """Arrow: Raw Audio -> Deepfake Agent, output signal scores for decision stage."""
        pass

    def normalize_deepfake_signals(self, raw_scores: list[float]) -> list[float]:
        """Normalize deepfake output into stable score range for downstream engines."""
        pass

    def emit_deepfake_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Deepfake Agent -> signal/score payload forwarded to Decision Engine."""
        pass
