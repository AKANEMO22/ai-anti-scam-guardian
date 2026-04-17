import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';

class MobileAppRealtimeStreamBridge {
  MobileAppToRealtimeStreamRequest buildWebsocketCallChunkRequest({
    required String sessionId,
    required String chunkRef,
    required int sequence,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build websocket call-chunk request from Flutter layer.
    throw UnimplementedError('Stub only');
  }

  MobileAppToRealtimeStreamRequest buildGrpcCallChunkRequest({
    required String sessionId,
    required String chunkRef,
    required int sequence,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build grpc call-chunk request from Flutter layer.
    throw UnimplementedError('Stub only');
  }

  RealtimeCloudRunAck buildRealtimeStreamAck({
    required bool accepted,
    required String sessionId,
    String message = '',
  }) {
    // TODO: build local ack object for streaming flow state.
    throw UnimplementedError('Stub only');
  }
}
