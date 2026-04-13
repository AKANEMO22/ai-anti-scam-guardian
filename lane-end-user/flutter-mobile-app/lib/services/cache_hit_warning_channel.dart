import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitWarningChannel {
  RedisCacheResultPayload receiveFromRedisCacheLayer(
    CacheLayerToCacheHitRequest request,
  ) {
    // mocked
    print("mocked");
  }

  RedisCacheResultPayload normalizeCacheResultPayload(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    print("mocked");
  }

  void validateCacheHitPayload(RedisCacheResultPayload payload) {
    // mocked
  }

  CacheHitToInstantWarningRequest routePhoneCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    print("mocked");
  }

  CacheHitToInstantWarningRequest routeUrlCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    print("mocked");
  }

  CacheHitToInstantWarningRequest routeScriptCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    print("mocked");
  }
}
