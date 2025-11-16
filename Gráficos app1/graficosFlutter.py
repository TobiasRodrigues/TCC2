import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# CARREGAR DADOS
def load_flutter_series(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cpu_values = []
    fps_values = []
    ram_values = []
    time_values = []

    for iteration in data["iterations"]:
        for measure in iteration["measures"]:

            # CPU
            if "cpu" in measure:
                c = measure["cpu"]
                if "perName" in c and c["perName"]:
                    cpu_sum = sum(c["perName"].values())
                elif "perCore" in c and c["perCore"]:
                    cpu_sum = sum(c["perCore"].values())
                else:
                    cpu_sum = 0
                cpu_values.append(cpu_sum)

            # FPS
            if "fps" in measure:
                fps_values.append(measure["fps"])

            # RAM
            if "ram" in measure:
                ram_values.append(measure["ram"])

            # Tempo em ms
            if "time" in measure:
                time_values.append(measure["time"])

    return (
        pd.Series(cpu_values),
        pd.Series(fps_values),
        pd.Series(ram_values),
        pd.Series(time_values),
    )

# GRÁFICO INDIVIDUAL
def plot_single(time, values, ylabel, title, filename):
    plt.figure(figsize=(12, 5))
    plt.plot(time, values, color="blue")
    plt.xlabel("Tempo (ms)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# MÉDIA
def plot_mean_graph(times_list, values_list, ylabel, title, filename):
    min_len = min(len(v) for v in values_list)

    values_stack = np.array([v[:min_len] for v in values_list])
    mean_values = values_stack.mean(axis=0)

    mean_time = times_list[0][:min_len]

    plt.figure(figsize=(12, 5))
    plt.plot(mean_time, mean_values, color="green", linewidth=2)
    plt.xlabel("Tempo (ms)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def gerar_graficos_flutter():
    print("🔵 Gerando gráficos do Flutter...")

    arquivos = sorted(glob.glob("teste*_Flutter.json"))
    if not arquivos:
        print("Nenhum arquivo testeX_Flutter.json encontrado.")
        return

    cpu_list = []
    fps_list = []
    ram_list = []
    time_list = []

    # PASTA
    if not os.path.exists("graficos_flutter"):
        os.makedirs("graficos_flutter")

    for arq in arquivos:
        print(f"📂 Lendo {arq} ...")

        cpu, fps, ram, time = load_flutter_series(arq)

        nome = os.path.splitext(os.path.basename(arq))[0]

        plot_single(time, cpu, "CPU (%)",
                    f"Flutter - CPU ({nome})",
                    f"graficos_flutter/{nome}_CPU.png")

        plot_single(time, fps, "FPS",
                    f"Flutter - FPS ({nome})",
                    f"graficos_flutter/{nome}_FPS.png")

        plot_single(time, ram, "RAM (MB)",
                    f"Flutter - RAM ({nome})",
                    f"graficos_flutter/{nome}_RAM.png")

        cpu_list.append(cpu)
        fps_list.append(fps)
        ram_list.append(ram)
        time_list.append(time)

    print("Gerando gráficos médios...")

    plot_mean_graph(time_list, cpu_list, "CPU (%)",
                    "Flutter — CPU Média dos Testes",
                    "graficos_flutter/Flutter_CPU_media.png")

    plot_mean_graph(time_list, fps_list, "FPS",
                    "Flutter — FPS Média dos Testes",
                    "graficos_flutter/Flutter_FPS_media.png")

    plot_mean_graph(time_list, ram_list, "RAM (MB)",
                    "Flutter — RAM Média dos Testes",
                    "graficos_flutter/Flutter_RAM_media.png")

    print("Todos os gráficos do Flutter foram gerados em: graficos_flutter/")

if __name__ == "__main__":
    gerar_graficos_flutter()
