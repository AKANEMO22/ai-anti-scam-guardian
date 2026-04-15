from app.models.contracts import (
    CloudRunApiMicroservicesToUpdateDatabaseRequest,
    UpdateDatabasePayload,
)


class UpdateDatabaseChannel:
    def receive_from_cloud_run_api_microservices(
        self,
        request: CloudRunApiMicroservicesToUpdateDatabaseRequest,
    ) -> UpdateDatabasePayload:
        """Receive Cloud Run API Microservices payload and expose update-database stage input."""
        # Transform the Cloud Run API request into an update database payload
        return UpdateDatabasePayload(
            updateKey=request.updateKey or f"cloud-run-{request.result.microservice.lower()}-{hash(str(request.result.response))}",
            dataType=request.result.dataType,
            payload=request.result.response,
            metadata=request.result.metadata,
        )

    def normalize_update_database_payload(self, payload: UpdateDatabasePayload) -> UpdateDatabasePayload:
        """Normalize update-database payload before Vector Database Vertex AI stage."""
        # Create a normalized copy of the payload
        normalized_payload = payload.payload.copy()
        normalized_metadata = payload.metadata.copy()

        # Normalize string values in payload
        for key, value in normalized_payload.items():
            if isinstance(value, str):
                normalized_payload[key] = value.strip()

        # Normalize string values in metadata
        for key, value in normalized_metadata.items():
            if isinstance(value, str):
                normalized_metadata[key] = value.strip()

        # Ensure updateKey is clean
        clean_update_key = payload.updateKey.strip() if payload.updateKey else ""

        return UpdateDatabasePayload(
            updateKey=clean_update_key,
            dataType=payload.dataType,
            payload=normalized_payload,
            metadata=normalized_metadata,
        )

    def validate_update_database_payload(self, payload: UpdateDatabasePayload) -> None:
        """Validate update-database payload required for Vector Database Vertex AI write flow."""
        # Validate required fields
        if not payload.updateKey or not payload.updateKey.strip():
            raise ValueError("updateKey is required and cannot be empty")

        if not payload.dataType or not payload.dataType.strip():
            raise ValueError("dataType is required and cannot be empty")

        if payload.payload is None:
            raise ValueError("payload cannot be None")

        # Validate payload is a dict
        if not isinstance(payload.payload, dict):
            raise ValueError("payload must be a dictionary")

        # Validate metadata is a dict
        if payload.metadata is not None and not isinstance(payload.metadata, dict):
            raise ValueError("metadata must be a dictionary")
