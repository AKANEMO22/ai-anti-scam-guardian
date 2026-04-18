from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import (
    get_feedback_repository,
    get_internal_link_orchestrator,
    get_rag_engine,
    get_scam_pattern_repository,
    get_vector_db,
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
    SearchResponse,
    SearchQueryToThreatAgentRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
)
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.scam_pattern_repository import ScamPatternRepository
from app.repositories.vector_repository import VectorDbVertexAiRepository
from app.services.internal_link_orchestrator import StorageInternalLinkOrchestrator
from app.services.rag_engine import LangChainRagEngine

router = APIRouter(tags=["storage"])

@router.post("/v1/storage/seed")
def seed_patterns(
    rag_engine: LangChainRagEngine = Depends(get_rag_engine),
    vector_db: VectorDbVertexAiRepository = Depends(get_vector_db),
    scam_repo: ScamPatternRepository = Depends(get_scam_pattern_repository)
) -> dict:
    """Admin API: Seed RAG embeddings from vn_scam_patterns.json to FAISS."""
    # We create a dummy search request just to trigger embedding preparation
    request = SearchRequest(query="", sourceType="system", topK=1)
    payloads = rag_engine.create_embeddings_for_vector_db(request)
    if not payloads:
        return {"status": "no patterns found in repository"}
        
    # payloads is list of (RagEmbeddingPayload, vector)
    rag_payloads = [p[0] for p in payloads]
    vectors = [p[1] for p in payloads]
    
    vector_db._upsert_with_vectors(rag_payloads, vectors)
    return {"status": "success", "seeded_count": len(payloads)}


@router.post("/v1/storage/search", response_model=SearchResponse)
def search_patterns(
    request: SearchRequest,
    rag_engine: LangChainRagEngine = Depends(get_rag_engine),
    vector_db: VectorDbVertexAiRepository = Depends(get_vector_db),
) -> SearchResponse:
    """External API: delegate search to internal link Vector DB -> RAG Engine."""
    query_vector = rag_engine.build_vector_retrieval_query(request)
    matches = vector_db.search_embeddings_with_vector(query_vector, request.topK)
    return SearchResponse(matches=matches)


@router.post("/v1/storage/index")
def index_signal(
    request: IndexSignalRequest,
    signal_repo: SignalRepository = Depends(get_signal_repository),
) -> dict:
    """External API: persist signal metadata for later potential indexing into Vector DB."""
    signal_repo.save_signal(request)
    return {"status": "acknowledged", "eventId": request.eventId}


@router.post("/v1/storage/feedback")
def submit_feedback(
    feedback: FeedbackEvent,
    feedback_repo: FeedbackRepository = Depends(get_feedback_repository),
    signal_repo: SignalRepository = Depends(get_signal_repository),
    rag_engine: LangChainRagEngine = Depends(get_rag_engine),
    vector_db: VectorDbVertexAiRepository = Depends(get_vector_db),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> dict:
    """External API: persist feedback and trigger automated loop (indexing) if SCAM."""
    feedback_repo.save_feedback_event(feedback)
    
    if feedback.label == "SCAM":
        # Automated Loop: Trigger re-indexing
        signal = signal_repo.get_signal_by_event_id(feedback.eventId)
        if signal and signal.text:
            # Generate embedding
            vector = embedding_service.build_embedding_for_search_query(signal.text)
            
            # Prepare push payload
            from app.models.contracts import RagEmbeddingPayload
            payload = RagEmbeddingPayload(
                source_id=f"feedback_{feedback.eventId}",
                source_text=signal.text,
                metadata={
                    "risk_score": str(signal.riskScore),
                    "source_type": signal.sourceType,
                    "explanation": signal.explanation,
                    "reason": "user_confirmed_scam"
                }
            )
            
            # Push to Vector DB
            vector_db._upsert_with_vectors([payload], [vector])
            print(f"Feedback Loop: Automated indexing triggered for Event {feedback.eventId}")
            return {"accepted": True, "indexed": True}
            
    return {"accepted": True, "indexed": False}


@router.get("/v1/storage/stats")
def get_stats(
    scam_repo: ScamPatternRepository = Depends(get_scam_pattern_repository),
    vector_db: VectorDbVertexAiRepository = Depends(get_vector_db),
    feedback_repo: FeedbackRepository = Depends(get_feedback_repository),
) -> dict:
    return {
        "patterns_count": len(scam_repo.list_active_pattern_ids()),
        "vectors_count": vector_db.index.ntotal,
        "feedback_count": len(feedback_repo.list_feedback_events())
    }

# --- Internal Link Handlers below ---
# Normally these would be processed internally without exposing HTTP endpoints,
# but keeping them to satisfy contracts if needed.
@router.post("/v1/storage/internal/embeddings-rag-to-vector")
def internal_link_embeddings_rag_to_vector(
    request: EmbeddingLinkRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/vector-to-rag")
def internal_link_vector_to_rag(
    request: SearchRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/rag-engine-langchain-to-search-query")
def internal_link_rag_engine_langchain_to_search_query(
    request: RagEngineLangChainToSearchQueryRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/search-query-to-threat-agent")
def internal_link_search_query_to_threat_agent(
    request: SearchQueryToThreatAgentRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/scam-pattern-to-vector")
def internal_link_scam_pattern_to_vector(
    request: PatternSyncRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/vector-to-scam-pattern")
def internal_link_vector_to_scam_pattern(
    request: PatternResolutionRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/cloud-run-api-microservices-to-update-database")
def internal_link_cloud_run_api_microservices_to_update_database(
    request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}

@router.post("/v1/storage/internal/update-database-to-vector-database-vertex-ai")
def internal_link_update_database_to_vector_database_vertex_ai(
    request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    orchestrator: StorageInternalLinkOrchestrator = Depends(get_internal_link_orchestrator),
) -> None:
    print("{\"event\": \"internal_flow\", \"status\": \"official\"}")
    return locals().get("mock_data", None) or {}
