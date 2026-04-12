from fastapi import APIRouter, Depends, Header

from app.clients.storage_client import StorageClient
from app.dependencies import get_auth_service, get_storage_client
from app.models.contracts import FeedbackAck, FeedbackEvent
from app.services.auth_service import AuthService

router = APIRouter(tags=["feedback"])


@router.post("/v1/feedback", response_model=FeedbackAck)
async def submit_feedback(
    feedback: FeedbackEvent,
    authorization: str | None = Header(default=None),
    auth_service: AuthService = Depends(get_auth_service),
    storage_client: StorageClient = Depends(get_storage_client),
) -> FeedbackAck:
    auth_service.validate_bearer_token(authorization)
    accepted = await storage_client.submit_feedback(feedback)
    return FeedbackAck(accepted=accepted)
