from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PatternMatch(BaseModel):
    pattern_id: str
    pattern_text: str
    score: float = Field(ge=0.0, le=1.0)


class SearchRequest(BaseModel):
    query: str
    sourceType: str
    topK: int = Field(default=5, ge=1, le=20)


class SearchResponse(BaseModel):
    matches: List[PatternMatch] = Field(default_factory=list)


class SearchQueryPayload(BaseModel):
    query: str
    sourceType: str
    topK: int = Field(default=5, ge=1, le=20)
    metadata: Dict[str, str] = Field(default_factory=dict)


class RagEngineLangChainToSearchQueryRequest(BaseModel):
    query: SearchRequest
    traceId: Optional[str] = None


class SearchQueryToThreatAgentRequest(BaseModel):
    payload: SearchQueryPayload


class IndexSignalRequest(BaseModel):
    eventId: str
    sourceType: str
    text: Optional[str] = None
    callSessionId: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    riskScore: int = Field(ge=0, le=100)
    explanation: str
    textScore: int = Field(ge=0, le=100)
    entityScore: int = Field(ge=0, le=100)


class CloudRunApiMicroservicesResultPayload(BaseModel):
    microservice: str = "AGENTIC_CORE"
    dataType: str = "SCRIPT"
    metadata: Dict[str, str] = Field(default_factory=dict)
    response: Dict[str, object] = Field(default_factory=dict)


class CloudRunApiMicroservicesToUpdateDatabaseRequest(BaseModel):
    result: CloudRunApiMicroservicesResultPayload
    updateKey: Optional[str] = None


class UpdateDatabasePayload(BaseModel):
    updateKey: str
    dataType: str = "SCRIPT"
    payload: Dict[str, object] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=dict)


class UpdateDatabaseToVectorDatabaseVertexAiRequest(BaseModel):
    payload: UpdateDatabasePayload


class FeedbackEvent(BaseModel):
    eventId: str
    label: str
    sourceType: str
    riskScore: Optional[int] = Field(default=None, ge=0, le=100)
    timestamp: str


class AckResponse(BaseModel):
    accepted: bool


class RagEmbeddingPayload(BaseModel):
    source_id: str
    source_text: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    vector: Optional[List[float]] = None


class EmbeddingLinkRequest(BaseModel):
    items: List[RagEmbeddingPayload] = Field(default_factory=list)


class VectorRetrievalRequest(BaseModel):
    query_vector: List[float]
    topK: int = Field(default=5, ge=1, le=50)


class PatternSyncRequest(BaseModel):
    pattern_ids: List[str] = Field(default_factory=list)


class PatternResolutionRequest(BaseModel):
    embedding_ids: List[str] = Field(default_factory=list)
