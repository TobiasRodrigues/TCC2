import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: CpuButtonPage()));

class CpuButtonPage extends StatefulWidget {
  const CpuButtonPage({super.key});

  @override
  State<CpuButtonPage> createState() => _CpuButtonPageState();
}

class _CpuButtonPageState extends State<CpuButtonPage> {
  static const int DURATION_MS = 30000; // 30 segundos
  int iterations = 0;
  bool running = false;

  bool _isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
      if (n % i == 0) return false;
    }
    return true;
  }

  Future<void> _runCpu() async {
    if (running) return;
    setState(() {
      running = true;
      iterations = 0;
    });

    debugPrint('Iniciado ts=${DateTime.now().toIso8601String()}');
    final t0 = DateTime.now();
    final rand = Random(123);

    while (DateTime.now().difference(t0).inMilliseconds < DURATION_MS) {
      // JSON grande
      final list = List.generate(20000, (i) => {'i': i, 's': 'x' * 10});
      final s = jsonEncode(list);
      final _ = jsonDecode(s);

      // Ordenação
      final nums = List.generate(30000, (_) => rand.nextInt(1000000));
      nums.sort();

      // Primos
      int c = 0;
      for (int n = 100000; n < 101000; n++) {
        if (_isPrime(n)) c++;
      }

      setState(() => iterations++);
      await Future.delayed(Duration.zero);
    }

    debugPrint('Finalizado ts=${DateTime.now().toIso8601String()}');
    setState(() => running = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(height: 10),
            Text(
              'Iterações concluídas: $iterations',
              style: const TextStyle(color: Colors.white70, fontSize: 18),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: running ? null : _runCpu,
              style: ElevatedButton.styleFrom(
                backgroundColor: running ? Colors.grey[800] : Colors.blue,
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              child: running
                  ? const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                  ),
                  SizedBox(width: 10),
                  Text('Executando...', style: TextStyle(color: Colors.white)),
                ],
              )
                  : const Text('Iniciar Teste', style: TextStyle(fontSize: 18, color: Colors.white)),
            ),
          ],
        ),
      ),
    );
  }
}
