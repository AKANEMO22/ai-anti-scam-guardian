from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest


class AuthenticatedDataChannel:
    def receive_from_firebase_auth(self, request: FirebaseAuthToAuthenticatedDataRequest) -> AuthenticatedDataPayload:
        """Receive Firebase Auth output and package into Authenticated Data payload."""
        return AuthenticatedDataPayload(
            sourceType=request.sourceType,
            metadata=request.metadata or {}
        )

    def normalize_authenticated_data_payload(self, payload: AuthenticatedDataPayload) -> AuthenticatedDataPayload:
        """Normalize authenticated data payload before Cloud Run forwarding."""
        if payload.metadata:
            payload.metadata = {k.lower(): str(v).strip() for k, v in payload.metadata.items()}
        if payload.claims and payload.claims.email:
            payload.claims.email = payload.claims.email.lower().strip()
        return payload

    def validate_authenticated_data_payload(self, payload: AuthenticatedDataPayload) -> None:
        """Validate authenticated data payload required by Cloud Run API Microservices stage."""
        if not payload.claims or not payload.claims.uid:
            raise ValueError("Authenticated data payload must contain a valid user ID (uid).")
        if not payload.sourceType:
            raise ValueError("SourceType is required for authenticated data.")
