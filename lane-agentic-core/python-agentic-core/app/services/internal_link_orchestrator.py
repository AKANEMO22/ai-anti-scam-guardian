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

    def link_orchestrator_to_raw_audio(self, request: OrchestratorToRawAudioRequest) -> None:
        """Internal link: Orchestrator Agent LangGraph Route -> Raw Audio."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_orchestrator_to_voice_stream(self, request: OrchestratorToVoiceStreamRequest) -> None:
        """Internal link: Orchestrator Agent LangGraph Route -> Voice Stream."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_orchestrator_to_text_metadata(self, request: OrchestratorToTextMetadataRequest) -> None:
        """Internal link: Orchestrator Agent LangGraph Route -> Text/Metadata."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_raw_audio_to_deepfake(self, request: RawAudioToDeepfakeRequest) -> list[AgentSignalScore]:
        """Internal link: Raw Audio -> Deepfake Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_voice_stream_to_google_stt(self, request: VoiceStreamToSttRequest) -> None:
        """Internal link: Voice Stream -> Google STT API."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_google_stt_api_to_transcribed_text(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> None:
        """Internal link: Google STT API -> Transcribed Text."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_google_stt_to_threat(self, request: SttToThreatRequest) -> list[AgentSignalScore]:
        """Internal link: Google STT API -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_transcribed_text_to_threat_agent(
        self,
        request: TranscribedTextToThreatAgentRequest,
    ) -> list[AgentSignalScore]:
        """Internal link: Transcribed Text -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_google_stt_api_to_threat_agent(self, request: GoogleSttToThreatRequest) -> list[AgentSignalScore]:
        """Internal link: Google STT API -> Threat Agent (typed request)."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_search_query_to_threat_agent(self, request: SearchQueryToThreatAgentRequest) -> list[AgentSignalScore]:
        """Internal link: Search Query -> Threat Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_text_metadata_to_entity(self, request: TextMetadataToEntityRequest) -> list[AgentSignalScore]:
        """Internal link: Text/Metadata -> Entity Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_deepfake_to_decision(self, request: AgentToDecisionRequest) -> int:
        """Internal link: Deepfake Agent signal/score -> Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_deepfake_signal_score_to_decision(self, request: DeepfakeToDecisionRequest) -> int:
        """Internal link: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_threat_to_decision(self, request: AgentToDecisionRequest) -> int:
        """Internal link: Threat Agent signal/score -> Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_threat_signal_score_to_decision(self, request: ThreatToDecisionRequest) -> int:
        """Internal link: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_entity_to_decision(self, request: AgentToDecisionRequest) -> int:
        """Internal link: Entity Agent signal/score -> Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_entity_signal_score_to_decision(self, request: EntityToDecisionRequest) -> int:
        """Internal link: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_decision_to_gemini(self, request: DecisionToGeminiRequest) -> GeminiReasoningPayload:
        """Internal link: Decision Engine -> Gemini API Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_gemini_to_decision(self, request: GeminiToDecisionRequest) -> GeminiReasoningPayload:
        """Internal link: Gemini API Reasoning Engine -> Decision Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_decision_reasoning_explanation_to_gemini(
        self,
        request: DecisionReasoningExplanationToGeminiRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Decision & Reasoning Engine -> Gemini API Reasoning Engine (reasoning/explanation)."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_gemini_reasoning_explanation_to_decision(
        self,
        request: GeminiReasoningExplanationToDecisionRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Gemini API Reasoning Engine -> Decision & Reasoning Engine (reasoning/explanation)."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Internal link: Decision & Reasoning Engine -> JSON score + warning."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def link_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Internal link: JSON score + warning -> Cloud Run API Microservices."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_decision_bundle(self, signals: list[AgentSignalScore]) -> DecisionSignalBundle:
        """Compose DecisionSignalBundle from raw agent signal list for link handlers."""
        print("mocked")
        return locals().get("mock_data", None) or {}
