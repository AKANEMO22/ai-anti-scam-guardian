import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitWarningUiBridge {
  CacheLayerToCacheHitRequest buildPhoneCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build phone cache-hit request from redis response context.
    throw UnimplementedError('Stub only');
  }

  CacheLayerToCacheHitRequest buildUrlCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build URL cache-hit request from redis response context.
    throw UnimplementedError('Stub only');
  }

  CacheLayerToCacheHitRequest buildScriptCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build script cache-hit request from redis response context.
    throw UnimplementedError('Stub only');
  }

  UiWarningExplanationState buildUiWarningExplanationState({
    required int score,
    required String severity,
    required String explanation,
    required bool instant,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build UI warning explanation state object for presentation layer.
    throw UnimplementedError('Stub only');
  }
}
