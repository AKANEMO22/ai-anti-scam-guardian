import json
from typing import Optional
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
    SignalRequest,
)
from app.services.auth_service import AuthService
from app.services.cache_service import InMemoryRiskCache

# Import Links
from app.services.links.authenticated_data_cloud_run_link import AuthenticatedDataCloudRunLink
from app.services.links.cache_miss_orchestrator_langgraph_link import CacheMissOrchestratorLangGraphLink
from app.services.links.cloud_run_cache_link import CloudRunCacheLink
from app.services.links.cloud_run_cache_miss_link import CloudRunCacheMissLink
from app.services.links.cloud_run_update_database_link import CloudRunUpdateDatabaseLink
from app.services.links.feedback_ingestion_cache_link import FeedbackIngestionCacheLink
from app.services.links.feedback_label_ingestion_link import FeedbackLabelIngestionLink
from app.services.links.firebase_auth_authenticated_data_link import FirebaseAuthAuthenticatedDataLink
from app.services.links.update_database_vector_database_vertex_ai_link import UpdateDatabaseVectorDatabaseVertexAiLink

# Import Channels
from app.services.channels.authenticated_data_channel import AuthenticatedDataChannel
from app.services.channels.cache_miss_channel import CacheMissChannel
from app.services.channels.cloud_run_cache_miss_channel import CloudRunCacheMissChannel
from app.services.channels.cloud_run_result_channel import CloudRunResultChannel
from app.services.channels.feedback_ingestion_channel import FeedbackIngestionChannel
from app.services.channels.feedback_label_channel import FeedbackLabelChannel
from app.services.channels.update_database_channel import UpdateDatabaseChannel


