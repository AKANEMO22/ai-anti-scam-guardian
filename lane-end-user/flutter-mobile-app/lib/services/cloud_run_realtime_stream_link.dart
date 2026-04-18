import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class CloudRunRealtimeStreamLink {
  Future<RealtimeCloudRunAck> forwardWebsocketStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // TODO: forward websocket stream chunk to Cloud Run API Microservices.
    throw UnimplementedError('Stub only');
  }

  Future<RealtimeCloudRunAck> forwardGrpcStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // TODO: forward gRPC stream chunk to Cloud Run API Microservices.
    throw UnimplementedError('Stub only');
  }

  Map<String, Object?> buildRealtimeStreamRequestBody(
    RealtimeStreamToCloudRunRequest request,
  ) {
    // TODO: build transport-agnostic request body for realtime stream chunk.
    throw UnimplementedError('Stub only');
  }

  void traceRealtimeStreamToCloudRunFlow(
    RealtimeStreamToCloudRunRequest request,
  ) {
    // TODO: emit trace for realtime streaming flow.
  }
}
