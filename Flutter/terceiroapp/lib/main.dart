import 'dart:async';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;
  runApp(MaterialApp(home: CameraVideoPage(camera: firstCamera)));
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

  @override
  void initState() {
    super.initState();
    _controller = CameraController(widget.camera, ResolutionPreset.high);
    _initializeControllerFuture =
        _controller.initialize().then((_) => _startRecording());
  }

  Future<void> _startRecording() async {
    final dir = await getTemporaryDirectory();
    final filePath =
        '${dir.path}/video_${DateTime.now().millisecondsSinceEpoch}.mp4';

    await _controller.startVideoRecording();
    setState(() => _recording = true);

    debugPrint('Iniciando gravação por 30 segundos...');
    await Future.delayed(const Duration(seconds: 30));

    final file = await _controller.stopVideoRecording();
    await file.saveTo(filePath);

    setState(() {
      _recording = false;
      _videoPath = filePath;
    });

    debugPrint('Vídeo salvo em: $filePath');
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Teste de Câmera e Vídeo (30s)')),
      body: FutureBuilder(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return Column(
              children: [
                Expanded(child: CameraPreview(_controller)),
                const SizedBox(height: 10),
                Text(
                  _recording
                      ? 'Gravando vídeo...'
                      : (_videoPath != null
                      ? 'Vídeo salvo em:\n$_videoPath'
                      : 'Aguardando inicialização...'),
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 18),
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
