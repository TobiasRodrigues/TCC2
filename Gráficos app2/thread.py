import os
import json
import numpy as np
import matplotlib.pyplot as plt

def load_ui_thread(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ui_values = []
    time_values = []

    for iteration in data["iterations"]:
        for measure in iteration["measures"]:

            if "cpu" in measure:
                cpu = measure["cpu"]
                if "perName" in cpu and "UI Thread" in cpu["perName"]:
                    ui_values.append(cpu["perName"]["UI Thread"])
                else:
                    ui_values.append(0)

            if "time" in measure:
                time_values.append(measure["time"])

    return np.array(ui_values), np.array(time_values)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def plot_graph(time, values, title, out):
    plt.figure(figsize=(12,5))
    plt.plot(time, values, linewidth=2)
    plt.title(title)
    plt.xlabel("Tempo (ms)")
    plt.ylabel("CPU (%) – UI Thread")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def mean_series(list_series):
    min_len = min(len(s) for s in list_series)
    arr = np.array([s[:min_len] for s in list_series])
    return arr.mean(axis=0)

flutter_dir = "ui_app2_flutter"
rn_dir = "ui_app2_rn"
ensure_dir(flutter_dir)
ensure_dir(rn_dir)

flutter_files = [
    "teste1_Flutter.json",
    "teste2_Flutter.json",
    "teste3_Flutter.json"
]

rn_files = [
    "teste1.ReactNative.json",
    "teste2.ReactNative.json",
    "teste3.ReactNative.json"
]

flutter_series = []
flutter_times = []

for i, arq in enumerate(flutter_files, 1):
    ui, time = load_ui_thread(arq)
    flutter_series.append(ui)
    flutter_times.append(time)
    plot_graph(time, ui, f"Flutter – UI Thread – Teste {i}",
               f"{flutter_dir}/ui_flutter_t{i}.png")

flutter_mean = mean_series(flutter_series)
time_axis = flutter_times[0][:len(flutter_mean)]
plot_graph(time_axis, flutter_mean, "Flutter – UI Thread – MÉDIA",
           f"{flutter_dir}/ui_flutter_media.png")

rn_series = []
rn_times = []

for i, arq in enumerate(rn_files, 1):
    ui, time = load_ui_thread(arq)
    rn_series.append(ui)
    rn_times.append(time)
    plot_graph(time, ui, f"React Native – UI Thread – Teste {i}",
               f"{rn_dir}/ui_rn_t{i}.png")

rn_mean = mean_series(rn_series)
time_axis_rn = rn_times[0][:len(rn_mean)]
plot_graph(time_axis_rn, rn_mean, "React Native – UI Thread – MÉDIA",
           f"{rn_dir}/ui_rn_media.png")

min_len = min(len(flutter_mean), len(rn_mean))
flutter_mean = flutter_mean[:min_len]
rn_mean = rn_mean[:min_len]
time_axis = time_axis[:min_len]

plt.figure(figsize=(12,5))
plt.plot(time_axis, flutter_mean, linewidth=2, label="Flutter")
plt.plot(time_axis, rn_mean, linewidth=2, label="React Native")
plt.title("Comparativo – UI Thread CPU Usage – Aplicativo 2")
plt.xlabel("Tempo (ms)")
plt.ylabel("CPU (%) – UI Thread")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparativo_app2_UI.png")
plt.close()

print("Todos os gráficos do App2 foram gerados com sucesso!")
