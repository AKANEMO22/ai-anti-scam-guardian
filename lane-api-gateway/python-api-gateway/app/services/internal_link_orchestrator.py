from app.models.contracts import (
    AuthenticatedDataPayload,
    AuthenticatedDataToCloudRunRequest,
    CacheLayerToCacheMissRequest,
    CacheMissToOrchestratorAgentLangGraphRouterRequest,
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    CloudRunApiMicroservicesToCacheMissRequest,
    CloudRunToCacheLookupRequest,
    CloudRunToCacheRequest,
    FeedbackIngestionToCacheLookupRequest,
    FeedbackIngestionToCacheRequest,
    FeedbackLabelToIngestionRequest,
    FirebaseAuthToAuthenticatedDataRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
    UserFeedbackToFeedbackLabelRequest,
)
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache


class ApiGatewayInternalLinkOrchestrator:
    """
    PURPOSE:
    The "Factory Manager" for the Gateway pipeline.
    EVENTUAL GOAL:
    It orchestrates the flow of data between different states. It tells the system:
    'Take unauthenticated data -> send to Auth Link -> if passed, send to Cache Link 
    -> if it misses cache, send to AI Link.' It wires the Channels and Links together.
    """
    def __init__(self, auth_service: AuthService, cache_service: InMemoryRiskCache) -> None:
        self._auth_service = auth_service
        self._cache_service = cache_service

    def link_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Internal link: Firebase Auth -> Authenticated Data."""
        pass

    def link_authenticated_data_to_cloud_run_api_microservices(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> None:
        """Internal link: Authenticated Data -> Cloud Run API Microservices."""
        pass

    def link_cloud_run_api_microservices_to_cache_layer(
        self,
        request: CloudRunToCacheRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> Cache Layer (redis)."""
        pass

    def link_cloud_run_api_microservices_to_cache_layer_lookup(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> None:
        """Internal lookup link for Cloud Run API Microservices cache keys (phone/url/script)."""
        pass

    def link_cache_layer_to_cache_miss(self, request: CacheLayerToCacheMissRequest) -> None:
        """Internal link: Cache Layer (redis) phone/url/script -> cache miss."""
        pass

    def link_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> cache miss."""
        pass

    def link_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Internal link: cache miss -> Orchestrator Agent LangGraph Router."""
        pass

    def link_cloud_run_api_microservices_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Internal link: cache miss (from Cloud Run API Microservices) -> Orchestrator Agent LangGraph Router."""
        pass

    def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> Update database."""
        pass

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Internal link: Update database -> Vector Database Vertex AI."""
        pass

    def link_user_feedback_to_feedback_label(self, request: UserFeedbackToFeedbackLabelRequest) -> None:
        """Internal link: user feedback (scam/safe/not sure) -> feedback label."""
        pass

    def link_feedback_label_to_feedback_ingestion(self, request: FeedbackLabelToIngestionRequest) -> None:
        """Internal link: feedback label -> feedback ingestion."""
        pass

    def link_feedback_ingestion_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Internal link: feedback ingestion -> Cache Layer (redis) by phone/url/script."""
        pass

    def link_feedback_ingestion_to_cache_layer_lookup(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> None:
        """Internal lookup link for feedback-ingestion cache keys (phone/url/script)."""
        pass