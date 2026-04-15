from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import (
    get_feedback_repository,
    get_internal_link_orchestrator,
)
from app.models.contracts import (
    AckResponse,
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    EmbeddingLinkRequest,
    FeedbackEvent,
    IndexSignalRequest,
    PatternMatch,
    PatternResolutionRequest,
    PatternSyncRequest,
    RagEngineLangChainToSearchQueryRequest,
    SearchQueryPayload,
    SearchQueryToThreatAgentRequest,
    SearchRequest,
    SearchResponse,
    UpdateDatabasePayload,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)
from app.repositories.feedback_repository import FeedbackRepository
from app.services.internal_link_orchestrator import StorageInternalLinkOrchestrator

router = APIRouter(tags=["storage"])


@router.post("/v1/storage/search")
def search_patterns(
    request: SearchRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> SearchResponse:
    """External API: delegate search to internal link Vector DB -> RAG Engine."""
    try: 
        matches: list[PatternMatch] = orchestrator.link_semantic_matches_vector_db_to_rag_engine(request)
        return SearchResponse(matches=matches or [])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/index")
def index_signal(
    request: IndexSignalRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> AckResponse:
    """External API: stage signal indexing flow toward RAG->Vector internal embedding link."""
    try: 
        # Chuyển IndexSignalRequest thành EmbeddingLinkRequest để đưa vào RAG path
        from app.models.contracts import RagEmbeddingPayload

        source_text = request.text or request.explanation
        embedding_payload = RagEmbeddingPayload(
            source_id=request.eventId,
            source_text=source_text,
            metadata={
                "sourceType": request.sourceType,
                "riskScore": str(request.riskScore),
                "textScore": str(request.textScore),
                "entityScore": str(request.entityScore),
                **request.metadata,
            },
        )
        embedding_request = EmbeddingLinkRequest(items= [embedding_payload])
        orchestrator.link_embeddings_rag_engine_to_vector_db(embedding_request)
        return AckResponse(accepted=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/feedback")
def submit_feedback(
    feedback: FeedbackEvent,
    repository: FeedbackRepository = Depends(get_feedback_repository),
) -> AckResponse:
    """External API: persist feedback event for storage feedback loop."""
    try:
        repository.save_feedback_event(feedback)
        return AckResponse(accepted=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

@router.post("/v1/storage/internal/embeddings-rag-to-vector")
def internal_link_embeddings_rag_to_vector(
    request: EmbeddingLinkRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> AckResponse:
    """Internal link: embeddings path from RAG Engine to Vector DB Vertex AI."""
    try:
        orchestrator.link_embeddings_rag_engine_to_vector_db(request)
        return AckResponse(accepted=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/vector-to-rag")
def internal_link_vector_to_rag(
    request: SearchRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> SearchResponse:
    """Internal link: semantic retrieval path from Vector DB Vertex AI to RAG Engine."""
    try:
        matches: list[PatternMatch] = orchestrator.link_semantic_matches_vector_db_to_rag_engine(request)
        return SearchResponse(matches=matches or [])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/rag-engine-langchain-to-search-query")
def internal_link_rag_engine_langchain_to_search_query(
    request: RagEngineLangChainToSearchQueryRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> SearchQueryPayload:
    """Internal link: RAG Engine LangChain -> Search Query."""
    try:
        payload: SearchQueryPayload = orchestrator.link_rag_engine_langchain_to_search_query(request)
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    

@router.post("/v1/storage/internal/search-query-to-threat-agent")
def internal_link_search_query_to_threat_agent(
    request: SearchQueryToThreatAgentRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> SearchQueryPayload:
    """Internal link: Search Query -> Threat Agent."""
    try:
        payload: SearchQueryPayload = orchestrator.link_search_query_to_threat_agent(request)
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/scam-pattern-to-vector")
def internal_link_scam_pattern_to_vector(
    request: PatternSyncRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> AckResponse:
    """Internal link: sync path from Scam Pattern catalog into Vector DB metadata."""
    try:
        orchestrator.link_scam_pattern_to_vector_db(request)
        return AckResponse(accepted=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/vector-to-scam-pattern")
def internal_link_vector_to_scam_pattern(
    request: PatternResolutionRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> list[str]:
    """Internal link: resolve pattern IDs from Vector DB hits back to Scam Pattern records."""
    try:
        pattern_texts: list[str] = orchestrator.link_vector_db_to_scam_pattern(request)
        return pattern_texts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/cloud-run-api-microservices-to-update-database")
def internal_link_cloud_run_api_microservices_to_update_database(
    request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> UpdateDatabasePayload:
    """Internal link: Cloud Run API Microservices -> Update database."""
    try:
        payload: UpdateDatabasePayload = orchestrator.link_cloud_run_api_microservices_to_update_database(request)
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/v1/storage/internal/update-database-to-vector-database-vertex-ai")
def internal_link_update_database_to_vector_database_vertex_ai(
    request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> AckResponse:
    """Internal link: Update database -> Vector Database Vertex AI."""
    try:
        orchestrator.link_update_database_to_vector_database_vertex_ai(request)
        return AckResponse(accepted=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
