from dataclasses import dataclass
import os


def _env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    agentic_core_base_url: str
    storage_base_url: str
    request_timeout_seconds: float
    strict_auth: bool
    dev_bearer_token: str



def get_settings() -> Settings:
    return Settings(
        agentic_core_base_url=os.getenv("AGENTIC_CORE_BASE_URL", "http://localhost:8101"),
        storage_base_url=os.getenv("STORAGE_BASE_URL", "http://localhost:8102"),
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
        strict_auth=_env_flag("STRICT_AUTH", False),
        dev_bearer_token=os.getenv("DEV_BEARER_TOKEN", "dev-token"),
    )
