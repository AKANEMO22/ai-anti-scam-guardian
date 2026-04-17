from app.models.contracts import DeepfakeSignalPayload


class DeepfakeDecisionLink:
    def forward_signal_score_to_decision_engine(self, payload: DeepfakeSignalPayload) -> int:
        """Flow: Deepfake Agent -> signal/score -> Decision & Reasoning Engine."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_decision_input_from_deepfake_signal(self, payload: DeepfakeSignalPayload) -> dict[str, object]:
        """Build Decision Engine input object from deepfake signal/score payload."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_deepfake_to_decision_flow(self, payload: DeepfakeSignalPayload) -> None:
        """Emit trace point for Deepfake->Decision internal flow observability."""
        print("mocked")
        return locals().get("mock_data", None) or {}
