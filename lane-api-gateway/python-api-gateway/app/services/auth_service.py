from fastapi import HTTPException

from app.config import Settings
from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest


class AuthService:
    """
    PURPOSE:
    Handles API security and identity verification.
    EVENTUAL GOAL:
    Ensures that only traffic originating from our legitimate mobile app (via Firebase App Check)
    and valid internal microservices can access the expensive Agentic Core AI functions.
    """
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def validate_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Arrow: Firebase Auth -> Authenticated Data (skeleton placeholder)."""
        pass

    def validate_authenticated_data_for_cloud_run(self, payload: AuthenticatedDataPayload) -> None:
        """Validate Authenticated Data stage before forwarding to Cloud Run API Microservices."""
        pass

    def validate_bearer_token(self, authorization: str | None) -> None:
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        if not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization scheme")

        token = authorization.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=401, detail="Empty bearer token")

        # The purpose of strict_auth is False -> easier dev -> no need to generate token everytime
        # If strict -> token as to match the token of the setting
        if self._settings.strict_auth and token != self._settings.dev_bearer_token:
            raise HTTPException(status_code=401, detail="Token rejected")
