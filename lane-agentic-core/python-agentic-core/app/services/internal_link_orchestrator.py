from app.models.contracts import (
    AgentSignalScore,
    DeepfakeToDecisionRequest,
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    DecisionReasoningExplanationToGeminiRequest,
    DecisionSignalBundle,
    EntityToDecisionRequest,
    GoogleSttApiToTranscribedTextRequest,
    GeminiReasoningExplanationToDecisionRequest,
    GeminiReasoningPayload,
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
    RawAudioPayload,
    VoiceStreamPayload,
    TextMetadataPayload,
    TranscribedTextPayload,
)
from app.services.orchestrator import OrchestratorService

# Import Links
from app.services.links.google_stt_threat_link import GoogleSttThreatLink
from app.services.links.google_stt_transcribed_text_link import GoogleSttApiTranscribedTextLink
from app.services.links.threat_decision_link import ThreatDecisionLink
from app.services.links.entity_decision_link import EntityDecisionLink
from app.services.links.deepfake_decision_link import DeepfakeDecisionLink
from app.services.links.decision_gemini_reasoning_link import DecisionGeminiReasoningLink
from app.services.links.gemini_decision_reasoning_link import GeminiDecisionReasoningLink
from app.services.links.decision_json_score_warning_link import DecisionJsonScoreWarningLink
from app.services.links.json_score_warning_cloud_run_link import JsonScoreWarningCloudRunLink
from app.services.links.search_query_threat_link import SearchQueryThreatLink
from app.services.links.transcribed_text_threat_agent_link import TranscribedTextThreatAgentLink

# Import Channels
from app.services.channels.raw_audio_channel import RawAudioChannel
from app.services.channels.voice_stream_channel import VoiceStreamChannel
from app.services.channels.transcribed_text_channel import TranscribedTextChannel
from app.services.channels.text_metadata_channel import TextMetadataChannel
from app.services.channels.threat_signal_channel import ThreatSignalChannel
from app.services.channels.entity_signal_channel import EntitySignalChannel
from app.services.channels.deepfake_signal_channel import DeepfakeSignalChannel
from app.services.channels.reasoning_explanation_channel import ReasoningExplanationChannel
from app.services.channels.search_query_channel import SearchQueryChannel


