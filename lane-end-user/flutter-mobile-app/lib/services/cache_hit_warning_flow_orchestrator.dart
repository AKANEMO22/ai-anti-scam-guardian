import '../contracts/cache_hit_warning_flow_contracts.dart';
import 'cache_hit_instant_warning_link.dart';
import 'cache_hit_warning_channel.dart';
import 'instant_warning_ui_explanation_link.dart';

class CacheHitWarningFlowOrchestrator {
  CacheHitWarningFlowOrchestrator({
    required this.channel,
    required this.cacheHitInstantWarningLink,
    required this.instantWarningUiExplanationLink,
  });

  final CacheHitWarningChannel channel;
  final CacheHitInstantWarningLink cacheHitInstantWarningLink;
  final InstantWarningUiExplanationLink instantWarningUiExplanationLink;

  UiWarningExplanationState linkCacheLayerToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // TODO: orchestrate Redis cache layer -> cache hit -> instant warning -> UI explanation.
    throw UnimplementedError('Stub only');
  }

  UiWarningExplanationState linkPhoneCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // TODO: orchestrate phone branch for cache-hit instant warning flow.
    throw UnimplementedError('Stub only');
  }

  UiWarningExplanationState linkUrlCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // TODO: orchestrate URL branch for cache-hit instant warning flow.
    throw UnimplementedError('Stub only');
  }

  UiWarningExplanationState linkScriptCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // TODO: orchestrate script branch for cache-hit instant warning flow.
    throw UnimplementedError('Stub only');
  }
}
