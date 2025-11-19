import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_series(path, metric):
    """Lê um arquivo JSON e retorna a série da métrica escolhida + tempo."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    values, time_values = [], []

    for iteration in data["iterations"]:
        for measure in iteration["measures"]:
            if metric in measure:
                values.append(measure[metric])
            if "time" in measure:
                time_values.append(measure["time"])

    return pd.Series(values), pd.Series(time_values)


def media_series(lista_series):
    """Padroniza os tamanhos e calcula a média ponto a ponto."""
    tamanho = min(len(s) for s in lista_series)
    arr = np.array([s[:tamanho] for s in lista_series])
    return arr.mean(axis=0)

flutter_files = ["teste1_Flutter.json", "teste2_Flutter.json", "teste3_Flutter.json"]
rn_files = ["teste1_ReactNative.json", "teste2_ReactNative.json", "teste3_ReactNative.json"]

# FPS
flutter_fps, flutter_time = [], []
rn_fps, rn_time = [], []

for arq in flutter_files:
    fps, time = load_series(arq, "fps")
    flutter_fps.append(fps)
    flutter_time.append(time)

for arq in rn_files:
    fps, time = load_series(arq, "fps")
    rn_fps.append(fps)
    rn_time.append(time)

flutter_fps_mean = media_series(flutter_fps)
rn_fps_mean = media_series(rn_fps)

time_axis = flutter_time[0][:len(flutter_fps_mean)]

plt.figure(figsize=(12, 5))
plt.plot(time_axis, flutter_fps_mean, linewidth=2, label="Flutter")
plt.plot(time_axis, rn_fps_mean, linewidth=2, label="React Native")
plt.title("Comparativo de FPS – Aplicativo 1")
plt.xlabel("Tempo (ms)")
plt.ylabel("FPS")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparativo_app1_FPS.png")
plt.close()

print("Gráfico FPS App1 salvo como comparativo_app1_FPS.png")

# RAM
flutter_ram, flutter_time = [], []
rn_ram, rn_time = [], []

for arq in flutter_files:
    ram, time = load_series(arq, "ram")
    flutter_ram.append(ram)
    flutter_time.append(time)

for arq in rn_files:
    ram, time = load_series(arq, "ram")
    rn_ram.append(ram)
    rn_time.append(time)

flutter_ram_mean = media_series(flutter_ram)
rn_ram_mean = media_series(rn_ram)

time_axis = flutter_time[0][:len(flutter_ram_mean)]

plt.figure(figsize=(12, 5))
plt.plot(time_axis, flutter_ram_mean, linewidth=2, label="Flutter")
plt.plot(time_axis, rn_ram_mean, linewidth=2, label="React Native")
plt.title("Comparativo de RAM – Aplicativo 1")
plt.xlabel("Tempo (ms)")
plt.ylabel("RAM (MB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparativo_app1_RAM.png")
plt.close()

print("Gráfico RAM App1 salvo como comparativo_app1_RAM.png")
