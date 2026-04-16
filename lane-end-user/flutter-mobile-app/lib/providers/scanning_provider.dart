import 'package:flutter/material.dart';
import '../models/risk_response.dart';
import '../services/api_service.dart';

class ScanResult {
  final String text;
  final RiskResponse response;
  final DateTime timestamp;

  ScanResult({
    required this.text,
    required this.response,
    required this.timestamp,
  });
}

class ScanningProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  bool _isScanning = false;
  bool get isScanning => _isScanning;

  RiskResponse? _lastResponse;
  RiskResponse? get lastResponse => _lastResponse;

  final List<ScanResult> _history = [];
  List<ScanResult> get history => List.unmodifiable(_history);

  Future<void> scanText(String text, SourceType type) async {
    _isScanning = true;
    _lastResponse = null;
    notifyListeners();

    try {
      final response = await _apiService.analyzeSignal(
        sourceType: type,
        text: text,
      );
      
      _lastResponse = response;
      _history.insert(0, ScanResult(
        text: text,
        response: response,
        timestamp: DateTime.now(),
      ));
    } catch (e) {
      rethrow;
    } finally {
      _isScanning = false;
      notifyListeners();
    }
  }

  void clearHistory() {
    _history.clear();
    notifyListeners();
  }
}
