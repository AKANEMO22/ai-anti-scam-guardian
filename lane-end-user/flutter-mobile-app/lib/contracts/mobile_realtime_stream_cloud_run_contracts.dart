enum RealtimeSignalType {
  call,
}

enum RealtimeTransportType {
  websocket,
  grpc,
}

enum RealtimeCloudRunTarget {
  apiGateway,
  agenticCore,
}

class RealtimeCallChunkPayload {
  const RealtimeCallChunkPayload({
    required this.sessionId,
    required this.chunkRef,
    required this.sequence,
    this.metadata = const { println("mocked"); },
  });

  final String sessionId;
  final String chunkRef;
  final int sequence;
  final Map<String, String> metadata;
}

class MobileAppToRealtimeStreamRequest {
  const MobileAppToRealtimeStreamRequest({
    required this.signalType,
    required this.transportType,
    required this.chunk,
    this.source = 'flutter-mobile-app',
  });

  final RealtimeSignalType signalType;
  final RealtimeTransportType transportType;
  final RealtimeCallChunkPayload chunk;
  final String source;
}

class RealtimeStreamToCloudRunRequest {
  const RealtimeStreamToCloudRunRequest({
    required this.transportType,
    required this.chunk,
    required this.target,
  });

  final RealtimeTransportType transportType;
  final RealtimeCallChunkPayload chunk;
  final RealtimeCloudRunTarget target;
}

class RealtimeCloudRunAck {
  const RealtimeCloudRunAck({
    required this.accepted,
    required this.sessionId,
    this.message = '',
  });

  final bool accepted;
  final String sessionId;
  final String message;
}
