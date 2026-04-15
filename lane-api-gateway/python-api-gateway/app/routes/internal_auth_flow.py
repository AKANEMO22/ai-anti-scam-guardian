from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import AuthenticatedDataToCloudRunRequest, FirebaseAuthToAuthenticatedDataRequest, AuthenticatedDataPayload
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/firebase-auth-to-authenticated-data")
def internal_firebase_auth_to_authenticated_data(
    request: FirebaseAuthToAuthenticatedDataRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> AuthenticatedDataPayload:
    """Internal link: Firebase Auth -> Authenticated Data."""
    return internal_orchestrator.link_firebase_auth_to_authenticated_data(request)


@router.post("/v1/gateway/internal/authenticated-data-to-cloud-run-api-microservices")
def internal_authenticated_data_to_cloud_run_api_microservices(
    request: AuthenticatedDataToCloudRunRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Authenticated Data -> Cloud Run API Microservices."""
    pass