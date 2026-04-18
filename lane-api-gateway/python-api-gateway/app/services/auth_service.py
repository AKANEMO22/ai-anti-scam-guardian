import json
import logging
from typing import Optional
from fastapi import HTTPException

from app.config import Settings
from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def validate_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Arrow: Firebase Auth -> Authenticated Data."""
        self.validate_bearer_token(request.authorization)
        
        # In this Official flow, we simulate decoding the token.
        # In production: decoded_token = auth.verify_id_token(token)
        
        log_entry = {
            "event": "auth_validation",
            "status": "success",
            "userId": "dev-user-123"
        }
        print(json.dumps(log_entry))

        return AuthenticatedDataPayload(
            claims={"uid": "dev-user-123", "email": "dev@example.com", "provider": "google.com"},
            sourceType=request.sourceType,
            metadata=request.metadata
        )

    def validate_authenticated_data_for_cloud_run(self, payload: AuthenticatedDataPayload) -> None:
        """Validate Authenticated Data stage before forwarding to Cloud Run API Microservices."""
        if not payload.claims.get("uid"):
            raise HTTPException(status_code=403, detail="Invalid authenticated payload: missing UID")

    def validate_bearer_token(self, authorization: Optional[str]) -> None:
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        if not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization scheme")

        token = authorization.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=401, detail="Empty bearer token")

        # For the hackathon, we allow any token if strict_auth is False, 
        # or check against a dev token if it is True.
        if self._settings.strict_auth and token != self._settings.dev_bearer_token:
            raise HTTPException(status_code=401, detail="Token rejected")
