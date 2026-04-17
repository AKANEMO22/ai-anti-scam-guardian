from functools import lru_cache

from app.clients.agentic_core_client import AgenticCoreClient
from app.clients.storage_client import StorageClient
from app.config import Settings, get_settings as load_settings
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache
from app.services.internal_link_orchestrator import ApiGatewayInternalLinkOrchestrator


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()


@lru_cache(maxsize=1)
def get_auth_service() -> AuthService:
    return AuthService(settings=get_settings())


@lru_cache(maxsize=1)
def get_cache_service() -> InMemoryRiskCache:
    return InMemoryRiskCache(ttl_seconds=180)


@lru_cache(maxsize=1)
def get_agentic_core_client() -> AgenticCoreClient:
    return AgenticCoreClient(settings=get_settings())


@lru_cache(maxsize=1)
def get_storage_client() -> StorageClient:
    return StorageClient(settings=get_settings())


@lru_cache(maxsize=1)
def get_api_gateway_internal_link_orchestrator() -> ApiGatewayInternalLinkOrchestrator:
    return ApiGatewayInternalLinkOrchestrator(
        auth_service=get_auth_service(),
        cache_service=get_cache_service(),
    )
