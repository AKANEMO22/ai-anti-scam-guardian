import json
import os
from typing import Dict, Optional
from app.models.contracts import IndexSignalRequest
from app.utils.paths import get_base_data_dir

class SignalRepository:
    def __init__(self):
        self.data_file = os.path.join(get_base_data_dir(), "analysed_signals.jsonl")

    def save_signal(self, signal: IndexSignalRequest) -> None:
        """Store analysed signal metadata."""
        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(signal.model_dump()) + "\n")

    def get_signal_by_event_id(self, event_id: str) -> Optional[IndexSignalRequest]:
        """Retrieve signal metadata by event ID."""
        if not os.path.exists(self.data_file):
            return None
        
        with open(self.data_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data.get("eventId") == event_id:
                        return IndexSignalRequest(**data)
        return None
