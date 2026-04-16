import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class MobileAppRealtimeStreamBridge {
  MobileAppToRealtimeStreamRequest buildWebsocketCallChunkRequest({
    required String sessionId,
    required String chunkRef,
    required int sequence,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }

  MobileAppToRealtimeStreamRequest buildGrpcCallChunkRequest({
    required String sessionId,
    required String chunkRef,
    required int sequence,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }

  RealtimeCloudRunAck buildRealtimeStreamAck({
    required bool accepted,
    required String sessionId,
    String message = '',
  }) {
    // mocked
    throw UnimplementedError();
  }
}
