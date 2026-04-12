from app.models.contracts import SignalPayload, VoiceStreamPayload


class VoiceStreamChannel:
    def receive_from_orchestrator_route(self, payload: SignalPayload) -> VoiceStreamPayload:
        """Receive orchestrator output and represent it as Voice Stream stage payload."""
        pass

    def normalize_voice_stream_payload(self, payload: VoiceStreamPayload) -> VoiceStreamPayload:
        """Normalize voice stream metadata before forwarding to Google STT API."""
        pass

    def validate_voice_stream_payload(self, payload: VoiceStreamPayload) -> None:
        """Validate that voice-stream payload is complete for STT processing stage."""
        pass
