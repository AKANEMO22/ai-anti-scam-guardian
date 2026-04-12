# AI Anti-Scam Guardian - Pipeline-Aligned Android Workspace

## 1) Muc tieu
Project nay da duoc sap xep lai theo dung 4 lane trong pipeline he thong:
- Lane 1: End User
- Lane 2: API Gateway
- Lane 3: Agentic AI Core
- Lane 4: Storage/Contracts

Muc tieu la de team mobile, backend, va AI nhin folder la thay ngay trach nhiem va luong du lieu.

## 2) Cau truc lane
- `lane-end-user/`
   - App shell, feature dashboard/scan/callshield/warning/history/guardian/settings
   - Service monitor background, realtime call, feedback sync
   - Core UI va on-device ML (TFLite + masking)
   - Assets voice sample cho incoming-call test

- `lane-api-gateway/`
   - Core network contract de goi Cloud Run API
   - Firebase config zone

- `lane-agentic-core/`
   - Domain model/use-case (risk score, signal payload, classify call)
   - Data repository (remote/local) noi voi cloud va local history

- `lane-storage/`
   - Storage lane cho vector index + RAG search + feedback ingestion (Python)
   - Dung lam backend data plane cho API Gateway va Agentic Core

- `shared/`
   - Core common
   - OpenAPI va event-schema dung chung app-backend

- `ops/`
   - Script bootstrap, seed data, smoke check (template)

### 2.1) Python backend stack (giu nguyen lane-end-user)

End-user Android van giu nguyen. 3 lane backend da duoc bo sung ban Python tach module theo tung chuc nang:

- `lane-api-gateway/python-api-gateway/`
   - `app/routes/analyze.py`: REST `/v1/signals/analyze`
   - `app/routes/feedback.py`: REST `/v1/feedback`
   - `app/services/cache_service.py`: cache layer
   - `app/clients/agentic_core_client.py`: noi sang Agentic Core lane
   - `app/clients/storage_client.py`: noi sang Storage lane

- `lane-agentic-core/python-agentic-core/`
   - `app/services/orchestrator.py`: orchestration route
   - `app/services/agents/deepfake_agent.py`
   - `app/services/agents/stt_agent.py`
   - `app/services/agents/threat_agent.py`
   - `app/services/agents/entity_agent.py`
   - `app/services/agents/reasoning_agent.py`
   - `app/services/decision_engine.py`

- `lane-storage/python-storage/`
   - `app/services/rag_engine.py`: pattern retrieval
   - `app/repositories/vector_repository.py`: vector db mock
   - `app/repositories/scam_pattern_repository.py`: scam pattern store
   - `app/repositories/feedback_repository.py`: feedback loop store

Xem chi tiet lien ket 3 lane theo hinh tai:
- `docs/PYTHON_LANE_ARCHITECTURE.md`

## 3) Runtime flow (map voi pipeline)
1. Background service thu SMS/Call/URL
2. TFLite on-device filter + PII masking
3. Cache hit -> instant warning UI
4. Cache miss/suspicious -> Cloud Run API qua Firebase auth
5. Orchestrator route den Deepfake + STT/Threat + Entity
6. Decision engine tra Risk Score + Explanation
7. User feedback (Scam/Safe/Not sure) -> feedback ingestion

## 4) Android module mapping
Gradle module names van giu nguyen, nhung da duoc map sang path lane moi trong `settings.gradle.kts`:
- `:app` -> `lane-end-user/app`
- `:core:ui` -> `lane-end-user/core/ui`
- `:core:ml` -> `lane-end-user/core/ml`
- `:core:network` -> `lane-api-gateway/core/network`
- `:core:common` -> `shared/core/common`
- `:domain` -> `lane-agentic-core/domain`
- `:data` -> `lane-agentic-core/data`
- `:feature:*` -> `lane-end-user/feature/*`
- `:service:*` -> `lane-end-user/service/*`

## 5) Docs
- `docs/PIPELINE_MAPPING.md`: map lane -> folder -> trach nhiem
- `docs/FILE_ROLES.md`: vai tro tung file/chuc nang
- `docs/FOLDER_TREE.md`: cay thu muc tong quan

## 6) Build sequence de demo nhanh
1. Dashboard + Quick Scan + Warning detail
2. Incoming call test (scam/real) + call authenticity score
3. History + Guardian alert + feedback sync

## 7) GUI tabs - can lam gi (implementation checklist)

Bottom tab hien tai co 5 tab: `Home`, `Scan`, `History`, `Guardian`, `Settings`.

### 7.1 Home tab
Muc tieu:
- Hien dashboard tong quan (risk card, snapshot KPI, quick actions, latest warning).
- Lam diem vao chinh cho user truoc khi qua cac tab chuc nang.

Can lam:
- Card risk hien score + level + explanation ngan.
- KPI card cap nhat theo du lieu scan trong ngay.
- Quick action button:
   - `Scan URL/SMS` -> chuyen sang tab `Scan`.
   - `Test Scam Call` -> kich hoat flow xin quyen/goi role default dialer.
   - `Alert History` -> chuyen sang tab `History`.
   - `Notify Guardian` -> chuyen sang tab `Guardian`.
