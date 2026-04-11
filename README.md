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

- `shared/`
   - Core common
   - OpenAPI va event-schema dung chung app-backend

- `ops/`
   - Script bootstrap, seed data, smoke check (template)

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

## 7) Team outputs (4 nguoi)

### 7.1 Minh Hoang - Data Analyst
Output can ban giao:
- Scam scenario catalog (SMS/URL/Call script), severity rubric, label guideline.
- Risk signal dictionary cho `voice/text/entity` va threshold review.
- Dashboard KPI definition (scan/day, high-risk rate, feedback conversion).

Folder phu trach:
- `docs/` (bo sung business metric va evaluation note)
- `shared/contracts/event-schema/` (xac nhan schema field phuc vu phan tich)

### 7.2 Huy Hoang - AI/ML Engineer
Output can ban giao:
- On-device pre-filter rule + masking strategy.
- Risk score design theo trong so Voice 30% / Text 40% / Entity 30%.
- Call authenticity logic cho test `scam` vs `real`.

Folder phu trach:
- `lane-end-user/core/ml/`
- `lane-agentic-core/domain/`
- `lane-agentic-core/data/repository/`

### 7.3 Thanh Binh - Backend Engineer
Output can ban giao:
- Cloud API contract (`analyze signal`, `submit feedback`).
- Network adapter tu mobile sang Cloud Run/Firebase auth.
- Feedback ingestion route va storage metadata mapping.

Folder phu trach:
- `lane-api-gateway/core/network/`
- `shared/contracts/openapi/`
- `shared/contracts/event-schema/`

### 7.4 Khanh Ngoc - Frontend/Mobile Engineer
Output can ban giao:
- Dashboard app flow: Home, Scan, CallShield, Warning, History, Guardian, Settings.
- Incoming call UX (answer/decline/end) va hien thi explanation.
- Background/realtime service wiring phia mobile.

Folder phu trach:
- `lane-end-user/app/`
- `lane-end-user/feature/`
- `lane-end-user/service/`
- `lane-end-user/assets/audio/`

### 7.5 Definition of Done cho moi nguoi
- Co file/code trong dung lane phu trach.
- Co contract/data field khop pipeline.
- Co demo flow end-to-end tu signal -> warning -> feedback.
- Co note nguan trong `docs/` ve assumption va pending issue.

## 8) Huong dan GUI tab (can lam gi o moi tab)

Muc nay dung cho demo, handover va test nhanh. Moi tab ben duoi co muc tieu ro rang va thao tac de xac nhan.

### 8.1 Setup bat buoc truoc khi test call incoming
1. Mo app lan dau va cap quyen Phone + Notification neu duoc hoi.
2. Dat app lam Phone app mac dinh (default dialer).
3. Neu he dieu hanh chan, vao App info -> Allow restricted settings roi quay lai dat default app.
4. Xac nhan xong moi test incoming call (popup incoming + answer/decline + ongoing).

### 8.2 Tab Home
Muc tieu:
- Xem tong quan risk score trong ngay va cac KPI chinh.

Can lam:
1. Vao Home de kiem tra card `Today Risk Overview` va `Dashboard Snapshot`.
2. Bam `Scan URL/SMS` de chuyen nhanh sang tab Scan.
3. Bam `Call Shield` de kich hoat lai flow cap quyen/default dialer neu thieu.
4. Bam `Alert History` va `Notify Guardian` de chuyen nhanh sang dung tab tuong ung.

### 8.3 Tab Scan
Muc tieu:
- Thuc hien luong phan tich URL/SMS/cuoc goi nghi ngo.

Can lam:
1. Vao tab Scan.
2. Bam `Run Demo Scan` de chay demo scanner.
3. Kiem tra ket qua theo logic local truoc (NPU/TFLite), cloud fallback khi can.
4. Neu la case rui ro cao, xac nhan warning duoc dua vao lich su.

### 8.4 Tab History
Muc tieu:
- Theo doi timeline canh bao de review nhanh.

Can lam:
1. Vao tab History.
2. Xac nhan co danh sach su kien theo moc thoi gian.
3. Doi chieu muc do canh bao (An toan/Trung binh/Nguy hiem cao).
4. Dung tab nay de demo truoc/sau khi chay scan hoac test call.

### 8.5 Tab Guardian
Muc tieu:
- Gui canh bao cho nguoi than/nguoi giam sat khi gap case nguy hiem.

Can lam:
1. Vao tab Guardian.
2. Kiem tra thong tin lien he chinh (primary contact).
3. Bam `Send Guardian Alert` khi muon day canh bao khan.
4. Xac nhan event guardian duoc ghi nhan vao luong theo doi.

### 8.6 Tab Settings
Muc tieu:
- Xac nhan cau hinh runtime cho he thong bao ve.

Can lam:
1. Vao tab Settings.
2. Kiem tra cac trang thai:
   - `Auto scan incoming call: ON`
   - `Cloud assist on uncertain case: ON`
   - `Feedback sync interval: 30 min`
3. Neu test incoming call bi loi, quay lai check quyen + default dialer tu day va tu Home/Call Shield.

### 8.7 Checklist demo GUI end-to-end
1. Home: chup tong quan risk/KPI.
2. Scan: chay demo scan.
3. History: xac nhan event moi xuat hien.
4. Guardian: gui canh bao mau.
5. Settings: xac nhan cac thong so bao ve dang ON.
6. Test incoming call thuc te: popup hien, bam answer/decline khong crash.

## 9) Note
- Day la architecture scaffold chi tiet cho implementation.
- Chua bao gom full production hardening (observability, test coverage, security gate).
