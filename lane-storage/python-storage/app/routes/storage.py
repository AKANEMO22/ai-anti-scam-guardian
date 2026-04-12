from fastapi import APIRouter, Depends

from app.dependencies import (
    get_feedback_repository,
    get_internal_link_orchestrator,
)
from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    EmbeddingLinkRequest,
    FeedbackEvent,
    IndexSignalRequest,
    PatternResolutionRequest,
    PatternSyncRequest,
    RagEngineLangChainToSearchQueryRequest,
    SearchRequest,
    SearchQueryToThreatAgentRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)
from app.repositories.feedback_repository import FeedbackRepository
from app.services.internal_link_orchestrator import StorageInternalLinkOrchestrator

router = APIRouter(tags=["storage"])


@router.post("/v1/storage/search")
def search_patterns(
    request: SearchRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """External API: delegate search to internal link Vector DB -> RAG Engine."""
    pass


@router.post("/v1/storage/index")
def index_signal(
    request: IndexSignalRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """External API: stage signal indexing flow toward RAG->Vector internal embedding link."""
    pass


@router.post("/v1/storage/feedback")
def submit_feedback(
    feedback: FeedbackEvent,
    repository: FeedbackRepository = Depends(get_feedback_repository),
) -> None:
    """External API: persist feedback event for storage feedback loop."""
    pass


@router.post("/v1/storage/internal/embeddings-rag-to-vector")
def internal_link_embeddings_rag_to_vector(
    request: EmbeddingLinkRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: embeddings path from RAG Engine to Vector DB Vertex AI."""
    pass


@router.post("/v1/storage/internal/vector-to-rag")
def internal_link_vector_to_rag(
    request: SearchRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: semantic retrieval path from Vector DB Vertex AI to RAG Engine."""
    pass


@router.post("/v1/storage/internal/rag-engine-langchain-to-search-query")
def internal_link_rag_engine_langchain_to_search_query(
    request: RagEngineLangChainToSearchQueryRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: RAG Engine LangChain -> Search Query."""
    pass


@router.post("/v1/storage/internal/search-query-to-threat-agent")
def internal_link_search_query_to_threat_agent(
    request: SearchQueryToThreatAgentRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Search Query -> Threat Agent."""
    pass


@router.post("/v1/storage/internal/scam-pattern-to-vector")
def internal_link_scam_pattern_to_vector(
    request: PatternSyncRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: sync path from Scam Pattern catalog into Vector DB metadata."""
    pass


@router.post("/v1/storage/internal/vector-to-scam-pattern")
def internal_link_vector_to_scam_pattern(
    request: PatternResolutionRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: resolve pattern IDs from Vector DB hits back to Scam Pattern records."""
    pass


@router.post("/v1/storage/internal/cloud-run-api-microservices-to-update-database")
def internal_link_cloud_run_api_microservices_to_update_database(
    request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Cloud Run API Microservices -> Update database."""
    pass


@router.post("/v1/storage/internal/update-database-to-vector-database-vertex-ai")
def internal_link_update_database_to_vector_database_vertex_ai(
    request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    """Internal link: Update database -> Vector Database Vertex AI."""
    pass
