from typing import Optional
from fastapi import HTTPException

from app.config import Settings
from app.models.contracts import (
    AuthenticatedDataPayload,
    FirebaseAuthClaims,
    FirebaseAuthToAuthenticatedDataRequest,
)


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
        # TODO : replace these mockups with real firebase validation
        """Arrow: Firebase Auth -> Authenticated Data (skeleton placeholder)."""
        # STEP 3: Instead of real Firebase decoding, we reuse the bearer token validation
        # for our local development workflow.
        self.validate_bearer_token(request.authorization)

        # Assuming it's valid, we mock the extracted JWT claims.
        # In production, these claims come from parsing the Firebase JWT payload.
        mock_claims = FirebaseAuthClaims(
            uid="user_local_dev",
            email="dev@akanemo22.internal",
            provider="local",
        )

        return AuthenticatedDataPayload(
            claims=mock_claims,
            sourceType=request.sourceType,
            metadata=request.metadata,
        )

    def validate_authenticated_data_for_cloud_run(self, payload: AuthenticatedDataPayload) -> None:
        """Validate Authenticated Data stage before forwarding to Cloud Run API Microservices."""
        # Ensure that the payload actually possesses claims before allowing internal API action
        if not payload.claims or not payload.claims.uid:
            raise HTTPException(
                status_code=401,
                detail="Invalid AuthenticatedDataPayload: Missing user claims."
            )

    def validate_bearer_token(self, authorization: Optional[str]) -> None:
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
