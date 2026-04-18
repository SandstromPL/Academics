#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def read_csv(path):
    x = []
    y = []
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                x.append(float(row[0]))
                y.append(float(row[1]))
    return x, y


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 plot_metrics.py <output_prefix>")
        sys.exit(1)

    prefix = sys.argv[1]
    thr_csv = Path(f"{prefix}_throughput.csv")
    dly_csv = Path(f"{prefix}_delay.csv")

    if not thr_csv.exists() or not dly_csv.exists():
        print("Required CSV files not found.")
        print(f"Expected: {thr_csv} and {dly_csv}")
        sys.exit(1)

    tx, ty = read_csv(thr_csv)
    dx, dy = read_csv(dly_csv)

    plt.figure(figsize=(8, 5))
    plt.plot(tx, ty, marker="o")
    plt.title("Throughput vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbps)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    thr_png = Path(f"{prefix}_throughput.png")
    plt.savefig(thr_png, dpi=150)

    plt.figure(figsize=(8, 5))
    plt.plot(dx, dy, marker="o", color="tab:orange")
    plt.title("Delay vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    dly_png = Path(f"{prefix}_delay.png")
    plt.savefig(dly_png, dpi=150)

    print(f"Generated: {thr_png}")
    print(f"Generated: {dly_png}")


if __name__ == "__main__":
    main()
