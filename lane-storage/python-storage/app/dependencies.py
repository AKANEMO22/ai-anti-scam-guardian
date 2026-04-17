from functools import lru_cache

from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.scam_pattern_repository import ScamPatternRepository
from app.repositories.vector_repository import VectorDbVertexAiRepository
from app.services.embedding_service import EmbeddingService
from app.services.internal_link_orchestrator import StorageInternalLinkOrchestrator
from app.services.rag_engine import LangChainRagEngine
from app.services.scam_pattern_service import ScamPatternService
from app.services.links.rag_vector_embedding_link import RagVectorEmbeddingLink
from app.services.links.scam_pattern_vector_link import ScamPatternVectorLink
from app.services.vector_db_vertex_ai_service import VectorDbVertexAiService


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


@lru_cache(maxsize=1)
def get_scam_pattern_repository() -> ScamPatternRepository:
    return ScamPatternRepository()


@lru_cache(maxsize=1)
def get_vector_db() -> VectorDbVertexAiRepository:
    return VectorDbVertexAiRepository()


@lru_cache(maxsize=1)
def get_feedback_repository() -> FeedbackRepository:
    return FeedbackRepository()


@lru_cache(maxsize=1)
def get_rag_engine() -> LangChainRagEngine:
    return LangChainRagEngine(
        embedding_service=get_embedding_service(),
        scam_pattern_repository=get_scam_pattern_repository(),
    )


@lru_cache(maxsize=1)
def get_vector_db_service() -> VectorDbVertexAiService:
    return VectorDbVertexAiService(repository=get_vector_db())


@lru_cache(maxsize=1)
def get_scam_pattern_service() -> ScamPatternService:
    return ScamPatternService(repository=get_scam_pattern_repository())


@lru_cache(maxsize=1)
def get_rag_vector_embedding_link() -> RagVectorEmbeddingLink:
    return RagVectorEmbeddingLink(
        rag_engine=get_rag_engine(),
        vector_db_service=get_vector_db_service(),
    )


@lru_cache(maxsize=1)
def get_scam_pattern_vector_link() -> ScamPatternVectorLink:
    return ScamPatternVectorLink(
        scam_pattern_service=get_scam_pattern_service(),
        vector_db_service=get_vector_db_service(),
    )


@lru_cache(maxsize=1)
def get_internal_link_orchestrator() -> StorageInternalLinkOrchestrator:
    return StorageInternalLinkOrchestrator(
        rag_engine=get_rag_engine(),
        vector_db_service=get_vector_db_service(),
        scam_pattern_service=get_scam_pattern_service(),
    )
