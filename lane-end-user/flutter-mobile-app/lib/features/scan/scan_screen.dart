import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: AppTheme.dangerColor),
        );
      }
    });
  }

  void _copyToClipboard(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Baiter response copied to clipboard!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Anti-Scam Analysis'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'Paste suspicious text, SMS, or URL here...',
                fillColor: AppTheme.cardColor,
                filled: true,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: Consumer<ScanningProvider>(
                builder: (context, provider, child) {
                  return ElevatedButton(
                    onPressed: provider.isScanning ? null : _handleScan,
                    child: provider.isScanning
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                          )
                        : const Text('Analyze Risk with AI-in-the-Loop'),
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
                    _buildMainRiskCard(risk),
                    const SizedBox(height: 16),
                    _buildSubMetricsRow(risk),
                    const SizedBox(height: 16),
                    _buildExplanationCard(risk),
                    if (risk.baiterResponse != null && risk.baiterResponse!.isNotEmpty) ...[
                      const SizedBox(height: 16),
                      _buildBaiterCard(risk.baiterResponse!),
                    ],
                    const SizedBox(height: 32),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMainRiskCard(RiskResponse risk) {
    Color color = AppTheme.accentColor;
    if (risk.riskScore > 70) color = AppTheme.dangerColor;
    else if (risk.riskScore > 30) color = AppTheme.warningColor;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppTheme.cardColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: color.withOpacity(0.3), width: 2),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                '${risk.riskScore}',
                style: TextStyle(fontSize: 64, fontWeight: FontWeight.bold, color: color),
              ),
              Text(
                '%',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: color),
              ),
            ],
          ),
          Text(
            'TOTAL SCAM RISK',
            style: TextStyle(color: color.withOpacity(0.8), letterSpacing: 2, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }

  Widget _buildSubMetricsRow(RiskResponse risk) {
    return Row(
      children: [
        Expanded(child: _buildMiniMetric('PII Leak Risk', '${risk.piiScore}%', risk.piiScore > 50 ? AppTheme.dangerColor : Colors.white70)),
        const SizedBox(width: 12),
        Expanded(child: _buildMiniMetric('User Engagement', '${risk.engagementScore}%', risk.engagementScore > 50 ? AppTheme.warningColor : Colors.white70)),
      ],
    );
  }

  Widget _buildMiniMetric(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.cardColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.white54)),
          const SizedBox(height: 4),
          Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
        ],
      ),
    );
  }

  Widget _buildExplanationCard(RiskResponse risk) {
    final filteredPii = risk.piiTypes.where((t) => t.toLowerCase() != 'none').toList();
    
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.cardColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.psychology, color: AppTheme.accentColor, size: 20),
              SizedBox(width: 8),
              Text('AI Reasoning', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            ],
          ),
          const SizedBox(height: 12),
          Text(risk.explanation, style: const TextStyle(height: 1.5, color: Colors.white70)),
          if (filteredPii.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Divider(color: Colors.white10),
            const SizedBox(height: 8),
            const Text('Personal Info At Risk:', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppTheme.dangerColor)),
            const SizedBox(height: 4),
            Wrap(
              spacing: 8,
              children: filteredPii.map((t) => Chip(
                label: Text(t, style: const TextStyle(fontSize: 11)),
                backgroundColor: AppTheme.dangerColor.withOpacity(0.1),
                side: const BorderSide(color: AppTheme.dangerColor),
                padding: EdgeInsets.zero,
                visualDensity: VisualDensity.compact,
              )).toList(),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildBaiterCard(String response) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.accentColor.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.accentColor.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Row(
                children: [
                  Icon(Icons.reply, color: AppTheme.accentColor, size: 20),
                  SizedBox(width: 8),
                  Text('Suggest Scam-Baiting', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: AppTheme.accentColor)),
                ],
              ),
              IconButton(
                onPressed: () => _copyToClipboard(response),
                icon: const Icon(Icons.copy, size: 18, color: AppTheme.accentColor),
                visualDensity: VisualDensity.compact,
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            response,
            style: const TextStyle(height: 1.4, fontStyle: FontStyle.italic, color: Colors.white),
          ),
          const SizedBox(height: 12),
          const Text(
            'Use this response to waste the scammer\'s time safely.',
            style: TextStyle(fontSize: 11, color: Colors.white38),
          ),
        ],
      ),
    );
  }
}
