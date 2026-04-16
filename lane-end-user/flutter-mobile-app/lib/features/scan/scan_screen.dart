import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/risk_response.dart';
import '../../providers/scanning_provider.dart';
import '../../core/theme.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final TextEditingController _controller = TextEditingController();

  void _handleScan() {
    if (_controller.text.isEmpty) return;
    
    final provider = Provider.of<ScanningProvider>(context, listen: false);
    provider.scanText(_controller.text, SourceType.SMS).catchError((e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: AppTheme.dangerColor),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Manual Scan'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              maxLines: 6,
              decoration: InputDecoration(
                hintText: 'Paste suspicious text, SMS, or URL here...',
                fillColor: AppTheme.cardColor,
                filled: true,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: Consumer<ScanningProvider>(
                builder: (context, provider, child) {
                  return ElevatedButton(
                    onPressed: provider.isScanning ? null : _handleScan,
                    child: provider.isScanning
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text('Analyze with AI'),
                  );
                },
              ),
            ),
            const SizedBox(height: 32),
            Consumer<ScanningProvider>(
              builder: (context, provider, child) {
                if (provider.lastResponse == null) return const SizedBox();
                final risk = provider.lastResponse!;
                
                return Column(
                  children: [
                    _buildRiskIndicator(risk.riskScore),
                    const SizedBox(height: 24),
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: AppTheme.cardColor,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('AI Explanation', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                          const SizedBox(height: 12),
                          Text(risk.explanation, style: const TextStyle(height: 1.5)),
                        ],
                      ),
                    ),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRiskIndicator(int score) {
    Color color = AppTheme.accentColor;
    if (score > 70) color = AppTheme.dangerColor;
    else if (score > 30) color = AppTheme.warningColor;

    return Column(
      children: [
        Text(
          '$score%',
          style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: color),
        ),
        Text('RISK SCORE', style: TextStyle(color: color.withOpacity(0.7), letterSpacing: 2)),
      ],
    );
  }
}
