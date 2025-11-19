import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_cpu_series(path):
    """Lê CPU (somatório das threads) + tempo."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cpu_values = []
    time_values = []

    for iteration in data["iterations"]:
        for measure in iteration["measures"]:
            if "cpu" in measure:
                c = measure["cpu"]
                if "perName" in c and c["perName"]:
                    cpu_sum = sum(c["perName"].values())
                elif "perCore" in c and c["perCore"]:
                    cpu_sum = sum(c["perCore"].values())
                else:
                    cpu_sum = 0
                cpu_values.append(cpu_sum)

            if "time" in measure:
                time_values.append(measure["time"])

    return pd.Series(cpu_values), pd.Series(time_values)


def load_series(path, metric):
    """RAM + tempo."""
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


def media_series(lista):
    """Média ponto a ponto."""
    tamanho = min(len(x) for x in lista)
    arr = np.array([x[:tamanho] for x in lista])
    return arr.mean(axis=0)

flutter_files = ["teste1_Flutter.json", "teste2_Flutter.json", "teste3_Flutter.json"]
rn_files = ["teste1.ReactNative.json", "teste2.ReactNative.json", "teste3.ReactNative.json"]


flutter_cpu, flutter_time = [], []
rn_cpu, rn_time = [], []

for arq in flutter_files:
    cpu, t = load_cpu_series(arq)
    flutter_cpu.append(cpu)
    flutter_time.append(t)

for arq in rn_files:
    cpu, t = load_cpu_series(arq)
    rn_cpu.append(cpu)
    rn_time.append(t)

flutter_cpu_mean = media_series(flutter_cpu)
rn_cpu_mean = media_series(rn_cpu)

time_axis = flutter_time[0][:len(flutter_cpu_mean)]

plt.figure(figsize=(12, 5))
plt.plot(time_axis, flutter_cpu_mean, linewidth=2, label="Flutter")
plt.plot(time_axis, rn_cpu_mean, linewidth=2, label="React Native")
plt.title("Comparativo de CPU – Aplicativo 2")
plt.xlabel("Tempo (ms)")
plt.ylabel("CPU (%) (somatório das threads)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparativo_app2_CPU.png")
plt.close()

print("Gráfico CPU App2 salvo como comparativo_app2_CPU.png")

flutter_ram, flutter_time = [], []
rn_ram, rn_time = [], []

for arq in flutter_files:
    ram, t = load_series(arq, "ram")
    flutter_ram.append(ram)
    flutter_time.append(t)

for arq in rn_files:
    ram, t = load_series(arq, "ram")
    rn_ram.append(ram)
    rn_time.append(t)

flutter_ram_mean = media_series(flutter_ram)
rn_ram_mean = media_series(rn_ram)

time_axis = flutter_time[0][:len(flutter_ram_mean)]

plt.figure(figsize=(12, 5))
plt.plot(time_axis, flutter_ram_mean, linewidth=2, label="Flutter")
plt.plot(time_axis, rn_ram_mean, linewidth=2, label="React Native")
plt.title("Comparativo de RAM – Aplicativo 2")
plt.xlabel("Tempo (ms)")
plt.ylabel("RAM (MB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparativo_app2_RAM.png")
plt.close()

print("Gráfico RAM App2 salvo como comparativo_app2_RAM.png")
