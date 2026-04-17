import '../contracts/mobile_rest_cloud_run_contracts.dart';

class RestSmsUrlChannel {
  MobileRestSignalPayload receiveFromMobileApp(MobileAppToRestRequest request) {
    // TODO: receive Flutter mobile payload and map into REST stage payload.
    throw UnimplementedError('Stub only');
  }

  MobileRestSignalPayload normalizeSmsPayload(MobileRestSignalPayload payload) {
    // TODO: normalize SMS payload before Cloud Run REST request.
    throw UnimplementedError('Stub only');
  }

  MobileRestSignalPayload normalizeUrlPayload(MobileRestSignalPayload payload) {
    // TODO: normalize URL payload before Cloud Run REST request.
    throw UnimplementedError('Stub only');
  }

  void validateRestPayload(MobileRestSignalPayload payload) {
    // TODO: validate REST payload contract for SMS/URL channels.
  }
}
