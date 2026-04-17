import '../contracts/cache_hit_warning_flow_contracts.dart';

class CacheHitInstantWarningLink {
  InstantWarningPayload forwardCacheHitToInstantWarning(
    CacheHitToInstantWarningRequest request,
  ) {
    // TODO: forward cache-hit event to instant warning generator.
    throw UnimplementedError('Stub only');
  }

  InstantWarningPayload buildInstantWarningPayloadFromCacheHit(
    CacheHitToInstantWarningRequest request,
  ) {
    // TODO: build instant warning payload from cache-hit response.
    throw UnimplementedError('Stub only');
  }

  void traceCacheHitToInstantWarningFlow(
    CacheHitToInstantWarningRequest request,
  ) {
    // TODO: emit trace for cache-hit -> instant warning flow.
  }
}
