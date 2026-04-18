from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    SMS = "SMS"
    URL = "URL"
    CALL = "CALL"


class SignalRequest(BaseModel):
    sourceType: SourceType
    text: Optional[str] = None
    callSessionId: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class RiskResponse(BaseModel):
    riskScore: int = Field(ge=0, le=100)
    explanation: str
    voiceScore: int = Field(ge=0, le=100)
    textScore: int = Field(ge=0, le=100)
    entityScore: int = Field(ge=0, le=100)
    piiScore: int = Field(default=0, ge=0, le=100)
    engagementScore: int = Field(default=0, ge=0, le=100)
    piiTypes: list[str] = Field(default_factory=list)
    baiterResponse: Optional[str] = None
    cacheHit: bool = False


class FeedbackEvent(BaseModel):
    eventId: str
    userId: str
    label: str
    sourceType: SourceType
    riskScore: Optional[int] = Field(default=None, ge=0, le=100)
    timestamp: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class FeedbackAck(BaseModel):
    accepted: bool


class FirebaseAuthClaims(BaseModel):
    uid: str = ""
    email: Optional[str] = None
    provider: Optional[str] = None
    issuedAt: Optional[str] = None


class AuthenticatedDataPayload(BaseModel):
    claims: FirebaseAuthClaims = Field(default_factory=FirebaseAuthClaims)
    sourceType: Optional[SourceType] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class CloudRunMicroserviceTarget(str, Enum):
    AGENTIC_CORE = "AGENTIC_CORE"
    STORAGE = "STORAGE"
    FEEDBACK = "FEEDBACK"


class FirebaseAuthToAuthenticatedDataRequest(BaseModel):
    authorization: Optional[str] = None
    sourceType: Optional[SourceType] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class AuthenticatedDataToCloudRunRequest(BaseModel):
    authenticatedData: AuthenticatedDataPayload
    target: CloudRunMicroserviceTarget
    payload: Dict[str, Any] = Field(default_factory=dict)


class CacheLayerType(str, Enum):
    REDIS = "REDIS"


class TrafficDataType(str, Enum):
    PHONE = "PHONE"
    URL = "URL"
    SCRIPT = "SCRIPT"


class CloudRunMicroserviceResultPayload(BaseModel):
    microservice: CloudRunMicroserviceTarget = CloudRunMicroserviceTarget.AGENTIC_CORE
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    metadata: Dict[str, str] = Field(default_factory=dict)
    response: Dict[str, Any] = Field(default_factory=dict)


class CloudRunToCacheRequest(BaseModel):
    result: CloudRunMicroserviceResultPayload
    cacheLayer: CacheLayerType = CacheLayerType.REDIS
    cacheKey: Optional[str] = None


class CloudRunToCacheLookupRequest(BaseModel):
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    cacheLayer: CacheLayerType = CacheLayerType.REDIS
    cacheKey: str


class CacheLookupResultPayload(BaseModel):
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    cacheLayer: CacheLayerType = CacheLayerType.REDIS
    cacheKey: str
    cacheHit: bool = False
    metadata: Dict[str, str] = Field(default_factory=dict)


class CacheLayerToCacheMissRequest(BaseModel):
    lookup: CacheLookupResultPayload
    signal: SignalRequest


class CloudRunApiMicroservicesToCacheMissRequest(BaseModel):
    result: CloudRunMicroserviceResultPayload
    signal: SignalRequest
    cacheKey: Optional[str] = None


class CacheMissToOrchestratorAgentLangGraphRouterRequest(BaseModel):
    lookup: CacheLookupResultPayload
    signal: SignalRequest


class CloudRunApiMicroservicesToUpdateDatabaseRequest(BaseModel):
    result: CloudRunMicroserviceResultPayload
    signal: SignalRequest
    updateKey: Optional[str] = None


class UpdateDatabaseToVectorDatabaseVertexAiRequest(BaseModel):
    updateKey: str
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=dict)


class FeedbackLabelType(str, Enum):
    SCAM = "SCAM"
    SAFE = "SAFE"
    NOT_SURE = "NOT_SURE"


class UserFeedbackLabelPayload(BaseModel):
    eventId: str
    userId: str
    label: FeedbackLabelType
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    riskScore: Optional[int] = Field(default=None, ge=0, le=100)
    metadata: Dict[str, str] = Field(default_factory=dict)


class UserFeedbackToFeedbackLabelRequest(BaseModel):
    payload: UserFeedbackLabelPayload


class FeedbackLabelToIngestionRequest(BaseModel):
    payload: UserFeedbackLabelPayload


class FeedbackIngestionResultPayload(BaseModel):
    payload: UserFeedbackLabelPayload
    accepted: bool = True
    ingestionRef: Optional[str] = None


class FeedbackIngestionToCacheRequest(BaseModel):
    result: FeedbackIngestionResultPayload
    cacheLayer: CacheLayerType = CacheLayerType.REDIS
    cacheKey: Optional[str] = None


class FeedbackIngestionToCacheLookupRequest(BaseModel):
    dataType: TrafficDataType = TrafficDataType.SCRIPT
    cacheLayer: CacheLayerType = CacheLayerType.REDIS
    cacheKey: str
