import 'package:flutter/material.dart';
import '../core/theme.dart';

class PremiumCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;

  const PremiumCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(20),
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: AppTheme.cardColor,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: child,
    );
  }
}

class RiskBadge extends StatelessWidget {
  final int score;

  const RiskBadge({super.key, required this.score});

  @override
  Widget build(BuildContext context) {
    Color color = AppTheme.accentColor;
    String label = 'SAFE';
    
    if (score > 70) {
      color = AppTheme.dangerColor;
      label = 'CRITICAL';
    } else if (score > 30) {
      color = AppTheme.warningColor;
      label = 'SUSPICIOUS';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 10,
          fontWeight: FontWeight.bold,
          letterSpacing: 1,
        ),
      ),
    );
  }
}
