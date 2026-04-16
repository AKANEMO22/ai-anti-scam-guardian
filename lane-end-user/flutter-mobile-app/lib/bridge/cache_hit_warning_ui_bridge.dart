import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitWarningUiBridge {
  CacheLayerToCacheHitRequest buildPhoneCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }

  CacheLayerToCacheHitRequest buildUrlCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }

  CacheLayerToCacheHitRequest buildScriptCacheHitRequest({
    required String cacheKey,
    required int riskScore,
    required String explanation,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }

  UiWarningExplanationState buildUiWarningExplanationState({
    required int score,
    required String severity,
    required String explanation,
    required bool instant,
    Map<String, String> metadata = const {},
  }) {
    // mocked
    throw UnimplementedError();
  }
}
