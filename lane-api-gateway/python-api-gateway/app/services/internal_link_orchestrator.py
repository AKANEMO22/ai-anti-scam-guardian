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
    CacheLookupResultPayload,
)
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache
from app.clients.agentic_core_client import AgenticCoreClient
from app.clients.storage_client import StorageClient
from app.services.links.cloud_run_update_database_link import CloudRunUpdateDatabaseLink
from app.services.links.firebase_auth_authenticated_data_link import FirebaseAuthAuthenticatedDataLink
from app.services.links.cloud_run_cache_miss_link import CloudRunCacheMissLink
from app.services.links.cloud_run_cache_link import CloudRunCacheLink
from app.services.links.feedback_label_ingestion_link import FeedbackLabelIngestionLink
from app.services.links.feedback_ingestion_cache_link import FeedbackIngestionCacheLink


from app.services.links.cache_miss_orchestrator_langgraph_link import CacheMissOrchestratorLangGraphLink

class ApiGatewayInternalLinkOrchestrator:
    """
    PURPOSE:
    The "Factory Manager" for the Gateway pipeline.
    EVENTUAL GOAL:
    It orchestrates the flow of data between different states. It tells the system:
    'Take unauthenticated data -> send to Auth Link -> if passed, send to Cache Link 
    -> if it misses cache, send to AI Link.' It wires the Channels and Links together.
    """
    def __init__(
        self, 
        auth_service: AuthService, 
        cache_service: InMemoryRiskCache,
        core_client: AgenticCoreClient,
        storage_client: StorageClient
    ) -> None:
        self._auth_service = auth_service
        self._cache_service = cache_service
        self._core_client = core_client
        self._storage_client = storage_client

    async def link_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Execute the Firebase Auth validation flow."""
        link = FirebaseAuthAuthenticatedDataLink(self._auth_service)
        return await link.forward_firebase_auth_to_authenticated_data(request)

    async def link_cloud_run_api_microservices_to_cache(self, request: CloudRunToCacheRequest):
        link = CloudRunCacheLink(self._cache_service)
        return link.forward_cloud_run_api_microservices_to_cache_layer(request)

    async def link_feedback_label_to_ingestion(self, request: FeedbackLabelToIngestionRequest):
        link = FeedbackLabelIngestionLink(self._storage_client)
        return await link.forward_feedback_label_to_feedback_ingestion(request)

    async def link_feedback_ingestion_to_cache(self, request: FeedbackIngestionToCacheRequest):
        link = FeedbackIngestionCacheLink(self._cache_service)
        return link.forward_feedback_ingestion_to_cache_layer(request)

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

    async def link_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Internal link: Cloud Run API Microservices -> cache miss."""
        # Step 5: Start the worker and trigger the AI Agent call!
        worker = CloudRunCacheMissLink(agentic_core_client=self._core_client)
        return await worker.forward_cloud_run_api_microservices_to_cache_miss(request)

    async def link_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Internal link: cache miss -> Orchestrator Agent LangGraph Router."""
        link = CacheMissOrchestratorLangGraphLink()
        await link.forward_cache_miss_to_orchestrator_agent_langgraph_router(request)

    def link_cloud_run_api_microservices_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> None:
        """Internal link: cache miss (from Cloud Run API Microservices) -> Orchestrator Agent LangGraph Router."""
        pass

    async def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Internal link: Cloud Run API Microservices -> Update database."""
        # Step 5: Start the worker and trigger the background Database write!
        worker = CloudRunUpdateDatabaseLink(storage_client=self._storage_client)
        return await worker.forward_cloud_run_api_microservices_to_update_database(request)

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Internal link: Update database -> Vector Database Vertex AI."""
        pass

    def link_user_feedback_to_feedback_label(self, request: UserFeedbackToFeedbackLabelRequest) -> None:
        """Internal link: user feedback (scam/safe/not sure) -> feedback label."""
        pass