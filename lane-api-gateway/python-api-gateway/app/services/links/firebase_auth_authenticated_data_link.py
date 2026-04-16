from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest
from app.services.auth_service import AuthService

class FirebaseAuthAuthenticatedDataLink:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def forward_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Flow: Firebase Auth -> Authenticated Data."""
        self.trace_firebase_auth_to_authenticated_data_flow(request)
        return self.build_authenticated_data_from_firebase_auth(request)

    def build_authenticated_data_from_firebase_auth(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Build Authenticated Data payload from Firebase Auth request context."""
        # Delegates token validation to the Auth Service we built in Step 3!
        return self._auth_service.validate_firebase_auth_to_authenticated_data(request)

    def trace_firebase_auth_to_authenticated_data_flow(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> None:
        """Emit trace point for Firebase Auth -> Authenticated Data internal flow."""
        print(f"[Trace] Firebase Auth to Authenticated Data Flow started for source: {request.sourceType}")
