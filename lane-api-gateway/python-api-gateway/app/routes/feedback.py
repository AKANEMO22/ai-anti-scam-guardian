from fastapi import APIRouter, Depends, Header, BackgroundTasks

from app.dependencies import get_auth_service, get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    FeedbackAck, 
    FeedbackEvent, 
    UserFeedbackLabelPayload, 
    FeedbackLabelToIngestionRequest,
    FeedbackLabelType,
    TrafficDataType,
    SourceType
)
from app.services.auth_service import AuthService
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["feedback"])

def _map_source_type_to_traffic_data_type(source: SourceType) -> TrafficDataType:
    if source == SourceType.CALL:
        return TrafficDataType.PHONE
    elif source == SourceType.URL:
        return TrafficDataType.URL
    return TrafficDataType.SCRIPT

def _map_feedback_label_to_type(label: str) -> FeedbackLabelType:
    label_val = label.upper()
    if label_val == "SCAM":
        return FeedbackLabelType.SCAM
    elif label_val == "SAFE":
        return FeedbackLabelType.SAFE
    return FeedbackLabelType.NOT_SURE

# PURPOSE: 
# This file handles the user feedback loop. When a user tells the app: 
# "You said this was a scam, but it's safe" (or vice versa), this endpoint receives it.
# EVENTUAL GOAL:
# Sends this correction to the Storage lane so our AI models can be retrained over time.

@router.post("/v1/feedback", response_model=FeedbackAck)
async def submit_feedback(
    feedback: FeedbackEvent,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    auth_service: AuthService = Depends(get_auth_service),
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(get_api_gateway_internal_link_orchestrator),
) -> FeedbackAck:
    auth_service.validate_bearer_token(authorization)
    
    # Map the incoming FeedbackEvent into the internal Link Orchestrator payload
    payload = UserFeedbackLabelPayload(
        eventId=feedback.eventId,
        userId=feedback.userId,
        label=_map_feedback_label_to_type(feedback.label),
        dataType=_map_source_type_to_traffic_data_type(feedback.sourceType),
        riskScore=feedback.riskScore,
        metadata={"timestamp": feedback.timestamp}
    )
    
    request = FeedbackLabelToIngestionRequest(payload=payload)
    
    # Hand off the work to the background orchestrator
    background_tasks.add_task(
        internal_orchestrator.link_feedback_label_to_ingestion,
        request
    )
    
    # Return instantly to the mobile app
    return FeedbackAck(accepted=True)
