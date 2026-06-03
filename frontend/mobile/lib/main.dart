import 'package:flutter/material.dart';
import 'config/theme.dart';
import 'screens/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GBSB Digital Gurukul',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      home: const SplashScreen(),
      debugShowCheckedModeBanner: false,
      routes: {
        '/splash': (context) => const SplashScreen(),
        '/login': (context) => const LoginScreen(),
        '/dashboard': (context) => const DashboardScreen(),
        '/courses': (context) => const CourseScreen(),
        '/classes': (context) => const LiveClassScreen(),
        '/ai-tutor': (context) => const AITutorScreen(),
      },
    );
  }
}

// Import screens
from 'screens/login_screen.dart';
from 'screens/dashboard_screen.dart';
from 'screens/course_screen.dart';
from 'screens/live_class_screen.dart';
from 'screens/ai_tutor_screen.dart';
