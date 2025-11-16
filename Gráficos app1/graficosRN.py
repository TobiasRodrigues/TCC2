import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_series(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cpu_values = []
    fps_values = []
    ram_values = []
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

            if "fps" in measure:
                fps_values.append(measure["fps"])

            if "ram" in measure:
                ram_values.append(measure["ram"])

            if "time" in measure:
                time_values.append(measure["time"])

    return (
        pd.Series(cpu_values),
        pd.Series(fps_values),
        pd.Series(ram_values),
        pd.Series(time_values)
    )


def plot_single(time, values, ylabel, title, filename):
    plt.figure(figsize=(12, 5))
    plt.plot(time, values, linewidth=2)
    plt.xlabel("Tempo (ms)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_mean(times_list, values_list, ylabel, title, filename):
    min_len = min(len(v) for v in values_list)

    values_stack = np.array([v[:min_len] for v in values_list])
    mean_series = values_stack.mean(axis=0)
    mean_time = times_list[0][:min_len]

    plt.figure(figsize=(12, 5))
    plt.plot(mean_time, mean_series, linewidth=2)
    plt.xlabel("Tempo (ms)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":

    arquivos = ["teste1_ReactNative.json", "teste2_ReactNative.json", "teste3_ReactNative.json"]

    pasta = "graficos_reactnative"
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    cpu_list = []
    fps_list = []
    ram_list = []
    time_list = []

    for arq in arquivos:
        print(f"Lendo {arq}...")
        cpu, fps, ram, time = load_series(arq)

        nome = arq.replace(".json", "")

        plot_single(time, cpu, "CPU (%)", f"CPU - {nome}", f"{pasta}/{nome}_CPU.png")
        plot_single(time, fps, "FPS", f"FPS - {nome}", f"{pasta}/{nome}_FPS.png")
        plot_single(time, ram, "RAM (MB)", f"RAM - {nome}", f"{pasta}/{nome}_RAM.png")

        cpu_list.append(cpu)
        fps_list.append(fps)
        ram_list.append(ram)
        time_list.append(time)

    plot_mean(time_list, cpu_list, "CPU (%)", "CPU Média - React Native App 1", f"{pasta}/CPU_media.png")
    plot_mean(time_list, fps_list, "FPS", "FPS Média - React Native App 1", f"{pasta}/FPS_media.png")
    plot_mean(time_list, ram_list, "RAM (MB)", "RAM Média - React Native App 1", f"{pasta}/RAM_media.png")

    print("Gráficos do App 1 (React Native) gerados com sucesso!")
