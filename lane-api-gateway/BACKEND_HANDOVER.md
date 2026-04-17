# Backend & API Gateway Handover - Thanh Binh

This document summarizes the deliverables for the Backend Engineer role (8.3 Thanh Binh) within the AI Anti-Scam Guardian project.

## 1. Cloud API Contracts
Defined in `shared/contracts/`, these files are the source of truth for communication between the Mobile app and the Backend.

- **OpenAPI**: [cloudrun-api.yaml](../../shared/contracts/openapi/cloudrun-api.yaml)
  - Defines `/v1/signals/analyze` and `/v1/feedback`.
  - Includes Bearer Token security requirements.
- **Event Schema**: [feedback-event.json](../../shared/contracts/event-schema/feedback-event.json)
  - Enriched with `userId` and `metadata` for precise tracking.

## 2. Mobile Network Adapter (Kotlin)
Located in `lane-api-gateway/core/network/`, providing a ready-to-use foundation for the Android/Mobile team.

- **Interface**: `CloudApi.kt`
- **Implementation**: `RetrofitCloudApi.kt`
  - Uses Retrofit annotations for easy integration.
  - Supports Bearer token injection for Firebase Auth.
  - Includes `AuthenticatedCloudApi` helper class for token management.

## 3. Feedback Ingestion & Metadata Mapping
The Python API Gateway handles the ingestion of user feedback and maps it to the Storage lane.

- **Auth**: `auth_service.py` provides a structured way to verify Firebase tokens.
- **Mapping**: `storage_client.py` maps the `FeedbackEvent` to the storage payload, adding environment metadata and source tracking.
- **Orchestration**: `internal_link_orchestrator.py` connects the incoming feedback to analytical/caching flows.

## 4. Packaging & Deployment
The backend is now fully containerized for portability.

- **Local Execution (Mac)**:
  1. Navigate to `ops/scripts/`.
  2. Create a `.env` file from `.env.example`.
  3. Run `docker-compose -f docker-compose.python-lanes.yml up --build`.
- **Cloud/Host (FPT/Cloud Run)**:
  - Each lane has its own `Dockerfile` (e.g., `lane-api-gateway/python-api-gateway/Dockerfile`).
  - These are ready to be built and deployed to any container orchestration service.

## 5. Environment Configuration
See `ops/scripts/.env.example` for the required keys:
- `GEMINI_API_KEY`: Required for the Agentic Core.
- `DEV_BEARER_TOKEN`: Used when `STRICT_AUTH` is set to `false` for local testing.
