enum CacheSignalType {
  phone,
  url,
  script,
}

class RedisCacheResultPayload {
  const RedisCacheResultPayload({
    required this.signalType,
    required this.cacheKey,
    required this.cacheHit,
    required this.riskScore,
    required this.explanation,
    this.metadata = const {},
  });

  final CacheSignalType signalType;
  final String cacheKey;
  final bool cacheHit;
  final int riskScore;
  final String explanation;
  final Map<String, String> metadata;
}

class CacheLayerToCacheHitRequest {
  const CacheLayerToCacheHitRequest({
    required this.payload,
    this.source = 'redis-cache-layer',
  });

  final RedisCacheResultPayload payload;
  final String source;
}

class CacheHitToInstantWarningRequest {
  const CacheHitToInstantWarningRequest({
    required this.payload,
  });

  final RedisCacheResultPayload payload;
}

class InstantWarningPayload {
  const InstantWarningPayload({
    required this.signalType,
    required this.riskScore,
    required this.title,
    required this.message,
    this.metadata = const {},
  });

  final CacheSignalType signalType;
  final int riskScore;
  final String title;
  final String message;
  final Map<String, String> metadata;
}

class InstantWarningToUiExplanationRequest {
  const InstantWarningToUiExplanationRequest({
    required this.warning,
  });

  final InstantWarningPayload warning;
}

class UiWarningExplanationState {
  const UiWarningExplanationState({
    required this.score,
    required this.severity,
    required this.explanation,
    required this.instant,
    this.metadata = const {},
  });

  final int score;
  final String severity;
  final String explanation;
  final bool instant;
  final Map<String, String> metadata;
}
