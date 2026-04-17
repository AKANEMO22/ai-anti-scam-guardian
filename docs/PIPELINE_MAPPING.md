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
- Background monitor SMS/CALL/URL (Mobile App -> Background Service flow).
- Chay On-device TFLite pre-filter va masking theo flow Background Service -> TFLite Model On-device Filter truoc khi goi cloud.

Flow skeleton da setup:
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/background/MobileAppBackgroundServiceBridge.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/MobileBackgroundSignalContracts.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/MobileBackgroundSignalChannel.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/MobileAppBackgroundServiceLink.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/EndUserBackgroundFlowOrchestrator.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/BackgroundMonitorWorker.kt`
- `lane-end-user/service/background/src/main/java/com/sixseven/antiscam/service/background/BackgroundToOnDeviceFilterDispatcher.kt`
- `lane-end-user/core/ml/src/main/java/com/sixseven/antiscam/core/ml/OnDeviceFilterFlowContracts.kt`
- `lane-end-user/core/ml/src/main/java/com/sixseven/antiscam/core/ml/OnDeviceFilterInputChannel.kt`
- `lane-end-user/core/ml/src/main/java/com/sixseven/antiscam/core/ml/BackgroundServiceOnDeviceFilterLink.kt`
- `lane-end-user/core/ml/src/main/java/com/sixseven/antiscam/core/ml/OnDeviceFilterFlowOrchestrator.kt`

Flow skeleton TFLite -> UI warning explanation da setup:
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningFlowContract.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningFlowChannel.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningExplanationLink.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/OnDeviceWarningFlowOrchestrator.kt`
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/warning/OnDeviceWarningUiBridge.kt`

Flow skeleton UI warning explanation -> interact -> user feedback (scam/safe/not sure) da setup:
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/WarningUserFeedbackFlowContracts.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/WarningInteractionChannel.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/WarningFeedbackLink.kt`
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/WarningUserFeedbackFlowOrchestrator.kt`
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/feedback/WarningUserFeedbackBridge.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowContracts.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/UserFeedbackSyncChannel.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackIngestionLink.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowOrchestrator.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncWorker.kt`

Flow skeleton User feedback (scam/safe/not sure) -> feedback label -> feedback ingestion -> Cache layer (Redis) phone/url/script da setup:
- `lane-end-user/feature/warning/src/main/java/com/sixseven/antiscam/feature/warning/WarningUserFeedbackFlowContracts.kt`
- `lane-end-user/app/src/main/java/com/sixseven/antiscam/feedback/WarningUserFeedbackBridge.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowContracts.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackLabelChannel.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackIngestionLink.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackIngestionCacheLink.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncFlowOrchestrator.kt`
- `lane-end-user/service/feedbacksync/src/main/java/com/sixseven/antiscam/service/feedbacksync/FeedbackSyncWorker.kt`
- `lane-api-gateway/python-api-gateway/app/routes/internal_feedback_flow.py`
- `lane-api-gateway/python-api-gateway/app/services/channels/feedback_label_channel.py`
- `lane-api-gateway/python-api-gateway/app/services/channels/feedback_ingestion_channel.py`
- `lane-api-gateway/python-api-gateway/app/services/links/feedback_label_ingestion_link.py`
- `lane-api-gateway/python-api-gateway/app/services/links/feedback_ingestion_cache_link.py`
- `lane-api-gateway/python-api-gateway/app/services/cache_service.py`

Flow skeleton Flutter Mobile App -> REST SMS/URL -> Cloud Run API Microservices da setup:
- `lane-end-user/flutter-mobile-app/lib/contracts/mobile_rest_cloud_run_contracts.dart`
- `lane-end-user/flutter-mobile-app/lib/services/rest_sms_url_channel.dart`
- `lane-end-user/flutter-mobile-app/lib/services/cloud_run_microservices_rest_link.dart`
- `lane-end-user/flutter-mobile-app/lib/services/mobile_rest_sms_url_flow_orchestrator.dart`
- `lane-end-user/flutter-mobile-app/lib/bridge/mobile_app_flutter_rest_bridge.dart`

