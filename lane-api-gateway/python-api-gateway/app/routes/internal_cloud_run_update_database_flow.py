from fastapi import APIRouter, Depends

from app.dependencies import get_api_gateway_internal_link_orchestrator
from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator

router = APIRouter(tags=["api-gateway-internal"])


@router.post("/v1/gateway/internal/cloud-run-api-microservices-to-update-database")
def internal_cloud_run_api_microservices_to_update_database(
    request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Cloud Run API Microservices -> Update database."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}


@router.post("/v1/gateway/internal/update-database-to-vector-database-vertex-ai")
def internal_update_database_to_vector_database_vertex_ai(
    request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    internal_orchestrator: ApiGatewayInternalLinkOrchestrator = Depends(
        get_api_gateway_internal_link_orchestrator,
    ),
) -> None:
    """Internal link: Update database -> Vector Database Vertex AI."""
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}
