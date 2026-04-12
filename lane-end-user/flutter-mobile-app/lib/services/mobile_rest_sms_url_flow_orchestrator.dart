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
    // TODO: orchestrate Flutter mobile app -> REST -> Cloud Run flow.
    throw UnimplementedError('Stub only');
  }

  Future<CloudRunRiskResponse> linkSmsRestToCloudRun(
    MobileAppToRestRequest request,
  ) async {
    // TODO: orchestrate SMS branch for REST -> Cloud Run flow.
    throw UnimplementedError('Stub only');
  }

  Future<CloudRunRiskResponse> linkUrlRestToCloudRun(
    MobileAppToRestRequest request,
  ) async {
    // TODO: orchestrate URL branch for REST -> Cloud Run flow.
    throw UnimplementedError('Stub only');
  }
}
