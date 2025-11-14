import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    home: CameraVideoPage(camera: firstCamera),
  ));
}

class CameraVideoPage extends StatefulWidget {
  final CameraDescription camera;
  const CameraVideoPage({super.key, required this.camera});

  @override
  State<CameraVideoPage> createState() => _CameraVideoPageState();
}

class _CameraVideoPageState extends State<CameraVideoPage> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  bool _recording = false;
  String? _videoPath;
  Timer? _timer;
  int _secondsRemaining = 30;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
      enableAudio: true,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  Future<void> _startRecording() async {
    try {
      final dir = await getTemporaryDirectory();
      final filePath =
          '${dir.path}/video_${DateTime.now().millisecondsSinceEpoch}.mp4';

      await _controller.startVideoRecording();
      setState(() {
        _recording = true;
        _videoPath = null;
        _secondsRemaining = 30;
      });

      // Timer de 30 segundos
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) async {
        if (_secondsRemaining > 1) {
          setState(() => _secondsRemaining--);
        } else {
          await _stopRecording();
        }
      });
    } catch (e) {
      debugPrint("Erro ao iniciar gravação: $e");
    }
  }

  Future<void> _stopRecording() async {
    try {
      _timer?.cancel();
      final file = await _controller.stopVideoRecording();
      setState(() {
        _recording = false;
        _videoPath = file.path;
      });
      debugPrint("Vídeo salvo em: ${file.path}");
    } catch (e) {
      debugPrint("Erro ao parar gravação: $e");
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Teste de Câmera e Vídeo (30s)'),
        backgroundColor: Colors.blueAccent,
      ),
      body: FutureBuilder(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return Column(
              children: [
                Expanded(child: CameraPreview(_controller)),
                const SizedBox(height: 16),
                if (_recording)
                  Text(
                    "Gravando... ($_secondsRemaining s)",
                    style: const TextStyle(color: Colors.red, fontSize: 18),
                  )
                else if (_videoPath != null)
                  Text(
                    "Vídeo salvo em:\n$_videoPath",
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white, fontSize: 16),
                  )
                else
                  const Text(
                    "Pressione o botão para gravar 30s",
                    style: TextStyle(color: Colors.white, fontSize: 16),
                  ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: _recording ? _stopRecording : _startRecording,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _recording ? Colors.red : Colors.green,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 40, vertical: 14),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                  ),
                  child: Text(
                    _recording ? "Parar Gravação" : "Iniciar Gravação (30s)",
                    style: const TextStyle(fontSize: 16, color: Colors.white),
                  ),
                ),
                const SizedBox(height: 20),
              ],
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
