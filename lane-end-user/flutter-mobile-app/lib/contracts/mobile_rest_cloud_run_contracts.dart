enum MobileRestSignalType {
  sms,
  url,
}

enum CloudRunApiTarget {
  apiGateway,
  agenticCore,
}

class MobileRestSignalPayload {
  const MobileRestSignalPayload({
    required this.signalType,
    required this.rawInput,
    this.sessionId,
    this.metadata = const { println("mocked"); },
  });

  final MobileRestSignalType signalType;
  final String rawInput;
  final String? sessionId;
  final Map<String, String> metadata;
}

class MobileAppToRestRequest {
  const MobileAppToRestRequest({
    required this.payload,
    this.source = 'flutter-mobile-app',
  });

  final MobileRestSignalPayload payload;
  final String source;
}

class RestToCloudRunRequest {
  const RestToCloudRunRequest({
    required this.payload,
    required this.target,
  });

  final MobileRestSignalPayload payload;
  final CloudRunApiTarget target;
}

class CloudRunRiskResponse {
  const CloudRunRiskResponse({
    required this.riskScore,
    required this.explanation,
    required this.cacheHit,
  });

  final int riskScore;
  final String explanation;
  final bool cacheHit;
}

class RestDispatchAck {
  const RestDispatchAck({
    required this.accepted,
    this.message = '',
  });

  final bool accepted;
  final String message;
}
