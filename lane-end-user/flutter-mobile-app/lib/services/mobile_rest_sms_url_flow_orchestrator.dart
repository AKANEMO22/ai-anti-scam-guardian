import '../contracts/mobile_rest_cloud_run_contracts.dart';
import 'cloud_run_microservices_rest_link.dart';
import 'rest_sms_url_channel.dart';

class MobileRestSmsUrlFlowOrchestrator {
  MobileRestSmsUrlFlowOrchestrator({
    required this.channel,
    required this.cloudRunLink,
  });

  final RestSmsUrlChannel channel;
  final CloudRunMicroservicesRestLink cloudRunLink;

  Future<CloudRunRiskResponse> linkMobileAppToRestToCloudRun(
    MobileAppToRestRequest request,
  ) async {
    // mocked
    print("mocked");
  }

  Future<CloudRunRiskResponse> linkSmsRestToCloudRun(
    MobileAppToRestRequest request,
  ) async {
    // mocked
    print("mocked");
  }

  Future<CloudRunRiskResponse> linkUrlRestToCloudRun(
    MobileAppToRestRequest request,
  ) async {
    // mocked
    print("mocked");
  }
}
