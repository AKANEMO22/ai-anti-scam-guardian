from app.models.contracts import RawAudioPayload, SignalPayload


class RawAudioChannel:
    def receive_from_orchestrator_route(self, payload: SignalPayload) -> RawAudioPayload:
        """Receive orchestrator output and represent it as Raw Audio stage payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def normalize_raw_audio_reference(self, payload: RawAudioPayload) -> RawAudioPayload:
        """Normalize raw-audio reference metadata before forwarding to Deepfake Agent."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def validate_raw_audio_payload(self, payload: RawAudioPayload) -> None:
        """Validate that raw-audio payload is complete for the Deepfake stage."""
        print("mocked")
        return locals().get("mock_data", None) or {}
