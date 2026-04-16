import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class RealtimeCallStreamChannel {
  RealtimeCallChunkPayload receiveFromMobileApp(
    MobileAppToRealtimeStreamRequest request,
  ) {
    // mocked
    throw UnimplementedError();
  }

  RealtimeCallChunkPayload normalizeRealtimeChunk(
    RealtimeCallChunkPayload chunk,
  ) {
    // mocked
    throw UnimplementedError();
  }

  void validateRealtimeChunk(RealtimeCallChunkPayload chunk) { throw UnimplementedError(); }

  RealtimeStreamToCloudRunRequest routeWebsocketChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // mocked
    throw UnimplementedError();
  }

  RealtimeStreamToCloudRunRequest routeGrpcChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // mocked
    throw UnimplementedError();
  }
}
