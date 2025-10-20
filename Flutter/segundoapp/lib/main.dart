import 'dart:async';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:sensors_plus/sensors_plus.dart';

void main() => runApp(const MaterialApp(home: SensorGpsPage()));

class SensorGpsPage extends StatefulWidget {
  const SensorGpsPage({super.key});
  @override
  State<SensorGpsPage> createState() => _SensorGpsPageState();
}

class _SensorGpsPageState extends State<SensorGpsPage> {
  Position? _position;
  AccelerometerEvent? _accel;
  late StreamSubscription<Position> _posSub;
  late StreamSubscription<AccelerometerEvent> _accelSub;
  int _updates = 0;
  bool _running = false;
  final int _durationMs = 30000; // 30 segundos de teste

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _startTest());
  }

  Future<void> _startTest() async {
    if (_running) return;
    _running = true;
    final t0 = DateTime.now();

    // Solicita permissão de localização
    await Geolocator.requestPermission();

    // Inicia os sensores
    _posSub = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(accuracy: LocationAccuracy.high, distanceFilter: 0),
    ).listen((pos) {
      _position = pos;
      _updates++;
      if (mounted) setState(() {});
    });

    _accelSub = accelerometerEvents.listen((event) {
      _accel = event;
    });

    // Executa por 30 segundos
    while (DateTime.now().difference(t0).inMilliseconds < _durationMs) {
      await Future.delayed(const Duration(milliseconds: 500));
    }

    // Finaliza a leitura
    await _posSub.cancel();
    await _accelSub.cancel();
    _running = false;
    debugPrint('TESTE FINALIZADO - $_updates atualizações');
  }

  @override
  void dispose() {
    _posSub.cancel();
    _accelSub.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Tempo de teste: 30s', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            Text(
              _position == null
                  ? 'Aguardando GPS...'
                  : 'Lat: ${_position!.latitude.toStringAsFixed(5)}\nLon: ${_position!.longitude.toStringAsFixed(5)}',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(
              _accel == null
                  ? 'Acelerômetro: aguardando...'
                  : 'Accel X: ${_accel!.x.toStringAsFixed(2)}\n'
                  'Accel Y: ${_accel!.y.toStringAsFixed(2)}\n'
                  'Accel Z: ${_accel!.z.toStringAsFixed(2)}',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text('Atualizações: $_updates', style: const TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
