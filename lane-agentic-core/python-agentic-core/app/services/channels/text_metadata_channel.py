from app.models.contracts import SignalPayload, TextMetadataPayload


class TextMetadataChannel:
    def receive_from_orchestrator_route(self, payload: SignalPayload) -> TextMetadataPayload:
        """Receive orchestrator output and represent it as Text/Metadata stage payload."""
        pass

    def normalize_text_metadata_payload(self, payload: TextMetadataPayload) -> TextMetadataPayload:
        """Normalize text and metadata fields before forwarding to Entity Agent."""
        pass

    def validate_text_metadata_payload(self, payload: TextMetadataPayload) -> None:
        """Validate that text/metadata payload is complete for the Entity stage."""
        pass
