from __future__ import annotations

import httpx

from app.config import Settings
from app.models.contracts import FeedbackEvent, RiskResponse, SignalRequest


class StorageClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def index_signal(self, event_id: str, request: SignalRequest, risk: RiskResponse) -> None:
        url = f"{self._settings.storage_base_url}/v1/storage/index"
        timeout = httpx.Timeout(self._settings.request_timeout_seconds)
        payload = {
            "eventId": event_id,
            "sourceType": request.sourceType.value,
            "text": request.text,
            "callSessionId": request.callSessionId,
            "metadata": request.metadata,
            "riskScore": risk.riskScore,
            "explanation": risk.explanation,
            "voiceScore": risk.voiceScore,
            "textScore": risk.textScore,
            "entityScore": risk.entityScore,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # FALLBACK FOR LOCAL DEV: If storage lane isn't active, log and continue smoothly
            print(f"[Fallback] Could not connect to Storage at {url}. Skipping indexing.")

    async def submit_feedback(self, feedback: FeedbackEvent) -> bool:
        url = f"{self._settings.storage_base_url}/v1/storage/feedback"
        timeout = httpx.Timeout(self._settings.request_timeout_seconds)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=feedback.model_dump())
                response.raise_for_status()

            body = response.json()
            return bool(body.get("accepted", False))
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # FALLBACK FOR LOCAL DEV
            print(f"[Fallback] Could not submit feedback to Storage at {url}.")
            return True
