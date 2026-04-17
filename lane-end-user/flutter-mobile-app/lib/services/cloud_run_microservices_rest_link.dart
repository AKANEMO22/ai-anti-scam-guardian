import '../contracts/mobile_rest_cloud_run_contracts.dart';

class CloudRunMicroservicesRestLink {
  Future<CloudRunRiskResponse> forwardRestSmsUrlToCloudRun(
    RestToCloudRunRequest request,
  ) async {
    // TODO: send REST request to Cloud Run API Microservices.
    throw UnimplementedError('Stub only');
  }

  Map<String, Object?> buildCloudRunRequestBody(RestToCloudRunRequest request) {
    // TODO: build REST body for SMS/URL Cloud Run endpoint.
    throw UnimplementedError('Stub only');
  }

  void traceRestToCloudRunFlow(RestToCloudRunRequest request) {
    // TODO: emit trace for REST SMS/URL -> Cloud Run API Microservices flow.
  }
}
