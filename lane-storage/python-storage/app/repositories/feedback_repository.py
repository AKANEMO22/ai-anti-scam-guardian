from app.models.contracts import FeedbackEvent


class FeedbackRepository:
    def save_feedback_event(self, event: FeedbackEvent) -> None:
        """Persist feedback labels used by downstream training and evaluation loops."""
        pass

    def list_feedback_events(self) -> list[FeedbackEvent]:
        """Read feedback history for model improvement and audit workflows."""
        pass
