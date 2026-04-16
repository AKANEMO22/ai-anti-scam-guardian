import json
import os
from typing import List
from app.models.contracts import FeedbackEvent
from app.utils.paths import get_base_data_dir

class FeedbackRepository:
    def __init__(self):
        self.data_file = os.path.join(get_base_data_dir(), "feedback.jsonl")

    def save_feedback_event(self, event: FeedbackEvent) -> None:
        """Persist feedback labels used by downstream training and evaluation loops."""
        event_dict = event.model_dump()
        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_dict) + "\n")

    def list_feedback_events(self) -> List[FeedbackEvent]:
        """Read feedback history for model improvement and audit workflows."""
        events = []
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            events.append(FeedbackEvent(**data))
                        except Exception as e:
                            print(f"Error parsing feedback line: {e}")
        return events
