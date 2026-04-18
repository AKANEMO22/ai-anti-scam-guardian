import json
from app.models.contracts import AuthenticatedDataPayload, FirebaseAuthToAuthenticatedDataRequest

class FirebaseAuthAuthenticatedDataLink:
    def forward_firebase_auth_to_authenticated_data(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Flow: Firebase Auth -> authenticated-data."""
        log_entry = {
            "link": "gateway_auth_link",
            "event": "forward",
            "sourceType": request.sourceType
        }
        print(json.dumps(log_entry))
        
        return self.build_authenticated_data_payload(request)

    def build_authenticated_data_payload(
        self,
        request: FirebaseAuthToAuthenticatedDataRequest,
    ) -> AuthenticatedDataPayload:
        """Build Authenticated Data payload from Firebase Auth context."""
        # In a real app, this would extract info from the 'authorization' token
        return AuthenticatedDataPayload(
            claims=FirebaseAuthClaims(uid="user_from_token"),
            sourceType=request.sourceType,
            metadata=request.metadata
        )

    def trace_firebase_auth_to_authenticated_data_flow(self, request: FirebaseAuthToAuthenticatedDataRequest) -> None:
        """Emit trace point for Firebase Auth -> authenticated-data internal flow."""
        log_entry = {
            "link": "gateway_auth_link",
            "event": "trace",
            "status": "success"
        }
        print(json.dumps(log_entry))