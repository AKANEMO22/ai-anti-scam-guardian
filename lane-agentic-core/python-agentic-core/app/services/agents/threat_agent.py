from app.models.contracts import SearchQueryPayload, TranscribedTextPayload


class ThreatAgent:
    def ingest_google_stt_transcribed_text(self, payload: TranscribedTextPayload) -> str:
        """Arrow: Google STT API -> Threat Agent, ingest transcript payload from STT stage."""
        pass

    def extract_threat_features_from_transcript_payload(self, payload: TranscribedTextPayload) -> list[float]:
        """Extract raw threat features from transcribed-text payload before scoring."""
        pass

    def analyze_transcribed_text_to_signals(self, transcript: str, pattern_ids: list[str]) -> list[float]:
        """Arrow: Transcribed Text -> Threat Agent, output risk signals for decision stage."""
        pass

    def ingest_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent, ingest query payload from LangChain RAG stage."""
        pass

    def analyze_search_query_to_signals(self, payload: SearchQueryPayload, pattern_ids: list[str]) -> list[float]:
        """Analyze Search Query payload and matched patterns into threat-agent raw signals."""
        pass

    def map_threat_signals_to_scores(self, raw_signals: list[float]) -> list[float]:
        """Normalize threat raw signals into consistent score list."""
        pass

    def emit_threat_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Threat Agent -> signal/score payload forwarded to Decision Engine."""
        pass
