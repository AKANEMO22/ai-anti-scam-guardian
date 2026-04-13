from app.models.contracts import SignalPayload, TextMetadataPayload


class TextMetadataChannel:
    def receive_from_orchestrator_route(self, payload: SignalPayload) -> TextMetadataPayload:
        """Receive orchestrator output and represent it as Text/Metadata stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_text_metadata_payload(self, payload: TextMetadataPayload) -> TextMetadataPayload:
        """Normalize text and metadata fields before forwarding to Entity Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_text_metadata_payload(self, payload: TextMetadataPayload) -> None:
        """Validate that text/metadata payload is complete for the Entity stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}
