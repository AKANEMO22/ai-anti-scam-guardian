from app.models.contracts import (
    AgentSignalScore,
    AgentToDecisionRequest,
    DeepfakeToDecisionRequest,
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    DecisionReasoningExplanationToGeminiRequest,
    DecisionSignalBundle,
    DecisionToGeminiRequest,
    EntityToDecisionRequest,
    GoogleSttApiToTranscribedTextRequest,
    GoogleSttToThreatRequest,
    GeminiReasoningExplanationToDecisionRequest,
    GeminiReasoningPayload,
    GeminiToDecisionRequest,
    JsonScoreWarningPayload,
    JsonScoreWarningToCloudRunApiMicroservicesRequest,
    OrchestratorToRawAudioRequest,
    OrchestratorToTextMetadataRequest,
    OrchestratorToVoiceStreamRequest,
    RawAudioToDeepfakeRequest,
    SearchQueryToThreatAgentRequest,
    SttToThreatRequest,
    TextMetadataToEntityRequest,
    ThreatToDecisionRequest,
    TranscribedTextToThreatAgentRequest,
    VoiceStreamToSttRequest,
)
from app.services.orchestrator import OrchestratorService


class AgenticInternalLinkOrchestrator:
    def __init__(self, orchestrator: OrchestratorService) -> None:
        self._orchestrator = orchestrator

    def link_orchestrator_to_raw_audio(self, request: OrchestratorToRawAudioRequest) -> RawAudioPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Raw Audio."""
        return self._orchestrator.route_orchestrator_agent_to_raw_audio(request.payload)

    def link_orchestrator_to_voice_stream(self, request: OrchestratorToVoiceStreamRequest) -> VoiceStreamPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Voice Stream."""
        return self._orchestrator.route_orchestrator_agent_to_voice_stream(request.payload)

    def link_orchestrator_to_text_metadata(self, request: OrchestratorToTextMetadataRequest) -> TextMetadataPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Text/Metadata."""
        return self._orchestrator.route_orchestrator_agent_to_text_metadata(request.payload)

    def link_raw_audio_to_deepfake(self, request: RawAudioToDeepfakeRequest) -> list[AgentSignalScore]:
        """Internal link: Raw Audio -> Deepfake Agent."""
        return self._orchestrator.route_raw_audio_to_deepfake_agent(request.payload)

    def link_voice_stream_to_google_stt(self, request: VoiceStreamToSttRequest) -> TranscribedTextPayload:
        """Internal link: Voice Stream -> Google STT API."""
        return self._orchestrator.route_voice_stream_to_google_stt(request.payload)

    def link_google_stt_api_to_transcribed_text(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> TranscribedTextPayload:
        """Internal link: Google STT API -> Transcribed Text."""
        return self._orchestrator.route_google_stt_api_to_transcribed_text(request.payload)

    def link_google_stt_to_threat(self, request: SttToThreatRequest) -> list[AgentSignalScore]:
        """Internal link: Google STT API -> Threat Agent."""
        return self._orchestrator.route_transcribed_text_to_threat_agent(request.payload)

    def link_transcribed_text_to_threat_agent(
        self,
        request: TranscribedTextToThreatAgentRequest,
    ) -> list[AgentSignalScore]:
        """Internal link: Transcribed Text -> Threat Agent."""
        return self._orchestrator.route_transcribed_text_to_threat_agent(request.payload)

    def link_search_query_to_threat_agent(self, request: SearchQueryToThreatAgentRequest) -> list[AgentSignalScore]:
        """Internal link: Search Query -> Threat Agent."""
        return self._orchestrator.route_search_query_to_threat_agent(request.payload)

    def link_text_metadata_to_entity(self, request: TextMetadataToEntityRequest) -> list[AgentSignalScore]:
        """Internal link: Text/Metadata -> Entity Agent."""
        return self._orchestrator.route_text_metadata_to_entity_agent(request.payload)

    def link_deepfake_signal_score_to_decision(self, request: DeepfakeToDecisionRequest) -> int:
        """Internal link: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        return self._orchestrator.route_deepfake_signal_score_to_decision_engine(request.payload)

    def link_entity_signal_score_to_decision(self, request: EntityToDecisionRequest) -> int:
        """Internal link: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        return self._orchestrator.route_entity_signal_score_to_decision_engine(request.payload)

    def link_threat_signal_score_to_decision(self, request: ThreatToDecisionRequest) -> int:
        """Internal link: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        return self._orchestrator.route_threat_signal_score_to_decision_engine(request.payload)

    def link_decision_reasoning_explanation_to_gemini(
        self,
        request: DecisionReasoningExplanationToGeminiRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Decision & Reasoning Engine -> Gemini API Reasoning Engine (reasoning/explanation)."""
        return self._orchestrator.route_decision_reasoning_explanation_to_gemini(request.reasoning_context)

    def link_gemini_reasoning_explanation_to_decision(
        self,
        request: GeminiReasoningExplanationToDecisionRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Gemini API Reasoning Engine -> Decision & Reasoning Engine (reasoning/explanation)."""
        return self._orchestrator.route_gemini_reasoning_explanation_to_decision(request.reasoning)

    def link_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Internal link: Decision & Reasoning Engine -> JSON score + warning."""
        return self._orchestrator.route_decision_and_reasoning_engine_to_json_score_warning(request)

    def link_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Internal link: JSON score + warning -> Cloud Run API Microservices."""
        self._orchestrator.route_json_score_warning_to_cloud_run_api_microservices(request)

    def build_decision_bundle(self, signals: list[AgentSignalScore]) -> DecisionSignalBundle:
        """Compose DecisionSignalBundle from raw agent signal list for link handlers."""
        bundle = DecisionSignalBundle()
        for s in signals:
            if "voice" in s.signal_name or "deepfake" in s.signal_name:
                bundle.deepfake_signals.append(s)
            elif "entity" in s.signal_name:
                bundle.entity_signals.append(s)
            else:
                bundle.threat_signals.append(s)
        return bundle
