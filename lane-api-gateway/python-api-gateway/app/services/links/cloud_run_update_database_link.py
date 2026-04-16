from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabaseToVectorDatabaseVertexAiRequest,
    SignalRequest,
    RiskResponse
)
from app.clients.storage_client import StorageClient
from uuid import uuid4

class CloudRunUpdateDatabaseLink:
    def __init__(self, storage_client: StorageClient):
        self._storage_client = storage_client

    async def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Flow: Cloud Run API Microservices -> Update database."""
        # 1. Tracing
        self.trace_cloud_run_api_microservices_to_update_database_flow(request)

        # 2. Extract context to build the correct Request & Risk models out of raw metadata
        signal_req = SignalRequest(
            sourceType=request.result.metadata.get("sourceType", "SMS"),
            text=request.result.metadata.get("text", "")
        )
        
        # Because we successfully passed Cache Miss and finished AI execution, 
        # the RiskResponse should now live nicely inside request.result.response
        risk_res = RiskResponse.model_validate(request.result.response)

        # 3. Call the local Storage Client!
        # Just as analyze.py did earlier, but now done asynchronously by this Cloud Worker
        try:
            event_id = str(uuid4())
            await self._storage_client.index_signal(event_id, signal_req, risk_res)
        except Exception as e:
            print(f"[Error in DB Worker] Failed to index AI result into Storage: {e}")
        
        # 4. Finally build the payload ready for the next link in the chain (Vector Database/Vertex)
        return self.build_update_database_payload_from_cloud_run(request)

    def build_update_database_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabaseToVectorDatabaseVertexAiRequest:
        """Build update-database payload from Cloud Run API Microservices result context."""
        # Transform the Cloud Run event format down into whatever Vertex AI requires
        return UpdateDatabaseToVectorDatabaseVertexAiRequest(
            updateKey=request.updateKey or request.signal.callSessionId or "unknown_update_key",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata
        )

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> Update database flow."""
        print(f"[Worker] Handling Update Database Event with data type: {request.result.dataType.value}")
