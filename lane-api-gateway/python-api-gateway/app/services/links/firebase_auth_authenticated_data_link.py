from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest


class FirebaseAuthAuthenticatedDataLink:
    def forward_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Flow: Firebase Auth -> Authenticated Data."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def build_authenticated_data_from_firebase_auth(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Build Authenticated Data payload from Firebase Auth request context."""
        print("mocked")
        return locals().get("mock_data", None) or {}

    def trace_firebase_auth_to_authenticated_data_flow(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> None:
        """Emit trace point for Firebase Auth -> Authenticated Data internal flow."""
        print("mocked")
        return locals().get("mock_data", None) or {}