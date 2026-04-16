from typing import Optional

class DeepfakeAgent:
    def analyze_raw_audio_to_signals(self, call_session_id: Optional[str], raw_audio_ref: Optional[str]) -> list[float]:
        """Arrow: Raw Audio -> Deepfake Agent, output signal scores for decision stage."""
        # MVP: RawNet2 deepfake detection requires heavy models. We stub it 
        # to return 0.0 until fully integrated with the external inference endpoint.
        return [0.0]

    def normalize_deepfake_signals(self, raw_scores: list[float]) -> list[float]:
        """Normalize deepfake output into stable score range for downstream engines."""
        return raw_scores

    def emit_deepfake_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Deepfake Agent -> signal/score payload forwarded to Decision Engine."""
        return scored_signals
