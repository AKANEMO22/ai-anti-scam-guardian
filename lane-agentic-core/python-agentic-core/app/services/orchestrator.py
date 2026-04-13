import asyncio
from app.models.contracts import (
    AgentSignalScore,
    DeepfakeSignalPayload,
    DecisionAndReasoningEngineToJsonScoreWarningRequest,
    DecisionSignalBundle,
    EntitySignalPayload,
    GeminiReasoningPayload,
    JsonScoreWarningPayload,
    JsonScoreWarningToCloudRunApiMicroservicesRequest,
    PatternMatch,
    RawAudioPayload,
    RiskResponse,
    SearchQueryPayload,
    SignalPayload,
    SourceType,
    TextMetadataPayload,
    ThreatSignalPayload,
    TranscribedTextPayload,
    VoiceStreamPayload,
)
from app.services.agents.deepfake_agent import DeepfakeAgent
from app.services.agents.entity_agent import EntityAgent
from app.services.agents.reasoning_agent import GeminiApiReasoningEngine
from app.services.agents.threat_agent import ThreatAgent
from app.services.decision_engine import DecisionEngine
from app.clients.storage_client import StorageClient


class OrchestratorService:
    def __init__(self):
        self.deepfake_agent = DeepfakeAgent()
        self.entity_agent = EntityAgent()
        self.threat_agent = ThreatAgent()
        self.decision_engine = DecisionEngine()
        self.reasoning_engine = GeminiApiReasoningEngine()
        self.storage_client = StorageClient()

    async def process_pipeline_request(self, payload: SignalPayload) -> RiskResponse:
        """External flow: orchestrate complete pipeline and return client risk response."""
        
        # 1. Fetch relevant patterns from Storage Lane
        # Use asyncio.gather if we had multiple async fetches
        matches = await self.storage_client.forward_search_query_to_storage_for_threat_agent(
            query=payload.text or "Voice analysis only",
            source_type=payload.sourceType,
            top_k=3
        )
        patterns = [{"pattern_id": m.pattern_id, "pattern_text": m.pattern_text} for m in matches]
        
        bundle = DecisionSignalBundle()
        
        # 2. Run Agents concurrently where possible (Text vs Entity vs Voice)
        tasks = []
        
        # Text/Threat Analysis Task (only if text is present)
        async def run_threat():
            if payload.text:
                 search_payload = SearchQueryPayload(query=payload.text, sourceType=payload.sourceType)
                 scores = await self.threat_agent.analyze_search_query_to_signals(search_payload, patterns)
                 bundle.threat_signals.append(AgentSignalScore(signal_name="threat_score", score=scores[0]))
        tasks.append(run_threat())

        # Entity Analysis Task
        async def run_entity():
             if payload.text:
                 scores = await self.entity_agent.analyze_text_metadata_to_signals(payload.text, payload.metadata)
                 bundle.entity_signals.append(AgentSignalScore(signal_name="entity_score", score=scores[0]))
        tasks.append(run_entity())

        # Voice Deepfake Task
        async def run_voice():
            if payload.sourceType == SourceType.CALL:
                 # stubbed, returns sync, but wrapped
                 scores = self.deepfake_agent.analyze_raw_audio_to_signals(payload.callSessionId, None)
                 bundle.deepfake_signals.append(AgentSignalScore(signal_name="voice_score", score=scores[0]))
        tasks.append(run_voice())

        # Execute agent tasks concurrently
        await asyncio.gather(*tasks)

        # 3. Decision Engine Aggregation
        score_dict = self.decision_engine.aggregate_signal_scores(bundle)
        
        # 4. Reasoning Engine Explanation
        reasoning_payload = await self.reasoning_engine.request_reasoning_from_decision_signals(bundle)
        
        # 5. Build Risk Response
        explanation = self.decision_engine.merge_reasoning_explanation(reasoning_payload)
        
        # Format response
        response = self.decision_engine.build_risk_response(
            score_dict=score_dict,
            explanation=explanation,
            cacheHit=False,
            matched_patterns=matches
        )
        
        # Fire and forget storage sync (mocked for now)
        self.storage_client.sync_agentic_metadata_to_storage(payload.callSessionId, payload.metadata)

        return response

    # --- Other stubs to satisfy contracts if needed ---
    def route_orchestrator_agent_to_raw_audio(self, payload: SignalPayload) -> RawAudioPayload:
        pass
    def route_orchestrator_agent_to_voice_stream(self, payload: SignalPayload) -> VoiceStreamPayload:
        pass
    def route_orchestrator_agent_to_text_metadata(self, payload: SignalPayload) -> TextMetadataPayload:
        pass
    def route_raw_audio_to_deepfake_agent(self, payload: RawAudioPayload) -> list[AgentSignalScore]:
        pass
    def route_voice_stream_to_google_stt(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        pass
    def route_google_stt_api_to_transcribed_text(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        pass
    def route_transcribed_text_to_threat_agent(self, payload: TranscribedTextPayload) -> list[AgentSignalScore]:
        pass
    def route_search_query_to_threat_agent(self, payload: SearchQueryPayload) -> list[AgentSignalScore]:
        pass
    def route_text_metadata_to_entity_agent(self, payload: TextMetadataPayload) -> list[AgentSignalScore]:
        pass
    def route_deepfake_signal_score_to_decision_engine(self, payload: DeepfakeSignalPayload) -> int:
        pass
    def route_entity_signal_score_to_decision_engine(self, payload: EntitySignalPayload) -> int:
        pass
    def route_threat_signal_score_to_decision_engine(self, payload: ThreatSignalPayload) -> int:
        pass
    def collect_signals_for_decision_engine(self, bundle: DecisionSignalBundle) -> int:
        pass
    def exchange_reasoning_with_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        pass
    def route_decision_reasoning_explanation_to_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        pass
    def route_gemini_reasoning_explanation_to_decision(self, reasoning: GeminiReasoningPayload) -> GeminiReasoningPayload:
        pass
    def route_decision_and_reasoning_engine_to_json_score_warning(self, request: DecisionAndReasoningEngineToJsonScoreWarningRequest) -> JsonScoreWarningPayload:
        pass
    def route_json_score_warning_to_cloud_run_api_microservices(self, request: JsonScoreWarningToCloudRunApiMicroservicesRequest) -> None:
        pass
