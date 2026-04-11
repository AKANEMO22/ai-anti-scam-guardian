# File Roles (Lane-based)

## Root
- `settings.gradle.kts`
	- Include module va map module den duong dan lane moi.
- `build.gradle.kts`
	- Root plugin management.
- `gradle/libs.versions.toml`
	- Version catalog.
- `README.md`
	- Tong quan kien truc lane theo pipeline.

## Lane End User (`lane-end-user`)

### App shell
- `lane-end-user/app/src/main/AndroidManifest.xml`
	- Permission internet, audio, foreground service, notification.
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/GuardianApp.kt`
	- App bootstrap.
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/MainActivity.kt`
	- Host activity.
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/navigation/AppNavGraph.kt`
	- Route ten man hinh.

### Feature modules
- `lane-end-user/feature/dashboard/*`
	- Dashboard KPI + quick actions.
- `lane-end-user/feature/scan/*`
	- Quick scan SMS/URL + pipeline trace.
- `lane-end-user/feature/callshield/*`
	- Incoming call test flow (scam/real).
- `lane-end-user/feature/warning/*`
	- Warning detail + recommendation + action.
- `lane-end-user/feature/history/*`
	- Risk event timeline.
- `lane-end-user/feature/guardian/*`
	- Guardian threshold + emergency notify.
- `lane-end-user/feature/settings/*`
	- Protection toggles va privacy settings.

### Service modules
- `lane-end-user/service/background/*`
	- Background monitor worker.
- `lane-end-user/service/realtimecall/*`
	- Realtime call session manager.
- `lane-end-user/service/feedbacksync/*`
	- Push feedback labels len cloud.

### End-user core
- `lane-end-user/core/ui/*`
	- UI token, style constant.
- `lane-end-user/core/ml/*`
	- On-device pre-filter + masking.

### End-user assets
- `lane-end-user/assets/audio/*`
	- Voice sample cho demo incoming call.

## Lane API Gateway (`lane-api-gateway`)
- `lane-api-gateway/core/network/CloudApi.kt`
	- Mobile-side cloud contract interface.
- `lane-api-gateway/firebase/`
	- Firebase config zone (placeholder).

## Lane Agentic AI Core (`lane-agentic-core`)
- `lane-agentic-core/domain/model/*`
	- Risk model va signal model.
- `lane-agentic-core/domain/usecase/*`
	- Process pipeline va classify call authenticity.
- `lane-agentic-core/data/remote/*`
	- Cloud API datasource.
- `lane-agentic-core/data/local/*`
	- Local store cho risk event.
- `lane-agentic-core/data/repository/*`
	- Noi on-device + cloud + local theo flow pipeline.

## Shared (`shared`)
- `shared/core/common/*`
	- Dispatchers, utility dung chung.
- `shared/contracts/openapi/cloudrun-api.yaml`
	- API contract app-backend.
- `shared/contracts/event-schema/feedback-event.json`
	- Feedback schema cho loop update pattern.

## Ops (`ops`)
- `ops/scripts/README.md`
	- Script strategy bootstrap/seed/smoke-check.
