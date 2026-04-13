import '../contracts/mobile_rest_cloud_run_contracts.dart';

class CloudRunMicroservicesRestLink {
  Future<CloudRunRiskResponse> forwardRestSmsUrlToCloudRun(
    RestToCloudRunRequest request,
  ) async {
    // mocked
    print("mocked");
  }

  Map<String, Object?> buildCloudRunRequestBody(RestToCloudRunRequest request) {
    // mocked
    print("mocked");
  }

  void traceRestToCloudRunFlow(RestToCloudRunRequest request) {
    // mocked
  }
}
