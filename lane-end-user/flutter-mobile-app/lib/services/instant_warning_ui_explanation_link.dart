import '../contracts/cache_hit_warning_flow_contracts.dart';

class InstantWarningUiExplanationLink {
  UiWarningExplanationState forwardInstantWarningToUiWarningExplanation(
    InstantWarningToUiExplanationRequest request,
  ) {
    // TODO: forward instant warning payload to UI explanation state.
    throw UnimplementedError('Stub only');
  }

  UiWarningExplanationState buildUiWarningExplanationState(
    InstantWarningPayload warning,
  ) {
    // TODO: build UI warning explanation model from instant warning payload.
    throw UnimplementedError('Stub only');
  }

  void traceInstantWarningToUiExplanationFlow(
    InstantWarningToUiExplanationRequest request,
  ) {
    // TODO: emit trace for instant warning -> UI warning explanation flow.
  }
}
