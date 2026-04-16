import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitWarningChannel {
  RedisCacheResultPayload receiveFromRedisCacheLayer(
    CacheLayerToCacheHitRequest request,
  ) {
    // mocked
    throw UnimplementedError();
  }

  RedisCacheResultPayload normalizeCacheResultPayload(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    throw UnimplementedError();
  }

  void validateCacheHitPayload(RedisCacheResultPayload payload) { throw UnimplementedError(); }

  CacheHitToInstantWarningRequest routePhoneCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    throw UnimplementedError();
  }

  CacheHitToInstantWarningRequest routeUrlCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    throw UnimplementedError();
  }

  CacheHitToInstantWarningRequest routeScriptCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // mocked
    throw UnimplementedError();
  }
}
