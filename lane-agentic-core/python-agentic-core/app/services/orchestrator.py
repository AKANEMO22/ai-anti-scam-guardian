from app.models.contracts import (
    AgentSignalScore,
    DeepfakeSignalPayload,
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    DecisionSignalBundle,
    EntitySignalPayload,
    GeminiReasoningPayload,
    JsonScoreWarningPayload,
    JsonScoreWarningToCloudRunApiMicroservicesRequest,
    RawAudioPayload,
    RiskResponse,
    SearchQueryPayload,
    SignalPayload,
    TextMetadataPayload,
    ThreatSignalPayload,
    TranscribedTextPayload,
    VoiceStreamPayload,
)


class OrchestratorService:
    def route_orchestrator_agent_to_raw_audio(self, payload: SignalPayload) -> RawAudioPayload:
        """Arrow: Orchestrator Agent LangGraph Route -> Raw Audio stage."""
        pass

    def route_orchestrator_agent_to_voice_stream(self, payload: SignalPayload) -> VoiceStreamPayload:
        """Arrow: Orchestrator Agent LangGraph Route -> Voice Stream stage."""
        pass

    def route_orchestrator_agent_to_text_metadata(self, payload: SignalPayload) -> TextMetadataPayload:
        """Arrow: Orchestrator Agent LangGraph Route -> Text/Metadata stage."""
        pass

    def route_raw_audio_to_deepfake_agent(self, payload: RawAudioPayload) -> list[AgentSignalScore]:
        """Arrow: Raw Audio -> Deepfake Agent."""
        pass

    def route_voice_stream_to_google_stt(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        """Arrow: Voice Stream -> Google STT API."""
        pass

    def route_google_stt_api_to_transcribed_text(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        """Arrow: Google STT API -> Transcribed Text."""
        pass

    def route_transcribed_text_to_threat_agent(self, payload: TranscribedTextPayload) -> list[AgentSignalScore]:
        """Arrow: Transcribed Text -> Threat Agent."""
        pass

    def route_search_query_to_threat_agent(self, payload: SearchQueryPayload) -> list[AgentSignalScore]:
        """Arrow: Search Query -> Threat Agent."""
        pass

    def route_text_metadata_to_entity_agent(self, payload: TextMetadataPayload) -> list[AgentSignalScore]:
        """Arrow: Text/Metadata -> Entity Agent."""
        pass

    def route_deepfake_signal_score_to_decision_engine(self, payload: DeepfakeSignalPayload) -> int:
        """Arrow: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        pass

    def route_entity_signal_score_to_decision_engine(self, payload: EntitySignalPayload) -> int:
        """Arrow: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        pass

    def route_threat_signal_score_to_decision_engine(self, payload: ThreatSignalPayload) -> int:
        """Arrow: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        pass

    def collect_signals_for_decision_engine(self, bundle: DecisionSignalBundle) -> int:
        """Arrow: agent signals -> Decision & Reasoning Engine."""
        pass

    def exchange_reasoning_with_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Arrow: Decision Engine <-> Gemini API Reasoning Engine."""
        pass

    def route_decision_reasoning_explanation_to_gemini(
        self,
        bundle: DecisionSignalBundle,
    ) -> GeminiReasoningPayload:
        """Arrow: Decision & Reasoning Engine -> Gemini API Reasoning Engine (reasoning/explanation context)."""
        pass

    def route_gemini_reasoning_explanation_to_decision(
        self,
        reasoning: GeminiReasoningPayload,
    ) -> GeminiReasoningPayload:
        """Arrow: Gemini API Reasoning Engine -> Decision & Reasoning Engine (reasoning/explanation payload)."""
        pass

    def route_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Arrow: Decision & Reasoning Engine -> JSON score + warning."""
        pass

    def route_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Arrow: JSON score + warning -> Cloud Run API Microservices."""
        pass

    def process_pipeline_request(self, payload: SignalPayload) -> RiskResponse:
        """External flow: orchestrate complete pipeline and return client risk response."""
        pass
