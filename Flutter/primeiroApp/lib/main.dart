import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: CpuAutoPage()));

class CpuAutoPage extends StatefulWidget {
  const CpuAutoPage({super.key});
  @override State<CpuAutoPage> createState() => _CpuAutoPageState();
}

class _CpuAutoPageState extends State<CpuAutoPage> {
  static const int DURATION_MS = 30000; // 30s
  int iterations = 0;
  bool running = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _runCpu());
  }

  bool _isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) { if (n % i == 0) return false; }
    return true;
  }

  Future<void> _runCpu() async {
    if (running) return;
    running = true;
    final t0 = DateTime.now();
    final rand = Random(123);
    debugPrint('PHASE=CPU START ts=${DateTime.now().toIso8601String()}');

    while (DateTime.now().difference(t0).inMilliseconds < DURATION_MS) {
      // 1) JSON grande
      final list = List.generate(20000, (i) => {'i': i, 's': 'x' * 10});
      final s = jsonEncode(list);
      final _ = jsonDecode(s);

      // 2) sort
      final nums = List.generate(30000, (_) => rand.nextInt(1000000));
      nums.sort();

      // 3) primos
      int c = 0; for (int n = 100000; n < 101000; n++) { if (_isPrime(n)) c++; }

      iterations++;
      if (mounted) setState(() {});
      await Future.delayed(Duration.zero);
    }

    debugPrint('PHASE=CPU END ts=${DateTime.now().toIso8601String()}');
    running = false;
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: Center(child: Text('Iterações concluídas: $iterations',
        style: const TextStyle(fontSize: 20))),
  );
}
