from functools import lru_cache

from app.clients.storage_client import StorageClient
from app.services.internal_link_orchestrator import AgenticInternalLinkOrchestrator
from app.services.orchestrator import OrchestratorService


@lru_cache(maxsize=1)
def get_storage_client() -> StorageClient:
    return StorageClient()


@lru_cache(maxsize=1)
def get_orchestrator_service() -> OrchestratorService:
    return OrchestratorService()


@lru_cache(maxsize=1)
def get_internal_link_orchestrator() -> AgenticInternalLinkOrchestrator:
    return AgenticInternalLinkOrchestrator(orchestrator=get_orchestrator_service())
