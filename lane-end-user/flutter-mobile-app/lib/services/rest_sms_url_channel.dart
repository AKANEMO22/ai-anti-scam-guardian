import '../contracts/mobile_rest_cloud_run_contracts.dart';

class RestSmsUrlChannel {
  MobileRestSignalPayload receiveFromMobileApp(MobileAppToRestRequest request) {
    // mocked
    throw UnimplementedError();
  }

  MobileRestSignalPayload normalizeSmsPayload(MobileRestSignalPayload payload) {
    // mocked
    throw UnimplementedError();
  }

  MobileRestSignalPayload normalizeUrlPayload(MobileRestSignalPayload payload) {
    // mocked
    throw UnimplementedError();
  }

  void validateRestPayload(MobileRestSignalPayload payload) { throw UnimplementedError(); }
}
