from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    FeedbackIngestionToCacheLookupRequest,
    FeedbackIngestionToCacheRequest,
    FeedbackLabelToIngestionRequest,
    UserFeedbackToFeedbackLabelRequest,
)
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/user-feedback-to-feedback-label")
def internal_user_feedback_to_feedback_label(
    request: UserFeedbackToFeedbackLabelRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: user feedback (scam/safe/not sure) -> feedback label."""
    pass


@router.post("/v1/gateway/internal/feedback-label-to-feedback-ingestion")
async def internal_feedback_label_to_feedback_ingestion(
    request: FeedbackLabelToIngestionRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: feedback label -> feedback ingestion."""
    await internal_orchestrator.link_feedback_label_to_ingestion(request)


@router.post("/v1/gateway/internal/feedback-ingestion-to-cache-layer")
async def internal_feedback_ingestion_to_cache_layer(
    request: FeedbackIngestionToCacheRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: feedback ingestion -> Cache Layer (redis) by phone/url/script."""
    await internal_orchestrator.link_feedback_ingestion_to_cache(request)


@router.post("/v1/gateway/internal/feedback-ingestion-to-cache-layer-lookup")
def internal_feedback_ingestion_to_cache_layer_lookup(
    request: FeedbackIngestionToCacheLookupRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal lookup link for feedback-ingestion cache keys in phone/url/script channels."""
    pass