- `Latest warning` hien canh bao moi nhat trong 15 phut gan nhat.

Definition of done:
- Chuyen tab dung khi bam quick action.
- Khong crash neu thieu permission call.
- Co du lieu fallback neu backend chua san sang.

### 7.2 Scan tab
Muc tieu:
- Quet URL/SMS/transcript va tra ket qua risk score de canh bao nhanh.

Can lam:
- Input cho URL/SMS/text transcript.
- Nut `Run Demo Scan` (sau nay doi thanh `Run Scan`) goi pipeline scan.
- Hien ket qua: score, severity, explanation, signal nao bi danh co.
- Neu high risk -> tao warning event de day sang `History` va `Home`.

Definition of done:
- Scan xong trong 1 flow ro rang (loading -> result).
- Ket qua co explanation de user hieu vi sao bi canh bao.

### 7.3 History tab
Muc tieu:
- Luu va hien lich su canh bao de user tra cuu lai.

Can lam:
- Danh sach item theo thu tu moi nhat truoc.
- Moi item co: thoi gian, loai su kien (call/sms/url), muc do, tom tat.
- Cho phep mo chi tiet warning (warning detail).
- Dong bo feedback scam/safe/not sure ve backend khi co mang.

Definition of done:
- Sau moi lan scan/call warning, co item moi trong history.
- App restart van doc lai duoc history local.

### 7.4 Guardian tab
Muc tieu:
- Ho tro nguoi than nhan canh bao khan khi user gap nguy co cao.

Can lam:
- Form quan ly so lien he guardian chinh.
- Nut `Send Guardian Alert` gui critical alert (FCM/API).
- Log trang thai gui alert (success/fail + timestamp).

Definition of done:
- Co gui test alert thanh cong (mock hoac that).
- Log hien dung ket qua gui.

### 7.5 Settings tab
Muc tieu:
- Cho phep cau hinh che do bao ve va quyen he thong.

Can lam:
- Hien trang thai cac tuy chon:
   - Auto scan incoming call.
   - Cloud assist khi uncertain case.
   - Feedback sync interval.
- Hien va huong dan setup:
   - Runtime permissions (READ_PHONE_STATE, READ_CALL_LOG, POST_NOTIFICATIONS...).
   - Default dialer role.
- Nut mo nhanh setting he thong khi chua du quyen.

Definition of done:
- User tu tab `Settings` co the tu setup du quyen cho incoming-call flow.
- Trang thai setting cap nhat dung sau khi quay lai app.

### 7.6 Ngoai bottom tabs - incoming call flow
Phan nay khong nam trong tab, nhung bat buoc de app phone-like:
- Incoming banner/fullscreen UI co nut Answer/Decline.
- Ongoing in-call screen khi da nhan may.
- Notification fallback neu OEM chan popup.

Definition of done:
- Ringing -> popup/notification -> answer/decline -> ongoing screen khong crash.

## 8) Team outputs (4 nguoi)

### 8.1 Minh Hoang - Data Analyst
Output can ban giao:
- Scam scenario catalog (SMS/URL/Call script), severity rubric, label guideline.
- Risk signal dictionary cho `voice/text/entity` va threshold review.
- Dashboard KPI definition (scan/day, high-risk rate, feedback conversion).

Folder phu trach:
- `docs/` (bo sung business metric va evaluation note)
- `shared/contracts/event-schema/` (xac nhan schema field phuc vu phan tich)

### 8.2 Huy Hoang - AI/ML Engineer
Output can ban giao:
- On-device pre-filter rule + masking strategy.
- Risk score design theo trong so Voice 30% / Text 40% / Entity 30%.
- Call authenticity logic cho test `scam` vs `real`.

Folder phu trach:
- `lane-end-user/core/ml/`
- `lane-agentic-core/domain/`
- `lane-agentic-core/data/repository/`

### 8.3 Thanh Binh - Backend Engineer
Output can ban giao:
- Cloud API contract (`analyze signal`, `submit feedback`).
- Network adapter tu mobile sang Cloud Run/Firebase auth.
- Feedback ingestion route va storage metadata mapping.

Folder phu trach:
- `lane-api-gateway/core/network/`
- `shared/contracts/openapi/`
- `shared/contracts/event-schema/`

### 8.4 Khanh Ngoc - Frontend/Mobile Engineer
Output can ban giao:
- Dashboard app flow: Home, Scan, CallShield, Warning, History, Guardian, Settings.
- Incoming call UX (answer/decline/end) va hien thi explanation.
- Background/realtime service wiring phia mobile.

Folder phu trach:
- `lane-end-user/app/`
- `lane-end-user/feature/`
- `lane-end-user/service/`
- `lane-end-user/assets/audio/`

### 8.5 Definition of Done cho moi nguoi
- Co file/code trong dung lane phu trach.
- Co contract/data field khop pipeline.
- Co demo flow end-to-end tu signal -> warning -> feedback.
- Co note nguan trong `docs/` ve assumption va pending issue.

## 9) Note
- Day la architecture scaffold chi tiet cho implementation.
- Chua bao gom full production hardening (observability, test coverage, security gate).
