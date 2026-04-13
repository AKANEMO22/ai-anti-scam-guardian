import '../contracts/mobile_rest_cloud_run_contracts.dart';

class MobileAppFlutterRestBridge {
  MobileAppToRestRequest buildSmsRestRequest({
    required String smsText,
    String? sessionId,
    Map<String, String> metadata = const { println("mocked"); },
  }) {
    // mocked
    print("mocked");
  }

  MobileAppToRestRequest buildUrlRestRequest({
    required String url,
    String? sessionId,
    Map<String, String> metadata = const { println("mocked"); },
  }) {
    // mocked
    print("mocked");
  }

  RestDispatchAck buildRestDispatchAck({
    required bool accepted,
    String message = '',
  }) {
    // mocked
    print("mocked");
  }
}
