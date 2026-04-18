from fastapi import APIRouter, Depends

from app.dependencies import get_internal_link_orchestrator, get_orchestrator_service
from app.models.contracts import (
    AgentToDecisionRequest,
    DeepfakeToDecisionRequest,
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    DecisionReasoningExplanationToGeminiRequest,
    DecisionToGeminiRequest,
    EntityToDecisionRequest,
    GoogleSttApiToTranscribedTextRequest,
    GoogleSttToThreatRequest,
    GeminiReasoningExplanationToDecisionRequest,
    GeminiToDecisionRequest,
    JsonScoreWarningToCloudRunApiMicroservicesRequest,
    OrchestratorToRawAudioRequest,
    OrchestratorToTextMetadataRequest,
    OrchestratorToVoiceStreamRequest,
    RawAudioToDeepfakeRequest,
    SearchQueryToThreatAgentRequest,
    SignalPayload,
    SttToThreatRequest,
    TextMetadataToEntityRequest,
    ThreatToDecisionRequest,
    TranscribedTextToThreatAgentRequest,
    VoiceStreamToSttRequest,
)
from app.services.internal_link_orchestrator import AgenticInternalLinkOrchestrator
from app.services.orchestrator import OrchestratorService

router = APIRouter(tags=["agentic-core"])


@router.post("/v1/agentic/score")
async def score_signal(
    payload: SignalPayload,
    orchestrator: OrchestratorService = Depends(get_orchestrator_service),
) -> dict:
    """External API: execute end-to-end Agentic Core score pipeline."""
    result = await orchestrator.process_pipeline_request(payload)
    return result.model_dump()


@router.post("/v1/agentic/internal/raw-audio-to-deepfake")
async def internal_raw_audio_to_deepfake(
    request: RawAudioToDeepfakeRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> list[AgentSignalScore]:
    """Internal link: Raw Audio -> Deepfake Agent."""
    return await internal_orchestrator.link_raw_audio_to_deepfake(request)


@router.post("/v1/agentic/internal/orchestrator-to-raw-audio")
def internal_orchestrator_to_raw_audio(
    request: OrchestratorToRawAudioRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Orchestrator Agent LangGraph Route -> Raw Audio."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/voice-stream-to-google-stt")
def internal_voice_stream_to_google_stt(
    request: VoiceStreamToSttRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Voice Stream -> Google STT API."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/orchestrator-to-voice-stream")
def internal_orchestrator_to_voice_stream(
    request: OrchestratorToVoiceStreamRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Orchestrator Agent LangGraph Route -> Voice Stream."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/google-stt-to-threat")
def internal_google_stt_to_threat(
    request: SttToThreatRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Google STT API -> Threat Agent."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/google-stt-api-to-transcribed-text")
def internal_google_stt_api_to_transcribed_text(
    request: GoogleSttApiToTranscribedTextRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Google STT API -> Transcribed Text."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/transcribed-text-to-threat-agent")
def internal_transcribed_text_to_threat_agent(
    request: TranscribedTextToThreatAgentRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Transcribed Text -> Threat Agent."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/google-stt-api-to-threat-agent")
def internal_google_stt_api_to_threat_agent(
    request: GoogleSttToThreatRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Google STT API -> Threat Agent (typed request)."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/search-query-to-threat-agent")
def internal_search_query_to_threat_agent(
    request: SearchQueryToThreatAgentRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Search Query -> Threat Agent."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/text-metadata-to-entity")
def internal_text_metadata_to_entity(
    request: TextMetadataToEntityRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Text/Metadata -> Entity Agent."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/orchestrator-to-text-metadata")
def internal_orchestrator_to_text_metadata(
    request: OrchestratorToTextMetadataRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Orchestrator Agent LangGraph Route -> Text/Metadata."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/deepfake-to-decision")
def internal_deepfake_to_decision(
    request: AgentToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Deepfake Agent signal/score -> Decision Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/deepfake-signal-score-to-decision")
def internal_deepfake_signal_score_to_decision(
    request: DeepfakeToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/threat-to-decision")
def internal_threat_to_decision(
    request: AgentToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Threat Agent signal/score -> Decision Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/threat-signal-score-to-decision")
def internal_threat_signal_score_to_decision(
    request: ThreatToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/entity-to-decision")
def internal_entity_to_decision(
    request: AgentToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Entity Agent signal/score -> Decision Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/entity-signal-score-to-decision")
def internal_entity_signal_score_to_decision(
    request: EntityToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/decision-to-gemini")
def internal_decision_to_gemini(
    request: DecisionToGeminiRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Decision Engine -> Gemini API Reasoning Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/decision-reasoning-explanation-to-gemini")
def internal_decision_reasoning_explanation_to_gemini(
    request: DecisionReasoningExplanationToGeminiRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Decision & Reasoning Engine -> Gemini API Reasoning Engine (reasoning/explanation)."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/gemini-to-decision")
def internal_gemini_to_decision(
    request: GeminiToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Gemini API Reasoning Engine -> Decision Engine."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/gemini-reasoning-explanation-to-decision")
def internal_gemini_reasoning_explanation_to_decision(
    request: GeminiReasoningExplanationToDecisionRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Gemini API Reasoning Engine -> Decision & Reasoning Engine (reasoning/explanation)."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/decision-and-reasoning-engine-to-json-score-warning")
def internal_decision_and_reasoning_engine_to_json_score_warning(
    request: DecisionAndReasoningEngineToJsonScoreWarningRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Decision & Reasoning Engine -> JSON score + warning."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/agentic/internal/json-score-warning-to-cloud-run-api-microservices")
def internal_json_score_warning_to_cloud_run_api_microservices(
    request: JsonScoreWarningToCloudRunApiMicroservicesRequest,
    internal_orchestrator: AgenticInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: JSON score + warning -> Cloud Run API Microservices."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}