Flow skeleton Flutter Mobile App -> WebSocket/gRPC streaming realtime call -> Cloud Run API Microservices da setup:
- `lane-end-user/flutter-mobile-app/lib/contracts/mobile_realtime_stream_cloud_run_contracts.dart`
- `lane-end-user/flutter-mobile-app/lib/services/realtime_call_stream_channel.dart`
- `lane-end-user/flutter-mobile-app/lib/services/cloud_run_realtime_stream_link.dart`
- `lane-end-user/flutter-mobile-app/lib/services/mobile_realtime_stream_flow_orchestrator.dart`
- `lane-end-user/flutter-mobile-app/lib/bridge/mobile_app_realtime_stream_bridge.dart`

Flow skeleton Cache layer (Redis) phone/URL/script -> Cache hit -> instant warning -> UI warning explanation da setup:
- `lane-end-user/flutter-mobile-app/lib/contracts/cache_hit_warning_flow_contracts.dart`
- `lane-end-user/flutter-mobile-app/lib/services/cache_hit_warning_channel.dart`
- `lane-end-user/flutter-mobile-app/lib/services/cache_hit_instant_warning_link.dart`
- `lane-end-user/flutter-mobile-app/lib/services/instant_warning_ui_explanation_link.dart`
- `lane-end-user/flutter-mobile-app/lib/services/cache_hit_warning_flow_orchestrator.dart`
- `lane-end-user/flutter-mobile-app/lib/bridge/cache_hit_warning_ui_bridge.dart`

## Lane 2: API Gateway
Folder:
- `lane-api-gateway/core/network`
- `lane-api-gateway/firebase`
- `lane-api-gateway/python-api-gateway/app/*`
- `shared/contracts/openapi`

Trach nhiem:
- Attach Firebase auth token.
- Goi Cloud Run API.
- Xu ly response cache-hit/cache-miss o tan ung dung.
- Python lane route request tu mobile den Agentic Core va Storage lane.

Flow skeleton Cache Layer (Redis) phone/url/script -> cache miss -> Orchestrator Agent LangGraph Router da setup:
- `lane-api-gateway/python-api-gateway/app/models/contracts.py`
- `lane-api-gateway/python-api-gateway/app/services/internal_link_orchestrator.py`
- `lane-api-gateway/python-api-gateway/app/services/channels/cache_miss_channel.py`
- `lane-api-gateway/python-api-gateway/app/services/links/cache_miss_orchestrator_langgraph_link.py`
- `lane-api-gateway/python-api-gateway/app/routes/internal_cache_miss_flow.py`
- `lane-api-gateway/python-api-gateway/app/main.py`

Flow skeleton Cloud Run API Microservices -> cache miss -> Orchestrator Agent LangGraph Router da setup:
- `lane-api-gateway/python-api-gateway/app/models/contracts.py`
- `lane-api-gateway/python-api-gateway/app/services/internal_link_orchestrator.py`
- `lane-api-gateway/python-api-gateway/app/services/channels/cloud_run_cache_miss_channel.py`
- `lane-api-gateway/python-api-gateway/app/services/links/cloud_run_cache_miss_link.py`
- `lane-api-gateway/python-api-gateway/app/routes/internal_cloud_run_cache_miss_flow.py`
- `lane-api-gateway/python-api-gateway/app/main.py`

Flow skeleton Cloud Run API Microservices -> Update database -> Vector Database Vertex AI da setup:
- `lane-api-gateway/python-api-gateway/app/models/contracts.py`
- `lane-api-gateway/python-api-gateway/app/services/internal_link_orchestrator.py`
- `lane-api-gateway/python-api-gateway/app/services/channels/update_database_channel.py`
- `lane-api-gateway/python-api-gateway/app/services/links/cloud_run_update_database_link.py`
- `lane-api-gateway/python-api-gateway/app/services/links/update_database_vector_database_vertex_ai_link.py`
- `lane-api-gateway/python-api-gateway/app/routes/internal_cloud_run_update_database_flow.py`
- `lane-api-gateway/python-api-gateway/app/main.py`
- `lane-storage/python-storage/app/models/contracts.py`
- `lane-storage/python-storage/app/services/internal_link_orchestrator.py`
- `lane-storage/python-storage/app/services/channels/update_database_channel.py`
- `lane-storage/python-storage/app/services/links/cloud_run_update_database_link.py`
- `lane-storage/python-storage/app/services/links/update_database_vector_database_vertex_ai_link.py`
- `lane-storage/python-storage/app/routes/storage.py`

## Lane 3: Agentic AI Core
Folder:
- `lane-agentic-core/domain`
- `lane-agentic-core/data/repository`
- `lane-agentic-core/data/remote`
- `lane-agentic-core/python-agentic-core/app/*`

