from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    SMS = "SMS"
    URL = "URL"
    CALL = "CALL"


class SignalPayload(BaseModel):
    sourceType: SourceType
    text: Optional[str] = ""
    callSessionId: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class PatternMatch(BaseModel):
    pattern_id: str
    pattern_text: str
    score: float = Field(ge=0.0, le=1.0)


class RawAudioPayload(BaseModel):
    callSessionId: Optional[str] = None
    rawAudioRef: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class VoiceStreamPayload(BaseModel):
    callSessionId: Optional[str] = None
    streamRef: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class TranscribedTextPayload(BaseModel):
    callSessionId: Optional[str] = None
    transcript: str = ""
    metadata: Dict[str, str] = Field(default_factory=dict)


class TextMetadataPayload(BaseModel):
    text: str = ""
    metadata: Dict[str, str] = Field(default_factory=dict)


class AgentSignalScore(BaseModel):
    signal_name: str
    score: float = Field(ge=0.0, le=100.0)
    reason: Optional[str] = None


class DeepfakeSignalPayload(BaseModel):
    signals: List[AgentSignalScore] = Field(default_factory=list)
    source: str = "deepfake-agent"
    metadata: Dict[str, str] = Field(default_factory=dict)


class ThreatSignalPayload(BaseModel):
    signals: List[AgentSignalScore] = Field(default_factory=list)
    source: str = "threat-agent"
    metadata: Dict[str, str] = Field(default_factory=dict)


class EntitySignalPayload(BaseModel):
    signals: List[AgentSignalScore] = Field(default_factory=list)
    source: str = "entity-agent"
    metadata: Dict[str, str] = Field(default_factory=dict)


class DecisionSignalBundle(BaseModel):
    deepfake_signals: List[AgentSignalScore] = Field(default_factory=list)
    threat_signals: List[AgentSignalScore] = Field(default_factory=list)
    entity_signals: List[AgentSignalScore] = Field(default_factory=list)


class GeminiReasoningPayload(BaseModel):
    summary: str = ""
    explanation: str = ""


class JsonScoreWarningPayload(BaseModel):
    riskScore: int = Field(ge=0, le=100)
    warning: str = ""
    explanation: str = ""
    metadata: Dict[str, str] = Field(default_factory=dict)


class InternalAck(BaseModel):
    accepted: bool


class RawAudioToDeepfakeRequest(BaseModel):
    payload: RawAudioPayload


class OrchestratorToRawAudioRequest(BaseModel):
    payload: SignalPayload


class OrchestratorToVoiceStreamRequest(BaseModel):
    payload: SignalPayload


class VoiceStreamToSttRequest(BaseModel):
    payload: VoiceStreamPayload


class GoogleSttApiToTranscribedTextRequest(BaseModel):
    payload: VoiceStreamPayload


class SttToThreatRequest(BaseModel):
    payload: TranscribedTextPayload


class GoogleSttToThreatRequest(BaseModel):
    payload: TranscribedTextPayload


class TranscribedTextToThreatAgentRequest(BaseModel):
    payload: TranscribedTextPayload


class SearchQueryPayload(BaseModel):
    query: str = ""
    sourceType: SourceType = SourceType.CALL
    topK: int = Field(default=5, ge=1, le=50)
    metadata: Dict[str, str] = Field(default_factory=dict)


class SearchQueryToThreatAgentRequest(BaseModel):
    payload: SearchQueryPayload


class TextMetadataToEntityRequest(BaseModel):
    payload: TextMetadataPayload


class OrchestratorToTextMetadataRequest(BaseModel):
    payload: SignalPayload


class EntityToDecisionRequest(BaseModel):
    payload: EntitySignalPayload


class ThreatToDecisionRequest(BaseModel):
    payload: ThreatSignalPayload


class DeepfakeToDecisionRequest(BaseModel):
    payload: DeepfakeSignalPayload


class AgentToDecisionRequest(BaseModel):
    signals: List[AgentSignalScore] = Field(default_factory=list)


class DecisionToGeminiRequest(BaseModel):
    bundle: DecisionSignalBundle


class GeminiToDecisionRequest(BaseModel):
    reasoning: GeminiReasoningPayload


class DecisionReasoningExplanationToGeminiRequest(BaseModel):
    reasoning_context: DecisionSignalBundle


class GeminiReasoningExplanationToDecisionRequest(BaseModel):
    reasoning: GeminiReasoningPayload


class DecisionAndReasoningEngineToJsonScoreWarningRequest(BaseModel):
    score: int = Field(ge=0, le=100)
    warning: str = ""
    explanation: str = ""
    metadata: Dict[str, str] = Field(default_factory=dict)


class JsonScoreWarningToCloudRunApiMicroservicesRequest(BaseModel):
    payload: JsonScoreWarningPayload


class RiskResponse(BaseModel):
    riskScore: int = Field(ge=0, le=100)
    explanation: str
    voiceScore: int = Field(ge=0, le=100)
    textScore: int = Field(ge=0, le=100)
    entityScore: int = Field(ge=0, le=100)
    cacheHit: bool = False
    matchedPatterns: List[PatternMatch] = Field(default_factory=list)
