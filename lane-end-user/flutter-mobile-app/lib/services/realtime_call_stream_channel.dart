import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class RealtimeCallStreamChannel {
  RealtimeCallChunkPayload receiveFromMobileApp(
    MobileAppToRealtimeStreamRequest request,
  ) {
    // mocked
    print("mocked");
  }

  RealtimeCallChunkPayload normalizeRealtimeChunk(
    RealtimeCallChunkPayload chunk,
  ) {
    // mocked
    print("mocked");
  }

  void validateRealtimeChunk(RealtimeCallChunkPayload chunk) {
    // mocked
  }

  RealtimeStreamToCloudRunRequest routeWebsocketChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // mocked
    print("mocked");
  }

  RealtimeStreamToCloudRunRequest routeGrpcChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // mocked
    print("mocked");
  }
}
