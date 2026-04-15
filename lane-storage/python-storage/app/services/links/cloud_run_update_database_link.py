from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabasePayload,
)


class CloudRunUpdateDatabaseLink:
    def forward_cloud_run_api_microservices_to_update_database(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Flow: Cloud Run API Microservices -> Update database."""
        # Build the update database payload
        payload = self.build_update_database_payload_from_cloud_run(request)
        # Emit trace for the flow
        self.trace_cloud_run_api_microservices_to_update_database_flow(request)
        return payload

    def build_update_database_payload_from_cloud_run(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Build update-database payload from Cloud Run API Microservices result context."""
        # Use provided updateKey or generate one
        update_key = request.updateKey or f"cloud-run-{request.result.microservice.lower()}-{hash(str(request.result.response))}"

        return UpdateDatabasePayload(
            updateKey=update_key,
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata,
        )

    def trace_cloud_run_api_microservices_to_update_database_flow(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> None:
        """Emit trace point for Cloud Run API Microservices -> Update database flow."""
        # Simple logging - in a real implementation this might send to a tracing system
        print(f"[TRACE] Cloud Run API Microservices -> Update Database: {request.result.microservice} -> {request.updateKey or 'auto-generated'}")
