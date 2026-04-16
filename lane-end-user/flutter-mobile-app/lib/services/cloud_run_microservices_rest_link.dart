import '../contracts/mobile_rest_cloud_run_contracts.dart';

class CloudRunMicroservicesRestLink {
  Future<CloudRunRiskResponse> forwardRestSmsUrlToCloudRun(
    RestToCloudRunRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }

  Map<String, Object?> buildCloudRunRequestBody(RestToCloudRunRequest request) {
    // mocked
    throw UnimplementedError();
  }

  void traceRestToCloudRunFlow(RestToCloudRunRequest request) { throw UnimplementedError(); }
}