class ApiGatewayInternalLinkOrchestrator:
    def __init__(self, auth_service: AuthService, cache_service: InMemoryRiskCache) -> None:
        self._auth_service = auth_service
        self._cache_service = cache_service
        
        # Links
        self.auth_cloud_run_link = AuthenticatedDataCloudRunLink()
        self.cache_orchestrator_link = CacheMissOrchestratorLangGraphLink()
        self.cloud_run_cache_link = CloudRunCacheLink()
        self.cloud_run_cache_miss_link = CloudRunCacheMissLink()
        self.cloud_run_update_link = CloudRunUpdateDatabaseLink()
        self.feedback_cache_link = FeedbackIngestionCacheLink()
        self.feedback_label_link = FeedbackLabelIngestionLink()
        self.firebase_auth_link = FirebaseAuthAuthenticatedDataLink()
        self.update_vertex_link = UpdateDatabaseVectorDatabaseVertexAiLink()

        # Channels
        self.auth_data_channel = AuthenticatedDataChannel()
        self.cache_miss_channel = CacheMissChannel()
        self.cloud_run_cache_miss_channel = CloudRunCacheMissChannel()
        self.cloud_run_result_channel = CloudRunResultChannel()
        self.feedback_ingestion_channel = FeedbackIngestionChannel()
        self.feedback_label_channel = FeedbackLabelChannel()
        self.update_db_channel = UpdateDatabaseChannel()

    def link_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Internal link: Firebase Auth -> Authenticated Data."""
        payload = self.firebase_auth_link.forward_firebase_auth_to_authenticated_data(request)
        return self.auth_data_channel.receive_from_firebase_auth(payload)

    def link_authenticated_data_to_cloud_run_api_microservices(
        self,
        request: AuthenticatedDataToCloudRunRequest,
    ) -> None:
        """Internal link: Authenticated Data -> Cloud Run API Microservices."""
        self.auth_cloud_run_link.forward_authenticated_data_to_cloud_run(request)

    def link_cloud_run_api_microservices_to_cache_layer(
        self,
        request: CloudRunToCacheRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> Cache Layer (redis)."""
        payload = self.cloud_run_cache_link.forward_cloud_run_api_microservices_to_cache_layer(request)
        self.cloud_run_result_channel.receive_from_cloud_run_api_microservices(payload)
        self._cache_service.write_cloud_run_result_to_cache_layer(request)

    def link_cloud_run_api_microservices_to_cache_layer_lookup(
        self,
        request: CloudRunToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Internal lookup link for Cloud Run API Microservices cache keys (phone/url/script)."""
        return self._cache_service.read_cloud_run_result_from_cache_layer(request)

    def link_cache_layer_to_cache_miss(self, request: CacheLayerToCacheMissRequest) -> None:
        """Internal link: Cache Layer (redis) phone/url/script -> cache miss."""
        payload = self.cache_miss_channel.receive_from_cache_layer(request.lookup)
        routing_req = CacheMissToOrchestratorAgentLangGraphRouterRequest(
            lookup=payload,
            signal=request.signal
        )
        self.link_cache_miss_to_orchestrator_agent_langgraph_router(routing_req)

    def link_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> cache miss."""
        payload = self.cloud_run_cache_miss_link.forward_cloud_run_api_microservices_to_cache_miss(request)
        final_payload = self.cloud_run_cache_miss_channel.receive_from_cloud_run_api_microservices(payload)
        
        routing_req = CacheMissToOrchestratorAgentLangGraphRouterRequest(
            lookup=final_payload,
            signal=request.signal
        )
        self.link_cache_miss_to_orchestrator_agent_langgraph_router(routing_req)

    def link_cache_miss_to_orchestrator_agent_langgraph_router(
        self,
        request: CacheMissToOrchestratorAgentLangGraphRouterRequest,
    ) -> SignalRequest:
        """Internal link: cache miss -> Orchestrator Agent LangGraph Router."""
        return self.cache_orchestrator_link.forward_cache_miss_to_orchestrator_agent_langgraph_router(request)

    def link_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Internal link: Cloud Run API Microservices -> Update database."""
        self.cloud_run_update_link.forward_cloud_run_api_microservices_to_update_database(request)
        final_req = self.update_db_channel.receive_from_cloud_run_api_microservices(request.result)
        self.link_update_database_to_vector_database_vertex_ai(final_req)

    def link_update_database_to_vector_database_vertex_ai(
        self,
        request: UpdateDatabaseToVectorDatabaseVertexAiRequest,
    ) -> None:
        """Internal link: Update database -> Vector Database Vertex AI."""
        self.update_vertex_link.forward_update_database_to_vector_database_vertex_ai(request)

    def link_user_feedback_to_feedback_label(self, request: UserFeedbackToFeedbackLabelRequest) -> None:
        """Internal link: user feedback (scam/safe/not sure) -> feedback label."""
        payload = self.feedback_label_channel.receive_from_user_feedback(request.payload)
        ingestion_req = FeedbackLabelToIngestionRequest(payload=payload)
        self.link_feedback_label_to_feedback_ingestion(ingestion_req)

    def link_feedback_label_to_feedback_ingestion(self, request: FeedbackLabelToIngestionRequest) -> None:
        """Internal link: feedback label -> feedback ingestion."""
        payload = self.feedback_label_link.forward_feedback_label_to_feedback_ingestion(request.payload)
        result = self.feedback_ingestion_channel.receive_from_feedback_label(payload)
        
        cache_req = FeedbackIngestionToCacheRequest(result=result)
        self.link_feedback_ingestion_to_cache_layer(cache_req)

    def link_feedback_ingestion_to_cache_layer(self, request: FeedbackIngestionToCacheRequest) -> None:
        """Internal link: feedback ingestion -> Cache Layer (redis) by phone/url/script."""
        self.feedback_cache_link.forward_feedback_ingestion_to_cache_layer(request)
        self._cache_service.write_feedback_ingestion_result_to_cache_layer(request)

    def link_feedback_ingestion_to_cache_layer_lookup(
        self,
        request: FeedbackIngestionToCacheLookupRequest,
    ) -> Optional[dict[str, object]]:
        """Internal lookup link for feedback-ingestion cache keys (phone/url/script)."""
        return self._cache_service.read_feedback_ingestion_result_from_cache_layer(request)