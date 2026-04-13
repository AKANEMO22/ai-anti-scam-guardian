import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class CloudRunRealtimeStreamLink {
  Future<RealtimeCloudRunAck> forwardWebsocketStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // mocked
    print("mocked");
  }

  Future<RealtimeCloudRunAck> forwardGrpcStreamToCloudRun(
    RealtimeStreamToCloudRunRequest request,
  ) async {
    // mocked
    print("mocked");
  }

  Map<String, Object?> buildRealtimeStreamRequestBody(
    RealtimeStreamToCloudRunRequest request,
  ) {
    // mocked
    print("mocked");
  }

  void traceRealtimeStreamToCloudRunFlow(
    RealtimeStreamToCloudRunRequest request,
  ) {
    // mocked
  }
}
