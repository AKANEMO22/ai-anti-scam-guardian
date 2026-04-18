import '../contracts/mobile_rest_cloud_run_contracts.dart';

class MobileAppFlutterRestBridge {
  MobileAppToRestRequest buildSmsRestRequest({
    required String smsText,
    String? sessionId,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build Flutter SMS request for REST Cloud Run flow.
    throw UnimplementedError('Stub only');
  }

  MobileAppToRestRequest buildUrlRestRequest({
    required String url,
    String? sessionId,
    Map<String, String> metadata = const {},
  }) {
    // TODO: build Flutter URL request for REST Cloud Run flow.
    throw UnimplementedError('Stub only');
  }

  RestDispatchAck buildRestDispatchAck({
    required bool accepted,
    String message = '',
  }) {
    // TODO: build local ack result for app-side flow state.
    throw UnimplementedError('Stub only');
  }
}
