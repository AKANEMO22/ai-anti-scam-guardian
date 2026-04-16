import 'package:flutter/material.dart';
import 'core/theme.dart';
import 'features/home/home_screen.dart';

class AntiScamApp extends StatelessWidget {
  const AntiScamApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Anti-Scam Guardian',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const HomeScreen(),
    );
  }
}