class AgenticInternalLinkOrchestrator:
    def __init__(self, orchestrator: OrchestratorService) -> None:
        self._orchestrator = orchestrator
        
        # Links
        self.google_stt_threat_link = GoogleSttThreatLink()
        self.stt_transcribed_text_link = GoogleSttApiTranscribedTextLink()
        self.threat_decision_link = ThreatDecisionLink()
        self.entity_decision_link = EntityDecisionLink()
        self.deepfake_decision_link = DeepfakeDecisionLink()
        self.decision_gemini_link = DecisionGeminiReasoningLink()
        self.gemini_decision_link = GeminiDecisionReasoningLink()
        self.decision_json_link = DecisionJsonScoreWarningLink()
        self.json_cloud_run_link = JsonScoreWarningCloudRunLink()
        self.search_query_threat_link = SearchQueryThreatLink()
        self.transcript_threat_link = TranscribedTextThreatAgentLink()

        # Channels
        self.raw_audio_channel = RawAudioChannel()
        self.voice_stream_channel = VoiceStreamChannel()
        self.transcribed_text_channel = TranscribedTextChannel()
        self.text_metadata_channel = TextMetadataChannel()
        self.threat_signal_channel = ThreatSignalChannel()
        self.entity_signal_channel = EntitySignalChannel()
        self.deepfake_signal_channel = DeepfakeSignalChannel()
        self.reasoning_channel = ReasoningExplanationChannel()
        self.search_query_channel = SearchQueryChannel()

    def link_orchestrator_to_raw_audio(self, request: OrchestratorToRawAudioRequest) -> RawAudioPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Raw Audio."""
        payload = self._orchestrator.route_orchestrator_agent_to_raw_audio(request.payload)
        return self.raw_audio_channel.receive_from_orchestrator_route(payload)

    def link_orchestrator_to_voice_stream(self, request: OrchestratorToVoiceStreamRequest) -> VoiceStreamPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Voice Stream."""
        payload = self._orchestrator.route_orchestrator_agent_to_voice_stream(request.payload)
        return self.voice_stream_channel.receive_from_orchestrator_route(payload)

    def link_orchestrator_to_text_metadata(self, request: OrchestratorToTextMetadataRequest) -> TextMetadataPayload:
        """Internal link: Orchestrator Agent LangGraph Route -> Text/Metadata."""
        payload = self._orchestrator.route_orchestrator_agent_to_text_metadata(request.payload)
        return self.text_metadata_channel.receive_from_orchestrator_route(payload)

    async def link_raw_audio_to_deepfake(self, request: RawAudioToDeepfakeRequest) -> list[AgentSignalScore]:
        """Internal link: Raw Audio -> Deepfake Agent."""
        return await self._orchestrator.route_raw_audio_to_deepfake_agent(request.payload)

    def link_voice_stream_to_google_stt(self, request: VoiceStreamToSttRequest) -> TranscribedTextPayload:
        """Internal link: Voice Stream -> Google STT API."""
        return self._orchestrator.route_voice_stream_to_google_stt(request.payload)

    def link_google_stt_api_to_transcribed_text(
        self,
        request: GoogleSttApiToTranscribedTextRequest,
    ) -> TranscribedTextPayload:
        """Internal link: Google STT API -> Transcribed Text."""
        payload = self._orchestrator.route_google_stt_api_to_transcribed_text(request.payload)
        payload = self.stt_transcribed_text_link.forward_google_stt_api_to_transcribed_text(payload)
        return self.transcribed_text_channel.receive_from_google_stt_api(payload)

    def link_google_stt_to_threat(self, request: SttToThreatRequest) -> list[AgentSignalScore]:
        """Internal link: Google STT API -> Threat Agent."""
        payload = self.google_stt_threat_link.forward_transcribed_text_to_threat_agent(request.payload)
        return self._orchestrator.route_transcribed_text_to_threat_agent(payload)

    def link_transcribed_text_to_threat_agent(
        self,
        request: TranscribedTextToThreatAgentRequest,
    ) -> list[AgentSignalScore]:
        """Internal link: Transcribed Text -> Threat Agent."""
        payload = self.transcript_threat_link.forward_transcribed_text_to_threat_agent(request.payload)
        return self._orchestrator.route_transcribed_text_to_threat_agent(payload)

    def link_search_query_to_threat_agent(self, request: SearchQueryToThreatAgentRequest) -> list[AgentSignalScore]:
        """Internal link: Search Query -> Threat Agent."""
        payload = self.search_query_threat_link.forward_search_query_to_threat_agent(request.payload)
        return self._orchestrator.route_search_query_to_threat_agent(payload)

    def link_text_metadata_to_entity(self, request: TextMetadataToEntityRequest) -> list[AgentSignalScore]:
        """Internal link: Text/Metadata -> Entity Agent."""
        return self._orchestrator.route_text_metadata_to_entity_agent(request.payload)

    def link_deepfake_signal_score_to_decision(self, request: DeepfakeToDecisionRequest) -> int:
        """Internal link: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        payload = self.deepfake_signal_channel.receive_from_deepfake_agent(request.payload.signals)
        signals = self.deepfake_decision_link.forward_signal_score_to_decision_engine(payload)
        return self._orchestrator.route_deepfake_signal_score_to_decision_engine(DeepfakeToDecisionRequest(payload=payload).payload)

    def link_entity_signal_score_to_decision(self, request: EntityToDecisionRequest) -> int:
        """Internal link: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        payload = self.entity_signal_channel.receive_from_entity_agent(request.payload.signals)
        signals = self.entity_decision_link.forward_signal_score_to_decision_engine(payload)
        return self._orchestrator.route_entity_signal_score_to_decision_engine(EntityToDecisionRequest(payload=payload).payload)

    def link_threat_signal_score_to_decision(self, request: ThreatToDecisionRequest) -> int:
        """Internal link: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        payload = self.threat_signal_channel.receive_from_threat_agent(request.payload.signals)
        signals = self.threat_decision_link.forward_signal_score_to_decision_engine(payload)
        return self._orchestrator.route_threat_signal_score_to_decision_engine(ThreatToDecisionRequest(payload=payload).payload)

    def link_decision_reasoning_explanation_to_gemini(
        self,
        request: DecisionReasoningExplanationToGeminiRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Decision & Reasoning Engine -> Gemini API Reasoning Engine (reasoning/explanation)."""
        bundle = self.decision_gemini_link.forward_reasoning_context_to_gemini(request.reasoning_context)
        return self._orchestrator.route_decision_reasoning_explanation_to_gemini(bundle)

    def link_gemini_reasoning_explanation_to_decision(
        self,
        request: GeminiReasoningExplanationToDecisionRequest,
    ) -> GeminiReasoningPayload:
        """Internal link: Gemini API Reasoning Engine -> Decision & Reasoning Engine (reasoning/explanation)."""
        payload = self.reasoning_channel.receive_from_gemini_api_reasoning_engine(request.reasoning)
        payload = self.gemini_decision_link.forward_reasoning_explanation_to_decision(payload)
        return self._orchestrator.route_gemini_reasoning_explanation_to_decision(payload)

    def link_decision_and_reasoning_engine_to_json_score_warning(
        self,
        request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    ) -> JsonScoreWarningPayload:
        """Internal link: Decision & Reasoning Engine -> JSON score + warning."""
        payload = self.decision_json_link.forward_decision_and_reasoning_engine_to_json_score_warning(request)
        return payload

    def link_json_score_warning_to_cloud_run_api_microservices(
        self,
        request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    ) -> None:
        """Internal link: JSON score + warning -> Cloud Run API Microservices."""
        self.json_cloud_run_link.forward_json_score_warning_to_cloud_run_api_microservices(request)
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
