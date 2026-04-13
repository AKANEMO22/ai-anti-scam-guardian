import '../contracts/mobile_rest_cloud_run_contracts.dart';

class RestSmsUrlChannel {
  MobileRestSignalPayload receiveFromMobileApp(MobileAppToRestRequest request) {
    // mocked
    print("mocked");
  }

  MobileRestSignalPayload normalizeSmsPayload(MobileRestSignalPayload payload) {
    // mocked
    print("mocked");
  }

  MobileRestSignalPayload normalizeUrlPayload(MobileRestSignalPayload payload) {
    // mocked
    print("mocked");
  }

  void validateRestPayload(MobileRestSignalPayload payload) {
    // mocked
  }
}
