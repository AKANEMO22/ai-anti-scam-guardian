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
                 bundle.threat_signals.extend(scores) # scores is now a list[AgentSignalScore]
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
                 # Real multi-modal + acoustic analysis
                 audio_payload = RawAudioPayload(
                     callSessionId=payload.callSessionId,
                     rawAudioRef=payload.metadata.get("rawAudioRef") # Ensure client sends this
                 )
                 scores = await self.deepfake_agent.analyze_raw_audio_to_signals(audio_payload)
                 bundle.deepfake_signals.extend(scores)
        tasks.append(run_voice())

        # Execute agent tasks concurrently
        await asyncio.gather(*tasks)

        # 3. Decision Engine Aggregation
        score_dict = self.decision_engine.aggregate_signal_scores(bundle)
        
        # 4. Reasoning Engine Explanation
        reasoning_payload = await self.reasoning_engine.request_reasoning_from_decision_signals(bundle)
        
        # 5. Build Risk Response
        # Format response
        response = self.decision_engine.build_risk_response(
            score_dict=score_dict,
            reasoning=reasoning_payload,
            cacheHit=False,
            matched_patterns=matches
        )
        
        # Fire and forget storage indexing for feedback loop
        import uuid
        event_id = str(uuid.uuid4())
        
        index_data = {
            "eventId": event_id,
            "sourceType": payload.sourceType.value,
            "text": payload.text,
            "callSessionId": payload.callSessionId,
            "metadata": payload.metadata,
            "riskScore": response.riskScore,
            "explanation": response.explanation,
            "voiceScore": response.voiceScore,
            "textScore": response.textScore,
            "entityScore": response.entityScore
        }
        asyncio.create_task(self.storage_client.index_signal_to_storage(index_data))

        return response

    # --- Official Routing Arrows (Linking internal stages) ---
    
    def route_orchestrator_agent_to_raw_audio(self, payload: SignalPayload) -> RawAudioPayload:
        """Link: Orchestrator -> Raw Audio stage (Internal Link Orchestrator)."""
        return RawAudioPayload(
            callSessionId=payload.callSessionId,
            metadata=payload.metadata
        )

    def route_orchestrator_agent_to_voice_stream(self, payload: SignalPayload) -> VoiceStreamPayload:
        """Link: Orchestrator -> Voice Stream stage."""
        return VoiceStreamPayload(
            callSessionId=payload.callSessionId,
            metadata=payload.metadata
        )

    def route_orchestrator_agent_to_text_metadata(self, payload: SignalPayload) -> TextMetadataPayload:
        """Link: Orchestrator -> Text/Metadata stage."""
        return TextMetadataPayload(
            text=payload.text or "",
            metadata=payload.metadata
        )

    async def route_raw_audio_to_deepfake_agent(self, payload: RawAudioPayload) -> list[AgentSignalScore]:
        """Link: Raw Audio -> Deepfake Agent."""
        return await self.deepfake_agent.analyze_raw_audio_to_signals(payload)

    def route_voice_stream_to_google_stt(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        """Link: Voice Stream -> Google STT API."""
        # Use the real STT Agent for transcription
        from app.services.agents.stt_agent import SttAgent
        stt_agent = SttAgent()
        
        transcript = stt_agent.transcribe_voice_stream(
            call_session_id=payload.callSessionId,
            stream_ref=payload.streamRef
        )
        
        return stt_agent.emit_transcribed_text_from_google_stt_api(
            call_session_id=payload.callSessionId,
            transcript=transcript,
            metadata=payload.metadata
        )

    def route_google_stt_api_to_transcribed_text(self, payload: VoiceStreamPayload) -> TranscribedTextPayload:
        """Official Arrow: Google STT API -> Transcribed Text."""
        return self.route_voice_stream_to_google_stt(payload)

    def route_transcribed_text_to_threat_agent(self, payload: TranscribedTextPayload) -> list[AgentSignalScore]:
        """Official Arrow: Transcribed Text -> Threat Agent."""
        # This arrow triggers the threat analysis based on transcript
        # We wrap it in a SearchQueryPayload style context for the ThreatAgent
        return asyncio.run(self.threat_agent.analyze_transcribed_text_to_signals(payload.transcript, []))

    def route_search_query_to_threat_agent(self, payload: SearchQueryPayload) -> list[AgentSignalScore]:
        """Official Arrow: Search Query -> Threat Agent."""
        return asyncio.run(self.threat_agent.analyze_search_query_to_signals(payload, []))

    def route_text_metadata_to_entity_agent(self, payload: TextMetadataPayload) -> list[AgentSignalScore]:
        """Official Arrow: Text/Metadata -> Entity Agent."""
        scores = asyncio.run(self.entity_agent.analyze_text_metadata_to_signals(payload.text, payload.metadata))
        return [AgentSignalScore(signal_name="entity_score", score=s) for s in scores]

    def route_deepfake_signal_score_to_decision_engine(self, payload: DeepfakeSignalPayload) -> int:
        """Official Arrow: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        return self.decision_engine.ingest_deepfake_signal_scores([s.score for s in payload.signals])

    def route_entity_signal_score_to_decision_engine(self, payload: EntitySignalPayload) -> int:
        """Official Arrow: Entity Agent -> signal/score -> Decision & Reasoning Engine."""
        return self.decision_engine.ingest_entity_signal_scores([s.score for s in payload.signals])

    def route_threat_signal_score_to_decision_engine(self, payload: ThreatSignalPayload) -> int:
        """Official Arrow: Threat Agent -> signal/score -> Decision & Reasoning Engine."""
        return self.decision_engine.ingest_threat_signal_scores([s.score for s in payload.signals])

    def collect_signals_for_decision_engine(self, bundle: DecisionSignalBundle) -> int:
        """Official Link: Aggregate all signals for final decision."""
        result = self.decision_engine.aggregate_signal_scores(bundle)
        return result.get("total_score", 0)

    def exchange_reasoning_with_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Official Arrow: Decision & Reasoning Engine -> Gemini API Reasoning Engine."""
        return asyncio.run(self.reasoning_engine.request_reasoning_from_decision_signals(bundle))

    def route_decision_reasoning_explanation_to_gemini(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Official Link: Hand-off to Gemini reasoning."""
        return self.exchange_reasoning_with_gemini(bundle)

    def route_gemini_reasoning_explanation_to_decision(self, reasoning: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Official Arrow: Gemini API Reasoning Engine -> Decision & Reasoning Engine."""
        return reasoning

    def route_decision_and_reasoning_engine_to_json_score_warning(self, request: DecisionAndReasoningEngineToJsonScoreWarningRequest) -> JsonScoreWarningPayload:
        """Official Arrow: Decision & Reasoning Engine -> JSON score + warning."""
        return self.decision_engine.build_json_score_warning_payload(
            score=request.score,
            warning=request.warning,
            explanation=request.explanation
        )

    def route_json_score_warning_to_cloud_run_api_microservices(self, request: JsonScoreWarningToCloudRunApiMicroservicesRequest) -> None:
        """Official Arrow: JSON score + warning -> Cloud Run API Microservices."""
        # Final hand-off for potentially triggering external warnings or logs
        print(f"Final Outcome Propagated: Score={request.payload.riskScore}, Warning={request.payload.warning}")
