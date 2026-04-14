from __future__ import annotations

import httpx

from app.config import Settings
from app.models.contracts import RiskResponse, SignalRequest


class AgenticCoreClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def analyze_signal(self, request: SignalRequest) -> RiskResponse:
        url = f"{self._settings.agentic_core_base_url}/v1/agentic/score"
        timeout = httpx.Timeout(self._settings.request_timeout_seconds)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=request.model_dump())
                response.raise_for_status()

            data = response.json()
            if "cacheHit" not in data:
                data["cacheHit"] = False
            return RiskResponse.model_validate(data)
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # FALLBACK FOR LOCAL DEV: If the agentic-core isn't running, return a mock response
            print(f"[Fallback] Could not connect to Agentic Core at {url}. Returning mock risk response.")
            mock_score = 90 if request.text and "scam" in request.text.lower() else 10
            return RiskResponse(
                riskScore=mock_score,
                explanation="[Mock Fallback] Analysis unavailable",
                voiceScore=0,
                textScore=mock_score,
                entityScore=0,
                cacheHit=False
            )
