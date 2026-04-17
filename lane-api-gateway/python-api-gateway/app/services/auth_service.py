from typing import Optional
from fastapi import HTTPException

from app.config import Settings
from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest


class AuthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def validate_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Arrow: Firebase Auth -> Authenticated Data.
        In production, this would use firebase_admin.auth.verify_id_token(token).
        """
        self.validate_bearer_token(request.authorization)
        
        # Real-world: decoded_token = auth.verify_id_token(token)
        # For now, we return a simulated payload derived from the request
        return AuthenticatedDataPayload(
            claims={"uid": "dev-user-123", "email": "dev@example.com", "provider": "google.com"},
            sourceType=request.sourceType,
            metadata=request.metadata
        )

    def validate_authenticated_data_for_cloud_run(self, payload: AuthenticatedDataPayload) -> None:
        """Validate Authenticated Data stage before forwarding to Cloud Run API Microservices."""
        if not payload.claims.uid:
            raise HTTPException(status_code=403, detail="Invalid authenticated payload: missing UID")

    def validate_bearer_token(self, authorization: Optional[str]) -> None:
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        if not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization scheme")

        token = authorization.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=401, detail="Empty bearer token")

        if self._settings.strict_auth and token != self._settings.dev_bearer_token:
            raise HTTPException(status_code=401, detail="Token rejected")
