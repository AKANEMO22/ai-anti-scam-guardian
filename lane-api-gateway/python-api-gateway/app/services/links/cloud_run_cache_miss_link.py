from app.models.contracts import (
    CacheLookupResultPayload,
    CloudRunApiMicroservicesToCacheMissRequest,
    SignalRequest,
    RiskResponse
)
from app.clients.agentic_core_client import AgenticCoreClient

class CloudRunCacheMissLink:
    def __init__(self, agentic_core_client: AgenticCoreClient):
        self._core_client = agentic_core_client

    async def forward_cloud_run_api_microservices_to_cache_miss(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> CacheLookupResultPayload:
        """Flow: Cloud Run API Microservices -> cache miss."""
        # 1. Tracing
        self.trace_cloud_run_api_microservices_to_cache_miss_flow(request)

        # 2. Extract the actual payload text we missed in cache
        # In a real event-driven system, the incoming request tells us exactly what to analyze
        source_type = request.result.metadata.get("sourceType", "SMS")
        text = request.result.metadata.get("text", "")
        
        signal_request = SignalRequest(
            sourceType=source_type,
            text=text,
            metadata=request.result.metadata
        )

        # 3. THIS is where the Async Worker actually calls the AI Agent!
        # Notice we reuse the exact same AgenticCoreClient we tested in analyze.py
        try:
            risk_response = await self._core_client.analyze_signal(signal_request)
        except Exception as e:
            print(f"[Error in Cache Miss Worker] AI Analysis failed: {e}")
            risk_response = RiskResponse(
                riskScore=0, explanation="Error during analysis", 
                voiceScore=0, textScore=0, entityScore=0, cacheHit=False
            )

        # 4. We build the final package to send downstream
        return self.build_cache_miss_payload_from_cloud_run(request, risk_response)

    def build_cache_miss_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
        risk_response: RiskResponse = None
    ) -> CacheLookupResultPayload:
        """Build cache-miss payload from Cloud Run API Microservices result context."""
        # Wrap the AI's RiskResponse into the downstream contract
        return CacheLookupResultPayload(
            microservice=request.result.microservice,
            cacheKey=request.result.metadata.get("cacheKey", "unknown"),
            response=risk_response.model_dump() if risk_response else {}
        )

    def trace_cloud_run_api_microservices_to_cache_miss_flow(
        self,
        request: CloudRunApiMicroservicesToCacheMissRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> cache miss flow."""
        print(f"[Worker] Handling Cache Miss Event for microservice: {request.result.microservice}")
