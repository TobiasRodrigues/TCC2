import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Arquivos de entrada
react_files = [
    "teste1.ReactNative.json",
    "teste2.ReactNative.json",
    "teste3.ReactNative.json"
]

flutter_files = [
    "teste1_Flutter.json",
    "teste2_Flutter.json",
    "teste3_Flutter.json"
]

# Função para carregar o FPS de cada arquivo
def load_fps_series(file_list):
    series = []
    for f in file_list:
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            fps = [m["fps"] for m in data["iterations"][0]["measures"]]
            time = [m["time"] for m in data["iterations"][0]["measures"]]
            series.append(pd.DataFrame({"time": time, "fps": fps}))
    return series

# Carregar dados
react_series = load_fps_series(react_files)
flutter_series = load_fps_series(flutter_files)

# Função para alinhar as séries e tirar média
def average_series(series_list):
    min_len = min(len(s) for s in series_list)
    trimmed = [s.iloc[:min_len] for s in series_list]
    avg = sum(s["fps"].values for s in trimmed) / len(trimmed)
    ts = trimmed[0]["time"].values
    return ts, avg

# Gerar médias
ts_rn, avg_rn = average_series(react_series)
ts_fl, avg_fl = average_series(flutter_series)

# Plotar gráfico
plt.figure(figsize=(12,6))

plt.plot(ts_rn, avg_rn, label="React Native - FPS Médio", linewidth=2, color="#ff4444")
plt.plot(ts_fl, avg_fl, label="Flutter - FPS Médio", linewidth=2, color="#00c896")

plt.xlabel("Tempo (ms)")
plt.ylabel("FPS")
plt.title("Comparação de FPS – Segundo Aplicativo (RN vs Flutter)")
plt.legend()
plt.grid(alpha=0.3)

# Salvar
plt.savefig("fps_app2.png", dpi=300)
plt.show()
