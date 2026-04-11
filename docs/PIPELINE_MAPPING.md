# Pipeline Mapping (System Lane -> Folder)

## Lane 1: End User
Folder:
- `lane-end-user/app`
- `lane-end-user/feature/*`
- `lane-end-user/service/background`
- `lane-end-user/core/ui`
- `lane-end-user/core/ml`

Trach nhiem:
- UI dashboard, warning, incoming call, feedback button.
- Background monitor SMS/Call/URL.
- Chay on-device pre-filter va masking truoc khi goi cloud.

## Lane 2: API Gateway
Folder:
- `lane-api-gateway/core/network`
- `lane-api-gateway/firebase`
- `shared/contracts/openapi`

Trach nhiem:
- Attach Firebase auth token.
- Goi Cloud Run API.
- Xu ly response cache-hit/cache-miss o tan ung dung.

## Lane 3: Agentic AI Core
Folder:
- `lane-agentic-core/domain`
- `lane-agentic-core/data/repository`
- `lane-agentic-core/data/remote`

Trach nhiem:
- Dieu phoi process signal pipeline.
- Nhan score/explanation tu cloud, map sang domain model.
- Trigger flow classify call real/fake va guardian alert rule.

## Lane 4: Storage and Feedback Loop
Folder:
- `lane-agentic-core/data/local`
- `shared/contracts/event-schema`
- `lane-end-user/feature/history`
- `lane-end-user/service/feedbacksync`

Trach nhiem:
- Luu risk metadata local (history timeline).
- Dong bo feedback Scam/Safe/Not sure len feedback ingestion.
- Su dung schema thong nhat giua mobile-backend.

## Voice Test Asset Mapping
Folder:
- `lane-end-user/assets/audio`

File:
- `scam_call.wav`
- `real_call.wav`

Muc dich:
- Demo incoming call scenario truoc khi AI classify authenticity.
