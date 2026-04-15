import json
from pathlib import Path
from typing import Dict, List
import logging

DATA_PATH = Path(__file__).parent / "data" / "scam_patterns.json"

class ScamPatternRepository:
    def __init__(self):
        self._catalog: Dict[str, Dict] = self._load_catalog()

    def _load_catalog(self) -> Dict[str, str]:
        """Load scam-pattern catalog from JSON file."""
        try:
            if not DATA_PATH.exists():
                logging.error(f"Data file not found at {DATA_PATH}")
                return {}
            
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load scam patterns from JSON: {e}")
            return {}
        
    def list_active_pattern_ids(self) -> list[str]:
        """List active scam-pattern IDs that should be linked into vector index."""
        return sorted([
            pid for pid, data in self._catalog.items()
            if data.get("active", False)
        ])

    def list_active_patterns(self) -> list[str]:
        """List active scam-pattern texts used by RAG context preparation."""
        return [
            data["description"] 
            for pid, data in sorted(self._catalog.items())
            if data.get("active", False)
        ]

    def get_patterns_by_ids(self, pattern_ids: list[str]) -> list[str]:
        """Resolve scam-pattern texts from pattern IDs returned by internal links."""
        result: List[str] = []
        for pid in pattern_ids:
            entry = self._catalog.get(pid)
            if entry:
                result.append(entry["description"])
        return result
