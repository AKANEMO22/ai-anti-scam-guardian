import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../providers/scanning_provider.dart';
import '../../core/theme.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detection History'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_sweep),
            onPressed: () => Provider.of<ScanningProvider>(context, listen: false).clearHistory(),
          ),
        ],
      ),
      body: Consumer<ScanningProvider>(
        builder: (context, provider, child) {
          if (provider.history.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.history, size: 64, color: Colors.white10),
                  SizedBox(height: 16),
                  Text('No history yet. Start scanning!', style: TextStyle(color: Colors.white24)),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: provider.history.length,
            itemBuilder: (context, index) {
              final item = provider.history[index];
              return _HistoryCard(result: item);
            },
          );
        },
      ),
    );
  }
}

class _HistoryCard extends StatelessWidget {
  final ScanResult result;

  const _HistoryCard({required this.result});

  @override
  Widget build(BuildContext context) {
    final score = result.response.riskScore;
    Color scoreColor = AppTheme.accentColor;
    if (score > 70) scoreColor = AppTheme.dangerColor;
    else if (score > 30) scoreColor = AppTheme.warningColor;

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ExpansionTile(
        title: Text(
          result.text,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(
          DateFormat('MMM d, yyyy - HH:mm').format(result.timestamp),
          style: const TextStyle(fontSize: 12, color: Colors.white54),
        ),
        leading: CircleAvatar(
          backgroundColor: scoreColor.withOpacity(0.2),
          child: Text(
            '$score',
            style: TextStyle(color: scoreColor, fontWeight: FontWeight.bold, fontSize: 12),
          ),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('AI Verdict:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                const SizedBox(height: 8),
                Text(result.response.explanation, style: const TextStyle(color: Colors.white70)),
                if (result.response.matchedPatterns.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  const Text('Matched Patterns:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 8),
                  ...result.response.matchedPatterns.map((p) => Padding(
                    padding: const EdgeInsets.only(bottom: 4.0),
                    child: Text('• ${p.patternText}', style: const TextStyle(fontSize: 12, color: Colors.white38)),
                  )),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
