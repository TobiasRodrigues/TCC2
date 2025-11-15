import json
import matplotlib.pyplot as plt

def load_cpu_series(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    iterations = data["iterations"][0]["measures"]

    times = []
    cpu_totals = []

    for entry in iterations:
        time = entry["time"]
        per_core = entry["cpu"]["perCore"]

        total_cpu = sum(per_core.values())

        times.append(time)
        cpu_totals.append(total_cpu)

    return times, cpu_totals

# ARQUIVOS
react_files = [
    "teste1_ReactNative.json",
    "teste2_ReactNative.json",
    "teste3_ReactNative.json"
]

flutter_files = [
    "teste1_Flutter.json",
    "teste2_Flutter.json",
    "teste3_Flutter.json"
]

def load_group(file_list):
    all_times = []
    all_cpus = []
    for f in file_list:
        t, c = load_cpu_series(f)
        all_times.append(t)
        all_cpus.append(c)

    min_len = min(len(x) for x in all_times)

    avg_time = [ sum(t[i] for t in all_times) / len(all_times) for i in range(min_len) ]
    avg_cpu  = [ sum(c[i] for c in all_cpus)  / len(all_cpus)  for i in range(min_len) ]

    return avg_time, avg_cpu

# CARREGA OS ARQUIVOS
react_time, react_cpu = load_group(react_files)
flutter_time, flutter_cpu = load_group(flutter_files)

plt.figure(figsize=(12, 6))

plt.plot(react_time, react_cpu, label="React Native", linewidth=2)
plt.plot(flutter_time, flutter_cpu, label="Flutter", linewidth=2)

plt.title("Comparação de Uso de CPU — React Native vs Flutter (Média dos 3 testes)")
plt.xlabel("Tempo (ms)")
plt.ylabel("CPU (%)")
plt.legend()
plt.grid(True, alpha=0.2)

plt.show()