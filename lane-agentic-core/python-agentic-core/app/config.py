from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    storage_base_url: str
    request_timeout_seconds: float



def get_settings() -> Settings:
    return Settings(
        storage_base_url=os.getenv("STORAGE_BASE_URL", "http://localhost:8102"),
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "8")),
    )
