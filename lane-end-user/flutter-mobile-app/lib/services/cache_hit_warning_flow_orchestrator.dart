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
    // mocked
    print("mocked");
  }

  UiWarningExplanationState linkPhoneCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // mocked
    print("mocked");
  }

  UiWarningExplanationState linkUrlCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // mocked
    print("mocked");
  }

  UiWarningExplanationState linkScriptCacheHitToUiWarningExplanation(
    CacheLayerToCacheHitRequest request,
  ) {
    // mocked
    print("mocked");
  }
}