Trach nhiem:
- Dieu phoi process signal pipeline.
- Nhan score/explanation tu cloud, map sang domain model.
- Trigger flow classify call real/fake va guardian alert rule.
- Python Orchestrator route den cac module Deepfake/STT/Threat/Entity/Reasoning.

Flow skeleton Decision & Reasoning Engine -> JSON score + warning -> Cloud Run API Microservices da setup:
- `lane-agentic-core/python-agentic-core/app/models/contracts.py`
- `lane-agentic-core/python-agentic-core/app/services/decision_engine.py`
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/channels/json_score_warning_channel.py`
- `lane-agentic-core/python-agentic-core/app/services/links/decision_json_score_warning_link.py`
- `lane-agentic-core/python-agentic-core/app/services/links/json_score_warning_cloud_run_link.py`
- `lane-agentic-core/python-agentic-core/app/routes/score.py`

Flow skeleton Google STT API -> Transcribed Text -> Threat Agent da setup:
- `lane-agentic-core/python-agentic-core/app/models/contracts.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/stt_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/threat_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/channels/transcribed_text_channel.py`
- `lane-agentic-core/python-agentic-core/app/services/links/google_stt_transcribed_text_link.py`
- `lane-agentic-core/python-agentic-core/app/services/links/transcribed_text_threat_agent_link.py`
- `lane-agentic-core/python-agentic-core/app/routes/score.py`

Flow skeleton RAG Engine LangChain -> Search Query -> Threat Agent da setup:
- `lane-storage/python-storage/app/models/contracts.py`
- `lane-storage/python-storage/app/services/internal_link_orchestrator.py`
- `lane-storage/python-storage/app/services/channels/search_query_channel.py`
- `lane-storage/python-storage/app/services/links/rag_engine_langchain_search_query_link.py`
- `lane-storage/python-storage/app/services/links/search_query_threat_agent_link.py`
- `lane-storage/python-storage/app/routes/storage.py`
- `lane-agentic-core/python-agentic-core/app/models/contracts.py`
- `lane-agentic-core/python-agentic-core/app/clients/storage_client.py`
- `lane-agentic-core/python-agentic-core/app/services/agents/threat_agent.py`
- `lane-agentic-core/python-agentic-core/app/services/orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/internal_link_orchestrator.py`
- `lane-agentic-core/python-agentic-core/app/services/channels/search_query_channel.py`
- `lane-agentic-core/python-agentic-core/app/services/links/search_query_threat_link.py`
- `lane-agentic-core/python-agentic-core/app/routes/score.py`

## Lane 4: Storage and Feedback Loop
Folder:
- `lane-agentic-core/data/local`
- `lane-storage/python-storage/app/*`
- `shared/contracts/event-schema`
- `lane-end-user/feature/history`
- `lane-end-user/service/feedbacksync`

Trach nhiem:
- Luu risk metadata local (history timeline).
- Dong bo feedback Scam/Safe/Not sure len feedback ingestion.
- Su dung schema thong nhat giua mobile-backend.
- Python storage lane cung cap vector index, scam pattern retrieval, feedback ingestion API.

## Ban viet lai day du cac moc noi (4 lane)

Muc tieu phan nay: viet lai theo muc chi tiet cao, bo sung du cac moc noi runtime giua 4 lane:
- Lane 1 End User
- Lane 2 API Gateway
- Lane 3 Agentic AI Core
- Lane 4 Storage and Feedback Loop

### A) Luong phan tich chinh (signal -> score -> warning)

1. Mobile App thu nhan signal dau vao (SMS/CALL/URL) tai End User lane.
2. Mobile App day signal vao Background Service qua bridge Mobile App -> Background Service.
3. Background Service chuan hoa payload va chuyen qua TFLite On-device Filter.
4. TFLite tra ket qua suspicious/masked/confidence ve Warning flow o End User lane.
5. End User co 2 huong:
- Huong local warning ngay (UI warning explanation).
- Huong goi cloud de phan tich sau qua API Gateway lane.
6. API Gateway nhan request `/v1/signals/analyze`, validate auth, tao cache key.
7. API Gateway lookup cache layer theo phone/url/script key.
8. Neu cache-hit: API Gateway tra warning nhanh cho End User (khong can deep pipeline).
9. Neu cache-miss: API Gateway chuyen request sang Agentic Core lane (`/v1/agentic/score`).
10. Agentic Orchestrator fan-out thanh cac stage: Raw Audio, Voice Stream, Text/Metadata.
11. Raw Audio -> Deepfake Agent.
12. Voice Stream -> Google STT API -> Transcribed Text.
13. Transcribed Text -> Threat Agent.
14. Text/Metadata -> Entity Agent.
15. Threat/Deepfake/Entity signal-score hop ve Decision & Reasoning Engine.
16. Decision Engine tong hop score + explanation, dong bo reasoning voi Gemini stage.
17. Decision output -> JSON score + warning -> Cloud Run API Microservices stage.
18. Ket qua phan tich duoc tra nguoc ve API Gateway va tra response warning cho End User.

### B) Luong cache va moc noi cache-miss

1. Cloud Run API Microservices -> Cache Layer (redis) theo 3 kenh phone/url/script.
2. Cache Layer -> cache miss -> Orchestrator Agent LangGraph Router.
3. Cloud Run API Microservices -> cache miss -> Orchestrator Agent LangGraph Router.
4. Cac moc noi cache tren duoc scaffold rieng bang contracts/channels/links/routes de team co the dien logic.

### C) Luong update database va vector indexing

1. Cloud Run API Microservices -> Update database.
2. Update database -> Vector Database Vertex AI.
3. Storage lane tiep nhan du lieu update va dua vao vector write path.
4. Muc tieu: giu cho data-plane va retrieval-plane dong bo voi output tu cloud scoring.

### D) Luong RAG/Threat bo tro phan tich

1. Storage lane ho tro semantic retrieval qua `/v1/storage/search`.
2. RAG Engine LangChain -> Search Query.
3. Search Query -> Threat Agent (handoff retrieval context).
4. Threat Agent dung context tu Search Query de tao threat signals truoc khi dua vao Decision Engine.

### E) Luong STT chi tiet (tach ro 2 canh)

1. Voice Stream -> Google STT API.
2. Google STT API -> Transcribed Text.
3. Transcribed Text -> Threat Agent.
4. Vi tri tach canh nay da co contract va endpoint noi bo rieng de team trien khai theo stage.

### F) Luong feedback loop dong vong

1. End User warning UI -> user interact -> chon feedback (Scam/Safe/Not sure).
2. User feedback -> feedback label -> feedback ingestion.
3. Feedback ingestion -> Cache Layer (redis) theo phone/url/script.
4. API Gateway nhan feedback qua `/v1/feedback`, chuyen xuong Storage lane `/v1/storage/feedback`.
5. Storage lane luu feedback event cho training/evaluation/audit.

### G) Bang moc noi inbound/outbound theo lane

1. Lane 1 End User
- Inbound: warning result tu API Gateway; cache-hit instant warning.
- Outbound: signal dau vao, streaming call chunk, feedback labels.

2. Lane 2 API Gateway
- Inbound: `/v1/signals/analyze`, `/v1/feedback`.
- Outbound: `/v1/agentic/score`, `/v1/storage/index`, `/v1/storage/feedback`.
- Internal handoff: auth -> cloud run -> cache -> cache-miss -> orchestrator router; cloud run -> update database -> vector db.

3. Lane 3 Agentic AI Core
- Inbound: request score tu API Gateway, search-query handoff contexts.
- Outbound: JSON score + warning ve cloud stage; metadata sync xuong Storage.
- Internal handoff: orchestrator -> (deepfake, stt, threat, entity) -> decision -> reasoning -> json.

4. Lane 4 Storage and Feedback Loop
- Inbound: index signal, feedback event, search query.
- Outbound: semantic matches/pattern contexts, vector write ack.
- Internal handoff: rag <-> vector, scam pattern <-> vector, update database -> vector, rag-search-query -> threat handoff.

### H) Checklist kiem tra 4 lane sau moi dot scaffold

1. Kiem tra diagnostics toan workspace khong co error moi.
2. Kiem tra compile lane Python: API Gateway, Agentic Core, Storage.
3. Kiem tra compile lane Kotlin: app, service, feature, core/network, domain/data.
4. Kiem tra docs mapping cap nhat dong bo voi file contracts/channels/links/routes vua tao.

## Voice Test Asset Mapping
Folder:
- `lane-end-user/assets/audio`

File:
- `scam_call.wav`
- `real_call.wav`

Muc dich:
- Demo incoming call scenario truoc khi AI classify authenticity.
