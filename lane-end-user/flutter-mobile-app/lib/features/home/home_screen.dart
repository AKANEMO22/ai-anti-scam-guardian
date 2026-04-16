import 'package:flutter/material.dart';
import '../../core/theme.dart';
import '../scan/scan_screen.dart';
import '../history/history_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = [
    HomeDashboard(),
    ScanScreen(),
    HistoryScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        selectedItemColor: AppTheme.accentColor,
        unselectedItemColor: Colors.white24,
        backgroundColor: AppTheme.cardColor,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.shield), label: 'Guardian'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Scan'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'History'),
        ],
      ),
    );
  }
}

class HomeDashboard extends StatelessWidget {
  const HomeDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Guardian Active',
              style: Theme.of(context).textTheme.displayLarge,
            ),
            const SizedBox(height: 8),
            const Text(
              'Your device is being protected in real-time.',
              style: TextStyle(color: Colors.white54),
            ),
            const Spacer(),
            Center(
              child: Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppTheme.accentColor.withOpacity(0.1),
                  border: Border.all(color: AppTheme.accentColor, width: 2),
                ),
                child: const Icon(
                  Icons.security,
                  size: 100,
                  color: AppTheme.accentColor,
                ),
              ),
            ),
            const Spacer(),
            _buildStatCard(
              context,
              'Recent Scans',
              '0 threats detected today.',
              Icons.check_circle_outline,
              AppTheme.accentColor,
            ),
            const SizedBox(height: 16),
            _buildStatCard(
              context,
              'AI Reasoning',
              'Gemini 1.5 Flash is analyzing signals.',
              Icons.psychology,
              AppTheme.warningColor,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(BuildContext context, String title, String subtitle, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.cardColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                Text(subtitle, style: const TextStyle(color: Colors.white54, fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
