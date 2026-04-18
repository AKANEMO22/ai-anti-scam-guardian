import json
import logging
from typing import Optional
from fastapi import HTTPException

import firebase_admin
from firebase_admin import credentials, auth

from app.config import Settings
from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        
        # Initialize Firebase App if not already initialized
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(self._settings.firebase_credential_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not initialize Firebase Admin: {e}. Falling back to mock auth if strict_auth is False.")

    def validate_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Arrow: Firebase Auth -> Authenticated Data."""
        self.validate_bearer_token(request.authorization)
        token = request.authorization.split(" ", 1)[1].strip()
        
        # In this Official flow, we decode the token.
        if not self._settings.strict_auth and token == self._settings.dev_bearer_token:
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
            
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get("uid")
            email = decoded_token.get("email", "")
            
            log_entry = {
                "event": "auth_validation",
                "status": "success",
                "userId": uid
            }
            print(json.dumps(log_entry))

            return AuthenticatedDataPayload(
                claims={
                    "uid": uid, 
                    "email": email, 
                    "provider": decoded_token.get("firebase", {}).get("sign_in_provider", "firebase")
                },
                sourceType=request.sourceType,
                metadata=request.metadata
            )
        except auth.ExpiredIdTokenError:
            raise HTTPException(status_code=401, detail="Firebase token expired")
        except auth.InvalidIdTokenError:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        except Exception as e:
            logger.error(f"Firebase auth error: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")

    def validate_authenticated_data_for_cloud_run(self, payload: AuthenticatedDataPayload) -> None:
        """Validate Authenticated Data stage before forwarding to Cloud Run API Microservices."""
        if not payload.claims.get("uid"):
            raise HTTPException(status_code=403, detail="Invalid authenticated payload: missing UID")
    
    # TODO: need real firebase authentication later
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
