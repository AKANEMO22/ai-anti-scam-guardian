from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest


class AuthenticatedDataChannel:
    def receive_from_firebase_auth(self, request: FirebaseAuthToAuthenticatedDataRequest) -> AuthenticatedDataPayload:
        """Receive Firebase Auth output and package into Authenticated Data payload."""
        pass

    def normalize_authenticated_data_payload(self, payload: AuthenticatedDataPayload) -> AuthenticatedDataPayload:
        """Normalize authenticated data payload before Cloud Run forwarding."""
        pass

    def validate_authenticated_data_payload(self, payload: AuthenticatedDataPayload) -> None:
        """Validate authenticated data payload required by Cloud Run API Microservices stage."""
        pass