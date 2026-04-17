import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitWarningChannel {
  RedisCacheResultPayload receiveFromRedisCacheLayer(
    CacheLayerToCacheHitRequest request,
  ) {
    // TODO: receive Redis cache-layer payload for cache-hit stage.
    throw UnimplementedError('Stub only');
  }

  RedisCacheResultPayload normalizeCacheResultPayload(
    RedisCacheResultPayload payload,
  ) {
    // TODO: normalize phone/url/script cache payload before instant warning.
    throw UnimplementedError('Stub only');
  }

  void validateCacheHitPayload(RedisCacheResultPayload payload) {
    // TODO: validate cache-hit payload fields required by warning stage.
  }

  CacheHitToInstantWarningRequest routePhoneCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // TODO: build phone cache-hit request to instant warning stage.
    throw UnimplementedError('Stub only');
  }

  CacheHitToInstantWarningRequest routeUrlCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // TODO: build URL cache-hit request to instant warning stage.
    throw UnimplementedError('Stub only');
  }

  CacheHitToInstantWarningRequest routeScriptCacheHit(
    RedisCacheResultPayload payload,
  ) {
    // TODO: build script cache-hit request to instant warning stage.
    throw UnimplementedError('Stub only');
  }
}
