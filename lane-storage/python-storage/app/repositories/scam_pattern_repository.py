import json
import os
from typing import Dict, List, Any
from app.utils.paths import get_base_data_dir

class ScamPatternRepository:
    def __init__(self):
        self.data_file = os.path.join(get_base_data_dir(), "vn_scam_patterns.json")
        self._patterns: Dict[str, Any] = {}
        self._load_patterns()

    def _load_patterns(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        self._patterns[item["id"]] = item
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {self.data_file}")
                    self._patterns = {}
        else:
            print(f"Pattern file not found at {self.data_file}")
            self._patterns = {}

    def list_active_pattern_ids(self) -> list[str]:
        """List active scam-pattern IDs that should be linked into vector index."""
        return list(self._patterns.keys())

    def list_active_patterns(self) -> list[Dict[str, Any]]:
        """List active scam-patterns used by RAG context preparation."""
        return list(self._patterns.values())

    def get_patterns_by_ids(self, pattern_ids: list[str]) -> list[Dict[str, Any]]:
        """Resolve scam-pattern texts from pattern IDs returned by internal links."""
        return [self._patterns[pid] for pid in pattern_ids if pid in self._patterns]
    
    def get_all_patterns(self) -> list[Dict[str, Any]]:
        return list(self._patterns.values())
