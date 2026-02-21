import os
import subprocess
import time
import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


# Fase di Configurazione
RUNS = 1000 # Numero di esecuzioni

BENCHMARKS = [
    {
        "label": "Random Input",
        "c_file": "bubble_sort_completely_random.c",
        "executable": "bsort_random_exec",
        "color": "steelblue",
        "csv": "bsort_random_times.csv",
        "plot": "bsort_plot_random.png",
    },
    {
        "label": "Partially Ordered Input",
        "c_file": "bubble_sort_partially_ordered.c",
        "executable": "bsort_partial_exec",
        "color": "darkorange",
        "csv": "bsort_partial_times.csv",
        "plot": "bsort_plot_partial.png",
    },
]


# Fase di Compilazione
def compile_program(c_file, executable):
    print(f"Compiling {c_file} -> {executable} ...")
    try:
        subprocess.check_call(["gcc", c_file, "-O2", "-o", executable, "-w"])
        print("  Compilation successful")
    except subprocess.CalledProcessError:
        print(f"  Compilation of {c_file} failed")
        exit(1)


# Fase di Esecuzione - l'eseguibile viene eseguito RUNS volte
def run_benchmark(executable, label):
    times = []
    print(f"Running '{label}' for {RUNS} iterations...")
    for i in range(RUNS):
        start = time.perf_counter()
        subprocess.run(["./" + executable], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        end = time.perf_counter()
        times.append(end - start)
        if (i + 1) % 100 == 0:
            print(f"  Completed {i + 1} runs")
    print()
    return times


# Fase di Salvataggio in un file csv
def save_csv(times, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["run", "execution_time"])
        for i, t in enumerate(times):
            writer.writerow([i + 1, t])


# Calcolo delle statistiche
def compute_statistics(times):
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times),
        "min": min(times),
        "max": max(times),
    }


# ECDF + DKW bands: 
# si usa l'oggetto ECDF di statsmodels per calcolare CDF (funzione di distribuzione empirica) 
# e poi si applica la disuguaglianza DKW per ottenere le simultaneous confidence bands: 
# eps = sqrt( ln(2 / alpha) / (2 * n) )
# upper(x) = min( F_n(x) + eps, 1 )
# lower(x) = max( F_n(x) - eps, 0 )

# Fase di Calcolo di ECDF con DKW bands
def compute_ecdf_dkw(times, alpha=0.05):
    x = np.sort(times)
    n = len(x)

    # Chiamata dell'oggetto statsmodels ECDF sulla griglia temporale ordinata per ottenere F_n(x)
    ecdf_fn = ECDF(times)
    ecdf_y = ecdf_fn(x)

    # DKW epsilon
    eps = np.sqrt(np.log(2.0 / alpha) / (2.0 * n))
    upper = np.clip(ecdf_y + eps, 0.0, 1.0)
    lower = np.clip(ecdf_y - eps, 0.0, 1.0)

    return x, ecdf_y, upper, lower, eps


# Fase di Tracciamento di ECDF con DKW bands su ax
def plot_ecdf_dkw(ax, times, color, label, alpha=0.05):
    x, ecdf_y, upper, lower, eps = compute_ecdf_dkw(times, alpha)

    ax.step(x, ecdf_y, color=color, linewidth=1.4, where="post", label="ECDF")
    ax.step(x, upper,  color=color, linewidth=0.7, linestyle="--", alpha=0.7, where="post", label=f"DKW {int((1-alpha)*100)}% band  (ε={eps:.4f})")
    ax.step(x, lower, color=color, linewidth=0.7, linestyle="--", alpha=0.7, where="post")
    ax.fill_between(x, lower, upper, step="post", alpha=0.15, color=color)

    ax.set_xlabel("Execution Time (s)")
    ax.set_ylabel("Cumulative Probability")
    ax.set_title(f"{label} - ECDF + DKW Bands")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)


