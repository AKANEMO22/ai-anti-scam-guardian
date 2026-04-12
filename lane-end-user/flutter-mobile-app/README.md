# Flutter Mobile App Flow Skeleton

Flow:
- Mobile App Flutter -> REST for SMS/URL -> Cloud Run API Microservices
- Mobile App Flutter -> WebSocket/gRPC streaming for realtime call -> Cloud Run API Microservices
- Cache layer (Redis) phone/URL/script -> Cache hit -> Instant warning -> UI warning explanation

File mapping:
- `lib/contracts/mobile_rest_cloud_run_contracts.dart`
- `lib/services/rest_sms_url_channel.dart`
- `lib/services/cloud_run_microservices_rest_link.dart`
- `lib/services/mobile_rest_sms_url_flow_orchestrator.dart`
- `lib/bridge/mobile_app_flutter_rest_bridge.dart`
- `lib/contracts/mobile_realtime_stream_cloud_run_contracts.dart`
- `lib/contracts/cache_hit_warning_flow_contracts.dart`
- `lib/services/realtime_call_stream_channel.dart`
- `lib/services/cloud_run_realtime_stream_link.dart`
- `lib/services/mobile_realtime_stream_flow_orchestrator.dart`
- `lib/services/cache_hit_warning_channel.dart`
- `lib/services/cache_hit_instant_warning_link.dart`
- `lib/services/instant_warning_ui_explanation_link.dart`
- `lib/services/cache_hit_warning_flow_orchestrator.dart`
- `lib/bridge/mobile_app_realtime_stream_bridge.dart`
- `lib/bridge/cache_hit_warning_ui_bridge.dart`

Note:
- All methods are scaffold-only placeholders and intentionally throw `UnimplementedError`.
- Team implementation can fill HTTP/WebSocket/gRPC client logic, auth token attachment, and error handling.