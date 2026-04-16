import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/risk_response.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator to access localhost
  static const String baseUrl = 'http://10.0.2.2:8100'; 
  static const String bearerToken = 'test';

  Future<RiskResponse> analyzeSignal({
    required SourceType sourceType,
    required String text,
    Map<String, dynamic> metadata = const {},
  }) async {
    final url = Uri.parse('$baseUrl/v1/signals/analyze');
    
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $bearerToken',
        },
        body: jsonEncode({
          'sourceType': sourceType.name,
          'text': text,
          'metadata': metadata,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return RiskResponse.fromJson(data);
      } else {
        throw Exception('Failed to analyze signal: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Connection error: $e');
    }
  }

  Future<bool> submitFeedback({
    required String eventId,
    required bool isScam,
    String? userComment,
  }) async {
    final url = Uri.parse('$baseUrl/v1/feedback');
    
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $bearerToken',
        },
        body: jsonEncode({
          'eventId': eventId,
          'isScam': isScam,
          'userComment': userComment,
          'timestamp': DateTime.now().toIso8601String(),
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['accepted'] ?? false;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
