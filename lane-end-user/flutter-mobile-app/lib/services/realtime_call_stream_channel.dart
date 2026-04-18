import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class RealtimeCallStreamChannel {
  RealtimeCallChunkPayload receiveFromMobileApp(
    MobileAppToRealtimeStreamRequest request,
  ) {
    // TODO: receive Flutter realtime call chunk and map to stream payload.
    throw UnimplementedError('Stub only');
  }

  RealtimeCallChunkPayload normalizeRealtimeChunk(
    RealtimeCallChunkPayload chunk,
  ) {
    // TODO: normalize realtime call chunk before Cloud Run streaming.
    throw UnimplementedError('Stub only');
  }

  void validateRealtimeChunk(RealtimeCallChunkPayload chunk) {
    // TODO: validate chunk contract for websocket/grpc transport.
  }

  RealtimeStreamToCloudRunRequest routeWebsocketChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // TODO: build websocket streaming request for Cloud Run.
    throw UnimplementedError('Stub only');
  }

  RealtimeStreamToCloudRunRequest routeGrpcChunkToCloudRun(
    RealtimeCallChunkPayload chunk,
    RealtimeCloudRunTarget target,
  ) {
    // TODO: build gRPC streaming request for Cloud Run.
    throw UnimplementedError('Stub only');
  }
}