# Fase di Plot: line plot, istogramma e ECDF + DKW
def plot_single(times, label, color, stats, filename):
    # Calcolo delle statistiche
    mean, median, stdev = stats["mean"], stats["median"], stats["stdev"]

    # Impostazione della figura
    fig, (ax_line, ax_hist, ax_ecdf) = plt.subplots(1, 3, figsize=(21, 5))
    fig.suptitle(f"Bubble Sort Benchmark - {label} ({RUNS} Runs)", fontsize=13, fontweight="bold")

    # Line plot
    ax_line.plot(range(1, RUNS + 1), times, color=color, linewidth=0.7, alpha=0.75, label="Execution time")
    ax_line.axhline(mean, color="red",  linestyle="--", linewidth=1.1, label=f"Mean {mean:.6f}s")
    ax_line.axhline(median, color="gold", linestyle=":",  linewidth=1.1, label=f"Median {median:.6f}s")
    ax_line.set_xlabel("Run Number")
    ax_line.set_ylabel("Time (s)")
    ax_line.set_title("Time per Run")
    ax_line.legend(fontsize=8)
    ax_line.grid(True, alpha=0.25)

    # Istogramma
    ax_hist.hist(times, bins=40, color=color, edgecolor="white", alpha=0.85)
    ax_hist.axvline(mean, color="red", linestyle="--", linewidth=1.1, label=f"Mean {mean:.6f}s")
    ax_hist.axvline(median, color="gold", linestyle=":", linewidth=1.1, label=f"Median {median:.6f}s")
    ax_hist.axvline(mean - stdev, color="gray", linestyle="--", linewidth=0.8, alpha=0.7, label=f"±1σ  {stdev:.6f}s")
    ax_hist.axvline(mean + stdev, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
    ax_hist.set_xlabel("Time (s)")
    ax_hist.set_ylabel("Frequency")
    ax_hist.set_title("Distribution")
    ax_hist.legend(fontsize=8)
    ax_hist.grid(True, alpha=0.25)

    # ECDF + DKW
    plot_ecdf_dkw(ax_ecdf, times, color, label)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved -> {filename}")


# Fase di Plot: plot sovrapposti
def plot_combined(results, filename="bsort_plot_combined.png"):
    fig, (ax_line, ax_hist, ax_ecdf) = plt.subplots(1, 3, figsize=(21, 5))
    fig.suptitle(f"Bubble Sort Benchmark - Combined Comparison ({RUNS} Runs)", fontsize=13, fontweight="bold")

    for r in results:
        times = r["times"]
        label = r["label"]
        color = r["color"]
        mean = r["stats"]["mean"]

        # Line plot
        ax_line.plot(range(1, RUNS + 1), times, color=color, linewidth=0.7, alpha=0.7, label=label)
        ax_line.axhline(mean, color=color, linestyle="--", linewidth=1.1, label=f"Mean ({label}): {mean:.6f}s")

        # Istogramma
        ax_hist.hist(times, bins=40, color=color, edgecolor="white", alpha=0.55, label=label)
        ax_hist.axvline(mean, color=color, linestyle="--", linewidth=1.1, label=f"Mean: {mean:.6f}s")

        # ECDF + DKW
        x, ecdf_y, upper, lower, eps = compute_ecdf_dkw(times)
        ax_ecdf.step(x, ecdf_y, color=color, linewidth=1.4, where="post", label=f"ECDF - {label}")
        ax_ecdf.step(x, upper, color=color, linewidth=0.7, linestyle="--", alpha=0.7, where="post", label=f"DKW band (ε={eps:.4f})")
        ax_ecdf.step(x, lower, color=color, linewidth=0.7, linestyle="--", alpha=0.7, where="post")
        ax_ecdf.fill_between(x, lower, upper, step="post", alpha=0.15, color=color)

    ax_line.set_xlabel("Run Number")
    ax_line.set_ylabel("Time (s)")
    ax_line.set_title("Time per Run")
    ax_line.legend(fontsize=8)
    ax_line.grid(True, alpha=0.25)

    ax_hist.set_xlabel("Time (s)")
    ax_hist.set_ylabel("Frequency")
    ax_hist.set_title("Distribution")
    ax_hist.legend(fontsize=8)
    ax_hist.grid(True, alpha=0.25)

    ax_ecdf.set_xlabel("Execution Time (s)")
    ax_ecdf.set_ylabel("Cumulative Probability")
    ax_ecdf.set_title("ECDF + DKW 95% Confidence Bands")
    ax_ecdf.legend(fontsize=8)
    ax_ecdf.grid(True, alpha=0.25)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved -> {filename}")


# Fase di pulizia - rimozione degli eseguibili
def cleanup():
    for b in BENCHMARKS:
        if os.path.exists(b["executable"]):
            os.remove(b["executable"])


if __name__ == "__main__":
    for b in BENCHMARKS:
        compile_program(b["c_file"], b["executable"])

    print()

    results = []
    for b in BENCHMARKS:
        times = run_benchmark(b["executable"], b["label"])
        save_csv(times, b["csv"])
        stats = compute_statistics(times)
        results.append({**b, "times": times, "stats": stats})

    print()
    print("Saving plots...")
    for r in results:
        plot_single(r["times"], r["label"], r["color"], r["stats"], r["plot"])
    plot_combined(results)
    cleanup()