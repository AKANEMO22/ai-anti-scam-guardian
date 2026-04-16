import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class CloudRunRealtimeStreamLink {
  Future<RealtimeCloudRunAck> forwardWebsocketStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }

  Future<RealtimeCloudRunAck> forwardGrpcStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }

  Map<String, Object?> buildRealtimeStreamRequestBody(
    RealtimeStreamToCloudRunRequest request,
  ) {
    // mocked
    throw UnimplementedError();
  }

  void traceRealtimeStreamToCloudRunFlow(
    RealtimeStreamToCloudRunRequest request,
  ) { throw UnimplementedError(); }
}
