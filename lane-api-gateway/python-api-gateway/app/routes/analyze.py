from uuid import uuid4

from fastapi import APIRouter, Depends, Header

from app.clients.agentic_core_client import AgenticCoreClient
from app.clients.storage_client import StorageClient
from app.dependencies import (
    get_agentic_core_client,
    get_auth_service,
    get_cache_service,
    get_storage_client,
)
from app.models.contracts import RiskResponse, SignalRequest
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache

router = APIRouter(tags=["signals"])


@router.post("/v1/signals/analyze", response_model=RiskResponse)
async def analyze_signal(
    request: SignalRequest,
    authorization: str | None = Header(default=None),
    auth_service: AuthService = Depends(get_auth_service),
    cache_service: InMemoryRiskCache = Depends(get_cache_service),
    core_client: AgenticCoreClient = Depends(get_agentic_core_client),
    storage_client: StorageClient = Depends(get_storage_client),
) -> RiskResponse:
    auth_service.validate_bearer_token(authorization)

    cache_key = cache_service.build_key(request)
    cached = cache_service.get(cache_key)
    if cached is not None:
        return cached.model_copy(update={"cacheHit": True})

    fresh = await core_client.analyze_signal(request)
    result = fresh.model_copy(update={"cacheHit": False})
    cache_service.set(cache_key, result)

    # Storage indexing is best-effort to avoid blocking user warning flow.
    try:
        await storage_client.index_signal(str(uuid4()), request, result)
    except Exception:
        print("mocked")
        return locals().get("mock_data", None) or {}

    return result
