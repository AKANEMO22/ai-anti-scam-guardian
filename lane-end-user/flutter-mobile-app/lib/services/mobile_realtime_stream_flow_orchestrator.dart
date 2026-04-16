import '../contracts/mobile_realtime_stream_cloud_run_contracts.dart';
import 'cloud_run_realtime_stream_link.dart';
import 'realtime_call_stream_channel.dart';

class MobileRealtimeStreamFlowOrchestrator {
  MobileRealtimeStreamFlowOrchestrator({
    required this.channel,
    required this.cloudRunLink,
  });

  final RealtimeCallStreamChannel channel;
  final CloudRunRealtimeStreamLink cloudRunLink;

  Future<RealtimeCloudRunAck> linkMobileAppToRealtimeStreamToCloudRun(
    MobileAppToRealtimeStreamRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }

  Future<RealtimeCloudRunAck> linkWebsocketStreamToCloudRun(
    MobileAppToRealtimeStreamRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }

  Future<RealtimeCloudRunAck> linkGrpcStreamToCloudRun(
    MobileAppToRealtimeStreamRequest request,
  ) async {
    // mocked
    throw UnimplementedError();
  }
}
