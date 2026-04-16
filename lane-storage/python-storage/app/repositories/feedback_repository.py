from app.models.contracts import FeedbackEvent
from datetime import datetime, timezone
from typing import List

_FEEDBACK_LOG: List[FeedbackEvent] = []

_VALID_LABELS = {"scam", "safe", "not_sure"}

class FeedbackRepository:
    def save_feedback_event(self, event: FeedbackEvent) -> None:
        """Persist feedback labels used by downstream training and evaluation loops."""
        if event.label not in _VALID_LABELS:
            raise ValueError(f"Invalid feedback label: '{event.label}'. Allowed values: {sorted(_VALID_LABELS)}")
        if not event.timestamp:
            event = event.model_copy(update={"timestamp": datetime.now(timezone.utc).isoformat()})        
        _FEEDBACK_LOG.append(event)

    def list_feedback_events(self) -> list[FeedbackEvent]:
        """ Read feedback history for model improvement and audit workflows."""
        return list(_FEEDBACK_LOG)